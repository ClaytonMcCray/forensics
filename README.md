# forensics

This is a collection of file(s) I use in conjuction with data recovery tools such as **GNU ddrescue** and **testdisk**.

## datasort
I personally have this as just **datasort** in my /usr/bin so that it is available anywhere. It's mostly meant
for sorting the output of **photorec** into more useful locations. Basically, it walks through the *base* directory
you provide and tries to guess the filetype based on the extension. Then it puts a directory for each extension into
*target*, and creates a directory *target/unsorted* for files that it can't figure out. Then it walks through the *base*
again; this time copying (never deleteing) files into the appropriate subdirectory of *target*.

### Options for datasort
```
datasort [-option] /path/to/base /path/to/target

Note that flags should be compounded, i.e. -tb instead of -t -b. This has to do with how datasort interprets input.
-e		Target file 'e'xists; do not overwrite the target directory (default is to assume target does not exist)
-b		Base path is abbreviated; it begins in the present working directory. Do not lead with `/` if in pwd. Default looks for a full path
-t		Target path is abbreviated; it beings in the pwd. Do not lead with `/` if in pwd. Same as -b, but for *target*
-h		Display a shorter version of this block
```
**Examples:**

>datasort /home/user/Dropbox /mnt/DataDrive/Backup

This would copy **Dropbox** to **Backup** on a mounted device. In this case, **Backup** should not exist already.

>datasort -e /home/user/Dropbox /mnt/DataDrive/Backup

This is the same as the first example, except that **Backup** can already exist and have content.

*Assume for the next example that `datasort` is in your /usr/bin folder, and you are launching the command from ~/*
>datasort -tb Documents datasorttest/one

This will run **datasort** on */home/user/Documents* and put the output into */home/user/datasorttest/one*, a directory which does not
exist yet.

### Output
**datasort** will print out first a list of all the extensions it scrapes and then each file as it moves it. Additonally,
if it encounters any errors with moving files, it will collect the names of the files and print them at the end of the
process along with an error statement. Typically, in my experience, errors are related to permissions issues. If you get an error,
try running **datasort** as root.

