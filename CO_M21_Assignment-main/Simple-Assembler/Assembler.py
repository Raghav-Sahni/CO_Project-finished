from sys import stdin

import re

import sys

flag = 0
ctr = 0
variables = []
labels = [[]]

def asmtoint(asm):
    global ctr
    global labels
    ctr = ctr + 1 
    asm_split = re.split("\s+",asm)
    args = []
    for i in range (len(asm_split)):
        if (asm_split[i] != ""):
            args.append(asm_split[i])
    #print args
    opcode = 0 #stores integer value of opcode
    func = 0 #stores function type A-0, B-1...
    rd = 0
    rs = 0
    rt = 0
    imm = 0
    V = 0
    L = 0
    G = 0
    E = 0
    if (args[0] == "add"):
        if (len(args) != 4):
            V = 1
            return 0,0,0,0,0,0
        opcode = 0
        func = 0
        rd = int(args[1][1:])
        rs = int(args[2][1:])
        rt = int(args[3][1:])
    elif (args[0] == "sub"):
        if (len(args) != 4):
            V = 1
            return 0,0,0,0,0,0
        opcode = 1
        func = 0
        rd = int(args[1][1:])
        rs = int(args[2][1:])
        rt = int(args[3][1:])
        if (rs < rt):
            V = 1
    elif (args[0] == "mov"):
        if (len(args) != 3):
            return 0,0,0,0,0,0
        func = 1
        rt = 0
        rd = int(args[1][1:])
        if (args[2]=="FLAGS"):
            opcode = 3
            func = 2
            rs = 7
            return opcode, rs, rt, rd, func, imm
        if (args[2][0] == "$"):
            opcode = 2
            imm = int(args[2][1:])
        else:
            opcode = 3
            func = 2
            rs = int(args[2][1:])  
    elif (args[0] == "mul"):
        if (len(args) != 4):
            V = 1
            return 0,0,0,0,0,0
        opcode = 6
        func = 0
        rd = int(args[1][1:])
        rs = int(args[2][1:])
        rt = int(args[3][1:])
    elif (args[0] == "div"):
        if (len(args) != 4):
            return 0,0,0,0,0,0
        opcode = 7
        func = 2
        rd = int(args[1][1:])
        rs = int(args[2][1:])
        rt = int(args[3][1:])
    elif (args[0] == "rs"):
        if (len(args) != 3):
            return 0,0,0,0,0,0
        opcode = 8
        func = 1
        rd = int(args[1][1:])
        imm = int(args[2][1:])
        rt = 0
        rs = 0
    elif (args[0] == "ls"):
        if (len(args) != 3):
            return 0,0,0,0,0,0
        opcode = 9
        func = 1
        rd = int(args[1][1:])
        imm = int(args[2][1:])
        rt = 0
        rs = 0
    elif (args[0] == "xor"):
        if (len(args) != 4):
            return 0,0,0,0,0,0
        opcode = 10
        func = 0
        rd = int(args[1][1:])
        rs = int(args[2][1:])
        rt = int(args[3][1:])
    elif (args[0] == "or"):
        if (len(args) != 4):
            return 0,0,0,0,0,0
        opcode = 11
        func = 0
        rd = int(args[1][1:])
        rs = int(args[2][1:])
        rt = int(args[3][1:])
    elif (args[0] == "and"):
        if (len(args) != 4):
            return 0,0,0,0,0,0
        opcode = 12
        func = 0
        rd = int(args[1][1:])
        rs = int(args[2][1:])
        rt = int(args[3][1:])
    elif (args[0] == "not"):
        if (len(args) != 3):
            return 0,0,0,0,0,0
        opcode = 13
        func = 2
        rd = int(args[1][1:])
        rs = int(args[2][1:])
        rt = 0
    elif (args[0] == "cmp"):
        if (len(args) != 3):
            return 0,0,0,0,0,0
        opcode = 14
        func = 2
        rs = 0
        rd = int(args[1][1:])
        rs= int(args[2][1:])
    elif (args[0] == "jmp"):
        func = 4
        if (len(args) != 2):
            return 0,0,0,0,0,0
        opcode = 15
        rt = 0
        if (len(args) == 2):
            imm = 0
            for i in range(len(labels)):
                if i == 0:
                    continue
                if(labels[i][0] in args[1]):
                    imm = labels[i][1]
            rs = 0
    elif (args[0] == "jlt"):
        func = 4
        if (len(args) != 2):
            return 0,0,0,0,0,0
        opcode = 16
        rt = 0
        if (len(args) == 2):
            imm = 0
            for i in range(len(labels)):
                if i == 0:
                    continue
                if(labels[i][0] in args[1]):
                    imm = labels[i][1]
            rs = 0
    elif (args[0] == "jgt"):
        func = 4
        if (len(args) != 2):
            return 0,0,0,0,0,0
        opcode = 17
        rt = 0
        if (len(args) == 2):
            imm = 0
            for i in range(len(labels)):
                if i == 0:
                    continue
                if(labels[i][0] in args[1]):
                    imm = labels[i][1]
            rs = 0
    elif (args[0] == "je"):
        func = 4
        if (len(args) != 2):
            return 0,0,0,0,0,0
        opcode = 18
        rt = 0
        if (len(args) == 2):
            imm = 0
            for i in range(len(labels)):
                if i == 0:
                    continue
                if(labels[i][0] in args[1]):
                    imm = labels[i][1]
            rs = 0
    elif (args[0] == "ld"):
        func = 3
        if (len(args) != 3):
            return 0,0,0,0,0,0
        opcode = 4
        rt = int(args[1][1:])
        if (len(args) == 3):
            imm = -1
            rs = 0
            rd = 0
    elif (args[0] == "st"):
        func = 3
        if (len(args) != 3):
            return 0,0,0,0,0,0
        opcode = 5
        rt = int(args[1][1:])
        if (len(args) == 3):
            imm = -1
            rs = 0
            rd = 0
    elif (args[0] == "hlt"):
        func = 6
        opcode = 19
    else:
        return 0,0,0,0,0,0
    return opcode, rs, rt, rd, func, imm

#function to convert instruction into binary
def inttobin(opcode, rs, rt, rd, func, imm):
    global flag
    if (opcode ==0 )and(rs==0)and(rd == 0)and(func ==0)and(imm == 0):
        flag = 1
        return
    opstr = format(opcode, "05b")
    if (func == 0):
        rsstr = format(rs, '03b')
        rtstr = format(rt, '03b')
        rdstr = format(rd, '03b')
        instruction = opstr + "00" + rdstr + rsstr + rtstr
    elif (func == 1):
        if (imm < 0):
            imm2s = ((-imm) ^ 255) + 1
            immstr = format(imm2s, '08b')
        else :
            immstr = format(imm, '08b')
        rdstr = format(rd, "03b")
        instruction = opstr + rdstr + immstr
    elif (func == 2):
        rdstr = format(rd, "03b")
        rsstr = format(rs, "03b")
        instruction = opstr + "00000" + rdstr + rsstr
    elif (func == 3):
        mem = ctr
        rtstr = format(rt, "03b")
        instruction = opstr + rtstr 
    elif (func == 4):
        mem = rs + imm
        memstr = format(mem, "08b")
        instruction = opstr + "000" + memstr
    elif (func == 6):
        instruction = opstr + "00000000000"
    return instruction

def decode(asm):
    opcode, rs, rt, rd, func, imm = asmtoint(asm)
    instruction = inttobin(opcode, rs, rt, rd, func, imm)
    return instruction

# work on the part below now i.e file reading and output
 
def compileASM():
    global flag
    global variables
    global labels
    op = []
    ip = []
    c=0
    for i in stdin:
        ip.append(i)
        if ("var" in i):
            continue
        if (":" in i):
            spli = re.split(":", i)
            spli[0] = spli[0].strip()
            spli[1] = spli[1].strip()
            labels.append([spli[0], c])
        c = c+1
    for line in ip:
        if ":" in line:
            spli = re.split(":", line)
            spli[1] = spli[1].strip()
            line = spli[1]
            a_split = re.split("\s+",spli[1])
        else:
            a_split = re.split("\s+",line)
        args = []
        for i in range (len(a_split)):
            if (a_split[i] != ""):
                args.append(a_split[i])
        if (args[0] == "var"):
            variables.append([args[1]])
            continue
        a = decode(line)
        if line == '': # If empty string is read then stop the loop
            break
        if flag == 1:
            y = 1
            #print("error")
            #break
        if flag == 2:
            continue
        op.append(a)
        #print(a)
    c = 0
    j = 0
    for i in ip:
        if ("var" in i):
            continue
        c = c+1
        if ("st" in i) or ("ld" in i):
            op[c-len(variables)] = op[c-len(variables)] + format(j+ctr,"08b")
            j = j + 1
    for k in op:
        print(k)

compileASM()

