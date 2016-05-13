# Assembler Specification

This document describes the assembler for VMLANG. The assembler is a basic two
pass assembler. This document also describes the assembler directives and
assembler macro formats. Assembler macros can also be used to define constant
values within the assembler which get evaluated on the first pass. The assembler
file is first passed through a preprocessor stage before being handed to the
assembler.

# Steps

1. Assembly source file **.s**
2. preprocessor
3. preprocessed intermediate assembly file **.s**
4. Assemble **.s** file
5. Produce **.o** file

# Assembler Directives

All assembler directives start with a period **.** followed by a keyword. The
following list of supported directives and their purpose is described below.

<pre>
+-----------+-------------------+---------------------------------------------+
| directive | usage             | description                                 |
+-----------+-------------------+---------------------------------------------+
| .align    | .align n          | Align the next assignment on a 2^n          |
|           |                   | boundary.                                   |
+-----------+-------------------+---------------------------------------------+
| .ascii    | .ascii str        | Store a non-null terminated string in       |
|           |                   | the .data section.                          |  
+-----------+-------------------+---------------------------------------------+
| .asciiz   | .asciiz str       | Store a null terminated string in the .data |
|           |                   | section.                                    |
+-----------+-------------------+---------------------------------------------+
| .byte     | .byte b1, ..., bn | Store n values in successive bytes of       |
|           |                   | of memory.                                  |
+-----------+-------------------+---------------------------------------------+
| .half     | .half h1, ..., hn | Store n values in successive 2-byte values  |
|           |                   | of memory.                                  |
+-----------+-------------------+---------------------------------------------+
| .data     | .data &lt;addr&gt;      | The following items should be stored        |
|           |                   | in the data segment. If the optional arg    |
|           |                   | addr is supplied, start storing them at     |
|           |                   | this address in memory instead.             |
+-----------+-------------------+---------------------------------------------+
| .globl    | .globl symbol     | Declare a symbol which can be referenced    |
|           |                   | in other files.                             |
+-----------+-------------------+---------------------------------------------+
| .space    | .space n          | Allocate n bytes of space in the current    |
|           |                   | data segment.                               |
+-----------+-------------------+---------------------------------------------+
| .text     | .text &lt;addr&gt;      | The following items should be stored        |
|           |                   | in the text segment. If the optional arg    |
|           |                   | addr is supplied, start storing them at     |
|           |                   | this address in memory instead.             |
+-----------+-------------------+---------------------------------------------+
| .unum     | .unum u1, ..., un | Store n unum values in successive memory    |
|           |                   | locations.                                  |
+-----------+-------------------+---------------------------------------------+
| .word     | .word w1, ..., wn | Store n values in successive 4-byte values  |
|           |                   | of memory.                                  |
+-----------+-------------------+---------------------------------------------+
</pre>

# Assembler Macros

Like assembler directives, assembler macros start with a **.** followed by a
keyword.

<pre>
+------------+--------------------+-------------------------------------------+
| macro      | usage              | description                               |
+------------+--------------------+-------------------------------------------+
| .define    | .define NAME VALUE | defines a named constant value which will |
|            |                    | be replaced during the first pass of the  |
|            |                    | assembly process.                         |    
+------------+--------------------+-------------------------------------------+
| .include   | .include path      | performs a substitution with the contents |
|            |                    | located at the path.                      |
+------------+--------------------+-------------------------------------------+
| .macro     |                    |                                           |
+------------+--------------------+-------------------------------------------+
| .end_macro |                    |                                           |
+------------+--------------------+-------------------------------------------+
</pre>
