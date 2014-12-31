#!/usr/bin/env python

"""
a simple commandline-driven scientific journal in LaTeX managed by git
"""

import argparse
import ConfigParser
import os
import sys

import build_util
import entry_util
import git_util


if __name__ == "__main__":

    # short circuit -- if there are no arguments, then we default to
    # entry, and we don't take any arguments, and we don't do an
    # argparse
    
    if len(sys.argv) == 1:  # the command name is first argument
        args = {"command": "entry",
                "images": [],
                "n": None}            
        
    else:
    
        p = argparse.ArgumentParser()

        sp = p.add_subparsers(title="subcommands",
                              description="valid subcommands",
                              help="subcommands (use -h to see options for each)",
                              dest="command")

        # the init command
        init_ps = sp.add_parser("init", help="initialize a journal")
        init_ps.add_argument("nickname", help="name of the journal",
                             nargs=1, default=None, type=str)
        init_ps.add_argument("master-path",
                             help="path where we will store the master (bare) git repo",
                             nargs=1, default=None, type=str)
        init_ps.add_argument("working-path",
                             help="path where we will store the working directory (clone of bare repo)",
                             nargs="?", default=None, type=str)

        # the connect command
        connect_ps = sp.add_parser("connect",
                                   help="create a local working copy of a remote journal")
        connect_ps.add_argument("remote-git-repo",
                                help="the full path to the remote '.git' bare repo",
                                nargs=1, default=None, type=str)
        connect_ps.add_argument("working-path",
                                help="the (local) path where we will store the working directory",
                                nargs=1, default=None, type=str)

        # the entry command
        entry_ps = sp.add_parser("entry",
                                 help="add a new entry, with optional images")
        entry_ps.add_argument("images", help="images to include as figures in the entry",
                              nargs="*", default=None, type=str)
        entry_ps.add_argument("-n", metavar="nickname",
                              help="nickname of the journal",
                              type=str, default=None)

        # the edit command
        edit_ps = sp.add_parser("edit",
                                help="edit an existing entry")
        edit_ps.add_argument("date-time string",
                             help="entry id to edit, in the form: yyyy-mm-dd hh.mm.ss",
                             nargs=1, default=None, type=str)
        edit_ps.add_argument("-n", metavar="nickname",
                             help="nickname of the journal",
                             type=str, default=None)

        # the list command
        list_ps = sp.add_parser("list",
                                help="list the recent entry id's and .tex file path for the last entries")
        list_ps.add_argument("-n", metavar="nickname",
                             help="nickname of the journal",
                             type=str, default=None)
        list_ps.add_argument("-N", help="number of entries to list",
                             type=int, default=10)    

        # the build command
        build_ps = sp.add_parser("build",
                                 help="build a PDF of the journal")
        build_ps.add_argument("-n", metavar="nickname",
                              help="nickname of the journal",
                              type=str, default=None)

        # the pull command
        pull_ps = sp.add_parser("pull",
                                help="pull from the remote journal" )
        pull_ps.add_argument("-n", metavar="nickname",
                             help="nickname of the journal",
                             type=str, default=None)

        # the push command
        push_ps = sp.add_parser("push",
                                help="push local changes to the remote journal")
        push_ps.add_argument("-n", metavar="nickname",
                             help="nickname of the journal",
                             type=str, default=None)

        # the status command
        stat_ps = sp.add_parser("status",
                                help="list the current journal information")
        stat_ps.add_argument("-n", metavar="nickname",
                             help="nickname of the journal",
                             type=str, default=None)

        # the show command
        show_ps = sp.add_parser("show",
                                help="build the PDF and launch a PDF viewer")
        show_ps.add_argument("-n", metavar="nickname",
                             help="nickname of the journal",
                             type=str, default=None)    
    
        args = vars(p.parse_args())


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
            
            
    action = args["command"]

    if not (action == "init" or action == "connect"):
        journals = defs.keys()
        journals.remove("param_file")
        journals.remove("image_dir")
        if len(journals) > 0:
            default_nickname = journals[0]
                
    if action == "init":

        nickname = args["nickname"][0]
        master_path = args["master-path"][0]


        working_path = args["working-path"]
        if working_path == None:
            working_path = master_path
        
        master_path = os.path.normpath(os.path.expanduser(master_path))
        working_path = os.path.normpath(os.path.expanduser(working_path))
        
        git_util.init(nickname, master_path, working_path, defs)

    elif action == "connect":

        master_repo = args["remote-git-repo"][0]
        working_path = args["working-path"][0]

        working_path = os.path.normpath(os.path.expanduser(working_path))
        
        git_util.connect(master_repo, working_path, defs)
        
    elif action == "entry":

        images = args["images"]

        if not args["n"] == None:
            nickname = args["n"]
        else:
            nickname = default_nickname
            
        entry_util.entry(nickname, images, defs)

    elif action == "edit":
        
        # options: date-string
        date_string = args["date-time string"][0]

        if not args["n"] == None:
            nickname = args["n"]
        else:
            nickname = default_nickname
        
        entry_util.edit(nickname, date_string, defs)

    elif action == "list":
        
        # options: number to list (optional)
        num = args["N"]

        if not args["n"] == None:
            nickname = args["n"]
        else:
            nickname = default_nickname
            
        entry_util.elist(nickname, num, defs)

        
    elif action == "build":

        if not args["n"] == None:
            nickname = args["n"]
        else:
            nickname = default_nickname

        build_util.build(nickname, defs)

    elif action == "show":

        if not args["n"] == None:
            nickname = args["n"]
        else:
            nickname = default_nickname
        
        build_util.build(nickname, defs, show=1)        
        
    elif action == "pull":

        if not args["n"] == None:
            nickname = args["n"]
        else:
            nickname = default_nickname
        
        git_util.pull(defs, nickname=nickname)
        
    elif action == "push":

        if not args["n"] == None:
            nickname = args["n"]
        else:
            nickname = default_nickname
        
        git_util.push(defs, nickname=nickname)

    elif action == "status":

        if not args["n"] == None:
            nickname = args["n"]
        else:
            nickname = default_nickname

        if nickname in defs.keys():
            print "pyjournal"
            print "  current journal: {}".format(nickname)
            print "  working directory: {}/journal-{}".format(defs[nickname]["working_path"], nickname)
            print "  master git repo: {}".format(defs[nickname]["master_repo"], nickname)
            print " "
    else:
        # we should never land here, because of the choices argument
        # to actions in the argparser
        sys.exit("invalid action")

