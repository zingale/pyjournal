import os
import sys

import entry_util
import master_util
import shell_util

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
    stdout0, stderr0 = shell_util.run("git init --bare")
    

    # create the local working copy
    try: os.chdir(os.path.normpath(working_path))
    except:
        sys.exit("ERROR: unable to change to {}".format(working_path))

    stdout0, stderr0 = shell_util.run("git clone " + git_master)
    

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
    f.write("master_repo = {}\n".format(git_master))
    f.write("working_path = {}\n".format(working_path))
    f.write("\n")
    f.close()

    defs[nickname] = {}
    defs[nickname]["master_repo"] = git_master
    defs[nickname]["working_path"] = working_path
    
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

    stdout0, stderr0 = shell_util.run("git push")
        
    
def connect(nickname, master_repo, working_path, defs):

    # does the nickname match the master repo name?
    
    # git clone the bare repo at master_repo into the working path
    try: os.chdir(working_path)
    except:
        sys.exit("ERROR: unable to switch to directory {}".format(working_path))
        
    stdout0, stderr0 = shell_util.run("git clone " + master_repo)
    print stdout0, stderr0
    
    # create (or add to) the .pyjournalrc file
    try: f = open(defs["param_file"], "a+")             
    except:
        sys.exit("ERROR: unable to open {} for appending".format(defs["param_file"]))

    f.write("[{}]\n".format(nickname))
    f.write("master_repo = {}\n".format(master_repo))
    f.write("working_path = {}\n".format(working_path))
    f.write("\n")
    f.close()


def pull(nickname):

    pass


def push(nickname):

    pass


