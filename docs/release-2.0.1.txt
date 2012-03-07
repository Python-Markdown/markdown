Python-Markdown 2.0.1 Release Notes
===================================

Python-Markdown 2.0.1 is a bug-fix release. No new features have been added.
Most notably, various issues with the command line script have been fixed.
There have also been a few fixes for minor parsing bugs in some edge cases.
For a full list of changes, see the git log.

Backwards-incompatible Changes
------------------------------

Due to various complications in how Python handles command line scripts in 
differance systems and with differant installation tools, we were forced to 
rename the commandline script to ``markdown`` (no ".py"). A matching batch
script will get installed on Windows. Any shell scripts which call 
``markdown.py`` will need to be altered to call ``markdown`` instead.
