from flask import Flask, render_template, request
import pyflakes.api
import pyflakes.reporter
import sys
import io
import ast
from radon.complexity import cc_visit
from memory_profiler import memory_usage
import tempfile
import subprocess
import os
import re
import time
from collections import defaultdict

app = Flask(__name__)

def get_rank(complexity):
    """Convert complexity score to letter grade"""
    if complexity <= 3:
        return "A"
    elif complexity <= 5:
        return "B"
    elif complexity <= 7:
        return "C"
    elif complexity <= 10:
        return "D"
    elif complexity <= 15:
        return "E"
    else:
        return "F"

def calculate_score(analysis_results):
    """Calculate overall code quality score"""
    score = 10.0

    # Penalize for unused code
    score -= 0.3 * len(analysis_results.get('unused_functions', []))
    score -= 0.2 * len(analysis_results.get('unused_variables', []))

    # Penalize for deep nesting
    if analysis_results.get('max_nesting', 0) > 4:
        score -= (analysis_results['max_nesting'] - 4) * 0.5

    # Penalize for high complexity
    avg_complexity = analysis_results.get('avg_complexity', 0)
    if avg_complexity > 3:
        score -= (avg_complexity - 3) * 0.4

    # Penalize for broad exceptions
    score -= 0.5 * len(analysis_results.get('broad_exceptions', []))

    # Penalize for high memory usage
    peak_memory = analysis_results.get('peak_memory', 0)
    if peak_memory > 50:
        score -= 1
    elif peak_memory > 30:
        score -= 0.5

    # Penalize for security issues
    score -= 0.5 * len(analysis_results.get('security_issues', []))

    return max(0.0, round(score, 2))

def generate_improvement_tips(analysis_results):
    """Generate actionable improvement tips"""
    tips = []
    
    if analysis_results.get('unused_functions'):
        tips.append("💡 Remove unused functions to simplify your code")
        
    if analysis_results.get('max_nesting', 0) > 4:
        tips.append("💡 Refactor deeply nested code into smaller functions")
        
    if analysis_results.get('broad_exceptions'):
        tips.append("💡 Replace broad exceptions with specific exception handling")
        
    if analysis_results.get('avg_complexity', 0) > 5:
        tips.append("💡 Break down complex functions into simpler ones")
        
    if analysis_results.get('security_issues'):
        tips.append("🔒 Review security findings and address vulnerabilities")
        
    if analysis_results.get('peak_memory', 0) > 50:
        tips.append("⚡ Optimize memory usage in your code")
        
    return tips

def dynamic_profile(code):
    """Run dynamic profiling using memory_profiler"""
    profile_data = {
        'peak_memory': None,
        'execution_time': None,
        'error': None
    }
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.py', mode='w') as temp_file:
        temp_file.write(code)
        temp_path = temp_file.name

    try:
        start_time = time.time()
        mem_usage = memory_usage(
            (subprocess.run, (['python', temp_path],), {}),
            interval=0.1,
            timeout=10
        )
        profile_data.update({
            'peak_memory': round(max(mem_usage), 2) if mem_usage else None,
            'execution_time': round(time.time() - start_time, 2)
        })
    except Exception as e:
        profile_data['error'] = str(e)
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)
    
    return profile_data

def run_security_scan(code):
    """Run security checks using Bandit and custom OWASP checks"""
    security_issues = []
    
    # Bandit analysis (if available)
    try:
        from bandit.core import manager
        with tempfile.NamedTemporaryFile(delete=False, suffix='.py', mode='w') as temp_file:
            temp_file.write(code)
            temp_path = temp_file.name
        
        b_mgr = manager.BanditManager()
        b_mgr.discover_files([temp_path], [temp_path])
        b_mgr.run_tests()
        for issue in b_mgr.get_issue_list():
            security_issues.append(f"Line {issue.lineno}: {issue.text} (Severity: {issue.severity})")
        
    except ImportError:
        security_issues.append("⚠️ Bandit not installed for advanced security scanning")
    except Exception as e:
        security_issues.append(f"⚠️ Bandit error: {str(e)}")
    finally:
        if 'temp_path' in locals() and os.path.exists(temp_path):
            os.unlink(temp_path)
    
    # Custom OWASP checks
    owasp_patterns = {
        'SQL Injection': r'(\bexecute\b|\bcursor\.execute\b).*(\%s|\{\})',
        'XSS': r'(response\.write|print|echo).*(\<script\>|\%3Cscript\%3E)',
        'Code Injection': r'\beval\s*\(',
        'Insecure Deserialization': r'pickle\.loads?\s*\(',
        'Shell Injection': r'subprocess\.(run|call|Popen)\(.*shell\s*=\s*True'
    }
    
    for lineno, line in enumerate(code.splitlines(), 1):
        for vuln_type, pattern in owasp_patterns.items():
            if re.search(pattern, line, re.IGNORECASE):
                security_issues.append(f"Line {lineno}: Potential {vuln_type} vulnerability")
    
    return security_issues

def analyze_code(code, dynamic=False, security_check=False):
    """Main analysis function with all checks"""
    analysis_results = defaultdict(list)
    output = io.StringIO()
    
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return {'error': f"Syntax Error: {e.msg} on line {e.lineno}"}

    # Static analysis
    defined_functions = set()
    used_functions = set()
    assigned_variables = set()
    used_variables = set()
    max_nesting = [0]

    def track_nesting(node, level=0):
        """Track maximum nesting level"""
        if isinstance(node, (ast.If, ast.For, ast.While, ast.With, ast.Try, ast.FunctionDef)):
            level += 1
            max_nesting[0] = max(max_nesting[0], level)
        for child in ast.iter_child_nodes(node):
            track_nesting(child, level)

    # AST traversal
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            defined_functions.add(node.name)
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            used_functions.add(node.func.id)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    assigned_variables.add(target.id)
        elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            used_variables.add(node.id)

    track_nesting(tree)

    # Store analysis results
    analysis_results.update({
        'unused_functions': list(defined_functions - used_functions),
        'unused_variables': list(assigned_variables - used_variables),
        'max_nesting': max_nesting[0],
        'broad_exceptions': [
            f"Line {lineno}: {line.strip()}"
            for lineno, line in enumerate(code.splitlines(), 1)
            if re.search(r'^\s*except\s*:\s*$', line) or re.search(r'^\s*except\s+Exception\s*:', line)
        ]
    })

    # Complexity analysis
    try:
        complexity_results = cc_visit(code)
        if complexity_results:
            analysis_results['complexity'] = [
                {
                    'name': func.name,
                    'complexity': func.complexity,
                    'rank': get_rank(func.complexity),
                    'line': func.lineno
                }
                for func in complexity_results
            ]
            analysis_results['avg_complexity'] = (
                sum(f['complexity'] for f in analysis_results['complexity']) / 
                len(analysis_results['complexity'])
            )
    except Exception as e:
        analysis_results['complexity_error'] = str(e)

    # PyFlakes analysis
    reporter = pyflakes.reporter.Reporter(output, output)
    try:
        pyflakes.api.check(code, filename="<string>", reporter=reporter)
        if output.getvalue():
            analysis_results['pyflakes_warnings'] = output.getvalue().splitlines()
    except Exception as e:
        analysis_results['pyflakes_error'] = str(e)

    # Dynamic profiling
    if dynamic:
        profile_data = dynamic_profile(code)
        if profile_data.get('error'):
            analysis_results['profile_error'] = profile_data['error']
        else:
            analysis_results.update({
                'peak_memory': profile_data['peak_memory'],
                'execution_time': profile_data['execution_time']
            })

    # Security scan
    if security_check:
        analysis_results['security_issues'] = run_security_scan(code)

    # Generate tips and score
    analysis_results['improvement_tips'] = generate_improvement_tips(analysis_results)
    analysis_results['score'] = calculate_score(analysis_results)
    
    return analysis_results

def format_results(analysis_results):
    """Format analysis results for HTML display"""
    formatted = []
    
    if 'error' in analysis_results:
        formatted.append(f"❌ {analysis_results['error']}")
        return "\n".join(formatted)
    
    # Unused code
    if analysis_results['unused_functions']:
        formatted.append("🔴 Unused Functions:")
        formatted.extend(f"• {func}" for func in analysis_results['unused_functions'])
        
    if analysis_results['unused_variables']:
        formatted.append("\n🔴 Unused Variables:")
        formatted.extend(f"• {var}" for var in analysis_results['unused_variables'])
    
    # Complexity
    if analysis_results.get('complexity'):
        formatted.append("\n🧠 Cyclomatic Complexity:")
        for func in analysis_results['complexity']:
            formatted.append(
                f"• {func['name']}(): Complexity {func['complexity']} "
                f"(Rank {func['rank']}, Line {func['line']})"
            )
    
    # Security
    if analysis_results.get('security_issues'):
        formatted.append("\n🛡️ Security Issues:")
        formatted.extend(f"• {issue}" for issue in analysis_results['security_issues'])
    
    # Performance
    if analysis_results.get('peak_memory'):
        formatted.append("\n⚡ Performance:")
        formatted.append(f"• Peak Memory: {analysis_results['peak_memory']:.2f} MiB")
        if analysis_results.get('execution_time'):
            formatted.append(f"• Execution Time: {analysis_results['execution_time']:.2f} seconds")
    
    # Tips
    if analysis_results.get('improvement_tips'):
        formatted.append("\n💡 Improvement Tips:")
        formatted.extend(f"• {tip}" for tip in analysis_results['improvement_tips'])
    
    # Score
    formatted.append(f"\n📊 Overall Code Quality Score: {analysis_results['score']}/10")
    
    return "\n".join(formatted)

@app.route("/", methods=["GET", "POST"])
def home():
    """Main Flask route"""
    result = ""
    code = ""
    
    if request.method == "POST":
        code = request.form.get("code", "")
        dynamic = request.form.get("dynamic") == "on"
        security = request.form.get("security") == "on"
        
        analysis = analyze_code(
            code,
            dynamic=dynamic,
            security_check=security
        )
        result = format_results(analysis)
    
    return render_template(
        "index.html",
        result=result,
        code=code,
        dynamic_checked="checked" if request.form.get("dynamic") else "",
        security_checked="checked" if request.form.get("security") else ""
    )

if __name__ == "__main__":
    print("✅ Static Analyzer Running at http://127.0.0.1:5000")
    app.run(debug=True)
