from radon.complexity import cc_visit

# Sample code to analyze
code = """
def test(x):
    if x > 10:
        return x
    return x + 1

def complex_func(a, b):
    if a > b:
        for i in range(5):
            if i % 2 == 0:
                print(i)
    elif a == b:
        while b > 0:
            b -= 1
"""

# Manual rank function
def get_rank(complexity):
    if complexity <= 5:
        return "A"
    elif complexity <= 10:
        return "B"
    elif complexity <= 20:
        return "C"
    elif complexity <= 30:
        return "D"
    elif complexity <= 40:
        return "E"
    else:
        return "F"

# Analyze and print
results = cc_visit(code)

for func in results:
    rank = get_rank(func.complexity)
    print(f"Function: {func.name}")
    print(f"  Complexity: {func.complexity}")
    print(f"  Rank: {rank}")
    print(f"  Start line: {func.lineno}")
    print("-" * 40)
