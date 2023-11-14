# CMSC 129 - PE03 Non-Recursive Predictive Parsing
# Members: Cepeda, Pandaan, Ponsica

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import os

parser = tk.Tk()
parser.title('Non-Recursive Predictive Parsing')
parser.geometry('650x900')
parser.configure(bg='#E6E6EA')

# Variable initiation
prod_table = None
parse_table= None
parsed = None
frame1 = None
frame2 = None
frame3 = None
frame4 = None
label1 = None
label2 = None
filename_label1 = None
filename_label2 = None

# Create a StringVar for the status label
status_var = tk.StringVar()
status_var.set("LOADED: No file loaded.")

# Create a StringVar for the parsing status label
parsing_status_var = tk.StringVar()
parsing_status_var.set("PARSING: No input specified.")

# Global variable to store the input filename
input_filename = ""
input_directory = ""

# Global variables to store the base filenames
prod_basenames = []
ptbl_basenames = []

def create_frames():
    global frame1, frame2, frame3, frame4, filename_label1, filename_label2, label1, label2

    frame1 = tk.Frame(parser, borderwidth=2, relief="solid")
    frame1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    label1 = tk.Label(frame1, text="Productions", font=("Helvetica", 12))
    label1.grid(row=0, column=0, columnspan=2)

    filename_label1 = tk.Label(frame1, text="", font=("Helvetica", 10))
    filename_label1.grid(row=1, column=0, columnspan=2)

    frame2 = tk.Frame(parser, borderwidth=2, relief="solid")
    frame2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    label2 = tk.Label(frame2, text="Parse Table", font=("Helvetica", 12))
    label2.grid(row=0, column=0, columnspan=3)

    filename_label2 = tk.Label(frame2, text="", font=("Helvetica", 10))
    filename_label2.grid(row=1, column=0, columnspan=3)

    frame4 = tk.Frame(parser, borderwidth=2, relief="solid")
    frame4.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    label4 = tk.Label(frame4, text="Parsed", font=("Helvetica", 12))
    label4.grid(row=0, column=0, columnspan=3)

def select_file():
    global input_filename, input_directory, prod_table, parse_table, filename_label1, filename_label2, label1, label2
    global parsing_status_var, prod_basenames, ptbl_basenames
    error_count = 0  # Reset error_count to 0
    filetypes = (
        ('.prod files', '*.prod'),  
        ('.ptbl files', '*.ptbl')
    )
    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)
    
    if filename:
        # Check the file extension to determine the type
        if filename.endswith('.prod'):
            input_filename = filename
            input_directory = os.path.dirname(filename)

            # Clear existing prod_table (except for filename_label1 and label1)
            if prod_table is not None:
                for widget in frame1.winfo_children():
                    if widget not in [filename_label1, label1]:
                        widget.destroy()

            # Add the base name to the list
            prod_basenames.append(os.path.splitext(os.path.basename(filename))[0])
                                                                               
            # Load and display .prod table
            prod_table = load_prod_table(filename)
            display_prod_table(prod_table)
            # Update filename label
            filename_label1.config(text=f"{os.path.basename(filename)}")
        elif filename.endswith('.ptbl'):
            input_filename = filename
            input_directory = os.path.dirname(filename)

            # Clear existing prod_table (except for filename_label2 and label2)
            if prod_table is not None:
                for widget in frame2.winfo_children():
                    if widget not in [filename_label2, label2]:
                        widget.destroy()

            # Add the base name to the list
            ptbl_basenames.append(os.path.splitext(os.path.basename(filename))[0])

            # Load and display parse table
            parse_table = load_parse_table(filename)
            display_parse_table(parse_table)
            # Update filename label
            filename_label2.config(text=f"{os.path.basename(filename)}")

# Load .prod table
def load_prod_table(file_path):
    prod_table = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Treat commas as delimiters in the CSV file
                line.replace("’","\'")
                row = line.strip().split(',')
                prod_table.append(row)
        # Update status label
        status_var.set(f"LOADED: {os.path.basename(input_filename)}")
        return prod_table
    except Exception as e:
        print(f"Error loading parse table: {e}")
        return None

# Function to display the product table inside frame1
def display_prod_table(prod_table):
    # Create a treeview widget
    tree = ttk.Treeview(frame1, columns=(0, 1, 2), show="headings")

    # Add column headings
    headers = ["ID", "NT", "P"]
    for i, heading in enumerate(headers):
        tree.heading(i, text=heading)
        tree.column(i, width=50)  # Adjust the width as needed

    # Add data to the treeview
    for row in prod_table:
        tree.insert("", "end", values=row)

    tree.grid(padx=10, pady=10, sticky='w')

# Load .ptbl
def load_parse_table(file_path):
    parse_table = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Treat commas as delimiters in the CSV file
                row = line.strip().split(',')
                parse_table.append(row)
        # Update status label
        status_var.set(f"LOADED: {os.path.basename(input_filename)}")
        return parse_table
    except Exception as e:
        print(f"Error loading parse table: {e}")
        return None
    
def display_parse_table(parse_table):
    if parse_table is not None:
        # Create a frame inside the main window
        # table_frame = ttk.Frame(parser)
        # table_frame.grid(row=8, column=0, columnspan=5, padx=10, pady=10)

        # Create a Treeview widget
        tree = ttk.Treeview(frame2, columns=tuple(range(len(parse_table[0]))), show="headings")

        # Use the first row from the parse table as column headings
        for i, heading_text in enumerate(parse_table[0]):
            tree.heading(i, text=heading_text)
            tree.column(i, width=50, anchor=tk.CENTER)

        # Add data to the Treeview (excluding the first row)
        for row in parse_table[1:]:
            tree.insert("", tk.END, values=tuple(row))

        tree.grid(padx=10, pady=10, sticky='w')

# used to convert stack and input into strings
def list_to_string(list):
    return ' '.join(list)

# clear frame 4 everytime parse button is clicked
def clear_parse_results():
    for item in frame4.winfo_children():
        item.destroy()

# Function to get user input from the text box
def parsing_function():
    global parsing_status_var, prod_basenames, ptbl_basenames
    # Clear previous parse results
    clear_parse_results()

    # stacks for input and stack and parsed
    input = []
    stack = []
    parsed = []

    action = ""

    # intialization of input
    user_input = input_entry.get()
    input = user_input.strip().split(' ')
    input.append('$')

    # Check if user input is not empty
    if not user_input:
        parsing_status_var.set("PARSING: Invalid. User input is empty.")
        return
    
    # Check if user input contains only valid symbols
    valid_symbols = {'id', '+', '*', '(', ')', '$'}
    if any(symbol not in valid_symbols for symbol in user_input.split()):
        parsing_status_var.set("PARSING: Invalid. User input contains invalid symbols.")
        return

    # Check if both .prod and .ptbl files are loaded
    if not prod_basenames or not ptbl_basenames:
        parsing_status_var.set("PARSING: Invalid. Both .prod and .ptbl files must be loaded.")
    else:
        # Check if the loaded .prod and .ptbl files are of the same base filename
        if prod_basenames and ptbl_basenames and prod_basenames[-1] != ptbl_basenames[-1]:
                # Display error message in parsing_status_var
                parsing_status_var.set("PARSING: Invalid. Loaded files must have the same base filename.")
                return
        else:
            # Update parsing status label
            parsing_status_var.set(f"PARSING: Valid.")
    
    # initialization of stack
    for i in range(0, len(prod_table)):
        if(prod_table[i][0]=='1'):
            stack.append(prod_table[i][1])
    stack.append('$')
    

    # main parsing function
    parsed.append([list_to_string(stack), list_to_string(input)])
    flag = 0
    while(flag == 0):

        # assign an int for each terminal
        top_input = input[0]
        match top_input:
            case 'id':
                top_input = 1
            case '+':
                top_input = 2
            case '*':
                top_input = 3
            case '(':
                top_input = 4
            case ')':
                top_input = 5
            case '$':
                top_input = 6

        # case when match found in stack and input buffer
        if stack[0] == input[0]:
            action = "Match " + input[0]
            stack.pop(0)
            input.pop(0)
            parsed.append([list_to_string(stack), list_to_string(input), action])
        # case when not matching, top element of stack popped and parse table is searched
        else:
            for i in range(1, len(parse_table)):
                if parse_table[i][0] == stack[0]:
                    # error if top of stack not found in parse table
                    if parse_table[i][top_input] == '':
                        action = "Error"
                        parsed.append([list_to_string(stack), list_to_string(input), action])
                        flag = 1
                    # if found, top is popped and replaced with the matching production
                    else:
                        current_prod = int(parse_table[i][top_input]) - 1
                        action = "Output " + prod_table[current_prod][1] + " -> " + prod_table[current_prod][2]
                        stack.pop(0)
                        current_action = prod_table[current_prod][2].strip().split(' ')
                        current_action.reverse()
                        for j in range(0, len(current_action)):
                            if current_action[j] == 'e':
                                break
                            else:
                                stack.insert(0, current_action[j])

                        parsed.append([list_to_string(stack), list_to_string(input), action])
        print(parsed)

        # success case
        if stack[0] == '$' and input[0] == '$':
            flag = 1
            action = "Match $"
            parsed.append(["", "", action])

    # Check if an "error" occurred in the last action
    if parsed[-1][2] == "error":
        parsing_status_var.set("PARSING: Invalid. An error occurred during parsing.")
    else:
        parsing_status_var.set("PARSING: Valid.")

    # Create a Treeview widget for parse information
    parse_tree = ttk.Treeview(frame4, columns=("Stack", "Input", "Action"), show="headings")
    parse_tree.heading("Stack", text="Stack")
    parse_tree.heading("Input", text="Input")
    parse_tree.heading("Action", text="Action")

    # Right-align the contents of the "Stack" and "Input" column 
    parse_tree.column("Stack", anchor=tk.E)
    parse_tree.column("Input", anchor=tk.E)  
    parse_tree.column("Action", anchor=tk.CENTER)  

    # Add data to the Treeview
    for row in parsed:
        parse_tree.insert("", tk.END, values=row)
    
    parse_tree.grid(padx=10, pady=10, sticky='w')

    save_to_prsd(parsed)

# Function to output .prsd file
def save_to_prsd(parsed):
    # Check if the parsed information is available
    if parsed:
        try:
            # Use the .prod filename as the default filename
            prod_filename = os.path.splitext(os.path.basename(input_filename))[0]

            # Prompt the user for the desired .prsd filename
            user_input_filename = fd.asksaveasfilename(
                filetypes=[("Parsed Files", "*.prsd")],
                title="Save Parsed Information",
                initialdir=input_directory
            )

            # Check if the user canceled the file dialog
            if not user_input_filename:
                parsing_status_var.set("PARSING: Save operation canceled.")
                return

            # Append prod filename before saving
            prsd_filename = f"{user_input_filename}_{prod_filename}.prsd"

            # Open the file in write mode and save the parsed information
            with open(prsd_filename, 'w') as prsd_file:
                for row in parsed:
                    prsd_file.write(','.join(row) + '\n')

            # Update the status label
            parsing_status_var.set(f"PARSING: Valid. Please see '{os.path.basename(prsd_filename)}'")
        except Exception as e:
            # Handle any errors that might occur during the saving process
            print(f"Error saving parsed information: {e}")
            status_var.set("PARSING: Failed to save parsed information.")
    else:
        # If parsed information is not available, update the status label
        status_var.set("PARSING: No parsed information to save.")


# Create a frame for user input elements
user_input_frame = tk.Frame(frame3, borderwidth=2, relief="solid")
user_input_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

# Create a label for the text box
input_label = tk.Label(user_input_frame, text="User Input:", font=('Helvetica', 12))
input_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

# Create a text box (Entry widget) for user input
input_entry = tk.Entry(user_input_frame, width=30, font=('Helvetica', 12))
input_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

# Create a button to get user input
input_button = tk.Button(user_input_frame, text="Parse", font=('Helvetica', 12),
                         command=parsing_function)
input_button.grid(row=0, column=2, padx=10, pady=5, sticky="w")


# Button for load file
button1 = tk.Button(font=('Helvetica', 12), text='Load File', bd=1, relief='ridge',
                 fg='black', height=1, width=21, command=select_file)

button1.grid(row=3, column=0, padx=10   , pady=10, sticky="w")

# Label for status
status_label = tk.Label(parser, textvariable=status_var, font=('Helvetica', 12))
status_label.grid(row=2, column=0, columnspan=5, padx=20, pady=5, sticky="w")

# Label for parsing status label
status_label2 = tk.Label(parser, textvariable=parsing_status_var, font=('Helvetica', 12))
status_label2.grid(row=5, column=0, columnspan=5, padx=20, pady=5, sticky="w")

# Configure rows and columns to expand with the window
parser.columnconfigure(0, weight=1)
parser.columnconfigure(1, weight=20)
parser.rowconfigure(0, weight=1)
parser.rowconfigure(6, weight=1) 

# Create frames and labels
create_frames()

parser.mainloop()