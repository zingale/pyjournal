import datetime
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
    entry_id = get_entry_string()
    ofile = entry_id + ".tex"

    # determine the directory we place it in -- this is the form yyyy-mm-dd/
    odir = "{}/journal-{}/entries/{}/".format(defs[nickname]["working_path"],
                                              nickname,
                                              get_dir_string())
    
    if not os.path.isdir(odir):
        try: os.mkdir(odir)
        except:
            sys.exit("ERROR: unable to make directory {}".format(odir))


    # create the entry file.  If we passed in a string, then write it
    # too.
    try: f = open(odir + ofile, "w")             
    except:
        sys.exit("ERROR: unable to open {}".format(odir + ofile))

    if not string == None:
        f.write(string)

    
    # if there are images, then copy them over and add the figure
    # headings to the entry
    if len(images) > 0:        
        for n in range(len(images)):
            # copy it
            im = images[n]
            src = "{}/{}".format(defs["image_dir"], im)
            dest = odir
            try: shutil.copy(src, dest)
            except:
                print src
                print dest
                sys.exit("ERROR: unable to copy image {}".format(im))
                
            # create a unique label for latex referencing
            idx = im.lower().rfind(".jpg")
            idx = max(idx, im.lower().rfind(".png"))
            idx = max(idx, im.lower().rfind(".pdf"))
            
            if idx >= 0:
                im0 = "{}:{}".format(entry_id, im[:idx])

            # add the figure text
            for l in figure_str.split("\n"):
                f.write("{}\n".format(l.replace("@figname@", im).replace("@figlabel@", im0).rstrip()))
                

    # add the entry id as a LaTeX comment
    f.write("\n\n% entry: {}".format(entry_id))    

    f.close()
        
        
    # launch the editor specified in the EDITOR environment variable
    if string == None:
        if editor == "emacs":
            prog = "{} {}/{}".format("emacs -nw", odir, ofile)
        else:
            prog = "{} {}/{}".format(editor, odir, ofile)
            
        stdout0, stderr0 = shell_util.run(prog)
        
        
    # commit the entry to the working git repo
    os.chdir(odir)
    
    stdout0, stderr0 = shell_util.run("git add " + ofile)
    stdout0, stderr0 = shell_util.run("git commit -m 'new entry' " + ofile)

    # commit any images too
