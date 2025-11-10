import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

TARGET_FOLDERS = {"bin", "obj"}

def get_dir_size(path):
    total = 0
    for root, dirs, files in os.walk(path):
        for f in files:
            try:
                total += os.path.getsize(os.path.join(root, f))
            except OSError:
                pass
    return total

def format_size(bytes_size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024
    return f"{bytes_size:.2f} PB"

def clean_projects(root, log_callback):
    total_freed = 0
    for dirpath, dirnames, filenames in os.walk(root):
        for dirname in list(dirnames):
            if dirname.lower() in TARGET_FOLDERS:
                full_path = os.path.join(dirpath, dirname)
                size = get_dir_size(full_path)
                total_freed += size
                try:
                    shutil.rmtree(full_path)
                    log_callback(f"🗑️ Deleted: {full_path} ({format_size(size)})")
                except Exception as e:
                    log_callback(f"⚠️ Failed to delete {full_path}: {e}")
    return total_freed

def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_path_var.set(folder_selected)

def run_cleaner():
    root_path = folder_path_var.get().strip()
    if not root_path or not os.path.isdir(root_path):
        messagebox.showwarning("Warning", "Please select a valid folder.")
        return
    
    log_box.delete(1.0, tk.END)
    log_box.insert(tk.END, f"🧽 Cleaning 'bin' and 'obj' folders in:\n{root_path}\n\n")
    app.update()

    freed_bytes = clean_projects(root_path, lambda msg: log_box.insert(tk.END, msg + "\n"))
    
    log_box.insert(tk.END, f"\n✅ Done!\n💾 Total space freed: {format_size(freed_bytes)}\n")
    messagebox.showinfo("Done", f"Cleaning complete.\nFreed {format_size(freed_bytes)}")

# --- GUI Setup ---
app = tk.Tk()
app.title("Visual Studio Cleaner")
app.geometry("700x400")
app.resizable(False, False)

# Folder selection
frame = tk.Frame(app)
frame.pack(pady=10, padx=10, fill="x")

folder_path_var = tk.StringVar()
entry = tk.Entry(frame, textvariable=folder_path_var, width=70)
entry.pack(side="left", padx=(0,5), expand=True, fill="x")

browse_btn = tk.Button(frame, text="...", width=3, command=browse_folder)
browse_btn.pack(side="left")

run_btn = tk.Button(app, text="Run Cleaner", command=run_cleaner, bg="#0078D7", fg="white", width=15)
run_btn.pack(pady=5)

# Log area
log_box = scrolledtext.ScrolledText(app, height=15, wrap=tk.WORD)
log_box.pack(padx=10, pady=5, fill="both", expand=True)

app.mainloop()
