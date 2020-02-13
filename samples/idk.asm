.data
len: .word 10

.main:
la $a0, len
lw $a0, 0($s0)
