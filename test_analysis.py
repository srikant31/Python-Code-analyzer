import unittest
from analysis import (
    find_unused_variables,
    find_unused_functions,
    analyze_complexity,
)

class TestCodeAnalysis(unittest.TestCase):

    def test_unused_variables(self):
        code = "a = 10\nprint('hello')"
        unused = find_unused_variables(code)
        self.assertIn('a', unused)

    def test_unused_functions(self):
        code = "def unused(): pass\ndef used(): pass\nused()"
        unused = find_unused_functions(code)
        self.assertIn('unused', unused)
        self.assertNotIn('used', unused)

    def test_complexity(self):
        code = "def hello():\n    if True:\n        print('hi')"
        complexity = analyze_complexity(code)
        self.assertTrue(len(complexity) > 0)

if __name__ == '__main__':
    unittest.main()
