import os
import pyperclip
from tkpygame import *
from tkinter import filedialog

# Add your useful file extensions here
USEFUL_EXTENSIONS = ['.txt', '.py', '.md']

def get_select_folder_inputfield_input(inputfield_text : InputField):
    print(inputfield_text)

def take_select_folder_inputfield_input(inputfield_text: InputField):
    path = filedialog.askdirectory(title='Select Folder')
    print(path)

    inputfield_text.text = path

    chunks = list_files(path)

    # Collect all old buttons to remove them later
    buttons_to_remove = [obj for obj in main_canvas.objects if isinstance(obj, Button)]

    # Remove all old buttons
    for button in buttons_to_remove:
        main_canvas.objects.remove(button)

    # Create new buttons for every chunk
    for i, chunk in enumerate(chunks):
        button = Button(main_canvas, f'part {i+1}/{len(chunks)}', 'S', ((-300 + ((i / (len(chunks) - 1)) * 600)) if len(chunks) > 1 else 0, 100), width=100, height=100, name='copy-button', command=lambda i=i: copy_to_clipboard(chunks[i]))



def list_files(start_path):
    files_to_read = []
    output = []

    def has_files(path):
        for root, _, files in os.walk(path):
            if len(files) > 0:
                return True
        return False

    def traverse_and_print(path, prefix=""):
        try:
            entries = sorted(os.listdir(path))
            entries = sorted(os.listdir(path))
        except PermissionError:
            output.append(f"{prefix}[Access Denied]")
            return

        dirs, files = [], []
        for entry in entries:
            full_path = os.path.join(path, entry)
            if os.path.isfile(full_path):
                files.append(entry)
                # Check if the file extension is in the useful extensions list
                if any(full_path.endswith(ext) for ext in USEFUL_EXTENSIONS):
                    files_to_read.append(full_path)
            elif os.path.isdir(full_path) and has_files(full_path):
                dirs.append(entry)

        for index, file in enumerate(files):
            connector = "├── " if index < len(files) - 1 else "└── "
            output.append(f"{prefix}{connector}{file}")


        for index, dir_name in enumerate(dirs):
            connector = "├── " if index < len(dirs) - 1 else "└── "
            output.append(f"{prefix}{connector}{dir_name}/")
            new_prefix = prefix + ("│   " if index < len(dirs) - 1 else "    ")
            traverse_and_print(os.path.join(path, dir_name), new_prefix)

    output.append(start_path)
    traverse_and_print(start_path)

    output.append("\n\n### Files Content ###\n")
    for file_path in files_to_read:
        output.append(f"--- {file_path} ---")
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                filtered_lines = [line for line in lines if 'base64' not in line.lower()]
                output.append("".join(filtered_lines))
        except Exception as e:
            output.append(f"Error reading {file_path}: {e}")
        output.append("\n")
        output.append("\n")

    full_output = "\n".join(output)
    chunks = [full_output[i:i + 15000] for i in range(0, len(full_output), 15000)]
    total_chunks = len(chunks)
    intro_text = f"""The total length of the content that I want to send you is too large to send in only one piece.
For sending you that content, I will follow this rule:

[START PART 1/{total_chunks}]
this is the content of the part 1 out of {total_chunks} in total
[END PART 1/{total_chunks}]

Then you just answer: \"Received part 1/{total_chunks}\".
And when I tell you \"ALL PARTS SENT\", then you can continue processing the data and answering my requests.
Do not answer yet. This is just another part of the text I want to send you. Just receive and acknowledge as \"Part 1/{total_chunks} received\" and wait for the next part. 
[START PART 1/{total_chunks}]
"""

    full_output = intro_text + full_output
    chunks = [full_output[i:i + 15000] for i in range(0, len(full_output), 15000)]
    outro_text = lambda part_num: f"[END PART {part_num}/{total_chunks}]\nRemember not answering yet. Just acknowledge you received this part with the message \"Part {part_num}/{total_chunks} received\" and wait for the next part."
    last_chunk_outro_text = lambda part_num: f"[END PART {part_num}/{total_chunks}]\nALL PARTS SENT. Now you can continue processing the request."

    for i in range(len(chunks) - 1):
    for i in range(len(chunks) - 1):
        chunks[i] += f"\n{outro_text(i + 1)}"


    if chunks:
        chunks[-1] += f"\n{last_chunk_outro_text(len(chunks))}"

    return chunks


def copy_to_clipboard(part_text):
    pyperclip.copy(part_text)


def main():
    global main_canvas, screen

    screen = init(screen_width=800, screen_height=600, resizable=False)

    main_canvas = Canvas(screen, 0, 0, 800, 600, 'main-canvas')
    
    select_folder_label = Label(main_canvas, 'ChatGPT File Structure Mapper', 'N', (0, 50), 100, 50, 'select-folder-labal', font_color='#ffffff')
    select_folder_inputfield = InputField(main_canvas, 'N', (0, 100), 500, 50, 'select-folder-inputfield', lambda: take_select_folder_inputfield_input(select_folder_inputfield), on_clicked_command=lambda: take_select_folder_inputfield_input(select_folder_inputfield), text='Select Folder', text_offset_y=6, text_offset_x=6)


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for object in main_canvas.objects:
            if object.__class__.__name__ == 'Button':
                print(object.text)
            print(object.name)

        flip()


if __name__ == '__main__':
    main()
