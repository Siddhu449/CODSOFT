def calculator():
    print("Simple Calculator")
    print("=================")
    
    while True:
        try:
            # Get user input
            num1 = float(input("\nEnter the first number: "))
            num2 = float(input("Enter the second number: "))
            
            print("\nAvailable operations:")
            print("+ : Addition")
            print("- : Subtraction")
            print("* : Multiplication")
            print("/ : Division")
            
            operation = input("\nEnter the operation (+, -, *, /): ")
            
            # Perform calculation based on operation
            if operation == '+':
                result = num1 + num2
                print(f"\n{num1} + {num2} = {result}")
                
            elif operation == '-':
                result = num1 - num2
                print(f"\n{num1} - {num2} = {result}")
                
            elif operation == '*':
                result = num1 * num2
                print(f"\n{num1} * {num2} = {result}")
                
            elif operation == '/':
                if num2 == 0:
                    print("\nError: Division by zero is not allowed!")
                else:
                    result = num1 / num2
                    print(f"\n{num1} / {num2} = {result}")
                    
            else:
                print("\nError: Invalid operation! Please use +, -, *, or /")
                
            # Ask if user wants to continue
            continue_calc = input("\nDo you want to perform another calculation? (y/n): ").lower()
            if continue_calc != 'y':
                print("Thank you for using the calculator!")
                break
                
        except ValueError:
            print("\nError: Please enter valid numbers!")
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")

# Run the calculator
calculator()