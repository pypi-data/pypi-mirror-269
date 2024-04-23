#!python
import subprocess
import glob
import os

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.realpath(__file__))

# Find all .cpp files in the script's directory
cpp_files = glob.glob(os.path.join(script_dir, '*.cpp'))

output_file = os.path.join(script_dir, 'prog')


# Run the compiler
subprocess.run(['g++', '-Wall', '-std=c++11', '-o', output_file] + cpp_files)