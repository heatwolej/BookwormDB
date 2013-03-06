About
=====
This is the code repository for BUILDING the databases we're working with on Bookworm. This takes three parameters, and builds a MySQL database out of them that can be queried using the Bookworm API. (And thus allows a Bookworm website to be set up on it. The Bookworm website project is a separate github directory at bmschmidt/Bookworm. That project is for the bookworm web site, which lives in a single directory on the web server.)

It requires a lot of time, memory and disk space to run. Don't try it on your laptop. (For example: the 600,000 article JSTOR version takes about 4 days, maxing out at 8 GB of RAM, and maybe a terabyte or so on disk.)

All work is done in two places: one, a local directory including this folder (presidio); and second, a MySQL database that must be pre-created with permissions in an appropriate place.

In general,we will assume access to the following files. Project-specific code is indicated by dollar signs: if you're working on arxiv, for example, metadata/$project.json would actually indicate a file called metadata/arxiv.json. All paths are relative to presidio.

Files to start with
===================

IN PRESIDIO
-----------

NOTE: Changes will be synced to git, because individual project code may be useful for other ones.

*  metadataParsers/$projectparser.py: This doesn't HAVE to be there, per se, but you might as well put your metadata parser here so people can see how it works and rerun on the data.
*  metadataParsers/$project/$project.json: A JSON file specifying the data types for keys in the JSON objects in ../metadata/jsoncatalog.json. On running, that jsoncatalog will be parsed and the files dealt with according to the rules laid out here: it will also dump out a file to ../$project.json that can be placed in Bookworm to make Bookworm work properly. To see examples, look in one of the existing files; for an explanation of the keys, see the README in the metadata folder.

IN OUTSIDE FILES (changes will not be synced, because they are too large)
----------------
*  ../texts/raw. This is where the actual texts are going to live, all at the same depth. (This can be big--about a million files in a single directory is pretty common.) They will have arbitrary, unique names. You'll have to create. 

*  ../metadata/jsoncatalog.txt: a set of lines with one JSON object per line. Each line looks something like this: {"title":"Ulysses","author":"James Joyce","authorbirth":"1880"}. Tabs and newlines ARE NOT currently permitted to appear in this file.

*  A MySQL database you are authorized to edit, and a my.cnf file that python can load with your permissions.

The general workflow
====================

*  Write a metadata parser and, if needed, a text downloader that fills the /text/raw and /metadata files with appropriately formatted information.

*  Run python Oneclick.py $project $username $password", which builds the database for you, assuming your my.cnf file is working.

*  Go do something else for several days.

*  It's still not finished? You can read the program output to see how far it's gotten. The initial steps, which involve pushing around text files, will writo texts/logs/{whatever process you care about}. They give some sense of how far along you are. In the later stages, which may not take quite as long, the documentation is less clear--you can check the MySQL index files, though. If you want to improve the code, note: The first step calls "ImportNewLibrary.py", which calls master.py a bunch of times and creates the necessary word files and encodes them. This leaves many text files on disk. The actual code is at the end of that file--it can be commented or uncommented to run only particular parts of the code if you've already, say, built up some Ngram counts.

*  OK, it's done.

*  Set up a bookworm installation with the Bookworm code and the API implementation: the file at WebsiteCreate.pl will do this locally on Chaucer, but details will be different for different servers.

*  Ensure that the user you specified in the create call has select permissions on the MySQL database, and that its password is specified in /etc/mysql/my.cnf.

*  Plug the settings in the API_SETTINGS table that has been create at the end of the hash at the beginning of 
(I know this is a pain--at some point we'll have to think of a way to update this automatically. The problem is that we need to explicitly tell the website what database to query, and it can't just pull that from the database. Probably this file should live somewhere in the web directory, or even the options settings, but that would make API calls much more complicated, and that's an extremely bad thing in my mind. (Far worse than a more circuitous set-up).

Adding new files is not currently supported--you just have to rebuild the database. We'll have to write a couple new methods to take care of that.
