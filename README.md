# Code Mirror
## Introduction
Code Mirror is a Python-based, simple, light-weight, and real-time* folder syncing solution. Just assign a source and destination folder, hit start, and forget about copying files over after each change. The application uses Merkle Trees as the underlying data structure to keep track of the contents of each folder. The GUI is implemented using Tkinter.

<sub><sup>*depends on the settings you choose.</sup></sub>

## Mechanism
Upon choosing a source and destination folder, the application constructs a Merkle Tree for each of those folders. For information on how Merkle Trees work, check [this](https://www.geeksforgeeks.org/introduction-to-merkle-tree/) out. The root hashes of those trees are compared together. In the event that they do not match, the program starts traversing the trees to find the point of change (a file or a folder) and adds it to a "list of changes". Once the traversal is done, the changes are synced over using Python's shutil package.

## Contributors
Code Mirror was developed as a final project for CS 201 - Data Structures II (Spring 2020) at Habib University. The team members are:
- Niha Karim Momin (Team Lead)
- Bahzad Ahmed Badvi
- Owais Bin Asad
- Rida Zahid Khan

## Features / Known Bugs
The program can (theoretically) recognize, hash, and sync all forms of text files. We have tested it for the following text formats:
- .txt
- .py
- .v
- .rtf
- .html
- .css

Since source files are just text files with fancier extensions, other source files *should* work as well. For example:
- .cpp
- .hpp
- .c
- .h
- .js
- .java

## Future Plan
The original authors of this program do not intend to work on it any further as of right now (check commit logs to see when is "now"). Feel free to fork/clone the repository and make changes to it or build on top of it.