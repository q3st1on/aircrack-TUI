import os
import sys
import subprocess

command = "airmon-ng check kill"
output = os.popen(command).read()
print(output)