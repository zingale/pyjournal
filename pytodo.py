#!/usr/bin/env python

import argparse
import ConfigParser
import os
import sys

import entry_util
import git_util

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(help="commands", dest="command")

    # the show command
    show_parser = subparsers.add_parser("show", help="show a list in an editor")
    show_parser.add_argument("list-name", help="the name of the todo list to show",
                             nargs=1, default=None, type=str)

    # the cat command
    show_parser = subparsers.add_parser("cat", help="display a list in the terminal (no editing)")
    show_parser.add_argument("list-name", help="the name of the todo list to show",
                             nargs=1, default=None, type=str)
    
    # the init command
    init_parser = subparsers.add_parser("init", help="initialize a todo collection")
    init_parser.add_argument("master-path",
                             help="path where we will store the master (bare) git repo",
                             nargs=1, default=None, type=str)
    init_parser.add_argument("working-path",
                             help="path where we will store the working directory (clone of bare repo)", 
                             nargs="?", default=None, type=str)

    # the connect command
    connect_parser = subparsers.add_parser("connect", help="create a local working copy of a remote todo collection")
    connect_parser.add_argument("remote-git-repo", help="the full path to the remote '.git' bare repo",
                                nargs=1, default=None, type=str)
    connect_parser.add_argument("working-path", help="the (local) path where we will store the working directory",
                                nargs=1, default=None, type=str)
                
    # the add command
    add_parser = subparsers.add_parser("add", help="add a new todo list to the collection")
    add_parser.add_argument("list-name", help="the name of the new todo list",
                            nargs=1, default=None, type=str)
    
    # the list command
    list_parser = subparsers.add_parser("list", help="list available todo lists")

    # the push command
    push_parser = subparsers.add_parser("push", help="push local changes to the master repo")

    # the push command
    pull_parser = subparsers.add_parser("pull", help="pull remote changes to the local todo collection")
    
    args = vars(parser.parse_args())


    # parse the .pytodorc file -- store the results in a dictionary
    defs = {}
    defs["param_file"] = os.path.expanduser("~") + "/.pytodorc"
    
    if os.path.isfile(defs["param_file"]):
        cp = ConfigParser.ConfigParser()
        cp.optionxform = str
        cp.read(defs["param_file"])

        if not "main" in cp.sections():
            sys.exit("ERROR: no lists initialized")

        # main -- there is only one working directory/master repo for
        # all lists
        defs["working_path"] = cp.get("main", "working_path")
        defs["master_repo"] = cp.get("main", "master_repo")
        

    # take the appropriate action
    action = args["command"]

    if action == "show":
        list_name = args["list-name"][0]
        entry_util.show(list_name, defs)

    if action == "cat":
        list_name = args["list-name"][0]
        entry_util.cat(list_name, defs)
        
    elif action == "init":
        master_path = args["master-path"][0]

        if "working-path" in args.keys():
            working_path = args["working-path"]  # when using "?" argparse doesn't make this a list
        else:
            working_path = master_path

        master_path = os.path.normpath(os.path.expanduser(master_path))
        working_path = os.path.normpath(os.path.expanduser(working_path))
        
        git_util.init_todo(master_path, working_path, defs)
        
    elif action == "connect":
        master_repo = args["remote-git-repo"][0]
        working_path = args["working-path"][0]

        working_path = os.path.normpath(os.path.expanduser(working_path))
        
        git_util.connect_todo(master_repo, working_path, defs)        
        
    elif action == "add":
        list_name = args["list-name"][0]
        entry_util.add_list(list_name, defs)
        
    elif action == "list":
        entry_util.tlist(defs)
        
    elif action == "push":
        git_util.push(defs)
        
    elif action == "pull":
        git_util.pull(defs)
        
    else:
        sys.exit("you should not have gotten here -- invalid action")

        

                                                    
    
    
    
