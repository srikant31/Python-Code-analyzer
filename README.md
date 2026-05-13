# Industrial Python Static Code Analyzer

<div align="center">

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Deployment](https://img.shields.io/badge/Render-Deployed-brightgreen?style=for-the-badge&logo=render&logoColor=white)](https://cc-pbl-7hdk.onrender.com)
[![Testing](https://img.shields.io/badge/Testing-100%25%20Pass-green?style=for-the-badge&logo=checkmarx&logoColor=white)](https://github.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=for-the-badge)](LICENSE)

**A professional-grade, multi-layered code auditing platform designed to provide a 360-degree view of Python software health.**

[View Live Demo](https://cc-pbl-7hdk.onrender.com) • [Report Bug](https://github.com/) • [Request Feature](https://github.com/)

</div>

---

## Section 1: About the Program

### Overview

The **Industrial Python Static Code Analyzer** is an enterprise-ready web application built to automate the rigorous auditing of Python source code. Unlike standard linters that merely check style, this platform performs deep structural and behavioral analysis. It is designed for developers, QA engineers, and security auditors who require deep insights into code quality, maintainability, and security resilience before deployment.

### Key Features & Technical Deep Dive

#### 1. **Deep Structural Analysis (AST)**

The "brain" of the analyzer uses Python’s **Abstract Syntax Tree (AST)** library. Instead of using simple regular expressions (which can be fooled by comments or strings), the analyzer programmatically "walks" through the hierarchical tree of your code.

* **Implementation:** Utilizes a **Visitor Pattern** to identify `ast.FunctionDef`, `ast.Assign`, and `ast.Call` nodes.
* **Result:** Accurately detects logically unused variables and functions, and calculates the maximum nesting depth of control flow.

#### 2. **Cyclomatic Complexity (McCabe Metric)**

Quantifies the mathematical complexity of your code using **McCabe’s Metric**: $M = E - N + 2P$.

* **Engine:** Powered by the **Radon** library.
* **Ranking:** Automatically assigns grades from **A (Low Complexity)** to **F (High Complexity/Danger)**.
* **Why it matters:** Higher complexity correlates directly with higher defect rates and lower maintainability.

#### 3. **Static Application Security Testing (SAST)**

Integrates a dual-layer security engine to catch vulnerabilities early:

* **Bandit Integration:** Scans the AST for common security issues like hardcoded passwords, insecure temporary files, and dangerous library usage.
* **Custom OWASP Checks:** Uses optimized regex patterns to flag **SQL Injection**, **Cross-Site Scripting (XSS)**, **Code Injection (eval)**, and **Shell Injection** (`subprocess.run(shell=True)`).

#### 4. **Real-Time Dynamic Profiling**

Goes beyond static analysis by executing code in a **sandboxed subprocess** to measure live performance metrics.

* **Resource Monitoring:** Tracks **Peak RAM Usage** (MiB) and **Execution Time** (seconds) using `memory_profiler`.
* **Safety:** Execution is isolated to prevent side effects on the main application server.

#### 5. **Proprietary Scoring & Grading**

The platform features an intelligent scoring algorithm that synthesizes all findings into a **0.0 - 10.0 Quality Score**.

* **Penalties:** Deducts points based on complexity, security risks, broad exception handling (`except Exception:`), and unused artifacts.
* **Actionable Intelligence:** Generates human-readable "Improvement Tips" to guide developers on exactly how to refactor their code for a better score.

### Technology Stack

* **Backend:** Flask 3.0 (Python Micro-framework)
* **Security:** Flask-Talisman (CSP, HSTS, XSS protection)
* **Analysis:** `ast`, `pyflakes`, `radon`, `bandit`
* **Profiling:** `memory_profiler`, `subprocess`
* **Frontend:** Bootstrap 5, Vanilla JavaScript, CSS3 (Glassmorphism design)

---

## Project Structure

```text
static_code_analyzer/
├── app.py              # Main Flask application & Analysis Logic
├── templates/          # HTML Templates (Bootstrap-based)
├── README.md           # Documentation
├── requirements.txt    # Project Dependencies
├── test_analysis.py    # Unit Testing Suite (Backend)
├── test_fuzz.py        # Property-Based Fuzz Testing
├── selenuim test_v2.py # E2E UI Automation (Selenium)
├── final_report.md     # Comprehensive Testing Report
└── test_plan_analyzer.md # Master Test Strategy
```

---

## Installation & Getting Started

### Prerequisites

* Python 3.10 or higher
* Google Chrome (for E2E tests)

### Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/static-code-analyzer.git
   cd static-code-analyzer
   ```
2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   source venv/bin/activate # Linux/Mac
   ```
3. **Install dependencies:**
   ```bash
   pip install flask flask-talisman pyflakes radon memory-profiler bandit selenium webdriver-manager hypothesis
   ```

### Running the Application

```bash
python app.py
```

The application will be available at `http://127.0.0.1:5000`.

---

## Section 2: Comprehensive Testing & Quality Assurance

### Testing Methodologies

| Level            | Methodology                   | Tool                | Total Executions |
| :--------------- | :---------------------------- | :------------------ | :--------------- |
| **Unit**   | Isolated Logic Verification   | `unittest`        | 6                |
| **Fuzz**   | Property-Based Stress Testing | `Hypothesis`      | 111              |
| **UI/E2E** | Browser User Flow             | `Selenium`        | 9                |
| **Perf**   | Resource Profiling            | `memory_profiler` | 2                |

**Total Aggregate Executions: 128 (100% Pass Rate)**

### Execution Commands

```powershell
# Run Unit Tests
python -m unittest test_analysis.py

# Run Fuzz Testing
python test_fuzz.py

# Run UI Automation
python "selenuim test_v2.py"
```

---

## License

Distributed under the MIT License. See `LICENSE` for more information.

---

<div align="center">

**[Deployed on Render](https://cc-pbl-7hdk.onrender.com)**

</div>
