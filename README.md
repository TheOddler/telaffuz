# Telafuzz (Turkish for pronunciation)

This program takes a list of words that are in file "words.txt" and looks up their pronunciations on a Dictionary website.
The words listed here are over 70,000 words from a Turkish spelling dictionary.
The website is an official Turkish dictionary website.

There is no database of Turkish words with their pronunciations.
This compiles such a database.

The output will be a file with per line a word followed by the pronunciations separated by a tab.
Words without pronunciation information will get "0" printed (this was requested by the user for easy handling by her).
If a word is not found "error" will be printed.
If too many network errors happen "failed" will be printed.

# How to run

python3 telaffuz.py

# Non-standard requirements

pip3 tqdm
