import os
import subprocess
import sys

import entry_util
import master_util

def init(nickname, master_path, working_path, defs):

    # make sure that a journal with this nickname doesn't already exist
    if nickname in defs.keys():
        sys.exit("ERROR: nickname already exists")
    
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
                  
    
    # create (or add to) the .pyjournalrc file
    try: f = open(defs["param_file"], "a+")             
    except:
        sys.exit("ERROR: unable to open {} for appending".format(defs["param_file"]))

    f.write("[{}]\n".format(nickname))
    f.write("master_path = {}\n".format(master_path))
    f.write("working_path = {}\n".format(working_path))

    f.close()

    defs[nickname] = {}
    defs[nickname]["working_path"] = working_path
    defs[nickname]["master_path"] = master_path
    
    # create an initial entry saying "journal created"
    images = []
    entry_util.entry(nickname, images, defs, string="journal created")

    
    # copy over the journal.tex
    try: f = open("{}/journal.tex".format(working_journal), "w")
    except:
        sys.exit("ERROR: unable to open {}/journal.tex".format(working_journal))

    for line in master_util.journal_master.split("\n"):
        f.write("{}\n".format(line.rstrip()))

    f.close()
    
    
    # do a git push to make it synced
    os.chdir(working_journal)
    prog = ["git", "push"]
    p0 = subprocess.Popen(prog, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT)
    stdout0, stderr0 = p0.communicate()
    
    
    
def connect(nickname, master_path, working_path):

    # git clone the bare repo at master_path into the working path

    # create (or add to) the .pyjournalrc file
    
    pass


def pull(nickname):

    pass


def push(nickname):

    pass


