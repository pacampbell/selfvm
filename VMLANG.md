# VM Instruction Set

This document contains the draft rules for the toy instruction set implemented
by this program.

# Section 1: Core instruction set

Below is a list of the core instructions and their formats. This is the minimum
instruction set that needs to be implemented to satisfy this design.. Section 4
lists an extension to these core instructions by using the assembler to translate
into the multiple core instructions. This allows us to implement a very small RISC
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
| 0b00110 | lh       | lh rd, rs  | Loads an 16-bit half word from the        |
|         |          |            | address stored in rs into the register rd.|
+---------+----------+------------+-------------------------------------------+
| 0b00111 | sh       | sh rs, rd  | Stores an 16-bit half from the register rs|
|         |          |            | into the memory address stored in rd.     |
+---------+----------+------------+-------------------------------------------+
| 0b01000 | not      | not rd, rs | Performs a bitwise not on rd, and stores  |
|         |          |            | the value in rs.                          |
+---------+----------+------------+-------------------------------------------+
| 0b01001 | mul      | mul rd, rs | Performs integer multiplication. Register |
|         |          |            | rd is multiplied by register rs. The      |
|         |          |            | lower 32-bits of the result are stored in |
|         |          |            | v0 and the upper 32-bits are stored in v1.|
+---------+----------+------------+-------------------------------------------+
| 0b01010 | div      | div rd, rs | Performs integer division. Register       |
|         |          |            | rs divides rd. The quotient is            |
|         |          |            | stored in register v0 and the             |
|         |          |            | remainder is stored in register v1.       |
+---------+----------+------------+-------------------------------------------+
| 0b01011 | push     | push rs    | Pushes the value in register rs onto the  |
|         |          |            | stack and then moves the stack pointer    |
|         |          |            | by 4 bytes. The direction moved is        |
|         |          |            | is opposite of the pop instruction.       |
+---------+----------+------------+-------------------------------------------+
| 0b01100 | pop      | pop rd     | Pops a 4 byte value from the stack into   |
|         |          |            | the register rd. The stack pointer is     |
|         |          |            | then moved by 4 bytes. The direction      |
|         |          |            | moved is opposite of the push             |
|         |          |            | instruction.                              |
+---------+----------+------------+-------------------------------------------+
| 0b01101 | popf     | popf rd    | Sets rd to the value of the flags special |
|         |          |            | register.                                 |
+---------+----------+------------+-------------------------------------------+
| 0b01110 | popm     | popm rd    | Sets rd to the value of the modifier      |
|         |          |            | special register.                         |
+---------+----------+------------+-------------------------------------------+
| 0b01111 | pushm    | pushm rs   | Sets the modifier special register to the |
|         |          |            | lower 4 bits of the register stored in    |
|         |          |            | rs.                                       |
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

### Section 1.1.6: Six byte instruction format

opcode = `1111110x`

Currently no described format

# Section 2: Pseudo Instructions

Aside from the core instructions, an assembler for the language can add additional
functionality by translating pseudo instructions into multiple core instructions.
Below we present a list of pseudo instructions which an assembler should translate.

TODO

# Section 3: Registers

The machine has 16 general purpose registers [0,15]. And All registers are 32-bits.
There also exists a single special purpose register to contain various state
and configuration.

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
|   7    |  v1  | Return value                   |
+--------+------+--------------------------------+
|   8    |  g0  | General purpose and argument 0 |
+--------+------+--------------------------------+
|   9    |  g1  | General purpose and argument 1 |
+--------+------+--------------------------------+
|  10    |  g2  | General purpose and argument 2 |
+--------+------+--------------------------------+
|  11    |  g3  | General purpose and argument 3 |
+--------+------+--------------------------------+
|  12    |  g4  | General purpose                |
+--------+------+--------------------------------+
|  13    |  g5  | General Purpose                |
+--------+------+--------------------------------+
|  14    |  g6  | General Purpose                |
+--------+------+--------------------------------+
|  15    |  g7  | General Purpose                |
+--------+------+--------------------------------+
</pre>

## Section 3.1: Special registers

There exists a set of special registers which are used to complement the existing
functionality of instruction set. Their format and use is documented below.

The special purpose register is partitioned into different sections within
a single 32-bit register. The sections can be accessed through special purpose
instructions.

<pre>
+---------+--------+---------------+-------------------------------+
| 16-bits | 4-bits | 4-bits        | 8-bits                        |
+---------+--------+---------------+-------------------------------+
| unused  | mode   | modifiers     | flags                         |
+---------+--------+---+---+---+---+---+---+---+---+---+---+---+---+
| R.....R |  0000  | R | R | R | U | R | R | R | R | Z | C | S | O |
+---------+--------+---+---+---+---+---+---+---+---+---+---+---+---+
</pre>

### Section 3.1.1: Special register section description

Each of the values in each of the special purpose registers are described
below.

#### Section 3.1.1.1 Flags

<pre>
+--------------+---------------+----------------------------------------------+
| abbreviation | name          | Description                                  |
+--------------+---------------+----------------------------------------------+
| Z            | Zero flag     | If the result of the previous operation was  |
|              |               | zero, this flag will be set.                 |
+--------------+---------------+----------------------------------------------+
| C            | Carry flag    | If the previous operation resulted in        |
|              |               | creating a carry bit, this flag will be set. |
+--------------+---------------+----------------------------------------------+
| S            | Sign flag     | If the result of the previous operation was  |
|              |               | negative, this flag will be set.             |
+--------------+---------------+----------------------------------------------+
| O            | Overflow flag | If the previous operation resulted in an     |
|              |               | overflow, this flag will be set.             |
+--------------+---------------+----------------------------------------------+
| R            | Reserved      | All bits marked with R are not in use and    |
|              |               | and reserved by the instruction set to be    |
|              |               | used in the future.                          |
+--------------+---------------+----------------------------------------------+
</pre>

#### Section 3.1.1.2 Modifiers

<pre>
+--------------+---------------+----------------------------------------------+
| abbreviation | name          | Description                                  |
+--------------+---------------+----------------------------------------------+
| U            | Unsigned      | When U is set to one, all operations are     |
|              |               | performed using unsigned arithmetic.         |
|              |               | Otherwise the instructions operate on the    |
|              |               | values as a two's complement number.         |
+--------------+---------------+----------------------------------------------+
| R            | Reserved      | All bits marked with R are not in use and    |
|              |               | and reserved by the instruction set to be    |
|              |               | used in the future.                          |
+--------------+---------------+----------------------------------------------+
</pre>

#### Section 3.1.1.3 Mode

The mode bits are used to configure how the system may interpret the instructions.
Currently they are hard coded to all zeros, but can be modified in the future
to support different types of instruction encodings.

<pre>
+--------+--------------------------------------------------------------------+
| Value  | Description                                                        |
+--------+--------------------------------------------------------------------+
| 0b0000 | Tells the machine to decode the instructions in the format         |
|        | described in this document.                                        |
+--------+--------------------------------------------------------------------+
| 0b0001 |                                                                    |
+--------+                                                                    |
| ...... |               Currently not in use                                 |
+--------+                                                                    |
| 0b1111 |                                                                    |
+--------+--------------------------------------------------------------------+
<pre>

#### Section 3.1.1.4 Unused

<pre>
+--------------+---------------+----------------------------------------------+
| abbreviation | name          | Description                                  |
+--------------+---------------+----------------------------------------------+
| R            | Reserved      | All bits marked with R are not in use and    |
|              |               | and reserved by the instruction set to be    |
|              |               | used in the future.                          |
+--------------+---------------+----------------------------------------------+
</pre>

# Section 4: System call table

When the system call instruction is executed, the value used in the register v0
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
|   0x7   | sbrk      | g0 = number of bytes to | v0 contains the starting    |
|         |           | allocate                | address of the allocated    |
|         |           |                         | memory.                     |
+---------+-----------+-------------------------+-----------------------------+
</pre>

# Section 5: Universal number - unum

TODO

Idea: Use the modifier like for unsigned numbers?

# Section 6: Programming conventions

TODO
