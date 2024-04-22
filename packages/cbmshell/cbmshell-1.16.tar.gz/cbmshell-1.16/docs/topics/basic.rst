========================
Working with BASIC Files
========================

Files containing BASIC programs can be modified in various ways.

BASIC files can be edited using any text editor using the ``edit``
command:

.. code-block:: text

    (cbm) edit example.prg

To select the program used as the editor either set the ``editor``
variable:

.. code-block:: text

    (cbm) set editor vim
    editor - was: 'emacs'
    now: 'vim'

or set the EDITOR environment variable before starting ``cbm-shell``.

Separate files can be merged together using the ``merge`` command:

.. code-block:: text

    (cbm) merge partA.prg partB.prg partC.prg

The lines in ``partB.prg`` and ``partC.prg`` are added to those in
``partA.prg`` and the result saved back to ``partA.prg``. Lines
present in later files replace those in earlier files.

The line numbers of a program can be renumbered to make more space
between lines or to merge with another file using the ``renumber``
command:

.. code-block:: text

    (cbm) list example.prg
    400 REM EXAMPLE
    401 A=A+1
    402 PRINTA;
    403 GOTO401
    (cbm) renumber example.prg
    Reading example.prg
    Renumbering starting at 10, increments of 10
    Writing example.prg
    (cbm) list example.prg
    10 REM EXAMPLE
    20 A=A+1
    30 PRINTA;
    40 GOTO20

The first line number used can be specified with the ``--start``
argument, the interval between lines with the ``--increment``
argument.

By default the whole program is renumbered, a subset of lines can be
renumbered, the beginning can be specified with the ``--region-start``
argument and the end with the ``--region-end`` argument. The new line
numbers must not overlap with lines outside the region.
