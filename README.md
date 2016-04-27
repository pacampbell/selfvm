# Description

This repository a proof of concept project where a program written in C loads
a custom section appended to itself. This custom section contains instructions
of a made up instruction set called **VMLANG**. The instructions are decoded and
then simulated or translated to x86_64 code depending on options given to the
loader.

You can find a specification of **VMLANG** in the specifications directory. An
assembler for **VMLANG** can be found in the assembler directory. The **VMLANG**
loader and runtime/translator can be found in the loader directory.

# Status

Currently work is being done in the specifications directory. **VMLANG** is
in the process of being described. The assembler will be written after **VMALNG**
has been completely specified. Proof of concept code which can memory map a custom
section of itself is currently located in the loader directory. After the assembler
has been completed, a simulation environment will be developed to fetch, decode,
and execute the **VMLANG** instruction set. After a reference simulator has been
constructed, a binary translator will be developed which can translate **VMLANG**
to x86_64 assembly language basic blocks. The blocks will then be executed and
hopefully have the same behavior as the simulator but at a higher performance.
