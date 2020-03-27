"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CMP = 0b10100111
JEQ = 0b01010101
JNE = 0b01010110
JMP = 0b01010100
E = 0b00000001
L = 0b00000100
G = 0b00000010

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # Add list properties to the CPU class to hold 256 bytes of memory and 8 general-purpose registers
        self.ram = [None] * (256)
        self.reg = [0] * (8)
        self.pc = 0
        self.sp = 7
        self.FL = 0b00000000

    def load(self,filename):
        """Load a program into memory."""

        address = 0

        try:
            with open(filename) as file:
                for line in file:
                    # ignore comments
                    content = line.split("#")
                    #print(f"content {content}")
                    if content[0] == "":
                        continue
                    # strip whitespace
                    value = content[0].split()
                    print(f"value {value[0]}")
                    
                    
                    
                    #value = int(value[0],2)
                    
                    self.ram[address] = int(value[0],2)
                    
                    address += 1
        except Exception:
            import os
            raise FileNotFoundError(f"No file named {filename} in {os.getcwd()}")
        print(self.ram[:20])

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                print(f"A and B are equal")
                self.FL = 0b00000001
            elif self.reg[reg_a] > self.reg[reg_b]:
                print("A is greater than B")
                self.FL = 0b00000010
            elif self.reg[reg_a] < self.reg[reg_b]:
                print("A is less than B")
                self.FL = 0b00000100

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True
        print('Running')
        while running:

            # read the memory address that's stored in register PC, 
            # and store that result in IR, the Instruction Register
            IR = self.ram[self.pc]
            # print("INSTRUCTION",IR)
            # print("PC",self.pc)
            # print("LDI", LDI)
            # print("PRN", PRN)
            # print("HLT", HLT)
            

            # Using ram_read(), read the bytes at PC+1 and PC+2 
            # from RAM into variables operand_a and operand_b in case the instruction needs them.
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if IR == LDI:
                #print("LDI")
                self.reg[operand_a] = operand_b
                self.pc += 3

            elif IR == HLT:
                print("Execution Finished")
                running = False
                self.pc += 1

            elif IR == PRN:
                #print("PRN")
                #r = int(input("Which register (1-8): "))
                # print(self.reg[r])
                print(self.reg[operand_a])
                self.pc += 2
            
            elif IR == MUL:
                #print("MUL")
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3
                
            elif IR == PUSH:
                reg = self.ram[self.pc + 1]
                val = self.reg[reg]
                # decrement the stack pointer
                self.reg[self.sp] -= 1
                # Copy the value in the given register to the address pointed to by SP.
                self.ram[self.reg[self.sp]] = val
                self.pc += 2

            elif IR == POP:
                reg = self.ram[self.pc + 1]
                val = self.ram[self.reg[self.sp]]
                self.reg[reg] = val
                self.reg[self.sp] += 1
                self.pc += 2
            
            elif IR == CMP:
                #print("CMP")
                self.alu("CMP", operand_a, operand_b)
                self.pc += 3

            elif IR == JMP:
                #print("JMP")
                # get the given register by looking at the next op code
                reg = self.ram[self.pc + 1]
                # set the PC to the address stored in the register
                self.pc = self.reg[reg]

            elif IR == JNE:
                #print("JNE")
                if self.FL != E:
                    # get the given register by looking at the next op code
                    reg = self.ram[self.pc + 1]
                    # set the PC to the address stored in the register
                    self.pc = self.reg[reg]
                else:
                    self.pc += 2

            if IR == JEQ:
                #print("JEQ")
                if self.FL == E:
                    # get the given register by looking at the next op code
                    reg = self.ram[self.pc + 1]
                    # set the PC to the address stored in the register
                    self.pc = self.reg[reg]
                else:
                    self.pc += 2





            

        


    def ram_read(self, address):
        '''
        accept the address to read and return the value stored there.
        '''
        return self.ram[address]

    def ram_write(self, address, value):
        '''
        accept a value to write, and the address to write it to.
        '''
        self.ram[address] = value

