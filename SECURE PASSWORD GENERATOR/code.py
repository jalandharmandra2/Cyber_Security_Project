import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
import math
import string
import webbrowser
import os

# Function definitions
def generate_password():
    try:
        password_length = int(length_entry.get())
        num_passwords = int(num_passwords_entry.get())
    except ValueError:
        result_label.config(text="Invalid input. Please enter valid numbers.")
        return

    if not (7 <= password_length <= 20) or not (1 <= num_passwords <= 5):
        result_label.config(text="Length must be 7-20 and passwords 1-5.")
        return

    lowercase_chars = string.ascii_lowercase if lowercase_var.get() else ''
    uppercase_chars = string.ascii_uppercase if uppercase_var.get() else ''
    digit_chars = string.digits if digits_var.get() else ''
    special_chars = string.punctuation if special_chars_var.get() else ''

    all_chars = lowercase_chars + uppercase_chars + digit_chars + special_chars

    if not all_chars:
        result_label.config(text="Please select at least one character type.")
    else:
        for row in result_table.get_children():
            result_table.delete(row)

        for _ in range(num_passwords):
            password = ''.join(random.choice(all_chars) for _ in range(password_length))
            strength = check_password_strength(password)
            crack_time = calculate_crack_time(password)

            result_table.insert("", tk.END, values=(password, strength, crack_time))

        copy_button.config(state=tk.NORMAL)  # Enable the copy button

def copy_to_clipboard():
    password_texts = [result_table.item(row)["values"][0] for row in result_table.get_children()]
    passwords = '\n'.join(password_texts)  # Join passwords with newline characters
    window.clipboard_clear()
    window.clipboard_append(passwords)
    window.update()  # Keep the clipboard content after the window is closed
    copy_button.config(text="Copied!", state=tk.DISABLED)

def refresh_form():
    # Only clear the result table and reset the copy button
    for row in result_table.get_children():
        result_table.delete(row)

    copy_button.config(text="Copy to Clipboard", state=tk.DISABLED)
    result_label.config(text="")

    # Reset checkboxes
    lowercase_var.set(0)
    uppercase_var.set(0)
    digits_var.set(0)
    special_chars_var.set(0)

def save_to_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if not file_path:
        return

    with open(file_path, 'w') as file:
        for row in result_table.get_children():
            password = result_table.item(row)["values"][0]
            file.write(password + '\n')

    result_label.config(text="Passwords saved to file.")

def check_password_strength(password):
    score = 0
    if len(password) >= 8:
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.islower() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in string.punctuation for c in password):
        score += 1

    strength = {
        5: 'Very Strong',
        4: 'Strong',
        3: 'Moderate',
        2: 'Weak',
        1: 'Very Weak',
        0: 'Very Weak'
    }

    return strength[score]

def calculate_crack_time(password):
    base_time = 1e-6  # 1 microsecond per attempt
    attempts_per_second = 1e9  # 1 billion attempts per second
    possible_characters = 26 + 26 + 10 + 32  # upper, lower, digits, special chars
    combinations = math.pow(possible_characters, len(password))
    time_in_seconds = combinations / attempts_per_second

    return format_time(time_in_seconds)

def format_time(seconds):
    units = [
        ('centuries', 60 * 60 * 24 * 365 * 100),
        ('years', 60 * 60 * 24 * 365),
        ('days', 60 * 60 * 24),
        ('hours', 60 * 60),
        ('minutes', 60),
        ('seconds', 1)
    ]

    for name, sec in units:
        if seconds >= sec:
            value = int(seconds // sec)
            return f"{value} {name}"

    return "less than a second"

def show_project_info():
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "project info .html")
    if os.path.exists(file_path):
        webbrowser.open(f"file:///{os.path.abspath(file_path)}")
    else:
        messagebox.showerror("Error", "Project info file not found.")



# Create the main window
window = tk.Tk()
window.title("Password Generator")
window.geometry("400x550")  # Reduced width for the window
window.attributes('-alpha', 1.0)  # Adjust transparency
window.config(bg='#0D0D0D')  # Shiny Black
shiny_silver = '#C0C0C0'
font_style = ("Arial", 10)  # Font style

# Add a Project Info button at the top
project_info_button = tk.Button(window, text="Project Info", command=show_project_info, bg='#0000FF', fg='#FFFFFF', font=font_style)
project_info_button.pack(pady=5)

# Create a frame for input elements
input_frame = tk.Frame(window, bg='#0D0D0D')
input_frame.pack(pady=10)

# Create a table-like structure for input elements
length_label = tk.Label(input_frame, text="Password Length:", bg='#0D0D0D', fg=shiny_silver, font=font_style)
length_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
length_entry = tk.Entry(input_frame, width=15, bg='#1A1A1A', fg=shiny_silver, insertbackground='white', font=font_style)
length_entry.grid(row=0, column=1, padx=5, pady=5, sticky="e")

num_passwords_label = tk.Label(input_frame, text="Number of Passwords:", bg='#0D0D0D', fg=shiny_silver, font=font_style)
num_passwords_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
num_passwords_entry = tk.Entry(input_frame, width=15, bg='#1A1A1A', fg=shiny_silver, insertbackground='white', font=font_style)
num_passwords_entry.grid(row=1, column=1, padx=5, pady=5, sticky="e")

# Create a frame for checkboxes
checkbox_frame = tk.Frame(window, bg='#0D0D0D')
checkbox_frame.pack(pady=10)

# Arrange checkboxes in a table-like format
lowercase_var = tk.IntVar()
lowercase_check = tk.Checkbutton(checkbox_frame, text="Include Lowercase Letters", variable=lowercase_var, bg='#0D0D0D', fg=shiny_silver, selectcolor='#1A1A1A', font=font_style)
lowercase_check.grid(row=0, column=0, padx=5, pady=5, sticky="w")

uppercase_var = tk.IntVar()
uppercase_check = tk.Checkbutton(checkbox_frame, text="Include Uppercase Letters", variable=uppercase_var, bg='#0D0D0D', fg=shiny_silver, selectcolor='#1A1A1A', font=font_style)
uppercase_check.grid(row=0, column=1, padx=5, pady=5, sticky="w")

digits_var = tk.IntVar()
digits_check = tk.Checkbutton(checkbox_frame, text="Include Digits", variable=digits_var, bg='#0D0D0D', fg=shiny_silver, selectcolor='#1A1A1A', font=font_style)
digits_check.grid(row=1, column=0, padx=5, pady=5, sticky="w")

special_chars_var = tk.IntVar()
special_chars_check = tk.Checkbutton(checkbox_frame, text="Include Special Characters", variable=special_chars_var, bg='#0D0D0D', fg=shiny_silver, selectcolor='#1A1A1A', font=font_style)
special_chars_check.grid(row=1, column=1, padx=5, pady=5, sticky="w")

# Generate Password Button
generate_button = tk.Button(window, text="Generate Password", command=generate_password, bg='#4CAF50', fg='#FFFFFF', font=font_style)
generate_button.pack(pady=10)

# Configure Treeview style
style = ttk.Style()
style.configure("Treeview",
                background='#FFFFFF',  # White background
                foreground='#0D0D0D',  # Shiny black text
                rowheight=20,  # Adjust row height if needed
                fieldbackground='#FFFFFF')  # White background for fields
style.map('Treeview', background=[('selected', '#C0C0C0')])  # Shiny silver background when selected

# Add a Treeview widget for displaying the passwords in a tabular format
result_table = ttk.Treeview(window, columns=("Password", "Strength", "Crack Time"), show='headings', height=5)
result_table.heading("Password", text="Password")
result_table.heading("Strength", text="Strength")
result_table.heading("Crack Time", text="Crack Time")

result_table.column("Password", width=120)  # Adjust width of the columns
result_table.column("Strength", width=120)
result_table.column("Crack Time", width=120)

result_table.pack(pady=10)  # Pack the Treeview

result_label = tk.Label(window, text="", font=("Arial", 11), wraplength=300, bg='#0D0D0D', fg=shiny_silver)
result_label.pack(pady=5)

# Add a frame to hold the buttons
button_frame = tk.Frame(window, bg='#0D0D0D')
button_frame.pack(pady=1)  # Reduced padding above and below the frame

copy_button = tk.Button(button_frame, text="Copy to Clipboard", command=copy_to_clipboard, state=tk.DISABLED, bg='#4CAF50', fg='#FFFFFF', font=font_style)
refresh_button = tk.Button(button_frame, text="Refresh", command=refresh_form, bg='#4CAF50', fg='#000000', font=font_style)
save_button = tk.Button(button_frame, text="Save", command=save_to_file, bg='#4CAF50', fg='#FFFFFF', font=font_style)

# Pack the buttons inside the frame with reduced padding between them
copy_button.pack(side=tk.LEFT, padx=4)
refresh_button.pack(side=tk.LEFT, padx=4)
save_button.pack(side=tk.LEFT, padx=4)

# Start the Tkinter main loop
window.mainloop()
