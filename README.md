# pyjournal

pyjournal is a simple set of commandline scripts to create a
LaTeX-based scientific journal that is managed via `git` so that we
can easily log day-to-day activities from the commandline on any of
our machines and have a consistent, searchable journal.


* Starting:

  -- `pyjournal.py init nickname path/ [working-path]`

     this initializes a bare git repo that will hold the journal data
     it will also add to (or create) a .pyjournal file with an entry

     creating a bare repo for others to clone to/from:

     ```
     cd path/
     mkdir nickname.git
     cd nickname.git
     git init --bare
     ```
     
    creating the working directory that we will interact with:

      cd working-path/
      git clone path/nicknmae

    contents of the .pyjournal

      [nickname]
      master = /path/nickname.git
      working = /working-path/nickname


  pyjournal.py connect git-path local-path

    this will create a clone of a journal on a remote machine (if you
    are only working on a single machine, then you don't need to do this).

      [nickname]
      master = git-path
      working = local-path
      


file structure:

  journal-name/

    entries/
       yyyy-mm-dd/
         entry-yyy-mm-dd-hh-ss.tex
	 ...
       yyyy-mm-dd/


    journal.tex
    GNUmakefile



Day-to-day use:

  pyjournal.py [-n name] entry [XXX [YYY [ZZZ]]]
  
    adds an entry to the journal (optionally named "name") XXX, YYY,
    and ZZZ are optional names of images that will automatically be
    added as figures to the new entry


  pyjournal.py [-n name] build

    builds the journal PDF


  pyjournal.py [-n name] pull

     gets any changes from the remote git


  pyjournal.py [-n name] push



LaTeX structure:

   should be in book form with year as Chapter, month as section, day
   as subsection

   each entry is in a separate `.tex` file (`yyyy-mm-dd-hh-mm-ss.tex`)
   to avoid `git` sync issues (i.e. there should be no conflicts this
   way)
   
   the build process will create a master file for year and month that
   has includes for each of the day's entries



`.pyjournal` structure:

```
[nickname]
   master_path = XXX    ; this is what we push to/pull from
   working_path = YYY   ; local directory we interact with on our machine
```
