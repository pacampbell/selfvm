.text
main:
  # Do some basic arithmetic
  li $g0, 1
  li $g1, 2
  add $g2, $g0, $g1
  # Print out the value
  li $v0, 1
  mov $g0, $g2 # $g0 = $g2
  syscall
exit:
  # Exit cleanly
  li $v0, 0
  li $g0, 0
  syscall
