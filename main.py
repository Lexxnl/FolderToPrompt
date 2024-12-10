import os
import pyperclip
import tkinter as tk
from tkinter import filedialog, messagebox

def list_py_files(start_path, output_text_widget):
    py_files_to_read = []
    output = []

    def has_py_files(path):
        for root, _, files in os.walk(path):
            if any(file.endswith('.py') for file in files):
                return True
        return False

    def traverse_and_print(path, prefix=""):
        try:
            entries = sorted(os.listdir(path))
        except PermissionError:
            output.append(f"{prefix}[Access Denied]")
            return

        dirs, py_files = [], []
        for entry in entries:
            full_path = os.path.join(path, entry)
            if os.path.isfile(full_path) and entry.endswith('.py'):
                py_files.append(entry)
                py_files_to_read.append(full_path)
            elif os.path.isdir(full_path) and has_py_files(full_path):
                dirs.append(entry)

        for index, file in enumerate(py_files):
            connector = "├── " if index < len(py_files) - 1 else "└── "
            output.append(f"{prefix}{connector}{file}")

        for index, dir_name in enumerate(dirs):
            connector = "├── " if index < len(dirs) - 1 else "└── "
            output.append(f"{prefix}{connector}{dir_name}/")
            new_prefix = prefix + ("│   " if index < len(dirs) - 1 else "    ")
            traverse_and_print(os.path.join(path, dir_name), new_prefix)

    output.append(start_path)
    traverse_and_print(start_path)

    output.append("\n\n### Python Files Content ###\n")
    for file_path in py_files_to_read:
        output.append(f"--- {file_path} ---")
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                filtered_lines = [line for line in lines if 'base64' not in line.lower()]
                output.append("".join(filtered_lines))
        except Exception as e:
            output.append(f"Error reading {file_path}: {e}")
        output.append("\n")

    full_output = "\n".join(output)
    chunks = [full_output[i:i + 15000] for i in range(0, len(full_output), 15000)]
    total_chunks = len(chunks)
    intro_text = f"""The total length of the content that I want to send you is too large to send in only one piece.
For sending you that content, I will follow this rule:

[START PART 1/{total_chunks}]
this is the content of the part 1 out of {total_chunks} in total
[END PART 1/{total_chunks}]

Then you just answer: \"Received part 1/{total_chunks}\"
And when I tell you \"ALL PARTS SENT\", then you can continue processing the data and answering my requests.
Do not answer yet. This is just another part of the text I want to send you. Just receive and acknowledge as \"Part 1/{total_chunks} received\" and wait for the next part. 
[START PART 1/{total_chunks}]
"""

    full_output = intro_text + full_output
    chunks = [full_output[i:i + 15000] for i in range(0, len(full_output), 15000)]
    outro_text = lambda part_num: f"[END PART {part_num}/{total_chunks}]\nRemember not answering yet. Just acknowledge you received this part with the message \"Part {part_num}/{total_chunks} received\" and wait for the next part."
    last_chunk_outro_text = lambda part_num: f"[END PART {part_num}/{total_chunks}]\nALL PARTS SENT. Now you can continue processing the request."

    for i in range(len(chunks) - 1):
        chunks[i] += f"\n{outro_text(i + 1)}"

    if chunks:
        chunks[-1] += f"\n{last_chunk_outro_text(len(chunks))}"

    output_text_widget.delete(1.0, tk.END)
    full_output = "\n".join(chunks)
    output_text_widget.insert(tk.END, full_output)

    return chunks

def open_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_path_entry.delete(0, tk.END)
        folder_path_entry.insert(0, folder_selected)

def copy_to_clipboard(part_text):
    pyperclip.copy(part_text)
    messagebox.showinfo("Success", "Part has been copied to clipboard.")

root = tk.Tk()
root.title("Python File Tree & Content Copier")
root.geometry("800x600")

folder_path_label = tk.Label(root, text="Select Folder:")
folder_path_label.pack(pady=10)

folder_path_entry = tk.Entry(root, width=60)
folder_path_entry.pack(pady=5)

browse_button = tk.Button(root, text="Browse", command=open_folder)
browse_button.pack(pady=5)

frame = tk.Frame(root)
frame.pack(pady=10)

output_text = tk.Text(frame, height=20, width=80)
output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=output_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

output_text.config(yscrollcommand=scrollbar.set)

def process_files():
    folder_path = folder_path_entry.get()
    if folder_path:
        chunks = list_py_files(folder_path, output_text)
        for widget in button_frame.winfo_children():
            widget.destroy()
        for i, chunk in enumerate(chunks):
            button = tk.Button(button_frame, text=f'Copy part {i+1}/{len(chunks)} to clipboard',
                               command=lambda part=chunk: copy_to_clipboard(part),
                               width=4, height=4)
            button.pack(side=tk.LEFT, padx=5)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

process_button = tk.Button(root, text="Process Files", command=process_files)
process_button.pack(pady=10)

root.mainloop()
