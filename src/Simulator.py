import sys
from Memory import Memory
from Registers import Registers
#from Executioner import Executioner
from Assemble import Assembler

class Simulator:
    def __init__(self, asm_filename, obj_filename="../test.o"):
        self.memory = Memory()
        self.registers = Registers()
#        self.executer = Executioner()
        self.assembler = Assembler()

        self.asm_filename = asm_filename
        self.obj_filename = obj_filename

        #address -> 8bit value
        #both are strings actually
        self.memory = {}

    def run(self):
        self.assembler.assemble(self.asm_filename, self.obj_filename)

        self.registers.cia = -1
        #TODO: NEED START OF TEXT SEGMENT HERE
        self.registers.nia = 0
        
        try:
            self.obj_file = open(filename, mode='r+', encoding='utf-8')
        except:
            print("error while reading file...")
            sys.exit(0)


        while self.registers.nia in self.memory:
            input("enter for next instruction...")
            self.executer.convert_and_run(
                    self.memory[self.registers.nia]
            )

if __name__ == "__main__":
    obj_filename = "test.o"
    if len(sys.argv[1:]) == 1:
        simulator = Simulator(asm_filename=sys.argv[1], obj_filename=obj_filename)
        simulator.run()
    else:
        print(f"Usage: python3 Simulator.py <assembly file name>")
