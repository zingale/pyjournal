# pyjournal

pyjournal is a simple set of commandline scripts to create a
LaTeX-based scientific journal that is managed via `git` so that we
can easily log day-to-day activities from the commandline on any of
our machines and have a consistent, searchable journal.


* Starting:

  - `pyjournal.py init nickname path/ [working-path]`

    this initializes a bare git repo that will hold the journal data
    it will also add to (or create) a `.pyjournal` file with an entry

    creating a bare repo for others to clone to/from:

    ```
    cd path/
    mkdir nickname.git
    cd nickname.git
    git init --bare
    ```
     
    creating the working directory that we will interact with:

    ```
    cd working-path/
    git clone path/nicknmae
    ```

    contents of the `.pyjournal`

    ```
    [nickname]
    master_path = /path/nickname.git
    working_path = /working-path/nickname
    ```

  - `pyjournal.py connect git-path local-path`

    this will create a clone of a journal on a remote machine (if you
    are only working on a single machine, then you don't need to do this).

    ```
    [nickname]
    master_path = git-path
    working_path = local-path
    ```  

* Directory structure:

  ```
  journal-nickname/

    entries/
      yyyy-mm-dd/
        entry-yyy-mm-dd-hh-ss.tex
        ...
      yyyy-mm-dd/

    journal.tex
  ```


* Day-to-day use:

  - `pyjournal.py [-n nickname] entry [XXX YYY ZZZ ...]`
  
    adds an entry to the journal (optionally named "nickname"). `XXX`,
    `YYY`, and `ZZZ` are optional names of images that will
    automatically be added as figures to the new entry

  - `pyjournal.py [-n nickname] build`

    builds the journal PDF

  - `pyjournal.py [-n nickname] pull`

     gets any changes from the master version of the journal (remote
     git bare repository)

  - `pyjournal.py [-n nickname] push`

    pushes any changes in the local journal to the remote (git bare
    repo) version
 

* LaTeX structure:

  The journal is in book form with the year as a chapter and month as
  a section.  The individual entries are separated with a horizontal
  rule and noted with the time of the entry.

  Each entry is in a separate `.tex` file (`yyyy-mm-dd-hh-mm-ss.tex`)
  to avoid `git` sync issues (i.e. there should be no conflicts this
  way)
   
  The build process will create a master file for year and month that
  has includes for each of the day's entries


* `.pyjournal` structure:

  ```
  [nickname]
  master_path = XXX    ; this is what we push to/pull from
  working_path = YYY   ; local directory we interact with on our machine
  ```
