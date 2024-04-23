import subprocess
import sys
import os

# List of required Python packages
required_packages = ["edapiwl==0.0.3", "colorama"]

current_script_dir = os.path.dirname(os.path.abspath(__file__))

package_dir = os.path.dirname(current_script_dir)

python_path = os.path.join('integration', 'get_data.py')
data_path = os.path.join('integration', 'storage','data.txt')
cpp_compile = os.path.join('integration', 'storage', 'compile.py')
cpp_path = os.path.join('integration', 'storage', 'prog')

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
def run_cpp_file(file_path, datafile_path):
    # Convert the file paths to absolute file paths
    file_path = os.path.join(os.getcwd(), file_path)
    datafile_path = os.path.join(os.getcwd(), datafile_path)

    # Path to the output file
    output_file_path = os.path.join(os.path.dirname(file_path), "prog")

    # Space out the output
    print("\n")

    # Run the output file with the data file path as an argument
    run_cpp_executable()

    print("\n")

    subprocess.run([output_file_path, datafile_path])

def run_cpp_executable():
    # Run the compile.py file
    compile_file = os.path.join(package_dir, cpp_compile)
    print(f"Running compile.py: {compile_file}")
    subprocess.run([sys.executable, compile_file])

def main():
    # Install required Python packages
    install_packages()
    # print(package_dir)
    
    # Run Python file from the package
    absolute_py_path = os.path.join(package_dir, python_path)
    run_python_file(absolute_py_path)

    # Run C++ file from the package
    absolute_cpp_path = os.path.join(package_dir, cpp_path)
    absolute_data_path = os.path.join(package_dir, data_path)
    run_cpp_file(absolute_cpp_path, absolute_data_path)

if __name__ == "__main__":
    main()
