import tkinter as tk
from tkinter import filedialog, simpledialog, scrolledtext, Menu
from tkinter import ttk
import subprocess

class CodeEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Opencode")
        self.root.geometry("800x600")
        self.root.configure(bg='#2e2e2e')

        # Modern font and colors
        font = ('Fira Code', 12)
        bg_color = '#2e2e2e'
        fg_color = '#dcdcdc'
        insert_bg = '#dcdcdc'

        # Using ttk styles
        style = ttk.Style()
        style.configure('TFrame', background=bg_color)
        style.configure('TButton', background=bg_color, foreground=fg_color, font=font)
        style.configure('TLabel', background=bg_color, foreground=fg_color, font=font)
        style.configure('TText', background=bg_color, foreground=fg_color, font=font)

        # Main frame
        self.main_frame = ttk.Frame(self.root, padding=5)
        self.main_frame.pack(expand=True, fill='both')

        # Text area
        self.text_area = scrolledtext.ScrolledText(self.main_frame, bg=bg_color, fg=fg_color, insertbackground=insert_bg, wrap='word', font=font)
        self.text_area.pack(side='left', expand=True, fill='both')

        # Line count
        self.line_count = tk.Text(self.main_frame, width=4, bg=bg_color, fg=fg_color, bd=0, font=font)
        self.line_count.pack(side='left', fill='y')
        self.update_line_count()

        # Terminal output
        self.terminal = tk.Text(self.root, height=10, bg=bg_color, fg=fg_color, font=font)
        self.terminal.pack(side='bottom', fill='x')

        self.language = tk.StringVar(value='Python')

        self.create_menu()
        self.text_area.bind("<KeyRelease>", self.update_line_count)

        # Bind shortcuts
        self.root.bind('<Control-s>', self.save_file)
        self.root.bind('<Shift-F5>', self.run_code)

    def create_menu(self):
        menu_bar = tk.Menu(self.root, bg='#3c3c3c', fg='#dcdcdc')
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0, bg='#3c3c3c', fg='#dcdcdc')
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)  # This will close the window

        settings_menu = tk.Menu(menu_bar, tearoff=0, bg='#3c3c3c', fg='#dcdcdc')
        menu_bar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Change Background Color", command=self.change_background_color)
        settings_menu.add_command(label="Change Font", command=self.change_font)

        execute_menu = tk.Menu(menu_bar, tearoff=0, bg='#3c3c3c', fg='#dcdcdc')
        menu_bar.add_cascade(label="Execute", menu=execute_menu)
        execute_menu.add_command(label="Run", command=self.run_code)

        language_menu = tk.Menu(menu_bar, tearoff=0, bg='#3c3c3c', fg='#dcdcdc')
        menu_bar.add_cascade(label="Code Language", menu=language_menu)
        language_menu.add_radiobutton(label="Python", variable=self.language, value='Python')
        language_menu.add_radiobutton(label="Bash", variable=self.language, value='Bash')

    def new_file(self):
        self.text_area.delete(1.0, tk.END)

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".py", filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, file.read())

    def save_file(self, event=None):
        file_extension = ".py" if self.language.get() == 'Python' else ".sh"
        file_path = filedialog.asksaveasfilename(defaultextension=file_extension, filetypes=[("Python Files", "*.py"), ("Bash Scripts", "*.sh"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.text_area.get(1.0, tk.END).strip())

    def save_as_file(self):
        self.save_file()

    def change_background_color(self):
        color = simpledialog.askstring("Background Color", "Enter a color code (e.g., '#2e2e2e'):")
        if color:
            self._set_color(color)

    def _set_color(self, color):
        style = ttk.Style()
        style.configure('TFrame', background=color)
        style.configure('TButton', background=color, foreground='#dcdcdc')
        style.configure('TLabel', background=color, foreground='#dcdcdc')
        style.configure('TText', background=color, foreground='#dcdcdc')

        self.text_area.configure(bg=color)
        self.line_count.configure(bg=color)
        self.terminal.configure(bg=color)
        self.root.configure(bg=color)

    def change_font(self):
        font = simpledialog.askstring("Font", "Enter font name (e.g., 'Fira Code'):")
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

    def run_code(self, event=None):
        code = self.text_area.get(1.0, tk.END).strip()
        language = self.language.get()
        if code:
            temp_filename = "temp_script"
            if language == 'Python':
                temp_filename += ".py"
            elif language == 'Bash':
                temp_filename += ".sh"

            with open(temp_filename, "w") as temp_file:
                temp_file.write(code)

            if language == 'Python':
                result = subprocess.run(['python3', temp_filename], capture_output=True, text=True)
            elif language == 'Bash':
                result = subprocess.run(['bash', temp_filename], capture_output=True, text=True)

            self.terminal.delete(1.0, tk.END)
            self.terminal.insert(tk.END, result.stdout + result.stderr)

if __name__ == "__main__":
    root = tk.Tk()
    editor = CodeEditor(root)
    root.mainloop()
