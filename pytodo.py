import os
import argparse



if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(help='commands', dest="command")

    # the show command
    show_parser = subparsers.add_parser("show", help="show a list")
    show_parser.add_argument("list-name", help="the name of the todo list to show",
                             nargs=1, default=None, type=str)
    
    # the init command
    init_parser = subparsers.add_parser("init", help="initialize a todo collection")
    init_parser.add_argument("master-path", help="path where we will store the master (bare) git repo",
                             nargs=1, default=None, type=str)
    init_parser.add_argument("working-path", help="path where we will store working directory (clone of bare repo)", 
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
    
    args = parser.parse_args()

    print vars(args)
    
    
    
