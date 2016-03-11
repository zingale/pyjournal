import calendar
import os
import sys

import shell_util

def get_appendices(nickname, defs):

    app_dir = "{}/journal-{}/entries/appendices/".format(defs[nickname]["working_path"], nickname)

    app = []
    if os.path.isdir(app_dir):
        for t in os.listdir(app_dir):
            if t.endswith(".tex"):
                app.append(t.split(".")[0])
    return app


def build(nickname, defs, show=0):

    entry_dir = "{}/journal-{}/entries/".format(defs[nickname]["working_path"], nickname)

    entries = []
    years = []

    # get the list of directories in entries/
    for d in os.listdir(entry_dir):
        if d.endswith("appendices"):
            continue

        if os.path.isdir(entry_dir + d):
            entries.append(d)

            y, m, d = d.split("-")
            if not y in years:
                years.append(y)


    os.chdir(entry_dir)

    years.sort()
    entries.sort()

    # years are chapters
    try: f = open("chapters.tex", "w")
    except:
        sys.exit("ERROR: unable to create chapters.tex")


    for y in years:
        f.write("\\chapter{{{}}}\n".format(y))
        f.write("\\input{{entries/{}.tex}}\n\n".format(y))

    # now do the appendices
    f.write("\\appendix\n")

    app_dir = "{}/journal-{}/entries/appendices/".format(defs[nickname]["working_path"], nickname)

    if os.path.isdir(app_dir):
        for t in os.listdir(app_dir):
            if t.endswith(".tex"):
                f.write("\\input{{entries/appendices/{}}}\n\n".format(t))

    f.close()


    # within each year, months are sections
    for y in years:

        try: f = open("{}.tex".format(y), "w")
        except:
            sys.exit("ERROR: unable to create chapters.tex")

        current_month = None
        current_day = None

        for e in entries:
            ytmp, m, d = e.split("-")
            if not ytmp == y:
                continue

            if not m == current_month:
                f.write("\\section{{{}}}\n".format(calendar.month_name[int(m)]))
                current_month = m

            tex = []
            for t in os.listdir(e):
                if t.endswith(".tex"):
                    tex.append(t)

            tex.sort()
            for t in tex:
                if not d == current_day:
                    f.write("\\subsection{{{} {}}}\n".format(calendar.month_name[int(m)], d))
                    current_day = d

                f.write("\\HRule\\\\ \n")
                idx = t.rfind(".tex")
                tout = t[:idx].replace("_", " ")
                f.write("{{\\bfseries {{\sffamily {} }} }}\\\\[0.5em] \n".format(tout))
                f.write("\\input{{entries/{}/{}}}\n\n".format(e, t))
                f.write("\\vskip 2em\n")

            f.write("\n")

        f.close()


    # now do the latexing to get the PDF
    build_dir = "{}/journal-{}/".format(defs[nickname]["working_path"], nickname)
    os.chdir(build_dir)

    for i in range(3):
        stdout, stderr, rc = shell_util.run("pdflatex --halt-on-error journal.tex")

    # if we were not successful, then the PDF is not produced
    # note: pdflatex does not seem to use stderr at all
    pdf = os.path.normpath("{}/journal.pdf".format(build_dir))
    if os.path.isfile(pdf):
        print "journal is located at {}".format(pdf)
    else:
        print stdout
        print "There were LaTeX errors"
        print "Check the source in {}/entries/".format(build_dir)
        print "be sure to 'git commit' to store any fixes"
        sys.exit()


    # show it in a PDF viewer
    if show == 1:
        os.system("evince {} &".format(pdf))
