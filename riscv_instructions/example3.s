	.file	"example3.c"
	.option nopic
	.attribute arch, "rv32i2p1"
	.attribute unaligned_access, 0
	.attribute stack_align, 16
	.text
	.globl	__mulsf3
	.globl	__subsf3
	.align	2
	.globl	FastInvSqrt
	.type	FastInvSqrt, @function
FastInvSqrt:
	lui	a5,%hi(.LC0)
	addi	sp,sp,-16
	lw	a1,%lo(.LC0)(a5)
	sw	s0,8(sp)
	li	s0,1597464576
	srai	a5,a0,1
	addi	s0,s0,-1569
	sw	ra,12(sp)
	sub	s0,s0,a5
	call	__mulsf3
	mv	a1,s0
	call	__mulsf3
	mv	a1,s0
	call	__mulsf3
	lui	a5,%hi(.LC1)
	mv	a1,a0
	lw	a0,%lo(.LC1)(a5)
	call	__subsf3
	mv	a1,s0
	call	__mulsf3
	lw	ra,12(sp)
	lw	s0,8(sp)
	addi	sp,sp,16
	jr	ra
	.size	FastInvSqrt, .-FastInvSqrt
	.section	.text.startup,"ax",@progbits
	.align	2
	.globl	main
	.type	main, @function
main:
	li	a0,563
	ret
	.size	main, .-main
	.section	.srodata.cst4,"aM",@progbits,4
	.align	2
.LC0:
	.word	1056964608
	.align	2
.LC1:
	.word	1069547520
	.ident	"GCC: (13.2.0-11ubuntu1+12) 13.2.0"
