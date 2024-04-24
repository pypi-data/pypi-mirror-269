import sys
import pyperclip
import os

def main():
    titles = [
        "1 Keras-NN",
        "2 Linear Regression",
        "3 Logistic Regression" ,
        "4 SVM",
        "5 Hebbian" , 
        "7 MP NN ",
        "8 perceptron",
        "9 PCA" ,
        "10 ALL DAV " 
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
            if 0 <= idx < 12:
                # Valid index provided, copy corresponding program to clipboard
                current_directory = os.path.dirname(os.path.realpath(__file__))
                file_name = f"ML-{idx + 1}.py"
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
