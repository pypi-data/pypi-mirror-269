#!python
import subprocess
subprocess.run(['g++', '-Wall', '-std=c++11', '-o prog', './*.cpp'])