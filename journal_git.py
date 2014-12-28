import os
import subprocess
import sys

def init(nickname, master_path, working_path, defs):

    param_file = defs["param_file"]
    
    # create the bare git repo
    git_master = "{}/journal-{}.git".format(os.path.normpath(master_path), nickname)
    try: os.mkdir(git_master)
    except:
        sys.exit("ERROR: unable to create a directory in {}".format(master_path))

    os.chdir(git_master)
    prog = ["git", "init", "--bare"]
    p0 = subprocess.Popen(prog, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT)
    stdout0, stderr0 = p0.communicate()
    

    # create the local working copy
    try: os.chdir(os.path.normpath(working_path))
    except:
        sys.exit("ERROR: unable to change to {}".format(working_path))

    prog = ["git", "clone", git_master]
    p0 = subprocess.Popen(prog, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT)
    stdout0, stderr0 = p0.communicate()
    

    # create the initial directory structure
    working_journal = "{}/journal-{}".format(os.path.normpath(working_path), nickname)
    
    try: os.mkdir(working_journal + "/entries/")
    except:
        sys.exit("ERROR: unable to create initial directory structure")
                  
    # create an initial entry saying "journal created"

    # copy over the journal.tex

    # do a git push to make it synced

    
    # create (or add to) the .pyjournalrc file
    try: f = open(defs["param_file"], "a+")             
    except:
        sys.exit("ERROR: unable to open {} for appending".format(defs["param_file"]))

    f.write("[{}]\n".format(nickname))
    f.write("master_path = {}\n".format(master_path))
    f.write("working_path = {}\n".format(working_path))

    f.close()

    
def connect(nickname, master_path, working_path):

    # git clone the bare repo at master_path into the working path

    # create (or add to) the .pyjournalrc file
    
    pass


def pull(nickname):

    pass


def push(nickname):

    pass


