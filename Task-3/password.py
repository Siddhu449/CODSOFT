import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import pyperclip

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Password Generator")
        self.root.geometry("500x450")
        self.root.configure(bg='#2c3e50')
        self.root.resizable(False, False)
        
        # Initialize variables
        self.password_var = tk.StringVar()
        self.length_var = tk.IntVar(value=12)
        self.uppercase_var = tk.BooleanVar(value=True)
        self.lowercase_var = tk.BooleanVar(value=True)
        self.numbers_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        
        self.create_widgets()
    
    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self.root, bg='#34495e', height=80)
        header_frame.pack(fill='x', padx=10, pady=10)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🔐 Secure Password Generator",
            font=('Arial', 18, 'bold'),
            bg='#34495e',
            fg='white'
        )
        title_label.pack(pady=20)
        
        # Main container
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Length selection
        length_frame = tk.Frame(main_frame, bg='#2c3e50')
        length_frame.pack(fill='x', pady=10)
        
        tk.Label(
            length_frame,
            text="Password Length:",
            font=('Arial', 12, 'bold'),
            bg='#2c3e50',
            fg='#ecf0f1'
        ).pack(side='left')
        
        length_scale = tk.Scale(
            length_frame,
            from_=6,
            to=32,
            orient='horizontal',
            variable=self.length_var,
            bg='#2c3e50',
            fg='#ecf0f1',
            highlightbackground='#2c3e50',
            length=200
        )
        length_scale.pack(side='right', padx=10)
        
        # Character options
        options_frame = tk.Frame(main_frame, bg='#34495e', relief='ridge', bd=2)
        options_frame.pack(fill='x', pady=15, padx=10)
        
        options_title = tk.Label(
            options_frame,
            text="Character Types:",
            font=('Arial', 12, 'bold'),
            bg='#34495e',
            fg='#ecf0f1'
        )
        options_title.pack(pady=10)
        
        # Checkboxes
        checkbox_frame = tk.Frame(options_frame, bg='#34495e')
        checkbox_frame.pack(pady=10)
        
        uppercase_cb = tk.Checkbutton(
            checkbox_frame,
            text="Uppercase Letters (A-Z)",
            variable=self.uppercase_var,
            font=('Arial', 10),
            bg='#34495e',
            fg='#ecf0f1',
            selectcolor='#2c3e50'
        )
        uppercase_cb.grid(row=0, column=0, sticky='w', padx=20, pady=5)
        
        lowercase_cb = tk.Checkbutton(
            checkbox_frame,
            text="Lowercase Letters (a-z)",
            variable=self.lowercase_var,
            font=('Arial', 10),
            bg='#34495e',
            fg='#ecf0f1',
            selectcolor='#2c3e50'
        )
        lowercase_cb.grid(row=0, column=1, sticky='w', padx=20, pady=5)
        
        numbers_cb = tk.Checkbutton(
            checkbox_frame,
            text="Numbers (0-9)",
            variable=self.numbers_var,
            font=('Arial', 10),
            bg='#34495e',
            fg='#ecf0f1',
            selectcolor='#2c3e50'
        )
        numbers_cb.grid(row=1, column=0, sticky='w', padx=20, pady=5)
        
        symbols_cb = tk.Checkbutton(
            checkbox_frame,
            text="Symbols (!@#$%^&*)",
            variable=self.symbols_var,
            font=('Arial', 10),
            bg='#34495e',
            fg='#ecf0f1',
            selectcolor='#2c3e50'
        )
        symbols_cb.grid(row=1, column=1, sticky='w', padx=20, pady=5)
        
        # Generate button
        generate_btn = tk.Button(
            main_frame,
            text="🔄 Generate Password",
            font=('Arial', 12, 'bold'),
            bg='#27ae60',
            fg='white',
            width=20,
            height=2,
            command=self.generate_password
        )
        generate_btn.pack(pady=15)
        
        # Password display
        password_frame = tk.Frame(main_frame, bg='#2c3e50')
        password_frame.pack(fill='x', pady=10)
        
        tk.Label(
            password_frame,
            text="Generated Password:",
            font=('Arial', 11, 'bold'),
            bg='#2c3e50',
            fg='#bdc3c7'
        ).pack(anchor='w')
        
        # Password entry with copy button
        entry_frame = tk.Frame(password_frame, bg='#2c3e50')
        entry_frame.pack(fill='x', pady=5)
        
        self.password_entry = tk.Entry(
            entry_frame,
            textvariable=self.password_var,
            font=('Arial', 12, 'bold'),
            justify='center',
            state='readonly',
            bg='#34495e',
            fg='#2ecc71',
            readonlybackground='#34495e'
        )
        self.password_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        copy_btn = tk.Button(
            entry_frame,
            text="📋 Copy",
            font=('Arial', 10, 'bold'),
            bg='#3498db',
            fg='white',
            command=self.copy_to_clipboard
        )
        copy_btn.pack(side='right')
        
        # Strength indicator
        self.strength_frame = tk.Frame(main_frame, bg='#2c3e50')
        self.strength_frame.pack(fill='x', pady=10)
        
        self.strength_label = tk.Label(
            self.strength_frame,
            text="",
            font=('Arial', 11, 'bold'),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        self.strength_label.pack()
        
        # Password tips
        tips_frame = tk.Frame(main_frame, bg='#34495e', relief='ridge', bd=2)
        tips_frame.pack(fill='x', pady=10, padx=10)
        
        tips_text = """
💡 Password Tips:
• Use at least 12 characters
• Combine uppercase, lowercase, numbers & symbols
• Avoid common words and patterns
• Use unique passwords for different accounts
        """
        
        tips_label = tk.Label(
            tips_frame,
            text=tips_text,
            font=('Arial', 9),
            bg='#34495e',
            fg='#bdc3c7',
            justify='left'
        )
        tips_label.pack(pady=10)
    
    def generate_password(self):
        """Generate a random password based on user preferences"""
        # Check if at least one character type is selected
        if not any([self.uppercase_var.get(), self.lowercase_var.get(), 
                   self.numbers_var.get(), self.symbols_var.get()]):
            messagebox.showwarning("Selection Error", "Please select at least one character type!")
            return
        
        # Define character sets
        uppercase = string.ascii_uppercase if self.uppercase_var.get() else ""
        lowercase = string.ascii_lowercase if self.lowercase_var.get() else ""
        numbers = string.digits if self.numbers_var.get() else ""
        symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?" if self.symbols_var.get() else ""
        
        # Combine all characters
        all_chars = uppercase + lowercase + numbers + symbols
        
        if not all_chars:
            messagebox.showwarning("Selection Error", "Please select at least one character type!")
            return
        
        # Generate password
        length = self.length_var.get()
        password = ''.join(random.choice(all_chars) for _ in range(length))
        
        # Ensure at least one character from each selected type is included
        password_chars = list(password)
        random.shuffle(password_chars)
        password = ''.join(password_chars)
        
        self.password_var.set(password)
        self.assess_password_strength(password)
    
    def assess_password_strength(self, password):
        """Assess and display password strength"""
        length = len(password)
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_symbol = any(not c.isalnum() for c in password)
        
        score = 0
        if length >= 12: score += 2
        elif length >= 8: score += 1
        
        if has_upper: score += 1
        if has_lower: score += 1
        if has_digit: score += 1
        if has_symbol: score += 1
        
        # Clear previous strength indicators
        for widget in self.strength_frame.winfo_children():
            widget.destroy()
        
        if score >= 6:
            strength = "🔒 Very Strong"
            color = "#27ae60"
        elif score >= 4:
            strength = "🔐 Strong"
            color = "#2ecc71"
        elif score >= 3:
            strength = "⚠️  Medium"
            color = "#f39c12"
        else:
            strength = "🔓 Weak"
            color = "#e74c3c"
        
        self.strength_label = tk.Label(
            self.strength_frame,
            text=f"Password Strength: {strength}",
            font=('Arial', 11, 'bold'),
            bg='#2c3e50',
            fg=color
        )
        self.strength_label.pack()
    
    def copy_to_clipboard(self):
        """Copy password to clipboard"""
        password = self.password_var.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Copied!", "Password copied to clipboard! 📋")
        else:
            messagebox.showwarning("No Password", "Please generate a password first!")

# Create and run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()