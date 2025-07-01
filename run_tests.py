#!/usr/bin/env python3
"""
Script to run tests with proper configuration.
"""
import subprocess
import sys
import os


def run_command(command):
    """Run a command and return the result."""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    
    return result.returncode


def main():
    """Main function to run tests."""
    # Set environment variables
    os.environ["PYTHONPATH"] = "."
    
    # Run tests with coverage
    test_command = (
        "python -m pytest "
        "--cov=src "
        "--cov-report=term-missing "
        "--cov-report=html:htmlcov "
        "--cov-fail-under=80 "
        "-v"
    )
    
    exit_code = run_command(test_command)
    
    if exit_code == 0:
        print("\n✅ All tests passed!")
        print("📊 Coverage report generated in htmlcov/index.html")
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    main() 