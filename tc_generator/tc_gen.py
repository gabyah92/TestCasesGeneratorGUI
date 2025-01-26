import re
import time
import math
import random
import shutil
import sys
import timeit
import webbrowser
import zipfile
import subprocess
from PIL import Image
from lang_compiler import LANGS
import customtkinter as ctk
import tkinter as tk
import os
import threading
from datetime import datetime

code = str()
language_value = 1
platform_value = 1
chk = False
inputs = list()
outputs = list()
times = list()
max_time = 0
program_name = str()
program_type = int()
tags = list()
description = str()
constraints = str()
in1, out1, in2, out2, in3, out3 = [""]*6




# Create the main application window
app = ctk.CTk()
app.title("Test Cases Generator GUI")
app.iconbitmap('_internal\\icons\\logo.ico')
width = 1500
height = 750
screenwidth = app.winfo_screenwidth()
screenheight = app.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
app.geometry(alignstr)
app.minsize(1200, 500)
#app.resizable(width=False, height=False)
app.grid_rowconfigure(1, weight=1)
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)
app.grid_columnconfigure(2, weight=1)
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def resource_path2(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    # Determine base path during runtime
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

    # Define the generated directory
    generated_dir = os.path.join(base_path, 'generated')

    # Create the directory if it does not exist
    if not os.path.exists(generated_dir):
        os.makedirs(generated_dir)

    return os.path.join(generated_dir, relative_path)


app.protocol("WM_DELETE_WINDOW", lambda : sys.exit(0))
# Configure grid weight for responsiveness


# Set colors and styles
ctk.set_appearance_mode("dark")  # Modes: "System" (default), "Light", "Dark"
ctk.set_default_color_theme("dark-blue")  # Customize color theme


class PythonCodeEditor(ctk.CTkTextbox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Configure tags for syntax highlighting
        #self.tag_config("keyword", foreground="#FF7F50")  # Coral color for keywords
        self.tag_config("string", foreground="#98FB98")  # Pale green for strings
        self.tag_config("comment", foreground="#D3D3D3")  # Light grey for comments

        self.keyword_colors = {
            "light_blue": "#ADD8E6",
            "light_green": "#90EE90",
            "light_orange": "#FFD580",
            "light_coral": "#F08080",
            "light_pink": "#FFB6C1",
            "light_yellow": "#FFFFE0",
            "light_cyan": "#E0FFFF",
            "light_salmon": "#FFA07A",
            "light_lavender": "#E6E6FA",
            "light_khaki": "#F0E68C",
            "light_turquoise": "#AFEEEE",
            "light_peach": "#FFDAB9",
            "light_mint": "#98FB98",
            "light_sky_blue": "#87CEFA",
            "light_tan": "#D2B48C",
            "light_apricot": "#FFE4B5",
            "light_lilac": "#C8A2C8",
            "light_mauve": "#D8BFD8",
            "light_honeydew": "#F0FFF0",
            "light_azure": "#F0FFFF",
            "light_lemon": "#FFFACD",
            "light_rose": "#FFE4E1",
            "light_thistle": "#D8BFD8",
            "light_periwinkle": "#CCCCFF"
        }

        self.keywords = [
            # Java-specific keywords and terms not in Python
            'abstract', 'boolean', 'byte', 'case', 'catch', 'char', 'const', 'default', 'do',
            'double', 'enum', 'extends', 'final', 'float', 'goto', 'implements', 'instanceof',
            'int', 'interface', 'long', 'native', 'new', 'package', 'private', 'protected',
            'public', 'short', 'static', 'strictfp', 'super', 'switch', 'synchronized', 'this',
            'throw', 'throws', 'transient', 'void', 'volatile',

            # Common Java terms not in Python
            'String', 'System', 'out', 'println', 'main', 'args', 'null', 'true', 'false',
            'ArrayList', 'HashMap', 'LinkedList', 'TreeMap', 'Vector', 'Iterator', 'Comparable',
            'Cloneable', 'Runnable', 'Thread', 'Exception', 'RuntimeException', 'Override',
            'Deprecated', 'SuppressWarnings', 'Annotation', 'FunctionalInterface',

            # Java access modifiers and other common terms
            'public', 'private', 'protected', 'default', 'static', 'final', 'abstract',
            'synchronized',
            'volatile', 'transient', 'native', 'strictfp',

            # Java control flow
            'if', 'else', 'switch', 'case', 'default', 'for', 'do', 'while', 'break', 'continue',
            'return', 'try', 'catch', 'finally', 'throw', 'throws',

            # Java OOP terms
            'class', 'interface', 'extends', 'implements', 'package', 'import',

            # Java primitive types
            'byte', 'short', 'int', 'long', 'float', 'double', 'boolean', 'char',

            # Common Java classes and interfaces
            'Object', 'String', 'StringBuffer', 'StringBuilder', 'Math', 'Integer', 'Double',
            'Boolean', 'Character', 'Byte', 'Short', 'Long', 'Float', 'Number', 'Arrays',
            'Collections', 'List', 'Set', 'Map', 'Queue', 'Deque', 'Stack',

            # Java exception handling
            'try', 'catch', 'finally', 'throw', 'throws', 'Exception', 'RuntimeException',
            'Error', 'Throwable',

            # Java concurrency
            'Thread', 'Runnable', 'Callable', 'synchronized', 'volatile', 'concurrent',

            # Java I/O
            'System', 'out', 'in', 'err', 'PrintStream', 'InputStream', 'OutputStream',
            'Reader', 'Writer', 'File', 'IOException',

            # Python keywords
            'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break',
            'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from',
            'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass',
            'raise', 'return', 'try', 'while', 'with', 'yield',

            # Built-in Functions
            'abs', 'all', 'any', 'ascii', 'bin', 'bool', 'breakpoint', 'bytearray', 'bytes', 'callable',
            'chr', 'classmethod', 'compile', 'complex', 'delattr', 'dict', 'dir', 'divmod', 'enumerate',
            'eval', 'exec', 'filter', 'float', 'format', 'frozenset', 'getattr', 'globals', 'hasattr',
            'hash', 'help', 'hex', 'id', 'input', 'int', 'isinstance', 'issubclass', 'iter', 'len',
            'list', 'locals', 'map', 'max', 'memoryview', 'min', 'next', 'object', 'oct', 'open',
            'ord', 'pow', 'print', 'property', 'range', 'repr', 'reversed', 'round', 'set', 'setattr',
            'slice', 'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple', 'type', 'vars', 'zip',

            # Built-in Constants
            'NotImplemented', 'Ellipsis', '__debug__',

            # Built-in Types
            'bool', 'bytearray', 'bytes', 'classmethod', 'complex', 'dict', 'float', 'frozenset',
            'int', 'list', 'object', 'property', 'range', 'set', 'slice', 'staticmethod', 'str', 'tuple', 'type',

            # String Methods
            'capitalize', 'casefold', 'center', 'count', 'encode', 'endswith', 'expandtabs', 'find',
            'format', 'format_map', 'index', 'isalnum', 'isalpha', 'isascii', 'isdecimal', 'isdigit',
            'isidentifier', 'islower', 'isnumeric', 'isprintable', 'isspace', 'istitle', 'isupper',
            'join', 'ljust', 'lower', 'lstrip', 'maketrans', 'partition', 'replace', 'rfind', 'rindex',
            'rjust', 'rpartition', 'rsplit', 'rstrip', 'split', 'splitlines', 'startswith', 'strip',
            'swapcase', 'title', 'translate', 'upper', 'zfill',

            # List/Dict/Set Methods
            'append', 'clear', 'copy', 'count', 'extend', 'index', 'insert', 'pop', 'remove', 'reverse',
            'sort', 'update', 'values', 'items', 'keys', 'get', 'add', 'discard', 'intersection',
            'difference', 'union', 'symmetric_difference',

            # File Methods
            'close', 'flush', 'fileno', 'isatty', 'read', 'readable', 'readline', 'readlines', 'seek',
            'seekable', 'tell', 'truncate', 'write', 'writable', 'writelines',

            # Numeric Types Methods
            'conjugate', 'fromhex', 'hex', 'imag', 'real',

            # Exception Handling
            'ArithmeticError', 'AssertionError', 'AttributeError', 'BaseException', 'BlockingIOError',
            'BrokenPipeError', 'BufferError', 'BytesWarning', 'ChildProcessError', 'ConnectionAbortedError',
            'ConnectionError', 'ConnectionRefusedError', 'ConnectionResetError', 'DeprecationWarning',
            'EOFError', 'EnvironmentError', 'Exception', 'FileExistsError', 'FileNotFoundError',
            'FloatingPointError', 'FutureWarning', 'GeneratorExit', 'IOError', 'ImportError',
            'ImportWarning', 'IndentationError', 'IndexError', 'InterruptedError', 'IsADirectoryError',
            'KeyError', 'KeyboardInterrupt', 'LookupError', 'MemoryError', 'ModuleNotFoundError',
            'NameError', 'NotADirectoryError', 'NotImplementedError', 'OSError', 'OverflowError',
            'PendingDeprecationWarning', 'PermissionError', 'ProcessLookupError', 'RecursionError',
            'ReferenceError', 'ResourceWarning', 'RuntimeError', 'RuntimeWarning', 'StopAsyncIteration',
            'StopIteration', 'SyntaxError', 'SyntaxWarning', 'SystemError', 'SystemExit', 'TabError',
            'TimeoutError', 'TypeError', 'UnboundLocalError', 'UnicodeDecodeError', 'UnicodeEncodeError',
            'UnicodeError', 'UnicodeTranslateError', 'UnicodeWarning', 'UserWarning', 'ValueError',
            'Warning', 'ZeroDivisionError',

            # Additional Built-in Functions and Types
            'copyright', 'credits', 'license', 'StringIO', 'TextIOWrapper', 'match', 'case'
        ]

        # Assign random colors to keywords
        self.keyword_color_map = {}
        for keyword in self.keywords:
            color = random.choice(list(self.keyword_colors.values()))
            self.keyword_color_map[keyword] = color
            self.tag_config(keyword, foreground=color)

        self.bind("<KeyRelease>", self.highlight_syntax)
        self.bind("<Return>", self.handle_return)
        self.bind("<Tab>", self.handle_tab)
        self.bind("(", lambda event: self.auto_close(event, "(", "()"))
        self.bind("[", lambda event: self.auto_close(event, "[", "[]"))
        self.bind("{", lambda event: self.auto_close(event, "{", "{}"))
        self.bind("<less>", lambda event: self.auto_close(event, "<", "<>"))
        self.bind("\"", lambda event: self.auto_close(event, '\"', "\"\""))
        self.bind("'", lambda event: self.auto_close(event, "'", "''"))

    def highlight_syntax(self, event=None):
        content = self.get("1.0", tk.END)
        for tag in ["keyword", "string", "comment"]:
            self.tag_remove(tag, "1.0", tk.END)

        for keyword in self.keywords:
            self.tag_remove(keyword, "1.0", tk.END)

        for keyword, color in self.keyword_color_map.items():
            start_index = "1.0"
            while True:
                start_index = self.search(r'\y' + keyword + r'\y', start_index, tk.END, regexp=True)
                if not start_index:
                    break
                end_index = f"{start_index}+{len(keyword)}c"
                self.tag_add(keyword, start_index, end_index)
                start_index = end_index

        # Highlight strings
        for match in re.finditer(r'(".*?"|\'.*?\')', content):
            start, end = match.span()
            self.tag_add("string", f"1.0+{start}c", f"1.0+{end}c")

        # Highlight comments
        for match in re.finditer(r'(#.*$)', content, re.MULTILINE):
            start, end = match.span()
            self.tag_add("comment", f"1.0+{start}c", f"1.0+{end}c")

    def handle_return(self, event):
        cursor_pos = self.index(tk.INSERT)
        line_start = self.index(f"{cursor_pos} linestart")
        line = self.get(line_start, cursor_pos)

        # Check if cursor is between curly braces
        if self.get(f"{cursor_pos}-1c") == "{" and self.get(cursor_pos) == "}":
            indent = self.get_indent(line)
            self.insert(tk.INSERT, f"\n{indent}    \n{indent}")
            self.mark_set(tk.INSERT, f"{self.index(tk.INSERT)}-{len(indent) + 1}c")
            return "break"

        # Check if cursor is between box braces
        if self.get(f"{cursor_pos}-1c") == "[" and self.get(cursor_pos) == "]":
            indent = self.get_indent(line)
            self.insert(tk.INSERT, f"\n{indent}    \n{indent}")
            self.mark_set(tk.INSERT, f"{self.index(tk.INSERT)}-{len(indent) + 1}c")
            return "break"

        # Check if cursor is between round braces
        if self.get(f"{cursor_pos}-1c") == "(" and self.get(cursor_pos) == ")":
            indent = self.get_indent(line)
            self.insert(tk.INSERT, f"\n{indent}    \n{indent}")
            self.mark_set(tk.INSERT, f"{self.index(tk.INSERT)}-{len(indent) + 1}c")
            return "break"

        # Check if cursor is between box braces
        if self.get(f"{cursor_pos}-1c") == "<" and self.get(cursor_pos) == ">":
            indent = self.get_indent(line)
            self.insert(tk.INSERT, f"\n{indent}    \n{indent}")
            self.mark_set(tk.INSERT, f"{self.index(tk.INSERT)}-{len(indent) + 1}c")
            return "break"


        # Normal indentation for other cases
        indent = self.get_indent(line)
        if line.strip().endswith(":"):
            indent += "    "

        self.insert(tk.INSERT, f"\n{indent}")
        return "break"

    def get_indent(self, line):
        return line[:len(line) - len(line.lstrip())]

    def handle_tab(self, event):
        self.insert(tk.INSERT, "    ")
        return "break"

    def handle_curly_brace(self, event):
        self.insert(tk.INSERT, "{}")
        self.mark_set(tk.INSERT, f"{tk.INSERT}-1c")
        return "break"

    def auto_close(self, event, opening, closing):
        self.insert(tk.INSERT, closing)
        self.mark_set(tk.INSERT, f"{tk.INSERT}-1c")
        return "break"

# Python Code Input
ctk.CTkLabel(app, text_color='orange', text="Python Code", font=("sans", 25, "bold"),
             anchor="center").grid(row=0, column=1, padx=20, pady=10)
python_code_entry = PythonCodeEditor(app, width=300, height=200, font=("sans", 25, "bold"),
                                     wrap='none')
python_code_entry.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")

# Logic Code Input
ctk.CTkLabel(app, text_color='orange', text="Logic Code", font=("sans", 25, "bold"),
             anchor="center").grid(row=0, column=0, padx=20, pady=10)
logic_code_entry = PythonCodeEditor(app, width=300, height=200, font=("sans", 25, "bold"),
                          wrap='none' )
logic_code_entry.grid(row=1,  column=0, padx=20, pady=10, sticky="nsew")

# Language selection dropdown
ctk.CTkLabel(app, text="Logic Code Language: ", font=("sans", 30, "bold")).grid(row=2, column=0,
                                                                                padx=10)
language_selection = ctk.CTkOptionMenu(app, width=100,
                                     values=["Java", "C", "Python", "C++", "C#", "Go"],
                                     state="readonly", font=("sans", 30, "bold"), fg_color='steelblue',
                                     dropdown_font=("sans", 60, "bold"),  bg_color='black', text_color='black', dynamic_resizing=False )
language_selection.grid(row=2, column=1, padx=12, pady=30, sticky='nsew' )
language_selection.set("Java")

# Test Cases Input
ctk.CTkLabel(app, text="Number Of Test Cases: ", font=("sans", 30, "bold")).grid(row=3, column=0,
                                                                                 padx=10)
num_test_cases_entry = ctk.CTkEntry(app, width=100, font=("sans", 30, "bold"))
num_test_cases_entry.grid(row=3, column=1, padx=10, pady=10, sticky='nsew' )
num_test_cases_entry.insert(0, 10)

# Platform selection dropdown
ctk.CTkLabel(app, text="Choose Your Platform: ", font=("sans", 30, "bold")).grid(row=4, column=0,
                                                                                 padx=10)
platform_selection = ctk.CTkOptionMenu(app, width=100, values=["HackerRank", "CodeRunner", "VPL", "HackerEarth",
                                            "CodeChef"], font=("sans", 30, "bold"), fg_color='steelblue',
                                            dropdown_font=("sans", 50, "bold"), bg_color='black', text_color='black', dynamic_resizing=False)
platform_selection.grid(row=4, column=1, padx=10, pady=10, sticky='nsew'  )
platform_selection.set("HackerRank")


progress_root = None
progress_label = None
progress_inputs = None
progress_outputs = None
progress_bar = None
firstchk = False
entry = None
taginp = None
samplein1, samplein2, samplein3, sampleout1, sampleout2, sampleout3 = [None] * 6
consinp, conslab, deslab, descriptioninp, proglab, progtype, inplab = [None]*7
ok_button = None
input_window = None

def show_error(message):
    error_window = ctk.CTkToplevel(app)  # Create a new window
    error_window.title("Alert!")
    error_window.after(250, lambda: error_window.iconbitmap('_internal\\icons\\logo.ico'))
    height = 150
    width = 800
    screenwidth = app.winfo_screenwidth()
    screenheight = app.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (
        width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    error_window.geometry(alignstr)
    error_window.resizable(width=False, height=False)
    error_window.grab_set()  # Modal window

    label = ctk.CTkLabel(error_window, text=message, padx=20, pady=10, font=('sans', 15, 'bold'))
    label.pack()

    ok_button = ctk.CTkButton(error_window, text="OK", command=error_window.destroy,
                              font=('sans', 15, 'bold'))
    ok_button.pack(pady=10, padx=10)

def description_make():
    global description, constraints, in1, in2, in3, out1, out2, out3
    tin1, tin2, tin3 = str(in1).rstrip(), str(in2).rstrip(), str(in3).rstrip()
    tout1, tout2, tout3 = str(out1).rstrip(), str(out2).rstrip(), str(out3).rstrip()
    if tin1 != "" or tin2 != "" or tin3 != "" or tout1 != "" or tout2 != "" or tout3 != "":
        description += "<h2>Sample TestCases:</h2>\n\n"
    if tout1 != "" or tin1 != "":
        description += "<b>Sample Input 1:</b>\n<p>"+tin1+"</p>\n<b>Sample Output 1:</b>\n<p>"+tout1+"</p>\n\n"
    if tout2 != "" or tin2 != "":
        description += "<b>Sample Input 2:</b>\n<p>" + tin2 + "</p>\n<b>Sample Output 2:</b>\n<p>" + tout2 + "</p>\n\n"
    if tout3 != "" or tin3 != "":
        description += "<b>Sample Input 3:</b>\n<p>" + tin3 + "</p>\n<b>Sample Output 3:</b>\n<p>" + tout3 + "</p>\n\n"
    description += "</p>"+constraints

def get_program_details():
    global program_name, firstchk, entry
    global taginp, samplein1, samplein2, samplein3, sampleout1, sampleout3
    global consinp, conslab, deslab, descriptioninp, proglab, progtype, inplab
    global ok_button, input_window
    def display_cases():
        global inplab, entry, samplein1, samplein2, samplein3, sampleout1, sampleout2, sampleout3

        ctk.CTkLabel(input_window, text="Sample Input 1", pady=40,
                     font=('sans', 18, 'bold'), anchor='e').grid(row=1, column=0, padx=10, pady=5)
        ctk.CTkLabel(input_window, text="Sample Output 1", pady=40,
                     font=('sans', 18, 'bold'), anchor='e').grid(row=3, column=0, padx=10, pady=5)

        ctk.CTkLabel(input_window, text="Sample Input 2", pady=40,
                     font=('sans', 18, 'bold'), anchor='e').grid(row=1, column=1, padx=10, pady=5)
        ctk.CTkLabel(input_window, text="Sample Output 2", pady=40,
                     font=('sans', 18, 'bold'), anchor='e').grid(row=3, column=1, padx=10, pady=5)

        ctk.CTkLabel(input_window, text="Sample Input 3", pady=40,
                     font=('sans', 18, 'bold'), anchor='e').grid(row=1, column=2, padx=10, pady=5)
        ctk.CTkLabel(input_window, text="Sample Output 3", pady=40,
                     font=('sans', 18, 'bold'), anchor='e').grid(row=3, column=2, padx=10, pady=5)

        samplein3 = ctk.CTkTextbox(input_window, width=300, height=200, font=("sans", 20, "bold"),
                                   wrap='none')
        samplein3.grid(row=2, column=2, sticky="nsew", pady=10, padx=10)

        sampleout3 = ctk.CTkTextbox(input_window, width=300, height=200, font=("sans", 20, "bold"),
                                    wrap='none')
        sampleout3.grid(row=4, column=2, sticky="nsew", pady=10, padx=10)

        samplein2 = ctk.CTkTextbox(input_window, width=300, height=200, font=("sans", 20, "bold"),
                                   wrap='none')
        samplein2.grid(row=2, column=1, sticky="nsew", pady=10, padx=10)

        sampleout2 = ctk.CTkTextbox(input_window, width=300, height=200, font=("sans", 20, "bold"),
                                    wrap='none')
        sampleout2.grid(row=4, column=1, sticky="nsew", pady=10, padx=10)

        samplein1 = ctk.CTkTextbox(input_window, width=300, height=200, font=("sans", 20, "bold"),
                                   wrap='none')
        samplein1.grid(row=2, column=0, sticky="nsew", pady=10, padx=10)

        sampleout1 = ctk.CTkTextbox(input_window, width=300, height=200, font=("sans", 20, "bold"),
                                    wrap='none')
        sampleout1.grid(row=4, column=0, sticky="nsew", pady=10, padx=10)

    def display_window2():
        global taginp, ok_button
        ok_button = ctk.CTkButton(input_window, text="OK", width=300, height=40, command=on_ok,
                                  font=('sans', 15, 'bold'))
        ok_button.grid(pady=10, padx=10, row=0, column=2)

        ctk.CTkLabel(input_window, text="Enter program tags(,): ", padx=10, pady=52,
                     font=('sans', 18, 'bold')).grid(row=0, column=0)
        taginp = ctk.CTkEntry(input_window, width=300, font=('sans', 18, 'bold'))
        taginp.grid(row=0, column=1)
    input_window = ctk.CTkToplevel(app)  # Create a new window
    input_window.title("Enter program Details")
    input_window.after(250, lambda: input_window.iconbitmap('_internal\\icons\\logo.ico'))
    height = 750
    width = 1000
    screenwidth = app.winfo_screenwidth()
    screenheight = app.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (
        width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    input_window.geometry(alignstr)
    input_window.resizable(width=False, height=False)

    input_window.grab_set()  # Modal window
    inplab = ctk.CTkLabel(input_window, text="Program Name:", padx=10, pady=10,
                          font=('sans', 18, 'bold'), anchor='e')
    inplab.grid(row=0, column=0)
    entry = ctk.CTkEntry(input_window, width=750, height=50, font=('sans', 20, 'bold'))
    entry.grid(row=0, column=1, padx=10, pady=10)

    deslab = ctk.CTkLabel(input_window, text="Problem Statement:", pady=40,
                          font=('sans', 18, 'bold'), anchor='e')
    deslab.grid(row=1, column=0, padx=10, pady=5)
    descriptioninp = ctk.CTkTextbox(input_window, width=500, height=300, font=("sans", 20, "bold"))
    descriptioninp.grid(row=1, column=1, sticky="nsew", pady=10, padx=10)

    conslab = ctk.CTkLabel(input_window, text="Constraints:", pady=40, font=('sans', 18, 'bold'), anchor='e')
    conslab.grid(row=2, column=0, padx=10, pady=5)
    consinp = ctk.CTkTextbox(input_window, width=500, height=150, font=("sans", 20, "bold"), wrap='none')
    consinp.grid(row=2, column=1, sticky="nsew", pady=10, padx=10)

    proglab = ctk.CTkLabel(input_window, text="Program Type:", pady=40, font=('sans', 18, 'bold'), anchor='e')
    proglab.grid(row=3, column=0, padx=10, pady=5)
    progtype = ctk.CTkOptionMenu(input_window, width=750, height=50,
                                 values=["multilanguage", "language specific"], state="readonly",
                                 font=("sans", 30, "bold"), dropdown_font=("sans", 50, "bold"))
    progtype.grid(row=3, column=1, padx=10, pady=5)
    progtype.set("multilanguage")

    input_window.protocol("WM_DELETE_WINDOW", lambda : on_ok())

    def on_ok():
        global program_name, tags, inplab, ok_button
        app.configure(state='disabled')
        global firstchk, entry, inplab, taginp, conslab, consinp, ok_button, deslab, descriptioninp, description
        if not firstchk:
            global description, constraints, progtype, program_type, proglab
            tmp = entry.get().strip()  # Store the entered name in the global variable
            if len(tmp) == 0:
                show_error('Invalid Name!')
                return
            elif [i for i in str(tmp) if i in '/\\:*?"<<>>||']:
                show_error('Name must not have Characters : / \\ : * ? " < > |')
                return
            else :
                program_name = tmp
            constraints = "<h2>Constraints:</h2>\n"
            loop = consinp.get("1.0", "end-1c")
            for i in loop.splitlines():
                constraints += f'<p>{i}</p>'
            constraints += "\n\n"
            description = "<h2>Problem Statement:</h2>\n\n" + "<p>"
            for line in str(descriptioninp.get("1.0", "end-1c")).splitlines():
                description += '<p>'+line+'</p>'
            description += "</p>\n\n"
            if progtype.get() == 'multilanguage':
                program_type = 1
            else:
                program_type = 0
            entry.destroy()
            inplab.destroy()
            descriptioninp.destroy()
            deslab.destroy()
            conslab.destroy()
            proglab.destroy()
            progtype.destroy()
            consinp.destroy()
            ok_button.destroy()
            firstchk = True
            display_cases()
            display_window2()
        else:
            global tags, samplein1, samplein2, samplein3, sampleout1, sampleout2, sampleout3
            global in1, in2, in3, out1, out2, out3, input_window
            tags = [f'<tag><text>{i}</text></tag>' for i in
                    taginp.get().replace(" ", "").split(",")]
            in1 = samplein1.get("1.0", "end-1c")
            in2 = samplein2.get("1.0", "end-1c")
            in3 = samplein3.get("1.0", "end-1c")
            out1 = sampleout1.get("1.0", "end-1c")
            out2 = sampleout2.get("1.0", "end-1c")
            out3 = sampleout3.get("1.0", "end-1c")
            description_make()
            input_window.grab_release()
            input_window.destroy()
            app.configure(state='normal')
            firstchk = False

    ok_button = ctk.CTkButton(input_window, text="OK", width=750, height=40, command=on_ok,
                              font=('sans', 15, 'bold'))
    ok_button.grid(pady=10, padx=10, row=4, column=1)
    app.wait_window(input_window)


# Define the functions that will be used in the GUI
def test_case():
    global num_test_cases_entry
    try:
        return int(num_test_cases_entry.get())
    except:
        show_error('ENTER A NUMBER IN TESTCASES!')


def set_language():
    global language_value, language_selection
    tmp = language_selection.get()
    if tmp == 'C':
        language_value = 1
    elif tmp == 'C++':
        language_value = 2
    elif tmp == 'Java':
        language_value = 3
    elif tmp == 'Python':
        language_value = 4
    elif tmp == 'C#':
        language_value = 5
    elif tmp == 'Go':
        language_value = 6
    else:
        show_error('INVALID LANGUAGE CHOICE. HOW IS THAT EVEN POSSIBLE!')
        # pltfrm_choice = int(input(
        #    "Enter your choice of platform\n1. HackerRank\n2. HackerEarth\n3. CodeChef\n"))


def set_platform():
    global platform_value, platform_selection
    try:
        tmp = platform_selection.get()
        if tmp == 'HackerRank':
            platform_value = 1
        elif tmp == 'HackerEarth':
            platform_value = 2
        elif tmp == 'CodeChef':
            platform_value = 3
        elif tmp == 'VPL':
            platform_value = 4
        elif tmp == 'CodeRunner':
            platform_value = 5
        else:
            show_error('WEIRD. STUCK AT PLATFORM CHOICE!')
    except:
        show_error('INVALID PLATFORM? HOW')

def fun():
    global chk, max_time, inputs, outputs, generate_button
    generate_button.configure(state = 'disabled')

    global program_name, platform_value
    chk = False
    print('reaches 5')
    try:
        if platform_value == 5:
            get_program_details()

        print('reaches 3')
        progressbar_setup()
        main()
        progressbar_destroy()
    except CompilationError:
        return
    except RuntimeError:
        return
    except Exception:
        show_error("Invalid options or code!")
        return
    finally:
        generate_button.configure(state='normal')

    show_error(f"Success! File is saved at {os.getcwd()}")


def genbun():
    global inputs, outputs, program_name, max_time, times, code, chk
    global program_type, tags, description, constraints, in1, out1, in2, out2, in3, out3

    if python_code_entry.get("1.0", "end-1c").strip() == '' or logic_code_entry.get("1.0", "end-1c").strip() == '' :
        show_error('Invalid Info! Enter the details properly!')
        return
    try:
        exec(python_code_entry.get("1.0", "end-1c").strip())
    except:
        show_error('Invalid Python Code!')
        return

    try :
        test_case()
        logic_code()
        set_platform()
        set_language()
    except Exception:
        show_error('Invalid Inputs!!!!')
        return

    try:
        int(num_test_cases_entry.get())
    except:
        show_error('Improper Number for Test Cases!')
        return

    try:
        chk = True
        testlogic()
    except:
        chk = False
        show_error('Invalid Logic!')
        return
    chk = False


    fun()
    inputs.clear()
    outputs.clear()
    times.clear()
    code = ""
    program_name = ""
    max_time = 0
    program_name = str()
    program_type = int()
    tags = list()
    description = str()
    constraints = str()
    in1, out1, in2, out2, in3, out3 = [""] * 6


def logic_code():
    try:
        global code
        code = logic_code_entry.get("1.0", "end-1c").strip()

        if code == '':
            show_error('INVALID LOGIC FILE!!!!')
            return

        language = language_selection.get()
        file_extension = {
            "Python": ".py",
            "C": ".c",
            "C++": ".cpp",
            "Java": ".java",
            "C#": ".cs",
            "Go": ".go"
        }.get(language)

        file_name = f"logic{file_extension}"
        with open(file_name, 'w') as f:
            f.write(code)
    except:
        pass
        # show_error('INVALID LOGIC FILE!')


def printoo():
    try:
        s = python_code_entry.get("1.0", "end-1c").strip()
        if s == '':
            show_error('INVALID Python Code!')
            return
        exec(s)
    except Exception:
        show_error('INVALID Python Code!')
        return


# Output Preview Display
ctk.CTkLabel(app, text_color='orange', text="Output Preview", font=("sans", 25, "bold"),
             anchor="center").grid(row=0, column=2, padx=20, pady=10)
preview_output = ctk.CTkTextbox(app, width=300, height=200, font=("sans", 20, "bold"), wrap='none',
                                state='disabled')
preview_output.grid(row=1, column=2, padx=20, pady=10, sticky="nsew")


def testlogic():
    global chk, max_time, inputs, outputs, times

    try:
        int(num_test_cases_entry.get())
    except:
        show_error('Improper Number for Test Cases!')
        return

    def clean():
        global chk, max_time
        chk = False
        inputs.clear()
        outputs.clear()
        times.clear()
        max_time = 0
        preview_output.configure(state='disabled')
        generate_button.configure(state='normal')
    if python_code_entry.get("1.0", "end-1c").strip() == '' or logic_code_entry.get("1.0",
                                                                                    "end-1c").strip() == '':
        clean()
        raise Exception("STOP")

    try:
        exec(python_code_entry.get("1.0", "end-1c").strip())
    except:
        clean()
        raise Exception("STOP 2")
    test_case()
    logic_code()
    set_platform()
    set_language()
    preview_output.configure(state='normal')
    chk = True
    try:
        main()
    except CompilationError:
        clean()
        raise Exception("Stop 3")
    except Exception:
        clean()
        raise Exception("Stop 4")
    preview_output.configure(state='disabled')


# Preview button
def preview_cases():
    global chk, max_time, inputs, outputs, times

    if python_code_entry.get("1.0", "end-1c").strip() == '' or logic_code_entry.get("1.0", "end-1c").strip() == '':
        show_error('Invalid Code! Enter the details properly!')
        return

    try:
        exec(python_code_entry.get("1.0", "end-1c").strip())
    except:
        show_error('Invalid Python Code!')
        return

    try:
        int(num_test_cases_entry.get())
    except:
        show_error('Improper Number for Test Cases!')
        return

    try:
        chk = True
        testlogic()
    except:
        chk = False
        show_error('Invalid Logic Code!')
        return

    test_case()
    logic_code()
    set_platform()
    set_language()


    chk = False

    preview_output.configure(state='normal')
    chk = True
    try:
        main()
    except CompilationError:
        return
    except Exception:
        show_error('An issue generating testcases!')
        return
    preview_output.delete("1.0", "end")
    for i in range(2):
        preview_output.insert('insert',
                              f'INPUT:\n{str(inputs[i])}\nOUTPUT:\n{str(outputs[i])}\nTime Taken:\n{times[i]:.4f}\n' + ('-' * 250) + '\n')
    preview_output.insert('insert', f"Max Time : {max_time:.4f}\n")

    preview_output.configure(state='disabled')
    chk = False
    inputs.clear()
    outputs.clear()
    times.clear()
    max_time = 0


preview_button = ctk.CTkButton(app, width=80, height=90, font=("sans", 30, "bold"),
                               text="Preview", text_color='black',
                               command=preview_cases,
                               image=ctk.CTkImage(dark_image=Image.open('_internal\\icons\\3671905_show_view_icon(1).png').resize((500, 50))),
                               compound='left')
preview_button.grid(row=2, column=2, padx=10, pady=(10, 0), sticky='nsew')

# Generate Button
generate_button = ctk.CTkButton(app, height=90, width=80, fg_color='green',
                                hover_color='darkgreen',
                                font=("sans", 30, "bold"), text="Generate", text_color='black',
                                command=genbun,
                                image= ctk.CTkImage(dark_image=Image.open('_internal\\icons\\8542038_download_data_icon.png').resize((500, 50))),
                                compound='left')
generate_button.grid(row=3, column=2, padx=10, pady=(20, 20), rowspan=2, sticky='nsew' )


info_button = ctk.CTkButton(app, height=5, width=300, fg_color='darkcyan',
                                hover_color='teal', bg_color='grey',
                                font=("sans", 16, "bold"), text="info", text_color='black',
                                image= ctk.CTkImage(dark_image=Image.open('_internal\\icons\\352432_info_icon(1).png').resize((500, 50))),
                                compound='left', command=lambda: webbrowser.open("https://www.github.com/gabyah92/TestCasesGeneratorGUI")   )
info_button.grid(row=5, column=0, padx=10, pady=5, sticky='nsew' )

github_button = ctk.CTkButton(app, height=5, width=300, fg_color='darkcyan',
                                hover_color='teal', bg_color='grey',
                                font=("sans", 16, "bold"), text="github", text_color='black',
                                image= ctk.CTkImage(dark_image=Image.open('_internal\\icons\\8666686_github_icon.png').resize((500, 50))),
                                compound='left', command=lambda: webbrowser.open("https://www.github.com/gabyah92")  )
github_button.grid(row=5, column=1, padx=10, pady=5, sticky='nsew' )

instagram_button = ctk.CTkButton(app, height=5, width=300, fg_color='darkcyan',
                                hover_color='teal', bg_color='grey',
                                font=("sans", 16, "bold"), text="gabyah92", text_color='black',
                                image= ctk.CTkImage(dark_image=Image.open('_internal\\icons\\9024634_instagram_logo_light_icon.png').resize((500, 50))),
                                compound='left', command=lambda: webbrowser.open("https://www.instagram.com/gabyah92")  )
instagram_button.grid(row=5, column=2, padx=10, pady=5, sticky='nsew' )


def progressbar_setup():
    global app, progress_bar, progress_root, progress_inputs, progress_outputs, progress_label
    progress_root = ctk.CTk()
    progress_root.iconbitmap("_internal\\icons\\logo.ico")
    progress_root.protocol("WM_DELETE_WINDOW", lambda: sys.exit(0))
    progress_label = ctk.CTkLabel(progress_root, text="Generating TestCases",
                                  font=("sans", 20, "bold"))
    progress_inputs = ctk.CTkLabel(progress_root, text="Generating Inputs...",
                                   font=("sans", 20, "bold"))
    progress_outputs = ctk.CTkLabel(progress_root, text="Generating Outputs...",
                                    font=("sans", 20, "bold"))
    progress_bar = ctk.CTkProgressBar(progress_root, width=250, progress_color='orange',
                                      fg_color='grey', height=20)

    height = 300
    width = 300
    screenwidth = app.winfo_screenwidth()
    screenheight = app.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (
        width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    progress_root.geometry(alignstr)
    progress_root.resizable(width=False, height=False)
    progress_root.after(250, progress_root.iconbitmap('_internal\\icons\\logo.ico'))
    progress_root.title("Progress")
    progress_root.grid_rowconfigure(0, weight=1)
    progress_root.grid_rowconfigure(1, weight=1)
    progress_root.grid_rowconfigure(2, weight=1)
    progress_root.grid_columnconfigure(0, weight=1)
    progress_root.grid_columnconfigure(1, weight=1)
    progress_root.grid_columnconfigure(2, weight=1)
    progress_label.pack(pady=20, padx=20)
    progress_inputs.configure(text_color='red')
    progress_inputs.pack(pady=20, padx=10)
    progress_outputs.configure(text_color='red')
    progress_outputs.pack(pady=20, padx=10)
    progress_bar.pack(pady=20)
    progress_root.grab_set()
    progress_root.update()
    progress_bar.start()
    progress_bar.set(0)

def progressbar_destroy():
    global progress_bar, progress_root
    progress_root.grab_release()
    progress_bar.stop()
    progress_bar.destroy()
    progress_root.destroy()




__all__ = ['IN_SOURCE', 'OUT_SOURCE', 'POWER', 'RINT', 'TC_SOURCE', 'generate',
           'compile_them', 'zip_codechef', 'zip_hackerrank', 'zip_hackerearth', 'zip_them',
           'check_empty', 'make_dirs', 'Error', 'EmptyFileException', 'CompilationError',
           'RunError', 'ValueOutsideRange', 'make_lf_ending']


class Error(Exception):
    """Base class for other exceptions."""
    pass


class EmptyFileException(Error):
    """Raised when output file is empty"""
    pass


class CompilationError(Error):
    """Raised when logic program is not compiled properly"""
    pass


class RunError(Error):
    """Raised when logic program encounters runtime error"""
    pass


class ValueOutsideRange(Error):
    """Raised when value entered is outside range"""
    pass


IN_SOURCE = resource_path2('input')
OUT_SOURCE = resource_path2('output')
TC_SOURCE = resource_path2('test-cases')
TC_ZIP = TC_SOURCE + '.zip'
POWER = math.pow
RINT = random.randint
WINDOWS_LINE_ENDING = b'\r\n'
UNIX_LINE_ENDING = b'\n'


def make_dirs():
    """Deletes old directories and creates new ones."""

    shutil.rmtree(IN_SOURCE, ignore_errors=True)
    shutil.rmtree(OUT_SOURCE, ignore_errors=True)
    shutil.rmtree(TC_SOURCE, ignore_errors=True)
    try:
        os.remove(TC_ZIP)
    except OSError:
        pass

    os.mkdir(IN_SOURCE)
    os.mkdir(OUT_SOURCE)


def check_empty(file):
    """Raises exception if file is empty."""

    if os.stat(file).st_size == 0:
        show_error('Empty output file!')
        raise EmptyFileException('Empty output file!')


def make_lf_ending(file):
    """Converts all crlf line endings to lf"""
    with open(file, 'rb') as in_file:
        content = in_file.read()
    content = content.replace(WINDOWS_LINE_ENDING, UNIX_LINE_ENDING)
    with open(file, 'wb') as out_file:
        out_file.write(content)


def compile_them(lang_choice):
    """
    Compiles the code.
    Raises error if there's some compilation error.

    Argument:
    lang_choice -- The choice of language which is chosen by the user
    """

    # Don't run compile for Python
    if lang_choice == 3:
        return

    compiled = subprocess.Popen(LANGS[lang_choice]['compile'],
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                universal_newlines=True, shell=True)
    stdout, stderr = compiled.communicate()
    if stderr:
        # show_error(f'Incorrect Language for logic code!\nCouldn\'t Compile!')
        raise CompilationError("Incorrect Language")


def generate(lang_choice, i):
    """
    Passes input through the compiled code (Except for Python) and generates
    output files.
    Raises error if there's a problem while running.

    Argument:
    lang_choice -- The choice of language which is chosen by the user
    i           -- 'i'th testcase for which output is to be generated
    """

    with open(os.path.join(IN_SOURCE, f'input{i:02d}.txt'), 'r+') as in_file:
        with open(os.path.join(OUT_SOURCE, f'output{i:02d}.txt'), 'w+') as out_file:
            generated = subprocess.Popen(LANGS[lang_choice]['command'],
                                         stdin=in_file,
                                         stdout=out_file,
                                         stderr=subprocess.PIPE,
                                         universal_newlines=True,shell = True)

    stdout, stderr = generated.communicate()
    if stderr:
        show_error(f'Runtime error!\n{stderr}')
        raise RunError(f'Runtime error!\n{stderr}')


def zip_hackerrank():
    """
    Zips files into 'test-cases.zip'.
    Input files are named as input<number>.txt and are placed inside
    'input' directory in zip.
    Output files are named as output<number>.txt and are placed inside
    'output' directory in zip.
    """

    with zipfile.ZipFile(TC_ZIP, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for in_file in os.listdir(IN_SOURCE):
            zip_file.write(os.path.join(IN_SOURCE, in_file), \
                           os.path.join('input', in_file))
        for out_file in os.listdir(OUT_SOURCE):
            zip_file.write(os.path.join(OUT_SOURCE, out_file), \
                           os.path.join('output', out_file))
    print(f"Test cases saved in {TC_ZIP}")


def zip_hackerearth():
    """
    Zips files into 'test-cases.zip'.
    Input files are named as in<number>.txt and are placed inside the zip.
    Output files are named as out<number>.txt and are placed inside the zip.
    """

    with zipfile.ZipFile(TC_ZIP, 'w', \
                         zipfile.ZIP_DEFLATED) as zip_file:
        for in_file in os.listdir(IN_SOURCE):
            zip_file.write(os.path.join(IN_SOURCE, in_file), \
                           in_file.replace('put', ''))
        for out_file in os.listdir(OUT_SOURCE):
            zip_file.write(os.path.join(OUT_SOURCE, out_file), \
                           out_file.replace('put', ''))
    print(f"Test cases saved in {TC_ZIP}")


def zip_codechef():
    """
    Places files inside 'test-cases' directory.
    Input files are named as input<number>.txt and are placed inside the directory.
    Output files are named as output<number>.txt and are placed inside the directory.
    """

    if not os.path.exists(TC_SOURCE):
        os.mkdir(TC_SOURCE)
    for in_file in os.listdir(IN_SOURCE):
        shutil.copy(os.path.join(IN_SOURCE, in_file), TC_SOURCE)
    for out_file in os.listdir(OUT_SOURCE):
        shutil.copy(os.path.join(OUT_SOURCE, out_file), TC_SOURCE)
    print(f"Test cases saved in {TC_SOURCE} directory")


def zip_them(test_files, lang_choice, pltfrm_choice):
    """
    Calls generate function for each test case, checks for empty output files and
    then calls the zipping function for the platform chosen by the user.

    Arguments:
    test_files    -- The number of test case files to be generated
    lang_choice   -- The choice of language which is chosen by the user
    pltfrm_choice -- The choice of platform which is chosen by the user
    """
    global platform_value, max_time, progress_bar, progress_inputs, progress_outputs, times
    platforms = [zip_hackerrank, zip_hackerearth, zip_codechef]
    if not chk:
        progress_inputs.configure(text_color='green', text='Generating Inputs '+u'\u2713')
    for i in range(0, test_files + 1):
        global max_time, progress_bar, times
        print(f'Generating output: {i}')
        if not chk:
            progress_bar.set(0.5 + (i + 1) * 0.5 / test_files)
            progress_bar.update_idletasks()
        exe_command = f'generate({lang_choice}, {i})'
        try:
            exe_time = timeit.timeit(exe_command, globals=globals(), number=1)
        except RunError as run_error:
            show_error('RunTimeError! Invalid Inputs!!')
            sys.exit(1)
        except FileNotFoundError as no_file:
            show_error('FileNotFound! Invalid Inputs!')
            sys.exit(1)

        print(f'Time taken to execute this TC {exe_time:02f} seconds')
        times.append(exe_time)
        max_time = max(max_time, exe_time)
        # print(OUT_SOURCE)
        out_file = os.path.join(OUT_SOURCE, f'output{i:02d}.txt')
        make_lf_ending(out_file)
        outputs.append(open(os.path.join(OUT_SOURCE, f'output{i:02d}.txt'), 'r').read())

        try:
            check_empty(out_file)
        except EmptyFileException as empty_file:
            show_error('Output Files Are Empty!!')
            return
            #print(empty_file, file=sys.stderr)
    if not chk:
        global progress_outputs, description, code, language_value, tags, in1, in2, in3, out1, out2, out3
        if platform_value < 4:
            print('Zipping ... ')
            zip_choice = platforms[pltfrm_choice]
            zip_choice()
        elif platform_value == 4:
            kr = open('_internal\\generated\\vpl_evaluate.cases', 'w')
            strr = ''
            for i in range(len(inputs)):
                strr += f'case = {i + 1}' + "\n"
                strr += f'input = {str(inputs[i])}'
                strr += f'output = {str(outputs[i])}' + "\n"

            kr.write(strr)
        elif platform_value == 5:
            kr = open(f'_internal\\generated\\{program_name}.xml', 'w', encoding='utf-8')
            strr = '''<?xml version="1.0" encoding="UTF-8"?>
    <quiz>
    <!-- question: 427  -->
      <question type="coderunner">
        <name>
          <text>'''
            strr += program_name
            strr += f'''</text>
        </name>
        <questiontext format="html"><text><![CDATA[{description}]]></text></questiontext>
        <generalfeedback format="html">
          <text></text>
        </generalfeedback>
        <defaultgrade>20</defaultgrade>
        <penalty>0</penalty>
        <hidden>0</hidden>'''
            strr+=f'''<idnumber>{datetime.now().strftime("%Y%m%d%H%M%S")}</idnumber><coderunnertype>'''

            if program_type == 1 or language_value > 4:
                strr+='''multilanguage'''
            else:
                tmp = language_value
                if tmp == 1:
                    strr += 'c_program'
                elif tmp == 2:
                    strr += 'cpp_program'
                elif tmp == 3:
                    strr += 'java_program'
                elif tmp == 4:
                    strr += 'python3'
            strr+='''</coderunnertype><prototypetype>0</prototypetype>
        <allornothing>0</allornothing>
        <penaltyregime>10, 20, ...</penaltyregime>
        <precheck>2</precheck>
        <hidecheck>0</hidecheck>
        <showsource>0</showsource>
        <answerboxlines>18</answerboxlines>
        <answerboxcolumns>100</answerboxcolumns>
        <answerpreload> </answerpreload>
        <globalextra></globalextra>
        <useace></useace>
        <resultcolumns></resultcolumns>
        <template></template>
        <iscombinatortemplate></iscombinatortemplate>
        <allowmultiplestdins></allowmultiplestdins>'''
            if program_type == 0:
                strr += f"<answer><![CDATA[{code}]]></answer>"
            else :
                strr += '<answer></answer>'
            strr += ''' 
        <validateonsave>1</validateonsave>
        <testsplitterre></testsplitterre>
        <language></language>
        <acelang></acelang>
        <sandbox></sandbox>
        <grader></grader>
        <cputimelimitsecs>''' + str(math.ceil(max_time) + 3) + '''</cputimelimitsecs>
        <memlimitmb></memlimitmb>
        <sandboxparams></sandboxparams>
        <templateparams></templateparams>
        <hoisttemplateparams>0</hoisttemplateparams>
        <extractcodefromjson>0</extractcodefromjson>
        <templateparamslang>None</templateparamslang>
        <templateparamsevalpertry>0</templateparamsevalpertry>
        <templateparamsevald>{}</templateparamsevald>
        <twigall>0</twigall>
        <uiplugin></uiplugin>
        <uiparameters><![CDATA[{
        "auto_switch_light_dark": false,
        "font_size": "15px",
        "import_from_scratchpad": true,
        "live_autocompletion": true,
        "theme": "tomorrow_night"
    }]]></uiparameters>
        <attachments>0</attachments>
        <attachmentsrequired>0</attachmentsrequired>
        <maxfilesize>10240</maxfilesize>
        <filenamesregex></filenamesregex>
        <filenamesexplain></filenamesexplain>
        <displayfeedback>1</displayfeedback>
        <giveupallowed>0</giveupallowed>
        <prototypeextra></prototypeextra>
        <testcases>'''
            sampleins = [in1, in2, in3]
            sampleouts = [out1, out2, out3]
            for i in range(1, 4):
                tmpppin, tmpppout = str(sampleins[i-1]), str(sampleouts[i-1])

                if tmpppin.strip() != '' or tmpppout.strip() != '':
                    strr += f'''<testcase testtype="0" useasexample="1" hiderestiffail="0" mark="1.0000000" >
                                <testcode>'''
                    strr += f'''<text>Sample Test Case {i}</text>'''
                    strr += f'''
                              </testcode>
                              <stdin>
                                        <text>{tmpppin}</text>
                              </stdin>
                              <expected>
                                        <text>{tmpppout}</text>
                              </expected>
                              <extra>
                                        <text></text>
                              </extra>
                              <display>
                                        <text>SHOW</text>
                              </display>
                            </testcase>
                                    '''
            for i in range(len(inputs)):
                strr += f'''
                <testcase testtype="0" useasexample="0" hiderestiffail="1" mark="1.0000000" >
          <testcode>
                    <text>Hidden Test Case {i + 1}</text>
          </testcode>
          <stdin>
                    <text>{str(inputs[i])}</text>
          </stdin>
          <expected>
                    <text>{str(outputs[i])}</text>
          </expected>
          <extra>
                    <text></text>
          </extra>
          <display>
                    <text>HIDE_IF_SUCCEED</text>
          </display>
        </testcase>
                '''

            strr += f'''</testcases>
        <tags>
          <tag><text>autoupload</text>
    </tag>{tags}
        </tags>
      </question>

    </quiz>'''
            kr.write(strr)
        progress_outputs.configure(text_color='green', text='Generating Outputs ' + u'\u2713')
        progress_outputs.update_idletasks()
        time.sleep(0.02)


def main():
    """
    Takes in the choice of language and platform from the user, creates input files as per the
    logic defined in the input area and calls in the compile_them and zip_them function.
    """
    global language_value
    global platform_value
    try:
        # lang_choice = int(input(
        #    "Enter your choice of language\n1. C\n2. C++\n3. Java\n4. Python\n5. C#\n6. Go\n"))
        lang_choice = language_value

        # pltfrm_choice = int(input(
        #    "Enter your choice of platform\n1. HackerRank\n2. HackerEarth\n3. CodeChef\n"))
        pltfrm_choice = platform_value
    except (SyntaxError, ValueError) as err:
        #print(err, file=sys.stderr)
        show_error("You didn't enter a number!")
        #print("You didn't enter a number!", file=sys.stderr)
        sys.exit(1)

    make_dirs()

    lang_choice -= 1
    pltfrm_choice -= 1
    test_files = test_case()  # number of test files, change it according to you.
    global chk, progress_bar
    if chk:
        test_files = 2
    for i in range(0, test_files + 1):
        print(f'Generating input: {i}')
        if not chk:
            progress_bar.set((i + 1) * 0.5 / test_files)
            progress_bar.update_idletasks()

        in_file = os.path.join(IN_SOURCE, f'input{i:02d}.txt')
        sys.stdout = open(in_file, 'w')

        # Input area will start here,
        # everything that you print out here will be taken as input in your logic file.

        # Input File Printing Starts
        # number of test cases in (1,10^5)
        printoo()

        # Input File Printing Ends
        sys.stdout = sys.__stdout__
        inputs.append(open(os.path.join(IN_SOURCE, f'input{i:02d}.txt'), 'r').read())
        make_lf_ending(in_file)
    compile_them(lang_choice)
    zip_them(test_files, lang_choice, pltfrm_choice)

    shutil.rmtree(IN_SOURCE)
    shutil.rmtree(OUT_SOURCE)


if __name__ == "__main__":
    try:
        main = threading.Thread(target=app.mainloop())
        main.start()
    except Exception:
        pass
    # main()
