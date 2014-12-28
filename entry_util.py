import datetime
import os
import sys

import shell_util

def get_entry_string():
    now = datetime.datetime.now()
    return str(now.replace(microsecond=0)).replace(" ", "_").replace(":",".")


def get_dir_string():
    now = datetime.date.today()
    return str(now)

    
def entry(nickname, images, defs, string=None):

    try: editor = os.environ["EDITOR"]
    except:
        editor = "emacs"

    # determine the filename
    ofile = get_entry_string() + ".tex"

    # determine the directory we place it in -- this is the form yyyy-mm-dd/
    odir = "{}/journal-{}/entries/{}/".format(defs[nickname]["working_path"],
                                              nickname,
                                              get_dir_string())
    
    if not os.path.isdir(odir):
        try: os.mkdir(odir)
        except:
            sys.exit("ERROR: unable to make directory {}".format(odir))

            
    # launch the editor specified in the EDITOR environment variable
    if string == None:
        if editor == "emacs":
            prog = "{} {}/{}".format("emacs -nw", odir, ofile)
        else:
            prog = "{} {}/{}".format(editor, odir, ofile)
            
        stdout0, stderr0 = shell_util.run(prog)

    else:
        try: f = open(odir + ofile, "w")             
        except:
            sys.exit("ERROR: unable to open {}".format(odir + ofile))

        f.write(string)
        f.close()
        
        
    # commit the entry to the working git repo
    os.chdir(odir)
    
    stdout0, stderr0 = shell_util.run("git add " + ofile)
    stdout0, stderr0 = shell_util.run("git commit -m 'new entry' " + ofile)


