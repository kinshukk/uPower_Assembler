.data #global data
X: .word 5
Y: .word 10
SUM: .word 0

.text
#.globl main
main:
    la R1, X
    la R2, Y
    lwz R3, 0(R0)
    lwz R4, 0(R1)

    add R5, R3, R4

    la R6, SUM
    stw R7, 0(R6)

#    .end
