from src.code_generator.generator import CodeGenerator
from tests.test_semantic_analyzer import AST_Input_1, AST_Input_2, AST_Input_3, AST_Input_4 

generator = CodeGenerator()

print("\nGERAÇÃO DO CÓDIGO 1: \n")
python_code = generator.generate(AST_Input_1)
print(python_code)

print("\nGERAÇÃO DO CÓDIGO 2: \n")
python_code = generator.generate(AST_Input_2)
print(python_code)

print("\nGERAÇÃO DO CÓDIGO 3: \n")
python_code = generator.generate(AST_Input_3)
print(python_code)

print("\n GERAÇÃO DO CÓDIGO 4: \n")
python_code = generator.generate(AST_Input_4)
print(python_code)