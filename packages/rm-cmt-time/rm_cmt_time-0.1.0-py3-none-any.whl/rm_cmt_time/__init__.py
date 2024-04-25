import zipfile
import re
import os
import shutil
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

def remove_comment_timestamps(docx_path):
    # Step 1: Create a copy of the original .docx
    base_path, ext = os.path.splitext(docx_path)
    original_copy_path = base_path + '_original' + ext
    shutil.copyfile(docx_path, original_copy_path)
    
    # Step 2: Rename the copied .docx to .zip
    zip_path = base_path + '_NoTimestamp.zip'
    os.rename(original_copy_path, zip_path)
    
    # Step 3: Unzip the file
    extract_dir = base_path + '_extracted'
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    
    # Step 4 & 5: Modify the comments.xml and commentsExtensible.xml
    comments_path = os.path.join(extract_dir, 'word', 'comments.xml')
    comments_ext_path = os.path.join(extract_dir, 'word', 'commentsExtensible.xml')

    # Modify comments.xml
    if os.path.exists(comments_path):
        with open(comments_path, 'r', encoding='utf-8') as file:
            content = file.read()
        # In this format:  w:date="2024-04-22T16:49:00Z"
        content = re.sub(r'w:date="\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z"', '', content)
        with open(comments_path, 'w', encoding='utf-8') as file:
            file.write(content)

    # Modify commentsExtensible.xml
    if os.path.exists(comments_ext_path):
        with open(comments_ext_path, 'r', encoding='utf-8') as file:
            content = file.read()
        # In this format:  w16cex:dateUtc="2024-04-22T08:49:00Z"
        content = re.sub(r'w16cex:dateUtc="\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z"', '', content)
        with open(comments_ext_path, 'w', encoding='utf-8') as file:
            file.write(content)

    # Step 6: Rezip the contents
    with zipfile.ZipFile(zip_path, 'w') as zip_ref:
        for foldername, subfolders, filenames in os.walk(extract_dir):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                in_zip_path = os.path.relpath(file_path, extract_dir)
                zip_ref.write(file_path, in_zip_path)
    
    # Cleanup: Remove the extracted folder and rename zip back to .docx
    shutil.rmtree(extract_dir)
    final_docx_path = base_path + '_(NoTimestamp).docx'
    os.rename(zip_path, final_docx_path)
    
    return final_docx_path

def rm_cmt_time(docx_path):
    '''
    Input: path to .docx file
    Output: modified .docx with comment timestamps removed
    '''
    print("Timestamps removed; Modified docx saved as:", remove_comment_timestamps(docx_path))

# Ask user to select a Word file for timestamps removal
def select_and_remove_timestamps():
    root = tk.Tk()
    root.withdraw()  # Hide the main Tkinter window
    
    # Ask user to select a Word document
    docx_path = filedialog.askopenfilename(
        title="Select a Word Document",
        filetypes=[("Word Documents", "*.docx")]
    )
    
    if docx_path:
        try:
            final_docx_path = remove_comment_timestamps(docx_path)
            messagebox.showinfo(
                "Success",
                f"Timestamps removed; Modified document saved as:\n{final_docx_path}"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred: {e}; you may feedback to Dr. Wang: wangzhiyuan@u.nus.edu")
    else:
        messagebox.showwarning("No Selection", "No file was selected.")

if __name__ == "__main__":
    select_and_remove_timestamps()