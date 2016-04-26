# VM Instruction Set

This document contains the rules for the toy instruction set implemented by this
program.

# Section 1: Instruction set properties

The instruction set of this machine is a variable sized instruction set. Every
instruction at a minimum is at least 1-byte. This first byte represents what is
know as the opcode. The value of the opcode will determine the number of following
bytes that should be read to make up the whole instruction.

## Section 1.1: Instruction format

Since each instruction can be encoded using a different number of bytes, and the
encoding tells us how many bytes make up the encoding, we use that property to
define different types of instructions based on encoding length.

### Section 1.1.1: Single byte instruction format

first byte = `0xxxxxxx`

<pre>
+--------+--------+
| 1-bit  | 7-bits |
+--------+--------+
| marker | opcode |
+--------+--------+
</pre>

Below a list of all single-byte instructions can be found.

<pre>
+------------+----------+---------+-------------------------------------------+
| opcode     | mnemonic | Usage   | Description                               |
+------------+----------+---------+-------------------------------------------+
| 0b0000000  | syscall  | syscall | Performs a system call. Check section 3   |
|            |          |         | for more information on system calls.     |
+------------+----------+---------+-------------------------------------------+
| 0b0000001  | nop      | nop     | Performs a no operation; wastes a cycle.  |
+------------+----------+---------+-------------------------------------------+
</pre>

### Section 1.1.2: Two byte instruction format

first byte = `110xxxxx`

<pre>
+--------+--------+--------+--------+
| 3-bits | 5-bits | 4-bits | 4-bits |
+--------+--------+--------+--------+
| marker | opcode | rd     | rs     |
+--------+--------+--------+--------+
</pre>

Below, a list of all two-byte instructions can be found.

<pre>
+---------+----------+------------+-------------------------------------------+
| opcode  | mnemonic | Usage      | Description                               |
+---------+----------+------------+-------------------------------------------+
| 0b00000 | mov      | mov rd, rs |                                           |
+---------+----------+------------+-------------------------------------------+
</pre>

### Section 1.1.3: Three byte instruction format

opcode = `1110xxxx`

<pre>
+--------+--------+--------+--------+--------+--------+
| 4-bits | 4-bits | 4-bits | 4-bits | 4-bits | 4-bits |
+--------+--------+--------+--------+--------+--------+
| marker | opcode | rd     | rs     | rt     |  func  |
+--------+--------+--------+--------+--------+--------+
</pre>

Below a list of all three-byte instructions can be found.

<pre>
+--------+----------+------------+--------------------------------------------+
| opcode | mnemonic | Usage      | Description                                |
+--------+----------+------------+--------------------------------------------+
| 0b0000 |          |            |                                            |
+--------+----------+------------+--------------------------------------------+
</pre>

### Section 1.1.4: Four byte instruction format

opcode = `11110xxx`

<pre>
+--------+--------+--------+--------+-----------+
| 5-bits | 3-bits | 4-bits | 4-bits | 16-bits   |
+--------+--------+--------+--------+-----------+
| marker | opcode | rd     | rs     | immediate |
+--------+--------+--------+--------+-----------+
</pre>


Below a list of all four-byte instructions cna be found.

<pre>
+--------+----------+------------+--------------------------------------------+
| opcode | mnemonic | Usage      | Description                                |
+--------+----------+------------+--------------------------------------------+
| 0b000  | lw       |            |                                            |
+--------+----------+------------+--------------------------------------------+
| 0b000  | sw       |            |                                            |
+--------+----------+------------+--------------------------------------------+
| 0b000  | li       |            |                                            |
+--------+----------+------------+--------------------------------------------+
</pre>


# Section 2: Registers

The machine has 16 registers [0,15]. All registers are 32-bits

<pre>
+--------+------+--------------------------------+
| number | name | description                    |
+--------+------+--------------------------------+
|   0    | zero | Register hard coded to zero    |
+--------+------+--------------------------------+
|   1    |  at  | Assembler temporary            |
+--------+------+--------------------------------+
|   2    |  sp  | Stack Pointer                  |
+--------+------+--------------------------------+
|   3    |  fp  | Frame Pointer                  |
+--------+------+--------------------------------+
|   4    |  pc  | Program Counter                |
+--------+------+--------------------------------+
|   5    |  ra  | Return address                 |
+--------+------+--------------------------------+
|   6    |  v0  | Return value and syscall value |
+--------+------+--------------------------------+
|   7    |  g0  | General purpose and argument 0 |
+--------+------+--------------------------------+
|   8    |  g1  | General purpose and argument 1 |
+--------+------+--------------------------------+
|   9    |  g2  | General purpose and argument 2 |
+--------+------+--------------------------------+
|  10    |  g3  | General purpose and argument 3 |
+--------+------+--------------------------------+
|  11    |  g4  | General purpose                |
+--------+------+--------------------------------+
|  12    |  g5  | General Purpose                |
+--------+------+--------------------------------+
|  13    |  g6  | General Purpose                |
+--------+------+--------------------------------+
|  14    |  g7  | General Purpose                |
+--------+------+--------------------------------+
|  15    |  g8  | General Purpose                |
+--------+------+--------------------------------+
</pre>

# Section 3: System call table

When the system call instruction is executed, the value used in the register $v0
will determine which system call will be used. The VM environment defines the
following small set of system calls.

<pre>
+---------+-----------+-------------------------+-----------------------------+
| syscall |   name    | arguments               |           results           |
+---------+-----------+-------------------------+-----------------------------+
|   0x0   |   exit    | g0 = exit code          |             N/A             |
+---------+-----------+-------------------------+-----------------------------+
|   0x1   | print int | g0 = integer to print   |             N/A             |
+---------+-----------+-------------------------+-----------------------------+
|   0x2   | print chr | g0 = character to print |             N/A             |
+---------+-----------+-------------------------+-----------------------------+
|   0x3   | print str | g0 = null terminated    |             N/A             |
|         |           | string to print         |                             |
+---------+-----------+-------------------------+-----------------------------+
|   0x4   | read int  |                         | v0 contains integer read    |
+---------+-----------+-------------------------+-----------------------------+
|   0x5   | read chr  |                         | v0 contains character read  |
+---------+-----------+-------------------------+-----------------------------+
|   0x6   | read str  | g0 = address of dest    | The dest buffer will        |
|         |           | g1 = max size of dest   | contain the newline         |
+---------+-----------+-------------------------+-----------------------------+
</pre>
