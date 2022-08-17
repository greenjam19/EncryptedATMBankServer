import os
import sys
while 1:
    os.system("python main.py")
    print("Restarting...")
    os.execl(sys.executable, sys.executable, *sys.argv)
    exit()