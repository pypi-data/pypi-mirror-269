=====================
Converting Data Files
=====================

Data files are typically stored as lines of PETSCII text ending in a
Carriage Return. The contents of a file can be converted to Unicode
with native line endings using the ``text`` command:

.. code-block:: text

    (cbm) text 0:WORDS
     224 
    AB
    AC
    ACK
    ACT
    ADE
    AH
    AIM
    AIN

To convert a text file from Unicode to a data files use the ``untext``
command:

.. code-block:: text

    (cbm) untext words.txt 0:WORDS
    Writing words.txt to ImagePath(0:b'WORDS')

With disk images the destination can be a relative file:

.. code-block:: text

    (cbm) untext --type REL --record-length 36 words.txt 0:DBASE
    Writing words.txt to ImagePath(0:b'DBASE')

In this case the record length must be supplied and should be at least
as long as the longest line in the source file.
