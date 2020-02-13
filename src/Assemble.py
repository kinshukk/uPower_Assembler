import sys

from Tokenizer import Tokenizer

class Assembler:
    def __init__(self):
        self.tokenizer = Tokenizer()

    def main(self):
        if len(sys.argv[1:]) == 1:
            with open(sys.argv[1], encoding="utf-8", mode="r") as f:
                lines = self.tokenizer.run(f.readlines())
                print(f"Lines: {lines}\n\n")
        else:
            print("Usage: assemble.py [filename]")
    
if __name__ == '__main__':
    assembler = Assembler()
    assembler.main()
