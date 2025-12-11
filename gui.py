import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from pathlib import Path
import threading
from script import convert_images_to_pdf


class ImageToPdfApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to PDF Converter")
        self.root.geometry("600x500")

        # Data
        self.file_list = []

        # UI Setup
        self.create_widgets()

    def create_widgets(self):
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Toolbar
        toolbar = ttk.Frame(main_frame)
        toolbar.pack(fill=tk.X, pady=(0, 10))

        ttk.Button(toolbar, text="Add Images...", command=self.add_images).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(toolbar, text="Remove Selected", command=self.remove_selected).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(toolbar, text="Clear All", command=self.clear_all).pack(
            side=tk.LEFT, padx=5
        )

        # File List Area
        list_frame = ttk.LabelFrame(
            main_frame,
            text="Selected Images (Drag to Reorder - Not Implemented, use buttons)",
        )
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # Scrollbar and Listbox
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(
            list_frame, selectmode=tk.EXTENDED, yscrollcommand=scrollbar.set
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox.yview)

        # Reorder Buttons (Side of list or below) - Let's put them below
        reorder_frame = ttk.Frame(main_frame)
        reorder_frame.pack(fill=tk.X, pady=5)

        ttk.Button(reorder_frame, text="Move Up", command=self.move_up).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(reorder_frame, text="Move Down", command=self.move_down).pack(
            side=tk.LEFT, padx=5
        )

        # Convert Area
        convert_frame = ttk.Frame(main_frame)
        convert_frame.pack(fill=tk.X, pady=20)

        self.convert_btn = ttk.Button(
            convert_frame, text="Convert to PDF", command=self.start_conversion
        )
        self.convert_btn.pack(side=tk.RIGHT, padx=5)

        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(
            convert_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W
        )
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

    def add_images(self):
        filetypes = [
            ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.webp"),
            ("All files", "*.*"),
        ]
        files = filedialog.askopenfilenames(title="Select Images", filetypes=filetypes)
        if files:
            for f in files:
                if f not in self.file_list:
                    self.file_list.append(f)
                    self.listbox.insert(tk.END, os.path.basename(f))
            self.status_var.set(f"Added {len(files)} files.")

    def remove_selected(self):
        selection = self.listbox.curselection()
        if not selection:
            return

        # Remove in reverse order so indices don't shift
        for index in reversed(selection):
            self.file_list.pop(index)
            self.listbox.delete(index)
        self.status_var.set("Items removed.")

    def clear_all(self):
        self.file_list.clear()
        self.listbox.delete(0, tk.END)
        self.status_var.set("List cleared.")

    def move_up(self):
        selection = self.listbox.curselection()
        if not selection:
            return

        for index in selection:
            if index == 0:
                continue
            # Swap data
            self.file_list[index], self.file_list[index - 1] = (
                self.file_list[index - 1],
                self.file_list[index],
            )
            # Swap listbox display
            text = self.listbox.get(index)
            self.listbox.delete(index)
            self.listbox.insert(index - 1, text)
            self.listbox.selection_set(index - 1)

    def move_down(self):
        selection = self.listbox.curselection()
        if not selection:
            return

        # Iterate reversed to handle multiple selections correctly
        for index in reversed(selection):
            if index == len(self.file_list) - 1:
                continue

            # Swap data
            self.file_list[index], self.file_list[index + 1] = (
                self.file_list[index + 1],
                self.file_list[index],
            )
            # Swap listbox display
            text = self.listbox.get(index)
            self.listbox.delete(index)
            self.listbox.insert(index + 1, text)
            self.listbox.selection_set(index + 1)

    def start_conversion(self):
        if not self.file_list:
            messagebox.showwarning("No Files", "Please add images to convert.")
            return

        # Ask for output path in main thread
        output_path = filedialog.asksaveasfilename(
            title="Save PDF As",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
        )

        if not output_path:
            return

        self.convert_btn.config(state=tk.DISABLED)
        self.status_var.set("Converting...")

        # Run in thread to prevent UI freezing
        thread = threading.Thread(target=self.run_conversion, args=(output_path,))
        thread.start()

    def run_conversion(self, output_path):
        try:
            success = convert_images_to_pdf(self.file_list, output_path, sort=False)

            msg = (
                f"Saved to {output_path}"
                if success
                else "Conversion failed check logs."
            )
            self.root.after(0, lambda: self.finish_conversion(success, msg))

        except Exception as e:
            self.root.after(0, lambda: self.finish_conversion(False, str(e)))

    def finish_conversion(self, success, message):
        self.convert_btn.config(state=tk.NORMAL)
        self.status_var.set(message)
        if success:
            messagebox.showinfo("Success", message)
        elif message != "Cancelled":
            messagebox.showerror("Error", message)


if __name__ == "__main__":
    root = tk.Tk()
    # Set icon if available, skipped for now
    app = ImageToPdfApp(root)
    root.mainloop()
