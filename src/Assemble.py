import sys

from pass_1 import get_symbol_table_instructions
from pass_22 import convert_lines

class Assembler:
    def __init__(self):
        pass

    def main(self):
        if len(sys.argv[1:]) == 1:
            with open(sys.argv[1], encoding="utf-8", mode="r") as f:
                lines = f.read().splitlines()
                (instructions, label, data) = get_symbol_table_instructions(lines)
                print(f"instructions: {instructions} \ndata: {data} \nlabel: {label}")
                print("\n\n\n")

                object_lines = convert_lines(instructions, label, data)

                print(object_lines)

        else:
            print("Usage: assemble.py [filename]")
    
if __name__ == '__main__':
    assembler = Assembler()
    assembler.main()
