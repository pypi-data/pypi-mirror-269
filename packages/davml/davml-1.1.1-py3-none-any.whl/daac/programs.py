import sys
import pyperclip
import os

def main():
    titles = [
        "Simple Linear Regression",
        "Multiple Linear Regression",
        "Time series analysis",
        "Arima Model",
        "Sentiment Analysis",
        "Data Visual R",
        "Data Visual Python"
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
                # Valid index provided, copy corresponding program to clipboard
                current_directory = os.path.dirname(os.path.realpath(__file__))
                file_name = f"p{idx + 1}.py"
                file_path = os.path.join(current_directory, file_name)
                
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
