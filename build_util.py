import os
import sys

month = {"1": "Jan", "2": "Feb", "3": "Mar",  "4": "Apr",  "5": "May",  "6": "Jun",
         "7": "Jul", "8": "Aug", "9": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"}

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

            for t in os.listdir(e):
                if t.endswith(".tex"):
                    f.write("\\input{{entries/{}/{}}}\n".format(e, t))

            f.write("\n")
            
        f.close()


