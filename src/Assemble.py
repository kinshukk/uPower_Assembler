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
                print("instructions: {0} \ndata: {1} \nlabel: {2}".format(instructions,data,label))
                print("\n\n\n")

                object_lines = convert_lines(instructions, label, data)
                with open('test.o',mode="w") as f:
                    result=sorted([(i,object_lines[i]) for i in object_lines])
                    result=[a[1] for a in result]
                    result="".join(result)
                    f.write(result)
                print(object_lines)

        else:
            print("Usage: assemble.py [filename]")
    
if __name__ == '__main__':
    assembler = Assembler()
    assembler.main()
