import sys
from Memory import Memory
from Registers import Registers
from Executioner import Executioner

class Simulator:
    def __init__(self, filename="../test.o"):
        self.memory = Memory()
        self.registers = Registers()
        self.executer = Executioner

        try:
            self.file = open(filename, mode='r+', encoding='utf-8')
        except:
            print("error while reading file...")
            sys.exit(0)

        #address -> 8bit value
        #both are strings actually
        self.memory = {
        }

    def run(self):
        
        
        while self.registers.nia in self.memory:
            self.executer.convert_and_run(
                    self.memory[self.registers.nia]
            )
