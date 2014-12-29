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

    help = {"init":
              "initialize a journal\n" + 
              "options: nickname path/ [working-path]\n",

            "connect":
              "connect to a remote journal for local editing\n" +
              "options: remote-git-repo local-path/\n",

            "entry":
              "add a new entry, with optional images\n" +
              "options: [image1 [image2 ... ]]\n",

            "build":
              "build a PDF of the journal\n" +
              "no options\n",

            "pull":
              "pull from the remote journal\n" +
              "no options\n",

            "push":
              "push local changes to the remote journal\n" +
              "no options\n",

            "status":
              "list the current journal information\n" +
              "no options\n",

            "show":
              "build the PDF and launch a PDF viewer\n" +
              "no options\n"}
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", help="nickname of the journal",
                        type=str, default=None)

    parser.add_argument("action", metavar="action",
                        type=str, nargs="?", default="entry", 
                        help="an action: {}".format(help.keys()))

    parser.add_argument("options", metavar="options", type=str,
                        default=None, nargs="*",
                        help="options for the actions.  " + \
                             "'pyjournal.py help action' lists options")
                        
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
                     
        ha = args.options[0]
        if not ha in help.keys():
            sys.exit("ERROR: invalid action to requires help for")
        else:
            print "pyjournal.py {} options: {}\n".format(ha, help[ha])
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
            print "ERROR: invalid number of options for 'init'"
            sys.exit("{}".format(help["init"]))

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
            print "ERROR: invalid number of options for 'connect'"
            sys.exit("{}".format(help["connect"]))

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

    elif action == "show":
        build_util.build(nickname, defs, show=1)        
        
    elif action == "pull":
        git_util.pull(nickname, defs)
        
    elif action == "push":
        git_util.push(nickname, defs)

    elif action == "status":
        if nickname in defs.keys():
            print "pyjournal"
            print "  current journal: {}".format(nickname)
            print "  working directory: {}/journal-{}".format(defs[nickname]["working_path"], nickname)
            print "  master git repo: {}".format(defs[nickname]["master_repo"], nickname)
            print " "
    else:
        sys.exit("invalid action")

