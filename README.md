# Python File Tree & Content Copier

This project provides a tool to list all Python files in a specified folder and its subdirectories, displaying their contents and organizing them into manageable chunks. The program breaks the output into smaller parts to bypass character limits in platforms like ChatGPT.

![Screenshot](Screenshot%202024-12-03%20132412.png)

## Features

- **Recursive Folder Traversal**: List `.py` files in the selected directory and subdirectories with a tree-like structure.
- **File Content Display**: Shows the content of `.py` files with filtering to exclude lines containing `base64`.
- **Chunk Splitting**: Automatically splits large outputs into smaller chunks (15,000 characters per chunk).
- **Clipboard Copying**: Allows users to copy each part of the output to the clipboard for easy processing.

## Requirements

- Python 3.x
- `tkinter` (usually comes pre-installed with Python)
- `pyperclip` for clipboard functionality

## Usage

1. Run the script.
2. A window will appear where you can select a folder to analyze.
3. The folder's `.py` files will be listed along with their contents, excluding any lines containing `base64`.
4. The output will be divided into smaller chunks and displayed in the window.
5. Use the buttons to copy each chunk to the clipboard.
6. Send each part to ChatGPT sequentially, and ChatGPT will acknowledge each part.

## How It Works

- The script starts by recursively scanning the selected folder for `.py` files.
- It generates a tree structure listing the files, followed by their contents.
- After listing the files and their content, it splits the output into chunks of 15,000 characters each to comply with ChatGPT's text size limits.
- The script creates an interface with `tkinter`, allowing the user to copy each chunk to the clipboard.

## Code Breakdown

### Function: `list_py_files`
This function recursively lists all `.py` files in the selected directory and its subdirectories, and retrieves their contents. It then splits the output into manageable chunks.

#### Parameters:
- `start_path`: The root directory to start the search.
- `output_text_widget`: The text widget in the Tkinter window where output is displayed.

### Function: `has_py_files`
Checks if a directory or its subdirectories contain any `.py` files.

### Function: `traverse_and_print`
Recursively traverses the directory, printing the structure of `.py` files in a tree-like format. It also reads and filters the content of these files.

### Function: `open_folder`
Opens a folder dialog to select the directory for processing.

### Function: `copy_to_clipboard`
Copies the given part of the output to the clipboard using `pyperclip`.

### Tkinter Setup
The script uses `tkinter` for the user interface, where:
- Users can select a folder.
- The structure of `.py` files is displayed in a text box.
- Buttons are provided for copying parts of the output to the clipboard.

### Main Process
- After selecting the folder, the program lists all `.py` files in the folder and its subdirectories.
- The contents of these files are displayed and divided into chunks.
- Each chunk can be copied separately for easy handling, ensuring compatibility with platforms like ChatGPT that have message length limitations.

## About Me
This project was created by **Lex Kimmel**, an aspiring web developer from the Netherlands. I am currently working on several projects related to web development. Feel free to explore my GitHub for more projects:  
[GitHub Profile](https://github.com/Lexxnl)
