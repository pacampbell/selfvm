# VM Instruction Set

This document contains the rules for the toy instruction set implemented by this
program.

# Instruction set properties

The instruction set is a variable sized instruction set. The bytes are encoded
in a way similar to [UTF-8](https://en.wikipedia.org/wiki/UTF-8). We use the
encoding which is similar to the original UTF-8 proposal which allows us to
specify instructions that have up to 33 bits of usable space, but take up [1,6]
bytes of total space in the instruction cache. The idea is that frequently used
instruction types will take advantage of the lesser byte representation, and
larger byte representations will will be less frequently used instructions. This
will also make our program appear to look like a bunch of UTF-8 encoded text which
is fun!

<pre>
Byte format table (Borrowed from the Wikipedia article about UTF-8)
+----------+----------+----------+----------+----------+----------+----------+--------+
| bytes in |  byte1   |  byte2   |  byte3   |  byte4   |  byte5   |  byte6   |  Bits  |
| sequence |          |          |          |          |          |          | Usable |
+----------+----------+----------+----------+----------+----------+----------+--------+
|    1     | 0xxxxxxx |          |          |          |          |          |   7    |
+----------+----------+----------+----------+----------+----------+----------+--------+
|    2     | 110xxxxx | 10xxxxxx |          |          |          |          |  11    |
+----------+----------+----------+----------+----------+----------+----------+--------+
|    3     | 1110xxxx | 10xxxxxx | 10xxxxxx |          |          |          |  16    |
+----------+----------+----------+----------+----------+----------+----------+--------+
|    4     | 11110xxx | 10xxxxxx | 10xxxxxx | 10xxxxxx |          |          |  21    |
+----------+----------+----------+----------+----------+----------+----------+--------+
|    5     | 111110xx | 10xxxxxx | 10xxxxxx | 10xxxxxx | 10xxxxxx |          |  26    |
+----------+----------+----------+----------+----------+----------+----------+--------+
|    6     | 1111110x | 10xxxxxx | 10xxxxxx | 10xxxxxx | 10xxxxxx | 10xxxxxx |  33    |
+----------+----------+----------+----------+----------+----------+----------+--------+
</pre>

# Instruction format

* Instructions have varying formats depending on the amount of bytes it is
encoded as.
* Generally instructions fit into the following types
  1. Instruction with no arguments
  2. An instruction that uses 2 registers
  3. An instruction that uses 1 register and an immediate field
  4. An instruction which contains a jump address

## Instruction encoded in 1-byte : 7 usable bits
<pre>
+--------+
| 7-bits |
+--------+
| opcode |
+--------+
</pre>

Instructions such as **syscall** and **nop** would take only one byte.

## Instruction encoded in 2-bytes : 11 usable bits

<pre>
+--------+----------+
| 6-bits |  5-bits  |
+--------+----------+
| opcode | register |
+--------+----------+
</pre>

Instructions like **jr** only take 1 argument.

## Instruction encoded in 4-bytes : 21 usable bits

These are our main instructions which most of our program will be comprised of.
We use not only the number of bytes that make up the encoding but also depending
on the value of the opcode field, we can create different sub instruction types.

### opcode == 0000

<pre>
+--------+--------+--------+--------+------------+
| 4-bits | 4-bits | 4-bits | 5-bits |   4-bits   |
+--------+--------+--------+--------+------------+
| opcode |   rd   |   rs   |  shamt |  function  |
+--------+--------+--------+--------+------------+
</pre>


### opcode != 0000

<pre>
+--------+--------+--------+---------------------+
| 4-bits | 4-bits | 1-bit  | 12-bits             |
+--------+--------+------------------------------+
| opcode |   rs   | flag   | immediate           |
+--------+--------+------------------------------+
</pre>

> If the flag value == 0 then we treat the immediate field as a 12-bit value
> If the flag value == 1 then we use the [arm immediate encoding scheme](https://alisdair.mcdiarmid.org/arm-immediate-value-encoding/)

## Instruction encoded in 6-Bytes : 33 usable bits

<pre>
+---------+---------------+
| 1-bit   |    32-bits    |
+---------+---------------+
| opcode  |  jump address |
+---------+---------------+
</pre>

> If the opcode == 0 then this is an absolute jump address with no side effects
> If the opcode == 1 then this is an absolute jump which sets the return address
> register to the starting address of the next instruction

# Registers

The machine has 16 registers [0,15]. All registers are 32-bits

<pre>
+--------+------+--------------------------------+
| number | name | description                    |
+--------+------+--------------------------------+
|   0    | zero | Register hard coded to zero    |
+--------+------+--------------------------------+
|   1    | at   | Assembler temporary            |
+--------+------+--------------------------------+
|   2    | sp   | Stack Pointer                  |
+--------+------+--------------------------------+
|   3    | fp   | Frame Pointer                  |
+--------+------+--------------------------------+
|   4    | pc   | Program Counter                |
+--------+------+--------------------------------+
|   5    | ra   | Return address                 |
+--------+------+--------------------------------+
|   6    | v0   | Return value and syscall value |
+--------+------+--------------------------------+
|   7    | a0   | Argument 0                     |
+--------+------+--------------------------------+
|   8    | a1   | Argument 1                     |
+--------+------+--------------------------------+
|   9    | a2   | Argument 2                     |
+--------+------+--------------------------------+
|  10    | a3   | Argument 3                     |
+--------+------+--------------------------------+
|  11    |  a   | General purpose                |
+--------+------+--------------------------------+
|  12    |  b   | General Purpose                |
+--------+------+--------------------------------+
|  13    |  c   | General Purpose                |
+--------+------+--------------------------------+
|  14    |  d   | General Purpose                |
+--------+------+--------------------------------+
|  15    |  e   | General Purpose                |
+--------+------+--------------------------------+
</pre>

# Instruction set

Since each instruction can be encoded using a different number of bytes, and the
encoding tells us how many bytes make up the encoding, we use that property to
define different types of instructions based on encoding length.

## Instructions encoded using 1 byte

<pre>
+--------+----------+--------------------------+
| opcode | mnemonic | Description              |
+--------+----------+--------------------------+
|  0x0   | syscall  | syscall                  |
+--------+----------+--------------------------+
|  0x1   | nop      | no operation             |
+--------+----------+--------------------------+
</pre>

## Instruction encoded in 2-bytes

+--------+----------+--------------------------+
| opcode | mnemonic | Description              |
+--------+----------+--------------------------+
|  0x0   |   jr     | jumps using a register   |
+--------+----------+--------------------------+

## Instructions encoded using 4 bytes

### opcode == 0000

### opcode != 0000

## Instructions encoded using 5 bytes

+--------+----------+--------------------------+
| opcode | mnemonic | Description              |
+--------+----------+--------------------------+
|  0x0   | j        | jump                     |
+--------+----------+--------------------------+
|  0x1   | jal      | jump and link with ra    |
+--------+----------+--------------------------+

# System call table

<pre>
+---------+-----------+-------------------------+-----------------------------+
| syscall |   name    | arguments               |            results          |
+---------+-----------+-------------------------+-----------------------------+
|   0x0   |   exit    | a0 = exit code          |              N/A            |
+---------+-----------+-------------------------+-----------------------------+
|   0x1   | print int | a0 = integer to print   |              N/A            |
+---------+-----------+-------------------------+-----------------------------+
|   0x2   | print chr | a0 = character to print |              N/A            |
+---------+-----------+-------------------------+-----------------------------+
|   0x3   | print str | $a0 = null terminated   |              N/A            |
|         |           | string to print         |                             |
+---------+-----------+-------------------------+-----------------------------+
|   0x4   | read int  |                         | v0 contains integer read    |
+---------+-----------+-------------------------+-----------------------------+
|   0x5   | read chr  |                         | v0 contains character read  |
+---------+-----------+-------------------------+-----------------------------+
|   0x6   | read str  | a0 = address of dest    | The dest buffer will        |
|         |           | a1 = max size of dest   | contain the newline         |
+---------+-----------+-------------------------+-----------------------------+
</pre>
