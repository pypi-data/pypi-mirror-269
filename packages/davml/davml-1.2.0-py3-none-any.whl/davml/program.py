import sys
import os

def main():
    titles = [
        "Keras & Tensorflow",
        "Linear Regression",
        "Logistic Regression",
        "SVM ",
        "Hebb Learning OR AND",
        "MP Neoron",  
        "Perceptron error backward",
        "Perceptron Single Layer",
        "PCA",


    ]
    
    if len(sys.argv) == 1:
        # No argument provided, print all titles
        print("Titles:")
        for idx, title in enumerate(titles, 1):
            print(f"{idx}. {title}")
    else:
        try:
            # Argument provided, try to convert it to an integer
            idx = int(sys.argv[1]) - 1
            if 0 <= idx < len(titles):
                # Valid index provided
                current_directory = os.path.dirname(os.path.realpath(__file__))
                file_name = f"m{idx + 1}.py"
                file_path = os.path.join(current_directory, file_name)
                
                if len(sys.argv) > 2 and sys.argv[2] == 'p':
                    # Print complete code to terminal
                    with open(file_path, 'r') as file:
                        code = file.read()
                        print(f"Code from {file_name}:\n")
                        print(code)
                else:
                    # Copy code to clipboard
                    import pyperclip
                    with open(file_path, 'r') as file:
                        code = file.read()
                        pyperclip.copy(code)
                        print(f"Code from {file_name} copied to clipboard!")
            else:
                print("Invalid index!")
        except ValueError:
            print("Invalid argument! Please provide a valid index.")

if __name__ == "__main__":
    main()
