.data #global data
X: .word 5
Y: .word 10
SUM: .word 0

.text
#.globl main
main:
    la R0, X
    la R1, Y
    lw R2, 0(R0)
    lw R3, 0(R1)

    add R5, R2, R3

    la R6, SUM
    sw R7, 0(R6)

#    .end
