import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import webbrowser

# Function to browse and select input video
def browse_file():
    filename = filedialog.askopenfilename(
        title="Select video file",
        filetypes=(("Video files", "*.mp4;*.avi;*.mov;*.wmv;*.mkv"), ("All files", "*.*"))
    )
    if filename:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, filename)

# Function to open the folder where the output is saved
def open_output_folder(folder_path):
    if os.path.exists(folder_path):
        os.startfile(folder_path)
    else:
        messagebox.showerror("Error", "Folder not found.")

# Function to compress video
def compress_video():
    input_file = input_entry.get()
    if not input_file or not os.path.isfile(input_file):
        messagebox.showerror("Error", "Please select a valid video file.")
        return

    folder = os.path.dirname(input_file)
    output_file = os.path.join(folder, "retro_output.mp4")

    ffmpeg_cmd = [
        "ffmpeg",
        "-y",  # overwrite without asking
        "-i", input_file,
        "-vf", "scale=320:240,setsar=1",
        "-r", "15",
        "-c:v", "mpeg4",
        "-b:v", "200k",
        "-q:v", "9",
        "-ac", "1",
        "-ar", "22050",
        "-b:a", "16k",
        "-acodec", "libmp3lame",
        output_file
    ]

    try:
        subprocess.run(ffmpeg_cmd, check=True)
        # Show message and give option to open folder
        if messagebox.askyesno("Success", f"Compressed file saved as:\n{output_file}\n\nOpen output folder?"):
            open_output_folder(folder)
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "FFmpeg failed. Make sure it's installed and in PATH.")

# --- GUI Setup ---
root = tk.Tk()
root.title("Retro 90s Video Compressor")
root.geometry("520x180")

tk.Label(root, text="Select a video file to compress:").pack(pady=10)

# Entry box to show selected file
input_entry = tk.Entry(root, width=60)
input_entry.pack(pady=5)

tk.Button(root, text="Browse", command=browse_file).pack(pady=5)
tk.Button(root, text="Compress Video", command=compress_video, bg="orange").pack(pady=10)

root.mainloop()
