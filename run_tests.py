import subprocess
import sys
import os
import docker

def run_pytest(test_files=None):
    """Run multiple pytest files or all tests in the 'tests/' directory."""
    
    # If no specific test files are provided, run all tests in 'tests/' folder
    if not test_files:
        test_dir = "tests"
        if not os.path.exists(test_dir):
            print(f"Error: The test directory '{test_dir}' does not exist.")
            sys.exit(1)
        command = ["pytest", test_dir]  # Run all tests in 'tests/' directory
    else:
        command = ["pytest"] + test_files  # Run specified test files
    
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Tests failed with exit code {e.returncode}")
        sys.exit(e.returncode)

if __name__ == "__main__":
    test_files = sys.argv[1:] 
    run_pytest(test_files)