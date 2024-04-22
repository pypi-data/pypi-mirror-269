======================
Listing BASIC Programs
======================

BASIC programs are stored in a binary format, to view the contents of
a file use the ``list`` command:

.. code-block:: text

    (cbm) list myprogram.prg
    5 INPUT"UPPER OR LOWER";C$:SA=0:IFC$="L"THENSA=7
    10 INPUT"FILENAME";F$
    11 OPEN4,4,SA
    15 OPEN2,8,2,F$+",S,R"
    20 GET#2,A$:IFST<>0THENPRINT#4:CLOSE4:CLOSE2:END
    21 IFA$="π"THENA$=","
    30 PRINT#4,A$;:GOTO20

To display just part of a program use the ``--start`` and ``--end``
arguments:

.. code-block:: text

    (cbm) list --start 9 --end 15 myprogram.prg
    10 INPUT"FILENAME";F$
    11 OPEN4,4,SA
    15 OPEN2,8,2,F$+",S,R"

To convert a text file containing BASIC lines use the ``unlist``
command:

.. code-block:: text

    (cbm) unlist myprogram.txt 0:MYPROGRAM
    Writing myprogram.txt to ImagePath(0:b'MYPROGRAM')

Unicode characters are translated to PETSCII (see :ref:`Character
Encoding`). Non-standard graphics characters can represented as an
escaped hexadecimal sequence:

.. code-block:: text

    ~a8

is character with shading at the bottom (PETSCII 168).

By default files are created in tape images as relocatable program
files, this can be changed by specifying the ``--type`` argument:

.. code-block:: text

    (cbm) unlist --type PRG myprogram.txt 0:MYPROGRAM
    Writing myprogram.txt to ImagePath(0:b'MYPROGRAM')

By default the address at which the program will load and run is $1201
(4609). Most BASIC programs are relocatable, if an alternative address
is desired it can be specified using the ``--start`` argument:

.. code-block:: text

    (cbm) unlist --start 0x0401 myprogram.txt 0:MYPROGRAM
