import subprocess
import sys
import os

# List of required Python packages
required_packages = ["edapiwl==0.0.3", "colorama"]

current_script_dir = os.path.dirname(os.path.abspath(__file__))

package_dir = os.path.dirname(current_script_dir)

python_path = "integration/get_data.py"
cpp_path = "integration/storage/main.cpp"

def install_packages():
    """
    Function to check and install Python packages
    """
    installed_packages = subprocess.check_output([sys.executable, "-m", "pip", "list"]).decode("utf-8")
    for package in required_packages:
        if package not in installed_packages:
            print(f"Installing {package}...")
            subprocess.run([sys.executable, "-m", "pip", "install", package])


def run_python_file(file_path):
    """
    Function to run a Python file
    """
    print(f"Running Python file: {file_path}")
    subprocess.run([sys.executable, file_path])

# Function to run a C++ file
def run_cpp_file(file_path):
    """
    Function to compile and run a C++ file
    """
    # Compile the C++ file
    compile_command = ["g++", "-std=c++11", file_path, "-o", os.path.join(os.path.dirname(file_path), "output")]
    subprocess.run(compile_command)

    # Run the output file
    subprocess.run([os.path.join(os.path.dirname(file_path), "output")])

def main():
    # Install required Python packages
    install_packages()
    print(package_dir)
    
    # Run Python file from the package
    absolute_py_path = os.path.join(package_dir, python_path)
    run_python_file(absolute_py_path)
    
    # Run C++ file from the package
    absolute_cpp_path = os.path.join(package_dir, cpp_path)
    run_cpp_file(absolute_cpp_path)

if __name__ == "__main__":
    main()
