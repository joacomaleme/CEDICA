from suma import suma
from resta import resta
from multiplicacion import multiplicacion
from division import division

def main():
    num1 = float(input("Ingresa el primer número: "))
    num2 = float(input("Ingresa el segundo número: "))
    operator = input("Ingresa el operador (+, -, *, /): ")

    if operator == "+":
        print(f"Resultado: {suma(num1, num2)}")
    elif operator == "-":
        print(f"Resultado: {resta(num1, num2)}")
    elif operator == "*":
        print(f"Resultado: {multiplicacion(num1, num2)}")
    elif operator == "/":
        print(f"Resultado: {division(num1, num2)}")
    else:
        print("Opción no válida")

if __name__ == "__main__":
    main()
