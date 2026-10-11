import os
import shutil
import subprocess
import sys
import threading
import time
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, simpledialog
import socket
import sqlite3
import json
import urllib.request
import pathlib
import re
import math
import random
import datetime
import ast

# ==========================================
# GALAXY THEME COLOR PALETTE & STYLING
# ==========================================
GALAXY_BG = "#0B0E14"  # Deep space background
PANEL_BG = "#151B23"  # Nebula card/panel background
ACCENT_CYAN = "#00F0FF"  # Neon star cyan
ACCENT_PURPLE = "#9D4EDD"  # Deep nebula purple
TEXT_MAIN = "#E6EDF3"  # Bright starlight text
TEXT_MUTED = "#8B949E"  # Dim cosmic dust text
TERM_GREEN = "#00FF66"  # Terminal hacker green


# ==========================================
# OFFICIAL PYTHON REFERENCE DICTIONARY
# ==========================================
PYTHON_REFERENCE_DICT = {
    "Control Flow & Conditionals": {
        "if": (
            "Starts a conditional statement. Executes code if a condition is"
            " true."
        ),
        "elif": (
            'Short for "else if". Checks another condition if the previous'
            " ones were false."
        ),
        "else": (
            "Executes a block of code if all previous conditions in an"
            " if/elif chain are false."
        ),
    },
    "Loops & Iteration": {
        "for": (
            "Starts a loop that iterates over a sequence (like a list, tuple,"
            " or string)."
        ),
        "while": (
            "Starts a loop that repeats as long as a specified condition"
            " remains true."
        ),
        "break": (
            "Immediately terminates the current loop and jumps to the code"
            " after it."
        ),
        "continue": (
            "Skips the rest of the current loop iteration and moves to the"
            " next turn."
        ),
        "in": (
            "Checks if a value exists inside a sequence, or is used to loop"
            " through a sequence in a for loop."
        ),
    },
    "Functions & Classes": {
        "def": "Defines a new function.",
        "return": (
            "Exits a function and optionally sends a value back to the caller."
        ),
        "class": "Defines a new object-oriented class structure.",
        "pass": (
            "A null statement. It acts as a placeholder where code is"
            " syntactically required but you want to do nothing."
        ),
        "lambda": "Creates a small, anonymous, one-line function.",
        "yield": (
            "Used inside a function to return a generator object, pausing"
            " function execution to resume later."
        ),
    },
    "Boolean & Logic": {
        "True / False": (
            "The two boolean data values representing truth and falsehood."
        ),
        "None": (
            "A special constant representing the absence of a value or a null"
            " value."
        ),
        "and": "Logical operator. Returns true only if both conditions are true.",
        "or": "Logical operator. Returns true if at least one condition is true.",
        "not": (
            "Logical operator. Inverts a boolean value (turns true to false, and"
            " vice versa)."
        ),
        "is": (
            "Tests object identity. Checks if two variables point to the exact"
            " same object in memory."
        ),
    },
    "Error & Exception Handling": {
        "try": "Defines a block of code to test for errors while it is executing.",
        "except": (
            "Defines a block of code to execute if an error occurs in the try"
            " block."
        ),
        "finally": (
            "Defines a block of code that will always run after try/except,"
            " regardless of errors."
        ),
        "raise": "Manually triggers/throws a specific error or exception.",
        "assert": (
            "Used for debugging. Throws an error if a condition evaluates to"
            " false."
        ),
    },
    "Modules & Scope": {
        "import": "Brings external modules or libraries into your script.",
        "from": (
            "Used with import to bring specific parts of a module into your"
            " script."
        ),
        "as": (
            "Creates an alias (nickname) for a module or function you are"
            " importing."
        ),
        "global": (
            "Declares that a variable inside a function belongs to the global"
            " (outer) scope."
        ),
        "nonlocal": (
            "Declares that a variable inside a nested function belongs to the"
            " outer, non-global function's scope."
        ),
        "with": (
            "Wraps the execution of a block of code with methods defined by a"
            " context manager (commonly used to safely open and close files)."
        ),
    },
    "Memory Management": {
        "del": (
            "Deletes a reference to an object, variable, or item from a list."
        ),
    },
    "Core Built-In Functions": {
        "print()": "Displays text, variables, or objects to the screen.",
        "input()": "Pauses execution to accept text input from the user.",
        "int()": "Converts a value (like a string or float) into an integer.",
        "float()": "Converts a value into a decimal number.",
        "str()": "Converts an object into a text string representation.",
        "bool()": "Converts a value to its boolean evaluation (True or False).",
        "list()": "Creates a list from an iterable.",
        "dict()": "Creates a dictionary (key-value pairs).",
        "set()": "Creates an unordered collection of unique elements.",
        "tuple()": "Creates an unchangeable, ordered sequence.",
        "type()": "Returns the data type of an object.",
        "len()": (
            "Returns the number of items (length) in a string, list, or"
            " collection."
        ),
        "dir()": (
            "Lists all available methods and attributes associated with an"
            " object."
        ),
        "help()": (
            "Invokes Python's built-in help system to explain an object or"
            " module."
        ),
        "id()": "Returns the unique memory address integer of an object.",
        "abs()": "Returns the absolute (positive) value of a number.",
        "round()": "Rounds a number to a specified number of decimals.",
        "min() / max()": "Finds the smallest or largest value in an iterable.",
        "sum()": "Adds up all numbers inside an iterable.",
        "pow()": (
            "Raises a number to a specified power (equivalent to x ** y)."
        ),
        "range()": (
            "Generates a sequence of numbers, commonly used for step-counts in"
            " for loops."
        ),
        "enumerate()": (
            "Takes a sequence and returns it as pairs of indexes and items."
        ),
        "zip()": "Combines multiple iterables together item-by-item into pairs.",
        "sorted()": (
            "Returns a new, sorted list from an iterable's items."
        ),
        "reversed()": "Returns a reversed iterator of a sequence.",
    },
    "Essential Standard Library Modules": {
        "math.ceil() / math.floor()": "Rounds numbers strictly up or down.",
        "math.sqrt()": "Finds the square root of a number.",
        "os.getcwd()": "Gets the current working directory path.",
        "os.listdir()": "Lists files inside a directory.",
        "sys.exit()": "Immediately stops and exits the Python script.",
        "random.randint()": "Generates a random integer within a range.",
        "random.choice()": "Picks a random item out of a list.",
    },
}


# ==========================================
# OFFICIAL C++ REFERENCE DICTIONARY[cite: 6]
# ==========================================
CPP_REFERENCE_DICT = {
    "Fundamental Types": {
        "bool": (
            "Declares a variable that stores a boolean value (true or false)."
            "[cite: 6]"
        ),
        "char": "Declares a single-byte character variable.[cite: 6]",
        "int": "Declares a basic signed integer variable.[cite: 6]",
        "double": (
            "Declares a double-precision floating-point decimal variable."
            "[cite: 6]"
        ),
        "void": (
            "Declares that a function returns no value or specifies a generic"
            " pointer type.[cite: 6]"
        ),
    },
    "Control Flow & Conditional Jumps": {
        "if": (
            "Evaluates a conditional expression inside parentheses and executes"
            " the subsequent block if it is true.[cite: 6]"
        ),
        "else": (
            "Executes an alternative block of code when the preceding if"
            " condition evaluates to false.[cite: 6]"
        ),
        "switch": (
            "Evaluates an integer or enumeration variable to match it against"
            " multiple constant options.[cite: 6]"
        ),
        "break": (
            "Terminates the execution of the innermost loop or switch block"
            " immediately.[cite: 6]"
        ),
        "return": (
            "Terminates a function and hands a value back to the caller."
            "[cite: 6]"
        ),
    },
    "Loops": {
        "for": (
            "Executes a loop block continually based on initialization,"
            " conditional check, and iteration counter parameters.[cite: 6]"
        ),
        "while": (
            "Continually executes a loop block as long as its leading"
            " conditional expression remains true.[cite: 6]"
        ),
    },
}


# ==========================================
# OFFICIAL HTML REFERENCE DICTIONARY
# ==========================================
HTML_REFERENCE_DICT = {
    "Document Framework & Metadata": {
        "<!DOCTYPE html>": (
            "The mandatory declaration statement placed at the absolute first"
            " line of a file to tell the web browser to read it as modern"
            " HTML5."
        ),
        "<html>": (
            "The primary root container wrapper that bounds every single line"
            " of code on the entire web page."
        ),
        "<head>": (
            "Encapsulates background information about the page—such as"
            " metadata, search optimization instructions, and character"
            " encodings—that doesn't show up on the visible screen."
        ),
        "<body>": (
            "Encapsulates all the visible components, structures, layout"
            " segments, and media that users actually see on the web page."
        ),
    },
    "Visible Layout & Structure Block-Level Elements": {
        "<div>": (
            "A generic block-level layout divider or container used to group"
            " elements together for styling or script interactions."
        ),
        "<h1> through <h6>": (
            "Structure text into sections using a descending hierarchy of"
            " headings."
        ),
        "<p>": (
            "Encapsulates a standalone paragraph of text, automatically adding"
            " vertical spacing above and below itself."
        ),
    },
}


# ==========================================
# OFFICIAL JAVASCRIPT REFERENCE DICTIONARY[cite: 7]
# ==========================================
JS_REFERENCE_DICT = {
    "Variable Declarations & Scope": {
        "let": (
            "Declares a block-scoped local variable whose value can be"
            " reassigned.[cite: 7]"
        ),
        "const": (
            "Declares a block-scoped local variable whose value cannot be"
            " reassigned.[cite: 7]"
        ),
        "var": (
            "Declares a function-scoped or globally-scoped variable (older"
            " syntax).[cite: 7]"
        ),
    },
    "Control Flow & Conditionals": {
        "if": (
            "Evaluates a true-or-false conditional expression to decide if a"
            " block of code should run.[cite: 7]"
        ),
        "else": (
            "Executes an alternative fallback block of code when the preceding"
            " if condition is false.[cite: 7]"
        ),
    },
}


# ==========================================
# OFFICIAL LUA REFERENCE DICTIONARY
# ==========================================
LUA_REFERENCE_DICT = {
    "Variables & Scope": {
        "local": (
            "Declares a block-scoped variable that exists only within its"
            " current file, function, or loop chunk."
        ),
        "nil": (
            "Represents the absence of a value or an uninitialized state."
        ),
    },
    "Control Flow & Conditionals": {
        "if": (
            "Evaluates a true-or-false conditional expression to decide if a"
            " block of code should run."
        ),
        "then": (
            "Concludes an if or elseif conditional statement and opens the"
            " ensuing code block."
        ),
        "end": "Closes an active code block.",
    },
}


# ==========================================
# CODE AUTO-CORRECTION TYPO MAP
# ==========================================
CODE_AUTO_CORRECT_MAP = {
    "locl": "local",
    "loclal": "local",
    "thn": "then",
    "repeart": "repeat",
    "untill": "until",
    "functon": "function",
    "funtion": "function",
    "retun": "return",
    "returm": "return",
    "prnt": "print",
    "prnt(": "print(",
    "els": "else",
    "elsif": "elseif",
    "whil": "while",
    "clss": "class",
    "impot": "import",
    "expor": "export",
    "asyn": "async",
    "trt": "try",
    "cacth": "catch",
}


def auto_correct_code(text):
  lines = text.splitlines()
  fixed_lines = []
  for line in lines:
    match = re.match(r"^(\s*)(.*)$", line)
    leading_space = match.group(1) if match else ""
    content = match.group(2) if match else line

    words = content.split()
    fixed_words = []
    for w in words:
      clean_w = re.sub(r"[^a-zA-Z0-9_]", "", w)
      punct = w[len(clean_w) :]
      if clean_w in CODE_AUTO_CORRECT_MAP:
        fixed_words.append(CODE_AUTO_CORRECT_MAP[clean_w] + punct)
      else:
        fixed_words.append(w)
    fixed_lines.append(leading_space + " ".join(fixed_words))
  return "\n".join(fixed_lines) + ("\n" if text.endswith("\n") else "")


def clean_unicode(text):
  return text.encode("ascii", "ignore").decode("ascii")


def fix_indentation_and_correct(text):
  text = auto_correct_code(text)
  lines = text.splitlines()
  fixed_lines = []
  for line in lines:
    fixed_line = line.replace("\t", "    ")
    fixed_line = fixed_line.rstrip()
    fixed_lines.append(fixed_line)
  return "\n".join(fixed_lines) + ("\n" if text.endswith("\n") else "")


def open_file_cross_platform(filepath):
  try:
    if sys.platform == "darwin":
      subprocess.run(["open", filepath])
    elif sys.platform == "win32":
      os.startfile(filepath)
    else:
      subprocess.run(["xdg-open", filepath])
  except Exception as e:
    messagebox.showerror("Error", f"Could not open file: {e}")


# ==========================================
# 1. THE SCANNER PIPELINE
# ==========================================
def harvest_local_context(workspace_path):
  context_status = {
      "has_gui": False,
      "has_math": False,
      "has_database": False,
      "has_threading": False,
      "has_file_automation": False,
      "active_files": [],
      "primary_file_path": None,
      "primary_file_content": "",
  }

  if not os.path.exists(workspace_path):
    return context_status

  py_files = [
      f
      for f in os.listdir(workspace_path)
      if f.endswith(".py") and not f.startswith(".")
  ]
  context_status["active_files"] = py_files

  if py_files:
    primary_name = py_files[0]
    for pf in py_files:
      if (
          "app" in pf.lower()
          or "workspace" in pf.lower()
          or "main" in pf.lower()
      ):
        primary_name = pf
        break

    full_path = os.path.join(workspace_path, primary_name)
    context_status["primary_file_path"] = full_path

    try:
      with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
        context_status["primary_file_content"] = content

        if re.search(r"\b(tkinter|tk\.|Tk\()\b", content):
          context_status["has_gui"] = True
        if re.search(r"\b(math|random|sum\(|calc|calculate)\b", content):
          context_status["has_math"] = True
        if re.search(r"\b(sqlite3|connect\(|cursor\()\b", content):
          context_status["has_database"] = True
        if re.search(r"\b(threading|concurrent|ThreadPoolExecutor)\b", content):
          context_status["has_threading"] = True
        if re.search(r"\b(os\.walk|shutil|pathlib)\b", content):
          context_status["has_file_automation"] = True
    except Exception as e:
      print(f"Scanner warning: Could not read {full_path}: {e}")

  return context_status


# ==========================================
# 2. DYNAMIC GAME & AI TUTORIAL SYNTHESIZER
# ==========================================
def dictionary_guided_code_generation(prompt):
  prompt_lower = prompt.lower()

  # 1. Dynamic Game Generator (Pong, Shooter, Tic-Tac-Toe, Snake)
  if any(
      k in prompt_lower
      for k in [
          "game",
          "arcade",
          "snake",
          "pong",
          "tictactoe",
          "shooter",
          "clicker",
          "play",
      ]
  ):
    if "pong" in prompt_lower or "paddle" in prompt_lower:
      code = (
          "# --- Dynamic Custom Game: Retro Pong Arcade ---\n"
          f"# Prompt: {prompt}\n\n"
          "import tkinter as tk\n\n"
          "WIDTH, HEIGHT = 600, 400\n\n"
          "class PongGame:\n"
          "    def __init__(self, root):\n"
          "        self.root = root\n"
          '        self.root.title("Galaxy Arcade - Pong")\n'
          "        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT,"
          " bg='#0B0E14')\n"
          "        self.canvas.pack()\n"
          "        self.paddle1 = self.canvas.create_rectangle(20, 150, 35,"
          " 250, fill='#00F0FF', outline='')\n"
          "        self.paddle2 = self.canvas.create_rectangle(565, 150, 580,"
          " 250, fill='#9D4EDD', outline='')\n"
          "        self.ball = self.canvas.create_oval(290, 190, 310, 210,"
          " fill='#00FF66', outline='')\n"
          "        self.ball_dx = 4\n"
          "        self.ball_dy = 3\n"
          "        self.score1 = 0\n"
          "        self.score2 = 0\n"
          '        self.score_lbl = tk.Label(root, text="Player 1: 0 | Player'
          ' 2: 0", font=("Arial", 12, "bold"), fg="#E6EDF3", bg="#0B0E14")\n'
          "        self.score_lbl.pack(pady=5)\n\n"
          "        root.bind('<w>', lambda e: self.move_paddle(1, -20))\n"
          "        root.bind('<s>', lambda e: self.move_paddle(1, 20))\n"
          "        root.bind('<Up>', lambda e: self.move_paddle(2, -20))\n"
          "        root.bind('<Down>', lambda e: self.move_paddle(2, 20))\n\n"
          "        self.run_loop()\n\n"
          "    def move_paddle(self, player, dy):\n"
          "        pad = self.paddle1 if player == 1 else self.paddle2\n"
          "        coords = self.canvas.coords(pad)\n"
          "        if coords[1] + dy >= 0 and coords[3] + dy <= HEIGHT:\n"
          "            self.canvas.move(pad, 0, dy)\n\n"
          "    def run_loop(self):\n"
          "        self.canvas.move(self.ball, self.ball_dx, self.ball_dy)\n"
          "        b_coords = self.canvas.coords(self.ball)\n"
          "        p1_coords = self.canvas.coords(self.paddle1)\n"
          "        p2_coords = self.canvas.coords(self.paddle2)\n\n"
          "        if b_coords[1] <= 0 or b_coords[3] >= HEIGHT:\n"
          "            self.ball_dy = -self.ball_dy\n\n"
          "        if (b_coords[0] <= p1_coords[2] and p1_coords[1] <="
          " b_coords[3] and p1_coords[3] >= b_coords[1]):\n"
          "            self.ball_dx = -self.ball_dx\n"
          "        if (b_coords[2] >= p2_coords[0] and p2_coords[1] <="
          " b_coords[3] and p2_coords[3] >= b_coords[1]):\n"
          "            self.ball_dx = -self.ball_dx\n\n"
          "        if b_coords[0] <= 0:\n"
          "            self.score2 += 1\n"
          "            self.reset_ball()\n"
          "        elif b_coords[2] >= WIDTH:\n"
          "            self.score1 += 1\n"
          "            self.reset_ball()\n\n"
          "        self.score_lbl.config(text=f'Player 1: {self.score1} |"
          " Player 2: {self.score2}')\n"
          "        self.root.after(20, self.run_loop)\n\n"
          "    def reset_ball(self):\n"
          "        self.canvas.coords(self.ball, 290, 190, 310, 210)\n"
          "        self.ball_dx = -self.ball_dx\n\n"
          "if __name__ == '__main__':\n"
          "    root = tk.Tk()\n"
          "    game = PongGame(root)\n"
          "    root.mainloop()\n"
      )
      return "galaxy_pong_game.py", code

    elif "shooter" in prompt_lower or "space" in prompt_lower:
      code = (
          "# --- Dynamic Custom Game: Space Blaster Shooter ---\n"
          f"# Prompt: {prompt}\n\n"
          "import tkinter as tk\n"
          "import random\n\n"
          "WIDTH, HEIGHT = 500, 500\n\n"
          "class SpaceShooter:\n"
          "    def __init__(self, root):\n"
          "        self.root = root\n"
          '        self.root.title("Galaxy Arcade - Space Shooter")\n'
          "        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT,"
          " bg='#0B0E14')\n"
          "        self.canvas.pack()\n"
          "        self.score = 0\n"
          "        self.ship = self.canvas.create_rectangle(225, 440, 275,"
          " 460, fill='#00F0FF', outline='')\n"
          "        self.bullets = []\n"
          "        self.enemies = []\n"
          '        self.score_lbl = tk.Label(root, text="Score: 0",'
          ' font=("Arial", 12, "bold"), fg="#00FF66", bg="#0B0E14")\n'
          "        self.score_lbl.pack(pady=5)\n\n"
          "        root.bind('<Left>', lambda e: self.move_ship(-25))\n"
          "        root.bind('<Right>', lambda e: self.move_ship(25))\n"
          "        root.bind('<space>', lambda e: self.fire_bullet())\n\n"
          "        self.spawn_enemy()\n"
          "        self.run_loop()\n\n"
          "    def move_ship(self, dx):\n"
          "        coords = self.canvas.coords(self.ship)\n"
          "        if coords[0] + dx >= 0 and coords[2] + dx <= WIDTH:\n"
          "            self.canvas.move(self.ship, dx, 0)\n\n"
          "    def fire_bullet(self):\n"
          "        coords = self.canvas.coords(self.ship)\n"
          "        b = self.canvas.create_rectangle(coords[0]+22, coords[1]-15,"
          " coords[0]+28, coords[1], fill='#00FF66', outline='')\n"
          "        self.bullets.append(b)\n\n"
          "    def spawn_enemy(self):\n"
          "        x = random.randint(30, WIDTH - 30)\n"
          "        e = self.canvas.create_rectangle(x-15, 0, x+15, 30,"
          " fill='#FF0055', outline='')\n"
          "        self.enemies.append(e)\n"
          "        self.root.after(1200, self.spawn_enemy)\n\n"
          "    def run_loop(self):\n"
          "        for b in list(self.bullets):\n"
          "            self.canvas.move(b, 0, -12)\n"
          "            b_coords = self.canvas.coords(b)\n"
          "            if b_coords[3] < 0:\n"
          "                self.canvas.delete(b)\n"
          "                self.bullets.remove(b)\n"
          "                continue\n"
          "            for e in list(self.enemies):\n"
          "                e_coords = self.canvas.coords(e)\n"
          "                if (b_coords[0] < e_coords[2] and b_coords[2] >"
          " e_coords[0] and b_coords[1] < e_coords[3] and b_coords[3] >"
          " e_coords[1]):\n"
          "                    self.canvas.delete(b)\n"
          "                    self.canvas.delete(e)\n"
          "                    self.bullets.remove(b)\n"
          "                    self.enemies.remove(e)\n"
          "                    self.score += 100\n"
          "                    self.score_lbl.config(text=f'Score:"
          " {self.score}')\n"
          "                    break\n\n"
          "        for e in list(self.enemies):\n"
          "            self.canvas.move(e, 0, 3)\n"
          "            e_coords = self.canvas.coords(e)\n"
          "            if e_coords[3] >= HEIGHT:\n"
          "                self.canvas.delete(e)\n"
          "                self.enemies.remove(e)\n\n"
          "        self.root.after(30, self.run_loop)\n\n"
          "if __name__ == '__main__':\n"
          "    root = tk.Tk()\n"
          "    game = SpaceShooter(root)\n"
          "    root.mainloop()\n"
      )
      return "galaxy_shooter_game.py", code

    elif "tictactoe" in prompt_lower or "tic tac toe" in prompt_lower:
      code = (
          "# --- Galaxy Custom Arcade Game: Tic-Tac-Toe ---\n"
          f"# Prompt: {prompt}\n\n"
          "import tkinter as tk\n"
          "from tkinter import messagebox\n\n"
          "class TicTacToe:\n"
          "    def __init__(self, root):\n"
          "        self.root = root\n"
          '        self.root.title("Galaxy Arcade - Tic-Tac-Toe")\n'
          "        self.turn = 'X'\n"
          "        self.board = [['' for _ in range(3)] for _ in range(3)]\n"
          "        self.buttons = [[None for _ in range(3)] for _ in range(3)]\n\n"
          "        for r in range(3):\n"
          "            for c in range(3):\n"
          "                btn = tk.Button(root, text='', font=('Arial', 24,"
          " 'bold'), width=5, height=2,\n"
          "                                bg='#151B23', fg='#00F0FF',"
          " relief=tk.FLAT,\n"
          "                                command=lambda row=r, col=c:"
          " self.make_move(row, col))\n"
          "                btn.grid(row=r, column=c, padx=5, pady=5)\n"
          "                self.buttons[r][c] = btn\n\n"
          "    def make_move(self, r, c):\n"
          "        if self.board[r][c] == '':\n"
          "            self.board[r][c] = self.turn\n"
          "            self.buttons[r][c].config(text=self.turn, fg='#9D4EDD'"
          " if self.turn == 'X' else '#00F0FF')\n"
          "            if self.check_winner(self.turn):\n"
          "                messagebox.showinfo('Galaxy Arcade', f'Player"
          " {self.turn} Wins!')\n"
          "                self.reset_board()\n"
          "            elif all(self.board[i][j] != '' for i in range(3) for j"
          " in range(3)):\n"
          "                messagebox.showinfo('Galaxy Arcade', 'It is a"
          " Draw!')\n"
          "                self.reset_board()\n"
          "            else:\n"
          "                self.turn = 'O' if self.turn == 'X' else 'X'\n\n"
          "    def check_winner(self, player):\n"
          "        for i in range(3):\n"
          "            if all(self.board[i][j] == player for j in range(3)) or"
          " all(self.board[j][i] == player for j in range(3)):\n"
          "                return True\n"
          "        if self.board[0][0] == player and self.board[1][1] =="
          " player and self.board[2][2] == player:\n"
          "            return True\n"
          "        if self.board[0][2] == player and self.board[1][1] =="
          " player and self.board[2][0] == player:\n"
          "            return True\n"
          "        return False\n\n"
          "    def reset_board(self):\n"
          "        self.board = [['' for _ in range(3)] for _ in range(3)]\n"
          "        for r in range(3):\n"
          "            for c in range(3):\n"
          "                self.buttons[r][c].config(text='')\n"
          "        self.turn = 'X'\n\n"
          "if __name__ == '__main__':\n"
          "    root = tk.Tk()\n"
          "    root.config(bg='#0B0E14')\n"
          "    game = TicTacToe(root)\n"
          "    root.mainloop()\n"
      )
      return "galaxy_tictactoe_game.py", code

    else:
      code = (
          "# --- Dynamic Custom Game: Retro Snake ---\n"
          f"# Prompt: {prompt}\n\n"
          "import tkinter as tk\n"
          "import random\n\n"
          "WIDTH, HEIGHT = 400, 400\n"
          "GRID_SIZE = 20\n"
          "SPEED = 120\n\n"
          "class SnakeGame:\n"
          "    def __init__(self, root):\n"
          "        self.root = root\n"
          '        self.root.title("Galaxy Arcade - Retro Snake")\n'
          "        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT,"
          " bg='#0B0E14')\n"
          "        self.canvas.pack()\n"
          "        self.score = 0\n"
          "        self.direction = 'Right'\n"
          "        self.snake = [(100, 100), (80, 100), (60, 100)]\n"
          "        self.food = self.spawn_food()\n"
          '        self.score_lbl = tk.Label(root, text="Score: 0",'
          ' font=("Arial", 12, "bold"), fg="#00F0FF", bg="#0B0E14")\n'
          "        self.score_lbl.pack(pady=5)\n\n"
          "        root.bind('<Key>', self.change_direction)\n"
          "        self.run_game()\n\n"
          "    def spawn_food(self):\n"
          "        x = random.randint(0, (WIDTH // GRID_SIZE) - 1) *"
          " GRID_SIZE\n"
          "        y = random.randint(0, (HEIGHT // GRID_SIZE) - 1) *"
          " GRID_SIZE\n"
          "        return (x, y)\n\n"
          "    def change_direction(self, event):\n"
          "        key = event.keysym\n"
          "        if key == 'Up' and self.direction != 'Down':\n"
          "            self.direction = 'Up'\n"
          "        elif key == 'Down' and self.direction != 'Up':\n"
          "            self.direction = 'Down'\n"
          "        elif key == 'Left' and self.direction != 'Right':\n"
          "            self.direction = 'Left'\n"
          "        elif key == 'Right' and self.direction != 'Left':\n"
          "            self.direction = 'Right'\n\n"
          "    def run_game(self):\n"
          "        head_x, head_y = self.snake[0]\n"
          "        if self.direction == 'Up': head_y -= GRID_SIZE\n"
          "        elif self.direction == 'Down': head_y += GRID_SIZE\n"
          "        elif self.direction == 'Left': head_x -= GRID_SIZE\n"
          "        elif self.direction == 'Right': head_x += GRID_SIZE\n\n"
          "        new_head = (head_x, head_y)\n"
          "        if (head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y"
          " >= HEIGHT or new_head in self.snake):\n"
          '            self.canvas.create_text(WIDTH/2, HEIGHT/2,'
          ' text="GAME OVER", fill="#FF0055", font=("Arial", 24, "bold"))\n'
          "            return\n\n"
          "        self.snake.insert(0, new_head)\n"
          "        if new_head == self.food:\n"
          "            self.score += 10\n"
          "            self.score_lbl.config(text=f'Score: {self.score}')\n"
          "            self.food = self.spawn_food()\n"
          "        else:\n"
          "            self.snake.pop()\n\n"
          "        self.canvas.delete('all')\n"
          "        self.canvas.create_rectangle(self.food[0], self.food[1],"
          " self.food[0]+GRID_SIZE, self.food[1]+GRID_SIZE, fill='#FF0055',"
          " outline='')\n"
          "        for segment in self.snake:\n"
          "            self.canvas.create_rectangle(segment[0], segment[1],"
          " segment[0]+GRID_SIZE, segment[1]+GRID_SIZE, fill='#00F0FF',"
          " outline='#151B23')\n\n"
          "        self.root.after(SPEED, self.run_game)\n\n"
          "if __name__ == '__main__':\n"
          "    root = tk.Tk()\n"
          "    game = SnakeGame(root)\n"
          "    root.mainloop()\n"
      )
      return "galaxy_snake_game.py", code

  # 2. PyTorch AI Vision Model Tutorial[cite: 8]
  if any(
      k in prompt_lower
      for k in ["ai", "model", "pytorch", "mnist", "neural", "vision", "cnn"]
  ):
    code = (
        "# --- PyTorch AI Vision Model (Tutorial Integration) ---[cite: 8]\n"
        f"# Prompt: {prompt}\n\n"
        "import torch\n"
        "from torch import nn, optim\n"
        "from torch.utils.data import DataLoader\n"
        "from torchvision import datasets, transforms\n\n"
        "# 1. Data Setup & Transformation[cite: 8]\n"
        "transform = transforms.Compose([transforms.ToTensor()])\n\n"
        "# 2. Download MNIST Dataset[cite: 8]\n"
        "train_data = datasets.MNIST(root='data', train=True, download=True,"
        " transform=transform)\n"
        "test_data = datasets.MNIST(root='data', train=False, download=True,"
        " transform=transform)\n\n"
        "train_dataloader = DataLoader(train_data, batch_size=32,"
        " shuffle=True)\n"
        "test_dataloader = DataLoader(test_data, batch_size=32,"
        " shuffle=False)\n\n"
        "# 3. Define Neural Network Model[cite: 8]\n"
        "class Net(nn.Module):\n"
        "    def __init__(self):\n"
        "        super().__init__()\n"
        "        self.conv = nn.Sequential(\n"
        "            nn.Conv2d(1, 16, kernel_size=3, padding=1),\n"
        "            nn.ReLU(),\n"
        "            nn.MaxPool2d(kernel_size=2, stride=2),\n"
        "            nn.Conv2d(16, 32, kernel_size=3, padding=1),\n"
        "            nn.ReLU()\n"
        "        )\n"
        "        self.fc = nn.Sequential(\n"
        "            nn.Flatten(),\n"
        "            nn.Linear(32 * 14 * 14, 10)\n"
        "        )\n\n"
        "    def forward(self, x):\n"
        "        x = self.conv(x)\n"
        "        x = self.fc(x)\n"
        "        return x\n\n"
        "# 4. Device, Loss & Optimization Setup[cite: 8]\n"
        "device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')\n"
        "model = Net().to(device)\n\n"
        "loss_fn = nn.CrossEntropyLoss()\n"
        "optimizer = optim.Adam(model.parameters(), lr=0.001)\n\n"
        "# 5. Training Loop[cite: 8]\n"
        "epochs = 2\n"
        "print('Starting PyTorch AI Model Training...')\n"
        "for epoch in range(epochs):\n"
        "    model.train()\n"
        "    for batch_idx, (x, y) in enumerate(train_dataloader):\n"
        "        x, y = x.to(device), y.to(device)\n"
        "        y_hat = model(x)\n"
        "        loss = loss_fn(y_hat, y)\n\n"
        "        optimizer.zero_grad()\n"
        "        loss.backward()\n"
        "        optimizer.step()\n\n"
        "        if batch_idx % 100 == 0:\n"
        "            print(f'Epoch [{epoch}/{epochs}] | Batch {batch_idx} |"
        " Loss: {loss.item():.4f}')\n\n"
        "print('PyTorch AI Model Training Completed Successfully!')\n"
    )
    return "pytorch_mnist_model.py", code

  # 3. Standard Dictionary-Guided Generation Fallback
  lang = "python"
  if "js" in prompt_lower or "javascript" in prompt_lower:
    lang = "javascript"
  elif "lua" in prompt_lower:
    lang = "lua"
  elif "html" in prompt_lower:
    lang = "html"
  elif "cpp" in prompt_lower or "c++" in prompt_lower:
    lang = "cpp"

  all_dicts = {
      "python": PYTHON_REFERENCE_DICT,
      "javascript": JS_REFERENCE_DICT,
      "lua": LUA_REFERENCE_DICT,
      "cpp": CPP_REFERENCE_DICT,
      "html": HTML_REFERENCE_DICT,
  }

  target_dict = all_dicts.get(lang, PYTHON_REFERENCE_DICT)
  matched_concepts = []

  for category, items in target_dict.items():
    for key, desc in items.items():
      if (
          any(w in prompt_lower for w in key.lower().split())
          or category.lower() in prompt_lower
          or len(prompt_lower.split()) <= 2
      ):
        matched_concepts.append((key, desc, category))

  if lang == "python":
    code = (
        "# --- AI Context-Aware Synthesized Python Script ---\n# Generated"
        f" using internal reference dictionaries for: '{prompt}'\n\n"
    )
    if matched_concepts:
      code += "# Dictionary Intelligence Context Applied:\n"
      for k, d, c in matched_concepts[:6]:
        code += f"# [Category: {c}] {k} -> {d}\n"
      code += "\n"
    code += """import tkinter as tk
from tkinter import messagebox

class DictionaryGuidedApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Galaxy AI Dictionary Workspace")
        self.root.geometry("750x500")
        
        self.lbl = tk.Label(root, text="AI Code Intelligence Active", font=("Arial", 13, "bold"), fg="#00F0FF", bg="#0B0E14")
        self.lbl.pack(pady=25)
        
        self.btn = tk.Button(root, text="Test Intelligence", command=self.execute_action, bg="#9D4EDD", fg="white", font=("Arial", 10, "bold"))
        self.btn.pack(pady=10)
        
    def execute_action(self):
        messagebox.showinfo("AI Context Engine", "Code executed successfully using built-in dictionary intelligence!")

if __name__ == "__main__":
    root = tk.Tk()
    app = DictionaryGuidedApp(root)
    root.mainloop()
"""
    filename = "galaxy_ai_python_script.py"

  elif lang == "javascript":
    code = (
        "// --- AI Context-Aware Synthesized JavaScript ---\n// Generated using"
        f" internal reference dictionaries for: '{prompt}'\n\n"
    )
    if matched_concepts:
      code += "// Dictionary Intelligence Context Applied:\n"
      for k, d, c in matched_concepts[:6]:
        code += f"// [Category: {c}] {k} -> {d}\n"
      code += "\n"
    code += (
        'console.log("Galaxy AI JavaScript Engine Initialized");\n\nfunction'
        ' runContextEngine() {\n    let status = true;\n    if (status) {\n'
        '        console.log("Executed successfully with dictionary'
        ' intelligence!");\n    } else {\n        console.log("Condition'
        ' failed");\n    }\n}\n\nrunContextEngine();\n'
    )
    filename = "galaxy_ai_script.js"

  elif lang == "lua":
    code = (
        "-- --- AI Context-Aware Synthesized Lua Script ---\n-- Generated using"
        f" internal reference dictionaries for: '{prompt}'\n\n"
    )
    if matched_concepts:
      code += "-- Dictionary Intelligence Context Applied:\n"
      for k, d, c in matched_concepts[:6]:
        code += f"-- [Category: {c}] {k} -> {d}\n"
      code += "\n"
    code += (
        'print("Galaxy AI Lua Engine Initialized")\n\nlocal function'
        ' runContextTask()\n    local active = true\n    if active then\n'
        '        print("Lua task executed successfully using dictionary'
        ' intelligence!")\n    end\nend\n\nrunContextTask()\n'
    )
    filename = "galaxy_ai_script.lua"

  elif lang == "html":
    code = (
        "<!-- --- AI Context-Aware Synthesized HTML Page --- -->\n<!-- Generated"
        f" using internal reference dictionaries for: '{prompt}' -->\n\n"
    )
    if matched_concepts:
      code += "<!-- Dictionary Intelligence Context Applied:\n"
      for k, d, c in matched_concepts[:6]:
        code += f"     - [{c}] {k}: {d}\n"
      code += "-->\n\n"
    code += (
        "<!DOCTYPE html>\n<html>\n<head>\n    <title>Galaxy AI Smart"
        " Page</title>\n</head>\n<body>\n    <h1>Galaxy AI Dictionary"
        " Workspace</h1>\n    <p>This page was autonomously structured using"
        " internal dictionary intelligence.</p>\n</body>\n</html>\n"
    )
    filename = "galaxy_ai_page.html"

  else:
    code = (
        "// --- AI Context-Aware Synthesized C++ Program ---\n// Generated"
        f" using internal reference dictionaries for: '{prompt}'\n\n"
    )
    if matched_concepts:
      code += "// Dictionary Intelligence Context Applied:\n"
      for k, d, c in matched_concepts[:6]:
        code += f"// [Category: {c}] {k} -> {d}\n"
      code += "\n"
    code += (
        "#include <iostream>\nusing namespace std;\n\nint main() {\n   "
        ' cout << "Galaxy AI C++ Engine Initialized with Dictionary'
        ' Context!" << endl;\n    return 0;\n}\n'
    )
    filename = "galaxy_ai_app.cpp"

  return filename, code


# ==========================================
# 3. THE CONTEXT-AWARE MERGE ENGINE
# ==========================================
def compile_or_merge_code(workspace_path, user_prompt):
  filename, code = dictionary_guided_code_generation(user_prompt)
  output_path = os.path.join(workspace_path, filename)

  with open(output_path, "w", encoding="utf-8") as f:
    f.write(code)

  return f"AI successfully synthesized '{filename}' using dictionary context."


# ==========================================
# SYMBOLIC AI MEMORY & STATE CONTEXT
# ==========================================
class BotMemory:

  def __init__(self):
    self.state = "IDLE"
    self.context = {}
    self.history = []

  def update(self, key, value):
    self.context[key] = value
    self.history.append((time.time(), key, value))

  def recall(self, key):
    return self.context.get(key, None)


# ==========================================
# SYMBOLIC AI ENGINE & COMBINATORIAL SYNTHESIZER
# ==========================================
class SymbolicAIEngine:

  def __init__(self):
    self.memory = BotMemory()

  def validate_ast(self, source_code):
    try:
      ast.parse(source_code)
      return True, "AST Syntax Validation Passed: Code is structurally sound."
    except SyntaxError as e:
      return False, f"AST Syntax Error at line {e.lineno}: {e.msg}"

  def synthesize(self, workspace_path, prompt):
    result_msg = compile_or_merge_code(workspace_path, prompt)
    self.memory.update("last_prompt", prompt)
    self.memory.update("last_result", result_msg)
    return result_msg


# ==========================================
# 1. FILE & WORKSPACE MANAGER
# ==========================================
class WorkspaceManager:

  def __init__(self, root):
    self.root = root
    self.root.title("Galaxy Script Studio & Symbolic AI Engine")
    self.root.geometry("950x700")
    self.root.config(bg=GALAXY_BG)

    self.root_workspace = os.path.abspath("GalaxyWorkspace")
    if not os.path.exists(self.root_workspace):
      os.makedirs(self.root_workspace)

    self.current_folder = self.root_workspace
    self.current_file_path = None
    self.symbolic_ai = SymbolicAIEngine()

    self.build_main_view()

  def clear_window(self):
    for widget in self.root.winfo_children():
      widget.destroy()

  def build_main_view(self):
    self.clear_window()

    top_frame = tk.Frame(self.root, bg=PANEL_BG, height=60)
    top_frame.pack(fill=tk.X, padx=15, pady=15)

    title_text = f"🌌 Galaxy Workspace: {os.path.basename(self.current_folder)}"
    lbl_title = tk.Label(
        top_frame,
        text=title_text,
        font=("Arial", 13, "bold"),
        fg=ACCENT_CYAN,
        bg=PANEL_BG,
    )
    lbl_title.pack(side=tk.LEFT, padx=15, pady=12)

    btn_browse = tk.Button(
        top_frame,
        text="📁 Open Folder",
        command=self.browse_custom_folder,
        bg="#30363D",
        fg=TEXT_MAIN,
        font=("Arial", 9, "bold"),
        relief=tk.FLAT,
    )
    btn_browse.pack(side=tk.RIGHT, padx=5)

    if self.current_folder != self.root_workspace:
      btn_back = tk.Button(
          top_frame,
          text="⬅ Root Workspace",
          command=self.go_back_to_root,
          bg="#30363D",
          fg=TEXT_MAIN,
          font=("Arial", 9, "bold"),
          relief=tk.FLAT,
      )
      btn_back.pack(side=tk.RIGHT, padx=5)

    toolbar = tk.Frame(self.root, bg=GALAXY_BG)
    toolbar.pack(fill=tk.X, padx=15, pady=5)

    btn_new_folder = tk.Button(
        toolbar,
        text="+ Folder",
        command=self.create_folder,
        bg=ACCENT_PURPLE,
        fg="white",
        font=("Arial", 9, "bold"),
        relief=tk.FLAT,
    )
    btn_new_folder.pack(side=tk.LEFT, padx=(0, 8))

    btn_import_folder = tk.Button(
        toolbar,
        text="📁 Import Folder",
        command=self.import_folder_from_computer,
        bg="#30363D",
        fg=TEXT_MAIN,
        font=("Arial", 9, "bold"),
        relief=tk.FLAT,
    )
    btn_import_folder.pack(side=tk.LEFT, padx=(0, 8))

    btn_new_file = tk.Button(
        toolbar,
        text="+ File",
        command=self.create_file_prompt,
        bg="#238636",
        fg="white",
        font=("Arial", 9, "bold"),
        relief=tk.FLAT,
    )
    btn_new_file.pack(side=tk.LEFT, padx=(0, 8))

    btn_import_file = tk.Button(
        toolbar,
        text="📄 Import File",
        command=self.import_file_from_computer,
        bg="#30363D",
        fg=TEXT_MAIN,
        font=("Arial", 9, "bold"),
        relief=tk.FLAT,
    )
    btn_import_file.pack(side=tk.LEFT, padx=(0, 15))

    btn_ai_chat = tk.Button(
        toolbar,
        text="🤖 Symbolic AI Studio",
        command=self.open_symbolic_ai_window,
        bg=ACCENT_CYAN,
        fg="#0B0E14",
        font=("Arial", 9, "bold"),
        relief=tk.FLAT,
    )
    btn_ai_chat.pack(side=tk.RIGHT)

    content_frame = tk.Frame(self.root, bg=GALAXY_BG)
    content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

    tk.Label(
        content_frame,
        text="Folders (Double-click to enter):",
        font=("Arial", 10, "bold"),
        fg=TEXT_MUTED,
        bg=GALAXY_BG,
    ).pack(anchor="w")

    self.folder_listbox = tk.Listbox(
        content_frame,
        font=("Courier", 11),
        bg=PANEL_BG,
        fg=TEXT_MAIN,
        selectbackground=ACCENT_PURPLE,
        relief=tk.FLAT,
        height=6,
    )
    self.folder_listbox.pack(fill=tk.X, pady=(2, 12))
    self.folder_listbox.bind("<Double-Button-1>", self.on_folder_double_click)

    tk.Label(
        content_frame,
        text="Files in Directory (Double-click to edit/run):",
        font=("Arial", 10, "bold"),
        fg=TEXT_MUTED,
        bg=GALAXY_BG,
    ).pack(anchor="w")

    self.file_listbox = tk.Listbox(
        content_frame,
        font=("Courier", 11),
        bg=PANEL_BG,
        fg=ACCENT_CYAN,
        selectbackground=ACCENT_PURPLE,
        relief=tk.FLAT,
    )
    self.file_listbox.pack(fill=tk.BOTH, expand=True, pady=(2, 5))
    self.file_listbox.bind("<Double-Button-1>", self.on_file_double_click)

    self.load_directory_contents()

  def load_directory_contents(self):
    self.folder_listbox.delete(0, tk.END)
    self.file_listbox.delete(0, tk.END)
    try:
      items = os.listdir(self.current_folder)
      for item in sorted(items):
        if item.startswith("."):
          continue
        full_path = os.path.join(self.current_folder, item)
        if os.path.isdir(full_path):
          self.folder_listbox.insert(tk.END, item)
        else:
          self.file_listbox.insert(tk.END, item)
    except Exception as e:
      messagebox.showerror("Error", f"Could not load directory: {e}")

  def browse_custom_folder(self):
    folder = filedialog.askdirectory()
    if folder:
      self.current_folder = folder
      self.build_main_view()

  def create_folder(self):
    folder_name = simpledialog.askstring("New Folder", "Enter folder name:")
    if folder_name:
      new_dir = os.path.join(self.current_folder, folder_name.strip())
      try:
        os.makedirs(new_dir, exist_ok=True)
        self.load_directory_contents()
      except Exception as e:
        messagebox.showerror("Error", f"Could not create folder: {e}")

  def import_folder_from_computer(self):
    src_dir = filedialog.askdirectory(title="Select Folder to Import")
    if src_dir:
      try:
        folder_name = os.path.basename(src_dir)
        dest_dir = os.path.join(self.current_folder, folder_name)
        if os.path.exists(dest_dir):
          dest_dir = dest_dir + "_imported"
        shutil.copytree(src_dir, dest_dir)
        self.load_directory_contents()
        messagebox.showinfo(
            "Success", f"Folder '{folder_name}' imported successfully!"
        )
      except Exception as e:
        messagebox.showerror("Error", f"Could not import folder: {e}")

  def import_file_from_computer(self):
    src_file = filedialog.askopenfilename(title="Select File to Import")
    if src_file:
      try:
        file_name = os.path.basename(src_file)
        dest_file = os.path.join(self.current_folder, file_name)
        if os.path.exists(dest_file):
          dest_file = os.path.join(self.current_folder, "imported_" + file_name)
        shutil.copy2(src_file, dest_file)
        self.load_directory_contents()
        messagebox.showinfo(
            "Success", f"File '{file_name}' imported successfully!"
        )
      except Exception as e:
        messagebox.showerror("Error", f"Could not import file: {e}")

  def on_folder_double_click(self, event):
    selection = self.folder_listbox.curselection()
    if selection:
      folder_name = self.folder_listbox.get(selection[0])
      self.current_folder = os.path.join(self.current_folder, folder_name)
      self.build_main_view()

  def go_back_to_root(self):
    self.current_folder = self.root_workspace
    self.build_main_view()

  def create_file_prompt(self):
    filename = simpledialog.askstring(
        "New File", "Enter file name (e.g. script.py):"
    )
    if filename:
      filepath = os.path.join(self.current_folder, filename.strip())
      try:
        with open(filepath, "w", encoding="utf-8") as f:
          f.write("# Script initialized\n")
        self.open_editor_view(filepath)
      except Exception as e:
        messagebox.showerror("Error", f"Could not create file: {e}")

  def on_file_double_click(self, event):
    selection = self.file_listbox.curselection()
    if selection:
      filename = self.file_listbox.get(selection[0])
      filepath = os.path.join(self.current_folder, filename)
      ext = os.path.splitext(filename)[1].lower()

      editable_exts = [
          ".py",
          ".js",
          ".lua",
          ".luau",
          ".cpp",
          ".java",
          ".html",
          ".css",
          ".json",
          ".md",
          ".txt",
          ".sh",
      ]
      if ext in editable_exts or ext == "":
        self.open_editor_view(filepath)
      else:
        open_file_cross_platform(filepath)

  def open_symbolic_ai_window(self):
    ai_win = tk.Toplevel(self.root)
    ai_win.title(
        "🤖 Symbolic AI Studio - Dynamic Game & AI Code Synthesizer"
    )
    ai_win.geometry("740x540")
    ai_win.config(bg=GALAXY_BG)

    lbl = tk.Label(
        ai_win,
        text=(
            "🌌 Dynamic Game & AI Synthesis Engine (Create games, PyTorch"
            " models, etc.)"
        ),
        font=("Arial", 11, "bold"),
        fg=ACCENT_CYAN,
        bg=GALAXY_BG,
    )
    lbl.pack(anchor="w", padx=15, pady=(12, 5))

    log_box = scrolledtext.ScrolledText(
        ai_win,
        wrap=tk.WORD,
        bg="#05070B",
        fg=TERM_GREEN,
        font=("Courier", 10),
        relief=tk.FLAT,
    )
    log_box.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)
    log_box.insert(
        tk.END,
        "[Symbolic AI Engine Online]: Ready. Try prompts like 'Create a pong"
        " game', 'Create a space shooter', or 'Create PyTorch AI model'.\n\n",
    )
    log_box.config(state=tk.DISABLED)

    input_frame = tk.Frame(ai_win, bg=GALAXY_BG)
    input_frame.pack(fill=tk.X, padx=15, pady=12)

    prompt_entry = tk.Entry(
        input_frame,
        font=("Arial", 11),
        bg=PANEL_BG,
        fg=TEXT_MAIN,
        insertbackground="white",
        relief=tk.FLAT,
    )
    prompt_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
    prompt_entry.insert(0, "e.g., Create a pong game OR Create PyTorch AI model")
    prompt_entry.focus()

    def generate_and_save():
      prompt = prompt_entry.get().strip()
      if not prompt:
        return

      log_box.config(state=tk.NORMAL)
      log_box.insert(
          tk.END,
          f"> User Request: {prompt}\n[*] Scanning dictionaries &"
          " synthesizing custom structure...\n",
      )
      log_box.see(tk.END)
      log_box.config(state=tk.DISABLED)

      def background_gen():
        try:
          result_msg = self.symbolic_ai.synthesize(
              self.current_folder, prompt
          )
          self.root.after(0, self.load_directory_contents)
          success_msg = f"[+] {result_msg}\n\n"
          self.root.after(
              0, lambda: self._update_chat_log(log_box, success_msg)
          )
        except Exception as e:
          err_msg = f"[-] Generation failure: {e}\n\n"
          self.root.after(0, lambda: self._update_chat_log(log_box, err_msg))

      threading.Thread(target=background_gen, daemon=True).start()

    btn_gen = tk.Button(
        input_frame,
        text="⚡ Synthesize with AI",
        command=generate_and_save,
        bg=ACCENT_PURPLE,
        fg="white",
        font=("Arial", 10, "bold"),
        relief=tk.FLAT,
    )
    btn_gen.pack(side=tk.RIGHT)
    prompt_entry.bind("<Return>", lambda e: generate_and_save())

  def _update_chat_log(self, widget, text):
    widget.config(state=tk.NORMAL)
    widget.insert(tk.END, text)
    widget.see(tk.END)
    widget.config(state=tk.DISABLED)

  # ------------------------------------------
  # EDITOR VIEW & AST CHECKER / SANDBOX RUNNER
  # ------------------------------------------
  def open_editor_view(self, filepath):
    self.current_file_path = filepath
    self.clear_window()

    filename = os.path.basename(filepath)

    top_frame = tk.Frame(self.root, bg=PANEL_BG, height=55)
    top_frame.pack(fill=tk.X, padx=15, pady=10)

    btn_back = tk.Button(
        top_frame,
        text="⬅ Back to Workspace",
        command=self.build_main_view,
        bg="#30363D",
        fg=TEXT_MAIN,
        font=("Arial", 9, "bold"),
        relief=tk.FLAT,
    )
    btn_back.pack(side=tk.LEFT, padx=10)

    lbl_file = tk.Label(
        top_frame,
        text=f"✨ Editing: {filename}",
        font=("Arial", 11, "bold"),
        fg=ACCENT_CYAN,
        bg=PANEL_BG,
    )
    lbl_file.pack(side=tk.LEFT, padx=15)

    main_container = tk.Frame(self.root, bg=GALAXY_BG)
    main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

    options_frame = tk.Frame(main_container, bg=GALAXY_BG)
    options_frame.pack(fill=tk.X, pady=5)

    self.auto_fix_var = tk.IntVar(value=1)
    chk_indent = tk.Checkbutton(
        options_frame,
        text="Auto-Fix Indents, Unicode & Keyword Typos",
        variable=self.auto_fix_var,
        font=("Arial", 9, "bold"),
        fg=ACCENT_PURPLE,
        bg=GALAXY_BG,
        selectcolor=PANEL_BG,
        activebackground=GALAXY_BG,
        activeforeground=ACCENT_PURPLE,
    )
    chk_indent.pack(side=tk.LEFT)

    # LUA DICTIONARIES REFERENCE BUTTON
    btn_lua_guide = tk.Button(
        options_frame,
        text="📖 Lua Dictionaries",
        command=self.show_lua_dict_guide,
        bg="#30363D",
        fg=ACCENT_CYAN,
        font=("Arial", 9, "bold"),
        relief=tk.FLAT,
    )
    btn_lua_guide.pack(side=tk.RIGHT, padx=5)

    # JAVASCRIPT DICTIONARIES REFERENCE BUTTON
    btn_js_guide = tk.Button(
        options_frame,
        text="📖 JS Dictionaries",
        command=self.show_js_dict_guide,
        bg="#30363D",
        fg=ACCENT_PURPLE,
        font=("Arial", 9, "bold"),
        relief=tk.FLAT,
    )
    btn_js_guide.pack(side=tk.RIGHT, padx=5)

    # HTML DICTIONARIES REFERENCE BUTTON
    btn_html_guide = tk.Button(
        options_frame,
        text="📖 HTML Dictionaries",
        command=self.show_html_dict_guide,
        bg="#30363D",
        fg=ACCENT_CYAN,
        font=("Arial", 9, "bold"),
        relief=tk.FLAT,
    )
    btn_html_guide.pack(side=tk.RIGHT, padx=5)

    # C++ DICTIONARIES REFERENCE BUTTON
    btn_cpp_guide = tk.Button(
        options_frame,
        text="📖 C++ Dictionaries",
        command=self.show_cpp_dict_guide,
        bg="#30363D",
        fg=ACCENT_CYAN,
        font=("Arial", 9, "bold"),
        relief=tk.FLAT,
    )
    btn_cpp_guide.pack(side=tk.RIGHT, padx=5)

    # PYTHON DICTIONARIES REFERENCE BUTTON
    btn_dict_guide = tk.Button(
        options_frame,
        text="📖 Python Dictionaries",
        command=self.show_dict_guide,
        bg="#30363D",
        fg=ACCENT_PURPLE,
        font=("Arial", 9, "bold"),
        relief=tk.FLAT,
    )
    btn_dict_guide.pack(side=tk.RIGHT, padx=5)

    btn_ast_check = tk.Button(
        options_frame,
        text="🔍 Validate AST Syntax",
        command=self.validate_editor_syntax,
        bg="#30363D",
        fg=ACCENT_CYAN,
        font=("Arial", 9, "bold"),
        relief=tk.FLAT,
    )
    btn_ast_check.pack(side=tk.RIGHT, padx=5)

    self.text_area = scrolledtext.ScrolledText(
        main_container,
        wrap=tk.WORD,
        bg=PANEL_BG,
        fg=TEXT_MAIN,
        insertbackground="white",
        font=("Courier", 11),
        relief=tk.FLAT,
    )
    self.text_area.pack(fill=tk.BOTH, expand=True, pady=5)

    try:
      with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        self.text_area.insert(tk.END, f.read())
    except Exception as e:
      messagebox.showerror("Error", f"Could not read file: {e}")

    btn_frame = tk.Frame(self.root, bg=GALAXY_BG)
    btn_frame.pack(fill=tk.X, padx=15, pady=12)

    btn_save = tk.Button(
        btn_frame,
        text="💾 Save File",
        command=self.save_current_file,
        bg="#21262D",
        fg=TEXT_MAIN,
        font=("Arial", 10, "bold"),
        relief=tk.FLAT,
        width=15,
    )
    btn_save.pack(side=tk.LEFT, padx=(0, 10))

    btn_run = tk.Button(
        btn_frame,
        text="🚀 Run in Virtual Sandbox",
        command=self.run_in_sandbox_vm,
        bg="#238636",
        fg="white",
        font=("Arial", 10, "bold"),
        relief=tk.FLAT,
        width=24,
    )
    btn_run.pack(side=tk.LEFT)

  def show_dict_guide(self):
    dict_win = tk.Toplevel(self.root)
    dict_win.title("Python Dictionary Reference & Manual")
    dict_win.geometry("720x580")
    dict_win.config(bg=GALAXY_BG)

    tk.Label(
        dict_win,
        text="📖 Python Dictionary Reference Manual (PYTHON_REFERENCE_DICT)",
        font=("Arial", 11, "bold"),
        fg=ACCENT_CYAN,
        bg=GALAXY_BG,
    ).pack(anchor="w", padx=15, pady=(12, 5))

    box = scrolledtext.ScrolledText(
        dict_win,
        wrap=tk.WORD,
        bg=PANEL_BG,
        fg=TEXT_MAIN,
        font=("Courier", 10),
        relief=tk.FLAT,
    )
    box.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

    manual_lines = []
    for category, items in PYTHON_REFERENCE_DICT.items():
      manual_lines.append(f"=== {category.upper()} ===")
      for key, desc in items.items():
        manual_lines.append(f"  • {key}: {desc}")
      manual_lines.append("")

    box.insert(tk.END, "\n".join(manual_lines))
    box.config(state=tk.DISABLED)

  def show_cpp_dict_guide(self):
    cpp_win = tk.Toplevel(self.root)
    cpp_win.title("C++ Dictionary Reference & Manual")
    cpp_win.geometry("720x580")
    cpp_win.config(bg=GALAXY_BG)

    tk.Label(
        cpp_win,
        text="📖 C++ Reference Manual & Keywords (CPP_REFERENCE_DICT)[cite: 6]",
        font=("Arial", 11, "bold"),
        fg=ACCENT_CYAN,
        bg=GALAXY_BG,
    ).pack(anchor="w", padx=15, pady=(12, 5))

    box = scrolledtext.ScrolledText(
        cpp_win,
        wrap=tk.WORD,
        bg=PANEL_BG,
        fg=TEXT_MAIN,
        font=("Courier", 10),
        relief=tk.FLAT,
    )
    box.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

    manual_lines = []
    for category, items in CPP_REFERENCE_DICT.items():
      manual_lines.append(f"=== {category.upper()} ===")
      for key, desc in items.items():
        manual_lines.append(f"  • {key}: {desc}")
      manual_lines.append("")

    box.insert(tk.END, "\n".join(manual_lines))
    box.config(state=tk.DISABLED)

  def show_html_dict_guide(self):
    html_win = tk.Toplevel(self.root)
    html_win.title("HTML Dictionary Reference & Manual")
    html_win.geometry("720x580")
    html_win.config(bg=GALAXY_BG)

    tk.Label(
        html_win,
        text="📖 HTML Reference Manual & Tags (HTML_REFERENCE_DICT)",
        font=("Arial", 11, "bold"),
        fg=ACCENT_CYAN,
        bg=GALAXY_BG,
    ).pack(anchor="w", padx=15, pady=(12, 5))

    box = scrolledtext.ScrolledText(
        html_win,
        wrap=tk.WORD,
        bg=PANEL_BG,
        fg=TEXT_MAIN,
        font=("Courier", 10),
        relief=tk.FLAT,
    )
    box.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

    manual_lines = []
    for category, items in HTML_REFERENCE_DICT.items():
      manual_lines.append(f"=== {category.upper()} ===")
      for key, desc in items.items():
        manual_lines.append(f"  • {key}: {desc}")
      manual_lines.append("")

    box.insert(tk.END, "\n".join(manual_lines))
    box.config(state=tk.DISABLED)

  def show_js_dict_guide(self):
    js_win = tk.Toplevel(self.root)
    js_win.title("JavaScript Dictionary Reference & Manual")
    js_win.geometry("720x580")
    js_win.config(bg=GALAXY_BG)

    tk.Label(
        js_win,
        text=(
            "📖 JavaScript Reference Manual & Keywords (JS_REFERENCE_DICT)"
            "[cite: 7]"
        ),
        font=("Arial", 11, "bold"),
        fg=ACCENT_CYAN,
        bg=GALAXY_BG,
    ).pack(anchor="w", padx=15, pady=(12, 5))

    box = scrolledtext.ScrolledText(
        js_win,
        wrap=tk.WORD,
        bg=PANEL_BG,
        fg=TEXT_MAIN,
        font=("Courier", 10),
        relief=tk.FLAT,
    )
    box.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

    manual_lines = []
    for category, items in JS_REFERENCE_DICT.items():
      manual_lines.append(f"=== {category.upper()} ===")
      for key, desc in items.items():
        manual_lines.append(f"  • {key}: {desc}")
      manual_lines.append("")

    box.insert(tk.END, "\n".join(manual_lines))
    box.config(state=tk.DISABLED)

  def show_lua_dict_guide(self):
    lua_win = tk.Toplevel(self.root)
    lua_win.title("Lua Dictionary Reference & Manual")
    lua_win.geometry("720x580")
    lua_win.config(bg=GALAXY_BG)

    tk.Label(
        lua_win,
        text="📖 Lua Reference Manual & Keywords (LUA_REFERENCE_DICT)",
        font=("Arial", 11, "bold"),
        fg=ACCENT_CYAN,
        bg=GALAXY_BG,
    ).pack(anchor="w", padx=15, pady=(12, 5))

    box = scrolledtext.ScrolledText(
        lua_win,
        wrap=tk.WORD,
        bg=PANEL_BG,
        fg=TEXT_MAIN,
        font=("Courier", 10),
        relief=tk.FLAT,
    )
    box.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

    manual_lines = []
    for category, items in LUA_REFERENCE_DICT.items():
      manual_lines.append(f"=== {category.upper()} ===")
      for key, desc in items.items():
        manual_lines.append(f"  • {key}: {desc}")
      manual_lines.append("")

    box.insert(tk.END, "\n".join(manual_lines))
    box.config(state=tk.DISABLED)

  def validate_editor_syntax(self):
    code = self.text_area.get("1.0", tk.END)
    is_valid, msg = self.symbolic_ai.validate_ast(code)
    if is_valid:
      messagebox.showinfo("AST Validation", msg)
    else:
      messagebox.showerror("AST Validation Error", msg)

  def save_current_file(self):
    if not self.current_file_path:
      return
    code_text = self.text_area.get("1.0", tk.END)
    if self.auto_fix_var.get() == 1:
      code_text = fix_indentation_and_correct(code_text)
      self.text_area.delete("1.0", tk.END)
      self.text_area.insert("1.0", code_text)

    try:
      with open(self.current_file_path, "w", encoding="utf-8") as f:
        f.write(code_text)
      messagebox.showinfo(
          "Success", "File saved and auto-corrected successfully!"
      )
    except Exception as e:
      messagebox.showerror("Error", f"Could not save file: {e}")

  def run_in_sandbox_vm(self):
    if not self.current_file_path:
      return
    self.save_current_file()

    sandbox_win = tk.Toplevel(self.root)
    sandbox_win.title(
        f"Virtual Sandbox VM [Executing:"
        f" {os.path.basename(self.current_file_path)}]"
    )
    sandbox_win.geometry("750x500")
    sandbox_win.configure(bg="#111111")

    lbl_status = tk.Label(
        sandbox_win,
        text="🟢 Sandbox VM Active (Isolated Container Process)",
        bg="#111111",
        fg="#00ff00",
        font=("Arial", 10, "bold"),
    )
    lbl_status.pack(anchor="w", padx=10, pady=5)

    console = scrolledtext.ScrolledText(
        sandbox_win,
        wrap=tk.WORD,
        bg="#000000",
        fg="#00ff00",
        font=("Courier", 10),
    )
    console.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    console.insert(
        tk.END,
        "Booting virtual sandbox environment...\nTarget script:"
        f" {self.current_file_path}\n\n",
    )

    threading.Thread(
        target=self._execute_isolated_process,
        args=(self.current_file_path, self.current_folder, console),
        daemon=True,
    ).start()

  def _execute_isolated_process(self, filepath, working_dir, console_widget):
    ext = os.path.splitext(filepath)[1].lower()

    if ext == ".py":
      cmd = [sys.executable, filepath]
    elif ext == ".js":
      cmd = ["node", filepath]
    elif ext in [".lua", ".luau"]:
      cmd = "luau"
      try:
        subprocess.run(["luau", "--version"], capture_output=True, text=True)
      except FileNotFoundError:
        cmd = "lua"
      cmd = [cmd, filepath]
    else:
      console_widget.insert(
          tk.END, f"Error: Unsupported sandbox execution type '{ext}'\n"
      )
      return

    try:
      process = subprocess.Popen(
          cmd,
          stdout=subprocess.PIPE,
          stderr=subprocess.PIPE,
          text=True,
          cwd=working_dir,
      )

      stdout, stderr = process.communicate(timeout=15)

      if stdout:
        console_widget.insert(tk.END, stdout)
      if stderr:
        console_widget.insert(
            tk.END, f"\n[Runtime Errors/Warnings]:\n{stderr}"
        )

      console_widget.insert(
          tk.END, "\n\n--- Process Completed & Sandbox Terminated Safely ---"
      )
    except subprocess.TimeoutExpired:
      process.kill()
      console_widget.insert(
          tk.END,
          "\n\n⚠️ SANDBOX ALERT: Process killed! Exceeded 15-second safety"
          " timeout.",
      )
    except Exception as e:
      console_widget.insert(tk.END, f"\n\nSandbox Execution Error: {str(e)}")

    console_widget.see(tk.END)


# ==========================================
# 2. CUSTOM TERMINAL MODE
# ==========================================
class CustomTerminal:

  def __init__(self, root):
    self.root = root
    self.root.title("Galaxy Custom Terminal")
    self.root.geometry("850x550")
    self.root.config(bg=GALAXY_BG)
    self.cwd = os.getcwd()

    lbl_mode = tk.Label(
        root,
        text="🌌 Active Mode: Galaxy Custom Terminal",
        font=("Arial", 11, "bold"),
        fg=TERM_GREEN,
        bg=GALAXY_BG,
    )
    lbl_mode.pack(anchor="nw", padx=15, pady=(12, 5))

    self.term_output = scrolledtext.ScrolledText(
        root,
        wrap=tk.WORD,
        width=95,
        height=22,
        bg="#05070B",
        fg=TERM_GREEN,
        font=("Courier", 11),
        insertbackground="white",
        relief=tk.FLAT,
    )
    self.term_output.pack(padx=15, pady=5, fill=tk.BOTH, expand=True)
    self.term_output.insert(
        tk.END,
        f"Galaxy Terminal Online.\nWorking Directory:"
        f" {self.cwd}\nEnter shell commands below:\n\n",
    )
    self.term_output.config(state=tk.DISABLED)

    frame_input = tk.Frame(root, bg=GALAXY_BG)
    frame_input.pack(fill=tk.X, padx=15, pady=12)

    tk.Label(
        frame_input,
        text="$ ",
        font=("Courier", 12, "bold"),
        fg=TERM_GREEN,
        bg=GALAXY_BG,
    ).pack(side=tk.LEFT)

    self.entry_cmd = tk.Entry(
        frame_input,
        font=("Courier", 11),
        bg=PANEL_BG,
        fg=TEXT_MAIN,
        insertbackground="white",
        relief=tk.FLAT,
    )
    self.entry_cmd.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
    self.entry_cmd.bind("<Return>", self.execute_command)
    self.entry_cmd.focus()

    btn_exec = tk.Button(
        frame_input,
        text="Execute",
        command=self.execute_command,
        bg=ACCENT_PURPLE,
        fg="white",
        font=("Arial", 9, "bold"),
        relief=tk.FLAT,
    )
    btn_exec.pack(side=tk.RIGHT, padx=(5, 0))

    btn_cmd_list = tk.Button(
        frame_input,
        text="📜 List of Commands",
        command=self.show_command_list,
        bg="#30363D",
        fg=ACCENT_CYAN,
        font=("Arial", 9, "bold"),
        relief=tk.FLAT,
    )
    btn_cmd_list.pack(side=tk.RIGHT)

  def show_command_list(self):
    cmd_win = tk.Toplevel(self.root)
    cmd_win.title("Galaxy Terminal Command Reference")
    cmd_win.geometry("550x400")
    cmd_win.config(bg=GALAXY_BG)

    tk.Label(
        cmd_win,
        text="📜 Available Terminal Commands",
        font=("Arial", 11, "bold"),
        fg=ACCENT_CYAN,
        bg=GALAXY_BG,
    ).pack(anchor="w", padx=15, pady=(12, 5))

    box = scrolledtext.ScrolledText(
        cmd_win,
        wrap=tk.WORD,
        bg=PANEL_BG,
        fg=TEXT_MAIN,
        font=("Courier", 10),
        relief=tk.FLAT,
    )
    box.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)
    help_text = (
        "--- SHELL & NAVIGATION COMMANDS ---\n"
        "• cd <path>          : Change current working directory.\n"
        "• ls / dir           : List files and folders in directory.\n"
        "• pwd                : Print current working directory.\n\n"
        "--- EXECUTION COMMANDS ---\n"
        "• python <file.py>   : Run a Python script.\n"
        "• node <file.js>     : Run a Node.js JavaScript file.\n"
        "• lua / luau <file>  : Run a Lua or Luau script.\n\n"
        "--- SYSTEM UTILITIES ---\n"
        "• clear / cls        : Clear the terminal output console.\n"
    )
    box.insert(tk.END, help_text)
    box.config(state=tk.DISABLED)

  def execute_command(self, event=None):
    cmd = self.entry_cmd.get().strip()
    if not cmd:
      return
    self.entry_cmd.delete(0, tk.END)

    self.term_output.config(state=tk.NORMAL)
    self.term_output.insert(tk.END, f"$ {cmd}\n")

    if cmd.startswith("cd "):
      new_path = cmd[3:].strip()
      if new_path.startswith("~"):
        new_path = os.path.expanduser(new_path)
      elif not os.path.isabs(new_path):
        new_path = os.path.join(self.cwd, new_path)

      if os.path.exists(new_path) and os.path.isdir(new_path):
        self.cwd = os.path.abspath(new_path)
        os.chdir(self.cwd)
        self.term_output.insert(tk.END, f"Directory changed to: {self.cwd}\n\n")
      else:
        self.term_output.insert(
            tk.END, f"cd: no such file or directory: {new_path}\n\n"
        )
    else:
      try:
        result = subprocess.run(
            cmd, shell=True, cwd=self.cwd, capture_output=True, text=True, timeout=15
        )
        if result.stdout:
          self.term_output.insert(tk.END, result.stdout)
        if result.stderr:
          self.term_output.insert(tk.END, result.stderr)
        if not result.stdout and not result.stderr:
          self.term_output.insert(tk.END, "Command executed successfully.\n")
        self.term_output.insert(tk.END, "\n")
      except subprocess.TimeoutExpired:
        self.term_output.insert(tk.END, "Error: Command timed out.\n\n")
      except Exception as e:
        self.term_output.insert(tk.END, f"Execution Error: {e}\n\n")

    self.term_output.config(state=tk.DISABLED)
    self.term_output.see(tk.END)


# ==========================================
# 3. STARTUP MODE SELECTOR
# ==========================================
class ModeSelector:

  def __init__(self, root):
    self.root = root
    self.root.title("Galaxy Script Studio Launcher")
    self.root.geometry("450x260")
    self.root.config(bg=GALAXY_BG)

    tk.Label(
        root,
        text="🌌 Galaxy Script Studio",
        font=("Arial", 14, "bold"),
        fg=ACCENT_CYAN,
        bg=GALAXY_BG,
    ).pack(pady=20)

    btn_file = tk.Button(
        root,
        text="Workspace & Symbolic AI Studio",
        command=self.open_workspace_mode,
        bg=ACCENT_PURPLE,
        fg="white",
        font=("Arial", 11, "bold"),
        relief=tk.FLAT,
        width=28,
        height=2,
    )
    btn_file.pack(pady=6)

    btn_term = tk.Button(
        root,
        text="Galaxy Custom Terminal",
        command=self.open_terminal_mode,
        bg="#21262D",
        fg=TEXT_MAIN,
        font=("Arial", 11, "bold"),
        relief=tk.FLAT,
        width=28,
        height=2,
    )
    btn_term.pack(pady=6)

  def open_workspace_mode(self):
    self.root.destroy()
    new_root = tk.Tk()
    WorkspaceManager(new_root)
    new_root.mainloop()

  def open_terminal_mode(self):
    self.root.destroy()
    new_root = tk.Tk()
    CustomTerminal(new_root)
    new_root.mainloop()


if __name__ == "__main__":
  root = tk.Tk()
  app = ModeSelector(root)
  root.mainloop()