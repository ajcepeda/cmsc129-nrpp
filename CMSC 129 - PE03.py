# CMSC 129 - PE03 Non-Recursive Predictive Parsing
# Members: Cepeda, Pandaan, Ponsica

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import os

parser = tk.Tk()
parser.title('Non-Recursive Predictive Parsing')
parser.geometry('650x400')
parser.configure(bg='#E6E6EA')

# Variable initiation
prod_table = None
parse_table= None
frame1 = None
frame2 = None
frame3 = None

# Create a StringVar for the status label
status_var = tk.StringVar()
status_var.set("LOADED: No file loaded.")

# Global variable to store the input filename
input_filename = ""
input_directory = ""

def create_frames():
    global frame1, frame2, frame3

    frame1 = tk.Frame(parser, borderwidth=2, relief="solid")
    frame1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    label1 = tk.Label(frame1, text="Productions", font=("Helvetica", 12))
    label1.grid(row=0, column=0, columnspan=2)

    frame2 = tk.Frame(parser, borderwidth=2, relief="solid")
    frame2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    label2 = tk.Label(frame2, text="Parse Table", font=("Helvetica", 12))
    label2.grid(row=0, column=0, columnspan=3)

def select_file():
    global input_filename, input_directory, prod_table, parse_table
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
            # Load and display .prod table
            prod_table = load_prod_table(filename)
            display_prod_table(prod_table)
        elif filename.endswith('.ptbl'):
            input_filename = filename
            input_directory = os.path.dirname(filename)
            # Load and parse table
            parse_table = load_parse_table(filename)
            display_parse_table(parse_table)

# Load .prod table
def load_prod_table(file_path):
    prod_table = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Treat commas as delimiters in the CSV file
                row = line.strip().split(',')
                prod_table.append(row)
        # Update status label
        status_var.set(f"LOADED: '{os.path.basename(input_filename)}'")
        return prod_table
    except Exception as e:
        print(f"Error loading parse table: {e}")
        return None

# Function to display .prod table
def display_prod_table(file_path):
    if prod_table is not None:
        # # Create a frame inside the main window
        # prod_frame = ttk.Frame(parser)
        # prod_frame.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        # Create a Treeview widget for .prod table
        prod_tree = ttk.Treeview(frame1, columns=tuple(range(len(prod_table[0]))), show="headings")

        # Use the first row from the .prod table as column headings
        for i, heading_text in enumerate(prod_table[0]):
            prod_tree.heading(i, text=heading_text)
            prod_tree.column(i, width=50, anchor=tk.CENTER)

        # Add data to the Treeview (excluding the first row)
        for row in prod_table[1:]:
            prod_tree.insert("", tk.END, values=tuple(row))

        prod_tree.grid(padx=10, pady=10, sticky='w')

def load_parse_table(file_path):
    parse_table = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Treat commas as delimiters in the CSV file
                row = line.strip().split(',')
                parse_table.append(row)
        # Update status label
        status_var.set(f"LOADED: '{os.path.basename(input_filename)}'")
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

# Function to get user input from the text box
def get_user_input():
    user_input = input_entry.get()
    print(f"User Input: {user_input}")

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
                         command=get_user_input)
input_button.grid(row=0, column=2, padx=10, pady=5, sticky="w")


# Button for load file
button1 = tk.Button(font=('Helvetica', 12), text='Load File', bd=1, relief='ridge',
                 fg='black', height=1, width=21, command=select_file)
# Button for process
# button2 = tk.Button(font=('times new roman', 12), text='Process', bd=1, relief='ridge',
#                  fg='black', height=1, width=21, command="")

button1.grid(row=3, column=0, padx=10   , pady=10, sticky="w")
# button2.grid(row=4, column=0, padx=0, pady=10, sticky="e")

# Label for status
status_label = tk.Label(parser, textvariable=status_var, font=('Helvetica', 12))
status_label.grid(row=2, column=0, columnspan=5, padx=20, pady=5, sticky="w")

# Configure rows and columns to expand with the window
parser.columnconfigure(0, weight=1)
parser.columnconfigure(1, weight=20)
parser.rowconfigure(0, weight=1)

# Create frames and labels
create_frames()

parser.mainloop()