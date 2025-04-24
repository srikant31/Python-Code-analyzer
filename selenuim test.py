import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os

class CodeAnalyzerUITest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set path to your downloaded ChromeDriver
        chrome_driver_path = r"C:\Users\HP\Desktop\chromedriver\chromedriver-win64\chromedriver.exe"  # ← Replace this path

        # Chrome options
        options = Options()
        # options.add_argument("--headless")  # Uncomment to run without opening browser
        options.add_argument("--window-size=1200,800")

        cls.driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)
        cls.driver.get("http://127.0.0.1:5000/")  # Make sure your Flask app is running

    def test_basic_code_analysis(self):
        driver = self.driver

        # Sample code to test
        sample_code = '''def add(a, b):\n    return a + b\nadd(2, 3)'''

        # Fill code into textarea
        textarea = driver.find_element(By.ID, "code")
        textarea.clear()
        textarea.send_keys(sample_code)

        # Enable dynamic profiling checkbox
        checkbox = driver.find_element(By.ID, "dynamic")
        if not checkbox.is_selected():
            checkbox.click()

        # Click the submit button
        submit = driver.find_element(By.XPATH, '//button[@type="submit"]')
        submit.click()

        time.sleep(2)  # Wait for result to appear

        # Get result
        result_div = driver.find_element(By.CLASS_NAME, "result-section")
        self.assertIn("add", result_div.text)  # Check if result contains function name

        print("\n✅ Test Passed. Output:")
        print(result_div.text)

    def test_code_with_syntax_error(self):
        driver = self.driver

        # Code with a syntax error
        sample_code = '''def subtract(a, b)\n    return a - b\nsubtract(5, 3)'''

        # Fill code into textarea
        textarea = driver.find_element(By.ID, "code")
        textarea.clear()
        textarea.send_keys(sample_code)

        # Enable dynamic profiling checkbox
        checkbox = driver.find_element(By.ID, "dynamic")
        if not checkbox.is_selected():
            checkbox.click()

        # Click the submit button
        submit = driver.find_element(By.XPATH, '//button[@type="submit"]')
        submit.click()

        time.sleep(2)  # Wait for result to appear

        # Get result
        result_div = driver.find_element(By.CLASS_NAME, "result-section")
        
        # Adjusted to match more specific error message
        self.assertIn("expected ':' on line 1", result_div.text)  # Check for specific syntax error

        print("\n✅ Test Passed. Output:")
        print(result_div.text)

    def test_code_without_function(self):
        driver = self.driver

        # Code without any function
        sample_code = '''print("Hello World!")'''

        # Fill code into textarea
        textarea = driver.find_element(By.ID, "code")
        textarea.clear()
        textarea.send_keys(sample_code)

        # Enable dynamic profiling checkbox
        checkbox = driver.find_element(By.ID, "dynamic")
        if not checkbox.is_selected():
            checkbox.click()

        # Click the submit button
        submit = driver.find_element(By.XPATH, '//button[@type="submit"]')
        submit.click()

        time.sleep(2)  # Wait for result to appear

        # Get result
        result_div = driver.find_element(By.CLASS_NAME, "result-section")

        # Look for the "Dynamic Analysis" section, not just "print"
        self.assertIn("Peak Memory Usage", result_div.text)  # Look for dynamic analysis info instead

        print("\n✅ Test Passed. Output:")
        print(result_div.text)

    def test_code_with_recursion(self):
        driver = self.driver

        # Sample code with recursion
        sample_code = '''def factorial(n):\n    if n == 0:\n        return 1\n    return n * factorial(n - 1)\nfactorial(5)'''

        # Fill code into textarea
        textarea = driver.find_element(By.ID, "code")
        textarea.clear()
        textarea.send_keys(sample_code)

        # Enable dynamic profiling checkbox
        checkbox = driver.find_element(By.ID, "dynamic")
        if not checkbox.is_selected():
            checkbox.click()

        # Click the submit button
        submit = driver.find_element(By.XPATH, '//button[@type="submit"]')
        submit.click()

        time.sleep(2)  # Wait for result to appear

        # Get result
        result_div = driver.find_element(By.CLASS_NAME, "result-section")
        self.assertIn("factorial", result_div.text)  # Check if recursion result is included

        print("\n✅ Test Passed. Output:")
        print(result_div.text)

    def test_code_with_large_input(self):
        driver = self.driver

        # Sample code with large input
        sample_code = '''def sum_numbers(n):\n    return sum(range(n))\nsum_numbers(1000000)'''

        # Fill code into textarea
        textarea = driver.find_element(By.ID, "code")
        textarea.clear()
        textarea.send_keys(sample_code)

        # Enable dynamic profiling checkbox
        checkbox = driver.find_element(By.ID, "dynamic")
        if not checkbox.is_selected():
            checkbox.click()

        # Click the submit button
        submit = driver.find_element(By.XPATH, '//button[@type="submit"]')
        submit.click()

        time.sleep(2)  # Wait for result to appear

        # Get result
        result_div = driver.find_element(By.CLASS_NAME, "result-section")
        self.assertIn("sum_numbers", result_div.text)  # Check if function result is included

        print("\n✅ Test Passed. Output:")
        print(result_div.text)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()
