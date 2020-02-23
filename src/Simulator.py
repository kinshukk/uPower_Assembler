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
            self.obj_file = open(self.obj_filename, mode='r+', encoding='utf-8')
        except:
            print("error while reading file...")
            sys.exit(0)

        

        while self.registers.nia in self.memory:
            input("enter for next instruction...")
            self.convert_and_run(
                    self.memory[self.registers.nia]
            )
    
    def twos_comp(self, val, bits):
        """compute the 2's complement of int value val"""
        if (val & (1 << (bits - 1))) != 0:
            val = val - (1 << bits)        
        return val            
    
    def int_string(self, val, bits):
        if val > 0:
            return "{:064b}".format(val)
    
        val=(1<<(bits-1))+val
        ans="1"+"{0:063b}".format(val)
        return ans
    
    
    def convert_and_execute(self, lin):
        op=int(lin[:6],2)
    
        if op==31:
            ex_op=int(lin[22:31],2)
            
            if ex_op==27:
                rs=int(lin[6:11],2)
                ra=int(lin[11:16],2)
                rb=int(lin[16:21],2)
                
                shift_amount=int(registers.registers[rb][57:],2)
                registers.registers[ra]=registers.registers[rs][:64-shift_amount]+"0"*shift_amount
                return
    
            if ex_op==539:
                rs=int(lin[6:11],2)
                ra=int(lin[11:16],2)
                rb=int(lin[16:21],2)
                
                shift_amount=int(registers.registers[rb][57:],2)
                registers.registers[ra]="0"*shitf_amount + registers.registers[rs][:64-shift_amount]
                return
    
            if ex_op==266:
                rt=int(lin[6:11],2)
                ra=int(lin[11:16],2)
                rb=int(lin[16:21],2)
                 
                
                registers.registers[rt]=self.int_string((self.twos_comp(int(registers.registers[ra],2),64)+self.twos_comp(int(registers.registers[rb],2),32)),64)
                
                return
            
            if ex_op==40:
                rt=int(lin[6:11],2)
                ra=int(lin[11:16],2)
                rb=int(lin[16:21],2) 
                
                registers.registers[rt]=self.int_string(-(self.twos_comp(int(registers.registers[ra],2),64)+self.twos_comp(int(registers.registers[rb],2),64)),64)
                
                return
    
            ex_op=int(lin[21:31],2)
    
            if ex_op==28:
                rs=int(lin[6:11],2)
                ra=int(lin[11:16],2)
                rb=int(lin[16:21],2) 
    
                registers.registers[ra]=self.int_string((int(registers.registers[rs],2))&(int(registers.registers[rb],2)))
                return 
    
            if ex_op==444:
                rs=int(lin[6:11],2)
                ra=int(lin[11:16],2)
                rb=int(lin[16:21],2) 
    
                registers.registers[ra]=self.int_string((int(registers.registers[rs],2))|(int(registers.registers[rb],2)))
                return 
    
            if ex_op==316:
                rs=int(lin[6:11],2)
                ra=int(lin[11:16],2)
                rb=int(lin[16:21],2) 
    
                registers.registers[ra]=self.int_string((int(registers.registers[rs],2))^(int(registers.registers[rb],2)))
                return 
    
        if op==14:
            rt=int(lin[6:11],2)
            ra=int(lin[11:16],2)
            si=int(lin[16:],2) 
    
            registers.registers[rt]=self.int_string(int(registers.registers[ra],2) + si)
    
            return
    
        if op==15:
            rt=int(lin[6:11],2)
            ra=int(lin[11:16],2)
            si=int(lin[16:]+"0"*16,0)
    
            rt=self.int_string(int(registers.registers[ra],2)+si)
            return
    
        if op==58:
            rt=int(lin[6:11],2)
            ra=int(lin[11:16],2)
            ds=int(lin[16:30]+"00",2)
            
            add=registers.registers[ra]+ds;
            
            # this function returns doubleword in signed bit format
            rt=get_doubleword(self.int_string(add))
    
            return
    
        if op==32:
           
            rt=int(lin[6:11],2)
            ra=int(lin[11:16],2)
            ds=int(lin[16:],2)
            
            add=registers.registers[ra]+ds;
    
            registers.registers[rt]="0"*32+get_word(self.int_string(add))
    
            return
    
        if op==62:
            rt=int(lin[6:11],2)
            ra=int(lin[11:16],2)
            ds=int(lin[16:30]+"00",2)
            
            add=registers.registers[ra]+ds;
            
            store_doubleword(add,registers.registers[rt])
  
        if op==36:
    
            rt=int(lin[6:11],2)
            ra=int(lin[11:16],2)
            d=int(lin[16:],2)
            
            add=registers.registers[ra]+ds;
            
            store_word(add,registers.registers[rt][32:])
    
            return
    
        if op==18:
    
            AA=int(lin[30],2)
            li=lin[6:30],2
    
            if AA=="1":
    
                registers.nia=li+"0"*40
                
                return
            
            if AA=="0":
    
                registers.nia=self.int_string(int(li+"0"*40,2)+int(registers.cia))
    
                return


if __name__ == "__main__":
    obj_filename = "test.o"
    if len(sys.argv[1:]) == 1:
        simulator = Simulator(asm_filename=sys.argv[1], obj_filename=obj_filename)
        simulator.run()
    else:
        print(f"Usage: python3 Simulator.py <assembly file name>")
