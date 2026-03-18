	.file	"example4.c"
	.option nopic
	.attribute arch, "rv32i2p1"
	.attribute unaligned_access, 0
	.attribute stack_align, 16
	.text
	.globl	__mulsi3
	.align	2
	.globl	factorial
	.type	factorial, @function
factorial:
	addi	sp,sp,-16
	sw	s0,8(sp)
	sw	ra,12(sp)
	mv	s0,a0
	li	a0,1
	ble	s0,a0,.L1
	sw	s1,4(sp)
	li	s1,1
.L2:
	mv	a1,s0
	addi	s0,s0,-1
	call	__mulsi3
	bne	s0,s1,.L2
	lw	s1,4(sp)
.L1:
	lw	ra,12(sp)
	lw	s0,8(sp)
	addi	sp,sp,16
	jr	ra
	.size	factorial, .-factorial
	.section	.text.startup,"ax",@progbits
	.align	2
	.globl	main
	.type	main, @function
main:
	li	a0,120
	ret
	.size	main, .-main
	.ident	"GCC: (13.2.0-11ubuntu1+12) 13.2.0"
