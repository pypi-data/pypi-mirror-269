import subprocess
import sys
import os

# Get the directory of the current script
current_script_dir = os.path.dirname(os.path.abspath(__file__))

# List of required Python packages
required_packages = ["edapiwl==0.0.3", "colorama"]

# Function to check and install Python packages
def install_packages():
    installed_packages = subprocess.check_output([sys.executable, "-m", "pip", "list"]).decode("utf-8")
    for package in required_packages:
        if package not in installed_packages:
            print(f"Installing {package}...")
            subprocess.run([sys.executable, "-m", "pip", "install", package])

# Function to run a Python file
def run_python_file(file_path):
    print(f"Running Python file: {file_path}")
    subprocess.run([sys.executable, file_path])

# Function to run a C++ file
def run_cpp_file(file_path):
    print(f"Compiling and running C++ file: {file_path}")
    subprocess.run(["g++", "-std=c++11", file_path, "-o", f"{current_script_dir}/output"])
    subprocess.run([f"{current_script_dir}/output"])

def main():
    # Install required Python packages
    install_packages()
    
    # Run Python file
    python_file_path = os.path.join(current_script_dir, "edstem/integration/get_data.py")
    run_python_file(python_file_path)
    
    # Run C++ file
    cpp_file_path = os.path.join(current_script_dir, "edstem/integration/storage/main.cpp")
    run_cpp_file(cpp_file_path)

if __name__ == "__main__":
    main()
