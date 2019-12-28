from __future__ import print_function

import datetime
import hashlib
import os
import shutil
import sys

import shell_util

figure_str = r"""
\begin{figure}[h]
\centering
\includegraphics[width=0.5\linewidth]{@figname@}
\caption{\label{fig:@figlabel@} caption goes here}
\end{figure}

"""

class _TermColors(object):
    WARNING = '\033[93m'
    SUCCESS = '\033[92m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'

def warning(ostr):
    """
    Output a string to the terminal colored orange to indicate a
    warning
    """
    print(_TermColors.WARNING + ostr + _TermColors.ENDC)


def success(ostr):
    """
    Output a string to the terminal colored green to indicate
    success
    """
    print(_TermColors.SUCCESS + ostr + _TermColors.ENDC)


#=============================================================================
# journal-specific routines
#=============================================================================

def get_entry_string():
    now = datetime.datetime.now()
    return str(now.replace(microsecond=0)).replace(" ", "_").replace(":", ".")


def get_dir_string():
    now = datetime.date.today()
    return str(now)


def entry(nickname, images, defs, string=None):

    try: editor = os.environ["EDITOR"]
    except:
        editor = "emacs"

    # determine the filename
    entry_id = get_entry_string()
    entry_dir = get_dir_string()
    ofile = entry_id + ".tex"

    # determine the directory we place it in -- this is the form yyyy-mm-dd/
    odir = "{}/journal-{}/entries/{}/".format(defs[nickname]["working_path"],
                                              nickname,
                                              entry_dir)

    if not os.path.isdir(odir):
        try: os.mkdir(odir)
        except:
            sys.exit("ERROR: unable to make directory {}".format(odir))


    # create the entry file.  If we passed in a string, then write it
    # too.
    try: f = open(odir + ofile, "w")
    except:
        sys.exit("ERROR: unable to open {}".format(odir + ofile))

    if string is not None:
        f.write(string)
    else:
        f.write("% journal: {}\n".format(nickname))


    # if there are images, then copy them over and add the figure
    # headings to the entry
    images_copied = []
    for im in images:

        # does an image by that name already live in the dest
        # directory?
        src = "{}/{}".format(defs["image_dir"], im)
        dest = odir

        if os.path.isfile("{}/{}".format(dest, im)):
            im_copy = "{}_{}".format(entry_id.replace(".", "_"), im)
        else:
            im_copy = im

        dest = "{}/{}".format(dest, im_copy)

        # copy it
        try: shutil.copy(src, dest)
        except:
            sys.exit("ERROR: unable to copy image {} to {}".format(src, dest))

        images_copied.append(im_copy)

        # create a unique label for latex referencing
        idx = im.lower().rfind(".jpg")
        idx = max(idx, im.lower().rfind(".png"))
        idx = max(idx, im.lower().rfind(".gif"))
        idx = max(idx, im.lower().rfind(".pdf"))

        if idx >= 0:
            im0 = "{}:{}".format(entry_id, im[:idx])

        fname = "entries/{}/{}".format(entry_dir, im_copy)
        # add the figure text
        for l in figure_str.split("\n"):
            f.write("{}\n".format(
                l.replace("@figname@", fname).replace("@figlabel@", im0).rstrip()))

    # add the entry id as a LaTeX comment
    f.write("\n\n% entry: {}".format(entry_id))

    f.close()

    # get the hash for the file
    hash_orig = hashlib.md5(open(odir + ofile, 'r').read().encode('utf-8')).hexdigest()


    # launch the editor specified in the EDITOR environment variable
    if string == None:
        if editor == "emacs":
            prog = "emacs -nw {}/{}".format(odir, ofile)
        else:
            prog = "{} {}/{}".format(editor, odir, ofile)

        stdout, stderr, rc = shell_util.run(prog)


    # did the user actually make edits?
    hash_new = hashlib.md5(open(odir + ofile, 'r').read().encode('utf-8')).hexdigest()

    if string == None and len(images) == 0 and (hash_new == hash_orig):
        # user didn't do anything interesting
        answer = raw_input("no input made -- add this to the journal? (y/N) ")
        if answer.lower() != "y":
            try: os.remove(odir + ofile)
            except:
                sys.exit("ERROR: unable to remove file -- entry aborted")

            sys.exit("entry aborted")

    # any tags?
    #tags = find_tags(odir + ofile)
    

    # commit the entry to the working git repo
    os.chdir(odir)

    stdout, stderr, rc = shell_util.run("git add " + ofile)
    stdout, stderr, rc = shell_util.run("git commit -m 'new entry' " + ofile)

    # commit any images too
    for im in images_copied:
        stdout, stderr, rc = shell_util.run("git add " + im)
        stdout, stderr, rc = shell_util.run("git commit -m 'new image' " + im)

    # helpful edit suggestion
    print("entry created.  Use 'pyjournal.py edit {}' to edit this entry.".format(entry_id))


def edit(nickname, date_string, defs):

    if date_string == "last":
        last = elist(nickname, 1, defs, print_out=False)
        date_string = last[0][0]

    # find the file corresponding to the date string
    entry_dir = "{}/journal-{}/entries/".format(defs[nickname]["working_path"], nickname)

    os.chdir(entry_dir)

    # if we got the date string from the prompt, it may have a "_"
    date_string = date_string.replace("_", " ")

    try: d, t = date_string.split(" ")
    except:
        sys.exit("invalid date string")

    if not os.path.isdir(d):
        sys.exit("entry directory does not exist")

    file = "{}/{}_{}.tex".format(d, d, t)

    if not os.path.isfile(file):
        sys.exit("entry {} does not exist".format(file))

    # open the file for appending
    try: editor = os.environ["EDITOR"]
    except:
        editor = "emacs"

    entry_id = get_entry_string()

    try: f = open(file, "a+")
    except:
        sys.exit("ERROR: unable to open {}".format(file))

    f.write("\n\n% entry edited: {}".format(entry_id))
    f.close()

    if editor == "emacs":
        prog = "emacs -nw {}".format(file)
    else:
        prog = "{} {}".format(editor, file)

    stdout, stderr, rc = shell_util.run(prog)

    # git commit any changes
    stdout, stderr, rc = shell_util.run("git commit -m 'edited entry' " + file)


def appendix(nickname, name, defs):

    # is there an appendix directory?
    app_dir = "{}/journal-{}/entries/appendices/".format(
        defs[nickname]["working_path"], nickname)

    if not os.path.isdir(app_dir):
        try: os.mkdir(app_dir)
        except:
            sys.exit("ERROR: unable to make the appendices/ directory")

    os.chdir(app_dir)

    # edit the file, create if it does not exist
    file = "{}.tex".format(name)

    if not os.path.isfile(file):
        warning("appendix {} will be created".format(name))

    # open the file for appending
    try: editor = os.environ["EDITOR"]
    except:
        editor = "emacs"

    try: f = open(file, "a+")
    except:
        sys.exit("ERROR: unable to open {}".format(file))

    entry_id = get_entry_string()

    f.write("\n\n% entry edited: {}".format(entry_id))
    f.close()

    if editor == "emacs":
        prog = "emacs -nw {}".format(file)
    else:
        prog = "{} {}".format(editor, file)

    stdout, stderr, rc = shell_util.run(prog)

    # git commit any changes
    stdout, stderr, rc = shell_util.run("git add " + file)
    stdout, stderr, rc = shell_util.run("git commit -m 'edited appendix' " + file)


def elist(nickname, num, defs, print_out=True):

    entry_dir = "{}/journal-{}/entries/".format(defs[nickname]["working_path"], nickname)
    entries = {}
    for d in os.listdir(entry_dir):
        if os.path.isdir(entry_dir + d):

            edir = os.path.normpath("{}/{}".format(entry_dir, d))

            for t in os.listdir(edir):
                if t.endswith(".tex") and not "appendices" in edir:
                    entries[t] = "{}/{}".format(edir, t)

    e = list(entries.keys())
    e.sort(reverse=True)

    last_entries = []
    for n in range(min(num, len(e))):
        idx = e[n].rfind(".tex")
        entry_id = e[n][:idx]
        last_entries.append((entry_id, entries[e[n]]))

    if print_out:
        for e in last_entries:
            print("{} : {}".format(e[0], e[1]))
    else:
        return last_entries


#=============================================================================
# todo-specific routines
#=============================================================================

def rename_list(old_name, new_name, defs):

    todo_dir = "{}/todo_list/".format(defs["working_path"])

    try: os.chdir(todo_dir)
    except:
        sys.exit("ERROR: unable to cd into working directory {}".format(todo_dir))

    if not os.path.isfile("{}.list".format(old_name)):
        sys.exit("ERROR: list does not exist")

    try: shutil.move("{}.list".format(old_name),
                     "{}.list".format(new_name))
    except:
        sys.exit("ERROR: unable to rename list")

    stdout, stderr, rc = shell_util.run("git add {}.list".format(new_name))
    stdout, stderr, rc = \
        shell_util.run("git commit -m 'renamed' {}.list {}.list".format(old_name, new_name))


def add_list(list_name, defs):

    todo_dir = "{}/todo_list/".format(defs["working_path"])

    try: os.chdir(todo_dir)
    except:
        sys.exit("ERROR: unable to cd into working directory {}".format(todo_dir))


    # does it already exist?
    if os.path.isfile("{}.list".format(list_name)):
        sys.exit("ERROR: list already exists")


    # create the list file
    try: f = open("{}.list".format(list_name), "w")
    except:
        sys.exit("ERROR: unable to create list {}".format(list_name))

    f.write("# list: {} managed by pytodo".format(list_name))
    f.close()


    # commit the list
    stdout, stderr, rc = shell_util.run("git add {}.list".format(list_name))
    stdout, stderr, rc = shell_util.run("git commit -m 'new list' {}.list".format(list_name))


def tlist(defs):

    todo_dir = "{}/todo_list/".format(defs["working_path"])

    try: os.chdir(todo_dir)
    except:
        sys.exit("ERROR: unable to cd into working directory {}".format(todo_dir))


    # find the lists
    known_lists = [os.path.splitext(f)[0] for f in os.listdir(".") if
                   os.path.isfile(f) and f.endswith(".list")]

    for l in sorted(known_lists):
        if l == defs["default_list"]:
            success("* {}".format(l))
        else:
            warning("  {}".format(l))


def show(list_name, defs):

    todo_dir = "{}/todo_list/".format(defs["working_path"])

    try: os.chdir(todo_dir)
    except:
        sys.exit("ERROR: unable to cd into working directory {}".format(todo_dir))


    # does it already exist?
    if not os.path.isfile("{}.list".format(list_name)):
        sys.exit("ERROR: list does not exist")


    hash_orig = hashlib.md5(open("{}.list".format(list_name), 'r').read().encode('utf-8')).hexdigest()

    # open for editing
    try: editor = os.environ["EDITOR"]
    except:
        editor = "emacs"

    if editor == "emacs":
        prog = "emacs -nw {}.list".format(list_name)
    else:
        prog = "{} {}.list".format(editor, list_name)

    stdout, stderr, rc = shell_util.run(prog)

    hash_new = hashlib.md5(open("{}.list".format(list_name), 'r').read().encode('utf-8')).hexdigest()

    if hash_orig != hash_new:

        # git-store the updates
        stdout, stderr, rc = \
            shell_util.run("git commit -m 'edited list {}.list' {}.list".format(list_name, list_name))

        if rc != 0:
            print(stdout, stderr)
            sys.exit("ERROR: there were git errors commiting the list")



def cat(list_name, defs):

    todo_dir = "{}/todo_list/".format(defs["working_path"])

    try: os.chdir(todo_dir)
    except:
        sys.exit("ERROR: unable to cd into working directory {}".format(todo_dir))


    try: f = open("{}.list".format(list_name), "r")
    except:
        sys.exit("ERROR: list {} does not exist".format(list_name))

    print(f.read())

    f.close()
