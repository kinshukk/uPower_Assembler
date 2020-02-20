.data
array: .space 11    #reserves space for a 10 elem array
char: .space 2
wodd: .word
prompt: .ascii "Please enter 10 numbers, then press ENTER:  \n"
null: .ascii ""
space: .ascii " "
.text
loop:           #start of read loop
lp:         #loop for all digits preceeding the LSB
add R3, R3, R0   #multiply power by 10 

lwz R5, 0(R1)

bca R7, R9, loop 
