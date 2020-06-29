from os import system
from time import sleep

n = int(input('Number of files to generate: '))
cmd = ""

for i in range(n):
    cmd = "echo " + str(i) + " > " + str(i) + ".txt"
    print("Creating file " + str(i+1) + "/" + str(n))
    system(cmd)
    