# Self hosted program

Sample program which reads instructions from within and executes them.

# Usage

This program itself is just a host to execute an actual program. To append the
program use the objcopy command to append the data to the binary.

<pre>
objcopy --add-section  sname=sample.data selfhosted selfhostedpadded
</pre>

# Dependencies

# Setup
