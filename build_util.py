import os
import sys

import shell_util

month = {"1": "January",
         "2": "February",
         "3": "March",
         "4": "April",
         "5": "May",
         "6": "June",
         "7": "July",
         "8": "August",
         "9": "September",
         "10": "October",
         "11": "November",
         "12": "December"}

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

            
    os.chdir(entry_dir)
                
    # years are chapters
    try: f = open("chapters.tex", "w")
    except:
        sys.exit("ERROR: unable to create chapters.tex")
        

    for y in years:
        f.write("\\chapter{{{}}}\n".format(y))
        f.write("\\input{{entries/{}.tex}}\n\n".format(y))

    f.close()

    
    # within each year, months are sections
    for y in years:

        try: f = open("{}.tex".format(y), "w")
        except:
            sys.exit("ERROR: unable to create chapters.tex")

        current_month = None
        
        for e in entries:
            ytmp, m, _ = e.split("-")            
            if not ytmp == y:
                continue

            if not m == current_month:
                f.write("\\section{{{}}}\n".format(month[m]))

            tex = []
            for t in os.listdir(e):
                if t.endswith(".tex"):
                    tex.append(t)

            tex.sort()
            for t in tex:
                f.write("\\HRule\\\\ \n")
                idx = t.rfind(".tex")
                tout = t[:idx].replace("_", " ")
                f.write("{{\\bf {} }}\\\\[0.5em] \n".format(tout))
                f.write("\\input{{entries/{}/{}}}\n\n".format(e, t))
                f.write("\\vskip 2em\n")
                    
            f.write("\n")
            
        f.close()

        
    # now do the latexing to get the PDF
    build_dir = "{}/journal-{}/".format(defs[nickname]["working_path"], nickname)
    os.chdir(build_dir)
    
    for i in range(3):
        stdout0, stderr0 = shell_util.run("pdflatex journal.tex")        

    print "journal is located at {}/journal.pdf".format(build_dir)
    
