import shlex
import subprocess

def run(string):

    # shlex.split will preserve inner quotes
    prog = shlex.split(string)
    
    p0 = subprocess.Popen(prog, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)
    stdout0, stderr0 = p0.communicate()
    return stdout0, stderr0, p0.returncode
