#!/usr/bin/env python3

"""
a simple commandline-driven scientific journal in LaTeX managed by git
"""

from __future__ import print_function

import argparse
try: import ConfigParser as configparser                                        
except ImportError:                                                             
    import configparser
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
                             help="entry id to edit, in the form: yyyy-mm-dd hh.mm.ss or use 'last' to edit the last entry",
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

        # the appendix command
        app_ps = sp.add_parser("appendix",
                               help="add or modify an appendix of the journal")
        app_ps.add_argument("-n", metavar="nickname",
                            help="nickname of the journal",
                            type=str, default=None)
        app_ps.add_argument("name",
                             help="the name of the appendix to edit",
                             nargs=1, default=None, type=str)

        # the make-default command
        make_default_ps = sp.add_parser("make-default",
                                        help="make a journal the default for showing")
        make_default_ps.add_argument("journal-name",
                                     help="the name of the journal",
                                     nargs=1, default=None, type=str)


        args = vars(p.parse_args())


    # parse the .pyjournalrc file -- store the results in a dictionary
    # e.g., defs["nickname"]["working_path"]
    defs = {}
    defs["param_file"] = os.path.expanduser("~") + "/.pyjournalrc"
    defs["image_dir"] = os.getcwd()
    defs["default_journal"] = None
    
    if os.path.isfile(defs["param_file"]):
        cp = configparser.ConfigParser()
        cp.optionxform = str
        cp.read(defs["param_file"])

        secs = cp.sections()
        
        if "main" in secs:
            secs.remove("main")
            defs["default_journal"] = cp.get("main", "default_journal")
            
        for sec in secs:
            defs[sec] = {}
            defs[sec]["working_path"] = cp.get(sec, "working_path")
            defs[sec]["master_repo"] = cp.get(sec, "master_repo")


    action = args["command"]

    if not (action == "init" or action == "connect"):
        journals = list(defs.keys())
        journals.remove("param_file")
        journals.remove("image_dir")
        journals.remove("default_journal")

        if len(journals) > 0:
            if defs["default_journal"] == None:
                default_nickname = journals[0]
            else:
                default_nickname = defs["default_journal"]

        if not args["n"] == None:
            nickname = args["n"]
        else:
            nickname = default_nickname                
        
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
        entry_util.entry(nickname, images, defs)

    elif action == "edit":
        # options: date-string
        date_string = args["date-time string"][0]
        entry_util.edit(nickname, date_string, defs)

    elif action == "appendix":
        name = args["name"][0]
        entry_util.appendix(nickname, name, defs)

    elif action == "list":

        # options: number to list (optional)
        num = args["N"]
        entry_util.elist(nickname, num, defs)

    elif action == "build":
        build_util.build(nickname, defs)

    elif action == "show":
        build_util.build(nickname, defs, show=1)

    elif action == "pull":
        git_util.pull(defs, nickname=nickname)

    elif action == "push":
        git_util.push(defs, nickname=nickname)

    elif action == "status":
        apps = build_util.get_appendices(nickname, defs)

        if nickname in defs.keys():
            print("pyjournal")
            print("  current journal: {}".format(nickname))
            print("  working directory: {}/journal-{}".format(defs[nickname]["working_path"], nickname))
            print("  master git repo: {}".format(defs[nickname]["master_repo"], nickname))
            print(" ")
            if not len(apps) == 0:
                print("  appendices: ")
                for a in apps:
                    print("    {}".format(a))
                print(" ")

        print("known journals:")
        for k in defs.keys():
            if k in ["main", "default_journal", "param_file", "image_dir"]:
                continue
            print("  {}".format(k))
                
    elif action == "make-default":
        if not cp.has_section("main"):
            cp.add_section("main")
        cp.set("main", "default_journal", args["journal-name"][0])
        with open(defs["param_file"], "w") as config_file:
            cp.write(config_file)
                
    else:
        # we should never land here, because of the choices argument
        # to actions in the argparser
        sys.exit("invalid action")
