.data
array: .space 11    #reserves space for a 10 elem array
char: .space 2
wodd: .word
prompt: .ascii "Please enter 10 numbers, then press ENTER:  \n"
null: .ascii ""
space: .ascii " "
.text
la $s1, array       #set base address of array to s1
loop:           #start of read loop
jal getc        #jump to getc subroutine
lp:         #loop for all digits preceeding the LSB
mul $t3, $t3, $t0   #multiply power by 10
beq $s1, $s0, FIN   #exit if beginning of string is reached
lb $t1, ($s1)  