import tkinter as tk
from tkinter import filedialog, scrolledtext, Menu
from tkinter import ttk
import subprocess
#Opencode 1.0.1
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
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.destroy)

        run_menu = tk.Menu(menu_bar, tearoff=0, bg='#3c3c3c', fg='#dcdcdc')
        menu_bar.add_cascade(label="Run", menu=run_menu)
        run_menu.add_command(label="Run Code", command=self.run_code)
        
        settings_menu = tk.Menu(menu_bar, tearoff=0, bg='#3c3c3c', fg='#dcdcdc')
        menu_bar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Change Background Color", command=self.change_background_color)
        settings_menu.add_command(label="Change Font", command=self.change_font)


        language_menu = tk.Menu(menu_bar, tearoff=0, bg='#3c3c3c', fg='#dcdcdc')
        menu_bar.add_cascade(label="Language", menu=language_menu)
        language_menu.add_radiobutton(label="Python", variable=self.language, value='Python')
        language_menu.add_radiobutton(label="Ruby", variable=self.language, value='Ruby')
        language_menu.add_radiobutton(label="Bash", variable=self.language, value='Bash')
        language_menu.add_radiobutton(label="JavaScript", variable=self.language, value='JavaScript')

    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'r') as file:
                code = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, code)

    def save_file(self, event=None):
        file_path = filedialog.asksaveasfilename(defaultextension=".py")
        if file_path:
            with open(file_path, 'w') as file:
                code = self.text_area.get(1.0, tk.END)
                file.write(code)
    
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

    def run_code(self, event=None):
        code = self.text_area.get(1.0, tk.END)
        language = self.language.get()

        if language == 'Python':
            command = ['python3', '-c', code]
        elif language == 'Ruby':
            command = ['ruby', '-e', code]
        elif language == 'Bash':
            command = ['bash', '-c', code]
        elif language == 'JavaScript':
            command = ['node', '-e', code]

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()

        self.terminal.delete(1.0, tk.END)
        self.terminal.insert(tk.END, output.decode('utf-8'))
        self.terminal.insert(tk.END, error.decode('utf-8'))
    def change_font(self):
        font = simpledialog.askstring("Font", "Enter font name (e.g., 'Fira Code'):")
        if font:
            self._set_font(font)

    def _set_font(self, font):
        self.text_area.configure(font=(font, 12))
        self.line_count.configure(font=(font, 12))
        self.terminal.configure(font=(font, 12))

    def update_line_count(self, event=None):
        lines = self.text_area.get(1.0, tk.END).split('\n')
        line_count_str = '\n'.join(str(i + 1) for i in range(len(lines)))
        self.line_count.config(state=tk.NORMAL)
        self.line_count.delete(1.0, tk.END)
        self.line_count.insert(tk.END, line_count_str)
        self.line_count.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = CodeEditor(root)
    root.mainloop()
