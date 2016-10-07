# Runtime

This document attempts to detail base runtime system used by the simulator/bt
engine. 

# Section 1: System call table

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
