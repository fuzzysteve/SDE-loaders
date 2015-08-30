# SDE-loaders
Python loaders for yaml, into MS SQL


With more moving into yaml, I'm looking to build up a basic platform of tools to load the yaml files into appropriate database tables. As I'll be wanting to work on this from windows boxes, python seemed appropriate.

With the use of SQL Alchemy, porting to other relational databases should be relatively simple too.


To achieve acceptable performance, make sure to get a version of PyYAML compiled against libyaml. On windows, this is a touch harder. I got my copy from http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyyaml

If you don't want to use someone's prebuilt copy, you'll need to either build your own, or go through each of the files and change CSafeLoader to SafeLoader



Creating your Database connection for the MS SQL server:

* Open the appropriate ODBC administrator control panel. 32 or 64 bit, depending on your python install
* Add
* SQL Server Native Client.
* Finish
* Give it the name ebs
* Select the sql server you want to use
* For now, this is designed to use Integrated Windows Auth. (so make sure the user you're using has rights on the database). So hit next
* Change the default database to where you have the export
* Next
* Finish

Make sure to fill in the config file appropriately. And stick the resource files requires into a resources directory.
