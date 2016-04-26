# VM Instruction Set

This document contains the draft rules for the toy instruction set implemented
by this program.

# Section 1: Core instruction set

Below is a list of the core instruction set that a machine implementing this
instruction set would need at a minimum. Section 3 lists an
extension to these core instructions by using the assembler to translate into
the multiple core instructions. This allows us to implement a very small and RISC
like instruction set but with a variable sized instruction format similar to CISC
machines.

## Section 1.1: Instruction format

Each instruction is made of up at least 1 byte. This first byte is known as the
opcode byte. The opcode byte will contain marker bits as shown below. The marker
bits are used as a way to determine the number of bytes used to encode the instruction.
Using this current bit marker technique a single instruction could be encoded in a
maximum of 6 bytes.

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
| 0b00000 | mov      | mov rd, rs | Moves the value stores in rs into rd.     |
+---------+----------+------------+-------------------------------------------+
| 0b00001 | jr       | jr rd      | Jumps to the 32-bit address held in rd.   |
+---------+----------+------------+-------------------------------------------+
| 0b00010 | lw       | lw rd, rs  | Loads a 32-bit word from the address      |
|         |          |            | stored in rs into the register rd.        |
+---------+----------+------------+-------------------------------------------+
| 0b00011 | sw       | sw rs, rd  | Stores a 32-bit word from the register rs |
|         |          |            | into the memory address stored in rd.     |
+---------+----------+------------+-------------------------------------------+
| 0b00100 | lb       | lb rd, rs  | Loads an 8-bit byte from the address      |
|         |          |            | stored in rs into the register rd.        |
+---------+----------+------------+-------------------------------------------+
| 0b00101 | sb       | sb rs, rd  | Stores an 8-bit byte from the register rs |
|         |          |            | into the memory address stored in rd.     |
+---------+----------+------------+-------------------------------------------+
| 0b00100 | lh       | lb rd, rs  | Loads an 16-bit half word from the        |
|         |          |            | address stored in rs into the register rd.|
+---------+----------+------------+-------------------------------------------+
| 0b00101 | sh       | sb rs, rd  | Stores an 16-bit half from the register rs|
|         |          |            | into the memory address stored in rd.     |
+---------+----------+------------+-------------------------------------------+
| 0b00110 | not      | not rd, rs | Performs a bitwise not on rd, and stores  |
|         |          |            | the value in rs                           |
+---------+----------+------------+-------------------------------------------+
| 0b00111 | mul      | mul rd, rs |                                           |
+---------+----------+------------+-------------------------------------------+
| 0b01000 | div      | div rd, rs | Performs integer division. Register       |
|         |          |            | rs divides rd. The quotient is            |
|         |          |            | stored in register v0 and the             |
|         |          |            | remainder is stored in register v1.       |
+---------+----------+------------+-------------------------------------------+


</pre>

### Section 1.1.3: Three byte instruction format

opcode = `1110xxxx`

<pre>
+--------+--------+--------+--------+--------+--------+
| 4-bits | 4-bits | 4-bits | 4-bits | 4-bits | 4-bits |
+--------+--------+--------+--------+--------+--------+
| marker | opcode | rd     | rs     | rt     | shamt  |
+--------+--------+--------+--------+--------+--------+
</pre>

Below a list of all three-byte instructions can be found.

<pre>
+--------+----------+-------------------+-------------------------------------+
| opcode | mnemonic | Usage             | Description                         |
+--------+----------+-------------------+-------------------------------------+
| 0b0000 | and      | and rd, rs, rt    |                                     |
+--------+----------+-------------------+-------------------------------------+
| 0b0001 | or       | or rd, rs, rt     |                                     |
+--------+----------+-------------------+-------------------------------------+
| 0b0010 | xor      | xor rd, rs, rt    |                                     |
+--------+----------+-------------------+-------------------------------------+
| 0b0011 |          |                   |                                     |
+--------+----------+-------------------+-------------------------------------+
| 0b0100 | sll      | sll rd, rs, shamt |                                     |
+--------+----------+-------------------+-------------------------------------+
| 0b0101 | srl      | srl rd, rs, shamt |                                     |
+--------+----------+-------------------+-------------------------------------+
| 0b0110 | sra      | sra rd, rs, shamt |                                     |
+--------+----------+-------------------+-------------------------------------+
| 0b0111 | sllv     | srav rd, rs, rt   |                                     |
+--------+----------+-------------------+-------------------------------------+
| 0b1000 | srlv     | srlv rd, rs, rt   |                                     |
+--------+----------+-------------------+-------------------------------------+
| 0b1001 | srav     | srav rd, rs, rt   |                                     |
+--------+----------+-------------------+-------------------------------------+
| 0b1010 | add      | add rd, rs, rt    |                                     |
+--------+----------+-------------------+-------------------------------------+
| 0b1011 | sub      | sub rd, rs, rt    |                                     |
+--------+----------+-------------------+-------------------------------------+
| 0b1100 |          |                   |                                     |
+--------+----------+-------------------+-------------------------------------+
| 0b1101 |          |                   |                                     |
+--------+----------+-------------------+-------------------------------------+
| 0b1110 |          |                   |                                     |
+--------+----------+-------------------+-------------------------------------+
| 0b1111 |          |                   |                                     |
+--------+----------+-------------------+-------------------------------------+

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


Below a list of all four-byte instructions can be found.

<pre>
+--------+----------+-------------------+-------------------------------------+
| opcode | mnemonic | Usage             | Description                         |
+--------+----------+-------------------+-------------------------------------+
| 0b000  | li       | li rd, immed      | Stores immediate into the lower     |
|        |          |                   | 16-bits of of rd.                   |
+--------+----------+-------------------+-------------------------------------+
| 0b001  | lui      | lui rd, immed     | Stores immediate into the upper     |
|        |          |                   | 16-bits of of rd.                   |
+--------+----------+-------------------+-------------------------------------+
| 0b010  | beq      | beq rd, rs, immed | If the values in the register rs    |
|        |          |                   | and rd are equivalent, jump by      |
|        |          |                   | +/- immed bytes from the current pc |
+--------+----------+-------------------+-------------------------------------+
</pre>


### Section 1.1.5: Five byte instruction format

opcode = `111110xx`

Currently no described format

### Section 1.1.5: Six byte instruction format

opcode = `1111110x`

Currently no described format

# Section 2: Pseudo Instructions

Aside from the core instructions, an assembler for the language can add additional
functionality by translating pseudo instructions into multiple core instructions.
Below we present a list of pseudo instructions which an assembler should translate.

TODO

# Section 3: Registers

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
|   6    |  v1  | Return value                   |
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
</pre>

# Section 4: System call table

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
