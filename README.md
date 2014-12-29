# pyjournal

pyjournal is a simple set of commandline scripts to create a
LaTeX-based scientific journal that is managed via `git` so that we
can easily log day-to-day activities from the commandline on any of
our machines and have a consistent, searchable journal.


* Starting:

  - `pyjournal.py init nickname path/ [working-path]`

    this initializes a bare git repo that will hold the journal data,
    creates the initial directory structure to hold the journal
    entries, and copies in the master journal.tex file.  It will also
    add to (or create) a `.pyjournal` file with an entry

    The master bare git repo is placed in `path`.  The working clone
    that we interact with is placed there too, unless we specify the
    optional `working-path` argument.
    
    The `git` operations that take place under the hood are:
    
      - Creating a bare repo for others to clone to/from:

        ```
        mkdir path/nickname.git
        cd path/nickname.git
        git init --bare
        ```
     
      - Creating the working directory that we will interact with:

        ```
        cd working-path/
        git clone path/nicknmae
        ```

    The contents of the `.pyjournal` are

    ```
    [nickname]
    master_repo = /path/nickname.git
    working_path = /working-path/
    ```

  - `pyjournal.py connect ssh://remote-machine:/git-path/journal-nickname.git local-path`

    If you already established a journal on another machine (using the
    `init` action, then `connect` is used to create a clone of that
    journal on your local machine (if you are only working on a single
    machine, then you don't need to do this).

    Note that for the remote git repo is specified as the complete path
    (including the `ssh://` prefix) to the `.git` bare repo.  The nickname
    for the journal is taken from the repo name.
    
    Only a working repo is stored locally (created though a `git clone`).
    In this case, your `.pyjournalrc` will look like:
    
    ```
    [nickname]
    master_path = ssh://remote-machine:/git-path/git-repo.git
    working_path = local-path/
    ```  

* Directory structure:

  ```
  journal-nickname/

    entries/
      yyyy-mm-dd/
        yyy-mm-dd-hh-ss.tex
        ...
      yyyy-mm-dd/

    journal.tex
  ```


* Day-to-day use:

  - `pyjournal.py [-n nickname] entry [XXX YYY ZZZ ...]` or
    `pyjournal [-n nickname]`
  
    adds an entry to the journal (optionally named "nickname"). `XXX`,
    `YYY`, and `ZZZ` are optional names of images that will
    automatically be added as figures to the new entry

    Note: you can run `pyjournal.py` without any action, and it will
    default to `entry`, but you don't have the option for images.

  - `pyjournal.py [-n nickname] edit 'yyyy-mm-dd hh.mm.ss'`

    edit the entry corresponding to the date/time string in the journal.
    This adds a comment to the LaTeX indicating the time of the edit
    and pops up an editor window with the entry for revision.  Since the
    new changes are committed to the git repo, the history of changes to
    the entry are preserved in the git history.
    
  - `pyjournal.py [-n nickname] build`

    builds the journal PDF

  - `pyjournal.py [-n nickname] show`

    builds the journal PDF and launches the `evince` viewer in the
    background to display it.

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
  master_repo = XXX.git  ; this is what we push to/pull from
  working_path = YYY     ; local directory we interact with on our machine
  ```
