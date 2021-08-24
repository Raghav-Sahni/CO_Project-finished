from sys import stdin

import re

pc = 0
mem = []
halted = False
reg = [0,0,0,0,0,0,0,0]
FLAGS = [0,0,0,0] #V - overflow,L - Less than,G - greater than,E - equal to


def inttobin(x):
    return bin(int(x))[2:].zfill(16)


def decode(inst):
    global reg
    global FLAGS
    global pc
    FLAGS[0] = 0
    FLAGS[1] = 0
    FLAGS[2] = 0
    FLAGS[3] = 0
    opcode = int(inst[:5],2)
    A = [0,1,6,10,11,12]
    B = [2,8,9]
    C = [3,7,13,14]
    D = [4,5]
    E = [15,16,17,18]
    F = [19]
    if opcode in A:
        rd = inst[7:10]
        rs = inst[10:13]
        rt = inst[13:16]
        if (opcode == 0):
            if (reg[int(rs, 2)] + reg[int(rt, 2)] > 65535):
                FLAGS[0] = 1
            else:
                FLAGS[0] = 0
            reg[int(rd, 2)] = reg[int(rs, 2)] + reg[int(rt, 2)]
        elif (opcode == 1):
            if(reg[int(rs, 2)] >= reg[int(rt, 2)]):
                FLAGS[0] = 0
                reg[int(rd, 2)] = reg[int(rs, 2)] - reg[int(rt, 2)]
            else:
                reg[int(rd, 2)] = 0
                FLAGS[0] = 1
        elif (opcode == 6):
            if (reg[int(rs, 2)] * reg[int(rt, 2)] > 65535):
                FLAGS[0] = 1
            else:
                FLAGS[0] = 0
            reg[int(rd, 2)] = reg[int(rs, 2)] * reg[int(rt, 2)]
        elif (opcode == 10):
            reg[int(rd, 2)] = reg[int(rs, 2)] ^ reg[int(rt, 2)]
        elif (opcode == 11):
            reg[int(rd, 2)] = reg[int(rs, 2)] | reg[int(rt, 2)]
        elif (opcode == 12):
            reg[int(rd, 2)] = reg[int(rs, 2)] & reg[int(rt, 2)]
    elif opcode in B:
        rd = inst[5:8]
        imm = inst[8:16]
        if (opcode == 2):
            reg[int(rd, 2)] = int(imm, 2)
        elif (opcode == 8):
            reg[int(rd, 2)] = reg[int(rd,2)]>>int(imm, 2)
        elif (opcode == 9):
            reg[int(rd, 2)] = reg[int(rd,2)]<<int(imm, 2)
    elif opcode in C:
        rd = inst[10:13]
        rs = inst[13:16]
        if (opcode == 3):
            reg[int(rd, 2)] = reg[int(rs, 2)]
        elif (opcode == 7):
            reg[0] = reg[int(rd, 2)]//reg[int(rs, 2)]
            reg[1] = reg[int(rd, 2)] % reg[int(rs, 2)]
        elif (opcode == 13):
            reg[int(rd, 2)] = ~reg[int(rs, 2)]
        elif (opcode ==14):
            if (reg[int(rd, 2)] > reg[int(rs, 2)]):
                FLAGS[2] = 1
            elif (reg[int(rd, 2)] < reg[int(rs, 2)]):
                FLAGS[1] = 1
            else:
                FLAGS[3] = 1
    elif opcode in D:
        rd = inst[5:8]
        var = inst[8:16]
        if (opcode == 5):
            mem[int(var, 2)] = inttobin(reg[int(rd, 2)])
        else:
            reg[int(rd, 2)] = int(mem[int(var, 2)],2)
    elif opcode in E:
        if (opcode == 15):
            pc = int(inst[8:16], 2)
        elif (opcode == 16):
            if (FLAGS[1] == 1):
                pc = int(inst[8:16], 2)
        elif (opcode == 17):
            if (FLAGS[2] == 1):
                pc = int(inst[8:16], 2)
        elif (opcode == 18):
            if (FLAGS[3] == 1):
                pc = int(inst[8:16], 2)
    reg[7] = int(("000000000000" + str(FLAGS[0]) + str(FLAGS[1]) + str(FLAGS[2]) + str(FLAGS[3])),2)
    return pc, reg


def main():
    for i in stdin:
        mem.append(i)
    
    for i in range(len(mem), 256):
        mem.append("0000000000000000")

    while (True):
        global pc
        instruction = mem[pc]
        pc, rf = decode(instruction)
        pcstr = format(pc, "08b")
        rfstr = map(inttobin, rf)
        print(pcstr, end = " ")
        for i in rfstr:
            print(i, end = " ")
        print()
        pc = pc + 1
        if (int(instruction[:5],2) == 19):
            break
    
    for i in mem:
        x = i.strip()
        print(x)

main()

