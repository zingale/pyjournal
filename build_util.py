import os
import sys

def build(nickname, defs):

    entry_dir = "{}/journal-{}/entries/".format(defs[nickname]["working_path"], nickname)


    entries = []
    years = []
    
    # get the list of directories in entries/
    for d in os.listdir(entry_dir):
        if os.path.isdir(entry_dir + d):
            entries.append(d)

            y, m, d = d.split("-")
            if not y in years:
                years.append(y)
            
    # years are chapters
    try: f = open(entry_dir + "/chapters.tex", "w")
    except:
        sys.exit("ERROR: unable to create chapters.tex")
        

    for y in years:
        f.write("\\chapter{{{}}}\n".format(y))
        f.write("\\include {}.tex\n\n".format(y))

    # within each year, months are sections


    # write chapters.tex


    # write yyyy.tex
