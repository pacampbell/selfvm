# VM Instruction Set

This document contains the rules for the toy instruction set implemented by this
program.

# Instruction format

Our instruction format has:
* 8-bit opcode
* 4-bit register field
* 4-bit register field
* 16-bit immediate field

<pre>
+--------+--------+--------+-----------+
| 8-bits | 4-bits | 4-bits |  16-bits  |
+--------+--------+--------+-----------+
| opcode |   rs   |   rt   | immediate |
+--------+--------+--------+-----------+
</pre>

# Instruction set

<pre>
+--------+----------+--------------------------+
| opcode | mnemonic | Description              |
+--------+----------+--------------------------+
| 0x00   | syscall  | syscall rt               |
+--------+----------+--------------------------+
</pre>

# Syscall table

<pre>
+---------+----------+
| syscall |   name   |
+---------+----------+
|    0    | exit     |
+---------+----------+
</pre>
