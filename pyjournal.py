#!/usr/bin/env python

"""
a simple commandline-driven scientific journal in LaTeX managed by git
"""

import os
import sys
import argparse
import ConfigParser

import build_util
import entry_util
import git_util




if __name__ == "__main__":

    help = {"init": "options: nickname path/ [working-path] -- initialize a journal\n",
            "connect": "options: remote-git-repo local-path/ -- connect to a remote journal for local editing\n",
            "entry": "options: [image1 image2 image3 ...] -- add a new entry, with optional images\n",
            "build": "no options -- build a PDF of the journal",
            "pull": "no options -- pull from the remote journal",
            "push": "no options -- push local changes to the remote journal",
            "status": "no options -- list the current journal information"}
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", help="nickname of the journal", type=str, default=None)

    parser.add_argument("action", metavar="action", type=str, nargs="?", default="entry", 
                        help="one of the allowable actions: init, connect, entry, help, build, pull, push, status")

    parser.add_argument("options", metavar="action-options", type=str,
                        default=None, nargs="*",
                        help="most actions take actions, do 'pyjournal.py help action' to see the options for an action")
                        
    args = parser.parse_args()


    # parse the .pyjournalrc file -- store the results in a dictionary
    # e.g., defs["nickname"]["working_path"]
    defs = {}
    defs["param_file"] = os.path.expanduser("~") + "/.pyjournalrc"
    defs["image_dir"] = os.getcwd()
    
    if os.path.isfile(defs["param_file"]):
        cp = ConfigParser.ConfigParser()
        cp.optionxform = str
        cp.read(defs["param_file"])

        for sec in cp.sections():
            defs[sec] = {}
            defs[sec]["working_path"] = cp.get(sec, "working_path")
            defs[sec]["master_repo"] = cp.get(sec, "master_repo")
            
            
    action = args.action

    if action == "help":
        if not len(args.options) == 1:
            sys.exit("ERROR: help requires an argument (the action)")
                     
        help_action = args.options[0]
        if not help_action in help.keys():
            sys.exit("ERROR: invalid action to requires help for")
        else:
            print help[help_action]
            sys.exit()

    nickname = args.n
    if nickname == None and not (action == "init" or action == "connect"):
        journals = defs.keys()
        journals.remove("param_file")
        journals.remove("image_dir")
        nickname = journals[0]
                
    if action == "init":

        # options: nickname path/ [working-path] 
        if not (len(args.options) >= 2 and len(args.options) <= 3):
            sys.exit("ERROR: invalid number of options for 'init'\n{}".format(help["init"]))

        nickname = args.options[0]
        master_path = args.options[1]
        if len(args.options) == 3:
            working_path = args.options[2]
        else:
            working_path = master_path
            
        git_util.init(nickname, master_path, working_path, defs)

        
    elif action == "connect":

        # options: git-path/ local-path/
        if not len(args.options) == 2:
            sys.exit("ERROR: invalid number of options for 'connect'\n{}".format(help["connect"]))

        master_repo = args.options[0]
        working_path = args.options[1]
        
        git_util.connect(master_repo, working_path, defs)

        
    elif action == "entry":
        
        # options: [image1 image2 image3 ...]
        if len(args.options) >= 1:
            images = args.options
        else:
            images = []
            
        entry_util.entry(nickname, images, defs)

        
    elif action == "build":
        build_util.build(nickname, defs)
        

    elif action == "pull":
        git_util.pull(nickname)

        
    elif action == "push":
        git_util.push(nickname)


    elif action == "status":
        if nickname in defs.keys():
            print "pyjournal"
            print "  current journal: {}".format(nickname)
            print "  working directory: {}/journal-{}".format(defs[nickname]["working_path"], nickname)
            print "  master git repo: {}".format(defs[nickname]["master_repo"], nickname)
            print " "
    else:
        sys.exit("invalid action")

