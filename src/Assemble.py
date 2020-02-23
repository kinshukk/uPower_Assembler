import sys

from pass_1 import get_symbol_table_instructions
from pass_22 import convert_lines

class Assembler:
    def __init__(self):
        pass

    def assemble(self, input_filename, obj_filename="test.o"):
        with open(input_filename, encoding="utf-8", mode="r") as f:
            lines = f.read().splitlines()
            (instructions, label, data) = get_symbol_table_instructions(lines)
            print("instructions: {0} \ndata: {1} \nlabel: {2}".format(instructions,data,label))
            print("\n\n\n")

            object_lines = convert_lines(instructions, label, data)

            print(object_lines)

            #TODO: Proper object file format
            obj_file_str = ""

        with open(obj_filename, encoding="utf-8", mode="w+") as o:
            o.write(obj_file_str)
