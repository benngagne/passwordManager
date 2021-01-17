# Simple Python Password Manager
This python password manager hashes and salts passwords with SHA-512 and stores them in a simple .csv file. Info stored is the site for the password, username, the salt, and hashed password. You can specify length of the hashed password. You can also delete passwords from the .csv file, retrive the password for a given site, and list all sites stored in the file. There is also a salted master password file hashed in SHA-512 as well for "logging in" to the password manager.

## Usage
To use, create folder for python files and .csv and .txt file created by the program. Run with `python3 passwordManager.py`

Files names of passwords .csv file and master password .txt file are stored as variables in passwordManager.py -- change as needed.

## **DISCLAIMER**
This program is by **NO MEANS** deemed as secure. This was built for education purposes only. Use at own risk.
