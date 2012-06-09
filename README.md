DeDuper
=======

Runs through a set of paths looking for duplicate files, allowing you to perform operations
on the duplicates.

DeDuper will try to be smart in its detection of duplicates. Here are the things we do to
try to check:

* Are the files identical (duh!)
* Do we understand the type of file?
 * If it's a media file, check the header/tag information

DeDuper differentiates files it *knows* are duplicates (exact bits) from files it
*suspects* are duplicates (matching header information).

DeDuper lets you decide how to handle the duplicates.

* In its most basic form, DeDuper generates a report of known and suspected duplicates. 
* You can tell DeDuper the "master" location for various files and have it delete
  known duplicates and either delete or report suspected duplicates.

Dependencies
------------

* DeDuper is written using Python 2.7.
* Mutagen (http://code.google.com/p/mutagen/) for audio file tags.