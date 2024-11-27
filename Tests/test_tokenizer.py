from openpyxl.formula.tokenizer import Tokenizer



expression = "=SUMA(A1+1)"

tokenizer = Tokenizer(expression)

print(tokenizer.items)
print(len(tokenizer.items))

