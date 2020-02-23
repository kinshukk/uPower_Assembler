import sys

from pass_1 import get_symbol_table_instructions
from pass_22 import convert_lines
from instruc import int_string

def int_string(val,bits=32):
    #assume val is negative
    val=(1<<(bits-1))+val
    ans="1"+"{0:031b}".format(val)
    return ans

class Assembler:
    def __init__(self):
        pass

    def assemble(self, input_filename, obj_filename="test.o"):
        with open(input_filename, encoding="utf-8", mode="r") as f:
            lines = f.read().splitlines()
            (instructions, label, data, initialized) = get_symbol_table_instructions(lines)
            print("instructions: {0} \n\ndata: {1} \n\nlabel: {2}\n\ninitialized: {3}".format(instructions,data,label, initialized))
            print("\n\n\n")
            object_lines = convert_lines(instructions, label, data)

            print(object_lines)

            #TODO: Proper object file format
            obj_file_str = ""

        #data size
        obj_file_str += "{:032b}".format(len(initialized.keys()))
        #text size
        obj_file_str += "{:032b}".format(len(instructions.keys()))

        for d in sorted(initialized.keys()):
            val = int(initialized[d])
            if val < 0:
                val = int_string(val)
            
            obj_file_str += "{:032b}".format(val)

        for i in sorted(object_lines.keys()):
            obj_file_str += object_lines[i]

    

        with open(obj_filename, encoding="utf-8", mode="w+") as o:
            o.write(obj_file_str)

    def objectify(self):
        pass

