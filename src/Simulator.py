import sys
from Memory import Memory
from Registers import Registers
#from Executioner import Executioner
from Assemble import Assembler

#word in bytes
WORD = 4

class Simulator:
    def __init__(self, asm_filename, obj_filename="../test.o"):
        self.memory = Memory()
        self.registers = Registers()
#        self.executer = Executioner()
        self.assembler = Assembler()

        self.asm_filename = asm_filename
        self.obj_filename = obj_filename

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

        obj_data = self.obj_file.read()

        print(f"\n\nObject file inside Simulator.py: {obj_data}")

        print(f"length of object file in bits: {len(obj_data)} | words: {len(obj_data) / 32}")

        len_data = int(obj_data[:32], 2)
        len_text = int(obj_data[32:64], 2)
        print(f"len of data: {len_data} | len of text: {len_text}")
        
        print(f"{obj_data[:32]} | {obj_data[32:64]}")

        #for now
        data_start = 8
        text_start = data_start + len_data

        #load text and data into memory
        data = obj_data[64:len_data*8+64]
        text = obj_data[64+len_data*8:]

        print("data: {data}\n\ntext: {text}")

        print("starting writing data to memory")
        for i in range(len_data):
            self.memory.set_address(str(data_start + i), data[i*8:8+(i*8)])

        print("\n\nstarting writing text to memory")
        for i in range(len_text):
            self.memory.set_address(str(text_start + i), text[i*8:8+(i*8)])

        print(f"\n\ndata:{data} {len(data)}\n\ntext: {text} {len(text)}")

        #################################################################
        #now the big bois
        #initialize PCs
        self.registers.cia = text_start
        self.registers.nia = text_start + WORD

        print(f"\n\nmemory:{self.memory.memory}\n\n")
        print("before loop")
        print(f"cia: {self.registers.cia} | cia in memory? {self.registers.cia in self.memory.memory.keys()}")

        while str(self.registers.cia) in self.memory.memory.keys():
            input("\n\npress [enter] to execute next instruction")
            print("\n\n\n")
            instruction = self.memory.get_word(str(self.registers.cia))
            print(f"instruction: {instruction}")
            
            self.convert_and_execute(instruction)

            self.registers.cia += 4
            print(self.registers)


    def twos_comp(self, val, bits):
        """compute the 2's complement of int value val"""
        if (val & (1 << (bits - 1))) != 0:
            val = val - (1 << bits)        
        return val            
    
    def int_string(self, val, bits=64):
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
                
                shift_amount=int(self.registers.R[rb][57:],2)
                self.registers.R[ra]=self.registers.R[rs][:64-shift_amount]+"0"*shift_amount
                return
    
            if ex_op==539:
                rs=int(lin[6:11],2)
                ra=int(lin[11:16],2)
                rb=int(lin[16:21],2)
                
                shift_amount=int(self.registers.R[rb][57:],2)
                self.registers.R[ra]="0"*shitf_amount + self.registers.R[rs][:64-shift_amount]
                return
    
            if ex_op==266:
                rt=int(lin[6:11],2)
                ra=int(lin[11:16],2)
                rb=int(lin[16:21],2)
                 
                
                self.registers.R[rt]=self.int_string((self.twos_comp(int(self.registers.R[ra],2),64)+self.twos_comp(int(self.registers.R[rb],2),32)),64)
                
                return
            
            if ex_op==40:
                rt=int(lin[6:11],2)
                ra=int(lin[11:16],2)
                rb=int(lin[16:21],2) 
                
                self.registers.R[rt]=self.int_string(-(self.twos_comp(int(self.registers.R[ra],2),64)+self.twos_comp(int(self.registers.R[rb],2),64)),64)
                
                return
    
            ex_op=int(lin[21:31],2)
    
            if ex_op==28:
                rs=int(lin[6:11],2)
                ra=int(lin[11:16],2)
                rb=int(lin[16:21],2) 
    
                self.registers.R[ra]=self.int_string((int(self.registers.R[rs],2))&(int(self.registers.R[rb],2)))
                return 
    
            if ex_op==444:
                rs=int(lin[6:11],2)
                ra=int(lin[11:16],2)
                rb=int(lin[16:21],2) 
    
                self.registers.R[ra]=self.int_string((int(self.registers.R[rs],2))|(int(self.registers.R[rb],2)))
                return 
    
            if ex_op==316:
                rs=int(lin[6:11],2)
                ra=int(lin[11:16],2)
                rb=int(lin[16:21],2) 
    
                self.registers.R[ra]=self.int_string((int(self.registers.R[rs],2))^(int(self.registers.R[rb],2)))
                return 
    
        if op==14:
            rt=int(lin[6:11],2)
            ra=int(lin[11:16],2)
            si=int(lin[16:],2) 
    
            self.registers.R[rt]=self.int_string(int(self.registers.R[ra],2) + si)
    
            return
    
        if op==15:
            rt=int(lin[6:11],2)
            ra=int(lin[11:16],2)
            si=int(lin[16:]+"0"*16,0)
    
            rt=self.int_string(int(self.registers.R[ra],2)+si)
            return
    
        if op==58:
            rt=int(lin[6:11],2)
            ra=int(lin[11:16],2)
            ds=int(lin[16:30]+"00",2)
            
            add=self.registers.R[ra]+ds;
            
            # this function returns doubleword in signed bit format
            rt=get_doubleword(self.int_string(add))
    
            return
    
        if op==32:
           
            rt=int(lin[6:11],2)
            ra=int(lin[11:16],2)
            ds=int(lin[16:],2)
            
            add=self.registers.R[ra]+ds;
    
            self.registers.R[rt]="0"*32+get_word(self.int_string(add))
    
            return
    
        if op==62:
            rt=int(lin[6:11],2)
            ra=int(lin[11:16],2)
            ds=int(lin[16:30]+"00",2)
            
            add=self.registers.R[ra]+ds;
            
            store_doubleword(add,self.registers.R[rt])
  
        if op==36:
    
            rt=int(lin[6:11],2)
            ra=int(lin[11:16],2)
            d=int(lin[16:],2)
            
            add=self.registers.R[ra]+ds;
            
            store_word(add,self.registers.R[rt][32:])
    
            return
    
        if op==18:
    
            AA=int(lin[30],2)
            li=int(lin[6:30],2)
    
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
