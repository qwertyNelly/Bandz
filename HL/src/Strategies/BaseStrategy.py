
from os.path import exists
import ast
import os
from pathlib import Path
from dotenv import load_dotenv
import json

load_dotenv()
ast = Path(os.environ.get('AST_PATH', "/Users/ben/Desktop/bndni/bndni/HL/src/Strategies/AST/IchmokuTheory.ast"))
print(ast)
def import_from_ast(ast):
    astp = ast.parse(ast)
    exec(compile(astp))
        
        
        

def ast_from_file():
    ast = Path(os.environ.get('AST_PATH', "/Users/ben/Desktop/bndni/bndni/HL/src/Strategies/AST/IchmokuTheory.ast"))
    with open(ast, 'rb') as f:
        ast = f.readlines()
        f.flush()
    astp = ast.Module(ast.parse(ast, mode='eval'))
    for v in astp.values():
        print(v)
    print(compile(astp, mode=exec))
    return astp
        
    


if __name__ == '__main__':
    strat = ast_from_file()
    print(strat.Attribute)
    