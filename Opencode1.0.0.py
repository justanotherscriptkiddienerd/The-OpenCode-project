import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, scrolledtext, Menu
import subprocess
import os

class CodeEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Code Editor")
        self.root.geometry("800x600")
        self.root.configure(bg='black')

        self.text_area = scrolledtext.ScrolledText(self.root, bg='black', fg='white', insertbackground='white', wrap='word', font=('Consolas', 12))
        self.text_area.pack(expand=True, fill='both')

        self.line_count = tk.Text(self.root, width=4, bg='black', fg='white', bd=0, font=('Consolas', 12))
        self.line_count.pack(side='left', fill='y')
        self.update_line_count()

        self.terminal = tk.Text(self.root, height=10, bg='black', fg='white', font=('Consolas', 12))
        self.terminal.pack(side='bottom', fill='x')

        self.create_menu()
        self.text_area.bind("<KeyRelease>", self.update_line_count)

    def create_menu(self):
        menu = Menu(self.root)
        self.root.config(menu=menu)

        file_menu = Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        settings_menu = Menu(menu, tearoff=0)
        menu.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Change Background Color", command=self.change_background_color)
        settings_menu.add_command(label="Change Font", command=self.change_font)

        execute_menu = Menu(menu, tearoff=0)
        menu.add_cascade(label="Execute", menu=execute_menu)
        execute_menu.add_command(label="Run", command=self.run_code)

    def new_file(self):
        self.text_area.delete(1.0, tk.END)

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".py", filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, file.read())

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.text_area.get(1.0, tk.END).strip())

    def save_as_file(self):
        self.save_file()

    def change_background_color(self):
        color = simpledialog.askstring("Background Color", "Enter 'black' or 'white':")
        if color in ['black', 'white']:
            self._set_color(color)

    def _set_color(self, color):
        self.text_area.configure(bg=color)
        self.line_count.configure(bg=color)
        self.terminal.configure(bg=color)
        self.root.configure(bg=color)

    def change_font(self):
        font = simpledialog.askstring("Font", "Enter font name (e.g., 'Consolas'):")
        if font:
            self._set_font(font)

    def _set_font(self, font):
        self.text_area.configure(font=(font, 12))
        self.line_count.configure(font=(font, 12))
        self.terminal.configure(font=(font, 12))

    def update_line_count(self, event=None):
        line_count = self.text_area.index('end-1c').split('.')[0]
        self.line_count.delete(1.0, tk.END)
        self.line_count.insert(tk.END, '\n'.join(str(i) for i in range(1, int(line_count) + 1)))

    def run_code(self):
        code = self.text_area.get(1.0, tk.END).strip()
        if code:
            with open("temp_script.py", "w") as temp_file:
                temp_file.write(code)
            result = subprocess.run(['python', 'temp_script.py'], capture_output=True, text=True)
            self.terminal.delete(1.0, tk.END)
            self.terminal.insert(tk.END, result.stdout + result.stderr)

if __name__ == "__main__":
    root = tk.Tk()
    editor = CodeEditor(root)
    root.mainloop()
