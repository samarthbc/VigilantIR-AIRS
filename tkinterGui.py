import tkinter as tk
from tkinter import ttk
import subprocess
import threading

# To store the process objects
processes = {'DoS': None, 'Bruteforce': None, 'SQLInjection': None, 'Fileupload': None}

# Function to start or stop a process based on the toggle
def toggle_attack(attack_type):
    global processes

    if attack_type == 'DoS':
        if dos_var.get():
            # Start the DoS.py script and capture output
            processes['DoS'] = subprocess.Popen(
                ['python', 'DoS.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            display_output("DoS detection started\n")
            thread = threading.Thread(target=read_process_output, args=(processes['DoS'],))
            thread.start()
        else:
            # Stop the process
            if processes['DoS']:
                processes['DoS'].terminate()
                processes['DoS'] = None
                display_output("DoS detection stopped\n")

    elif attack_type == 'Bruteforce':
        if bf_var.get():
            # Start the hack.py script and capture output
            processes['Bruteforce'] = subprocess.Popen(
                ['python', 'hack.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            display_output("Bruteforce detection started\n")
            thread = threading.Thread(target=read_process_output, args=(processes['Bruteforce'],))
            thread.start()
        else:
            # Stop the process
            if processes['Bruteforce']:
                processes['Bruteforce'].terminate()
                processes['Bruteforce'] = None
                display_output("Bruteforce detection stopped\n")

    elif attack_type == 'SQLInjection':
        if sql_var.get():
            # Start the sqlinj.py script and capture output
            processes['SQLInjection'] = subprocess.Popen(
                ['python', 'sqlinj.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            display_output("SQL Injection detection started\n")
            thread = threading.Thread(target=read_process_output, args=(processes['SQLInjection'],))
            thread.start()
        else:
            # Stop the process
            if processes['SQLInjection']:
                processes['SQLInjection'].terminate()
                processes['SQLInjection'] = None
                display_output("SQL Injection detection stopped\n")

    elif attack_type == 'Fileupload':
        if fle_var.get():
            processes['Fileupload'] = subprocess.Popen(
                ['python', 'FileUpload.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            display_output("File Upload detection started\n")
            thread = threading.Thread(target=read_process_output, args=(processes['Fileupload'],))
            thread.start()
        else:
            # Stop the process
            if processes['Fileupload']:
                processes['Fileupload'].terminate()
                processes['Fileupload'] = None
                display_output("File Upload detection stopped\n")


# Function to read process output and display it in the Text widget
def read_process_output(process):
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            display_output(output)

    # Also read any error messages
    error = process.stderr.read()
    if error:
        display_output(error)


# Function to display the output in the Text widget
def display_output(message):
    output_text.configure(state='normal')
    output_text.insert(tk.END, message)
    output_text.see(tk.END)
    output_text.configure(state='disabled')


# Setup the GUI window
root = tk.Tk()
root.title("VigilantIR: Automated Incident Response")

# Labels for section headings
toggle_label = tk.Label(root, text="VigilantIR", font=("Helvetica", 14, "bold"))
output_label = tk.Label(root, text="VigilantIR Console:", font=("Helvetica", 10, "bold"))

# Toggle switches for attacks
dos_var = tk.BooleanVar()
bf_var = tk.BooleanVar()
sql_var = tk.BooleanVar()
fle_var = tk.BooleanVar()

dos_toggle = ttk.Checkbutton(root, text="DoS Detection                ", variable=dos_var, command=lambda: toggle_attack('DoS'))
bf_toggle = ttk.Checkbutton(root, text="Bruteforce Detection     ", variable=bf_var,
                            command=lambda: toggle_attack('Bruteforce'))
sql_toggle = ttk.Checkbutton(root, text="SQL Injection Detection", variable=sql_var,
                             command=lambda: toggle_attack('SQLInjection'))
fle_toggle = ttk.Checkbutton(root, text="Malicious File Detection", variable=fle_var,
                             command=lambda: toggle_attack('Fileupload'))

# Display panel (Text widget) for output
output_text = tk.Text(root, height=15, width=80, state='disabled')

# Packing the widgets
toggle_label.pack(pady=(10,0))  # Section heading for toggles
sub_title_label = tk.Label(root, text="To enchance and monitor your protection", font=("Arial", 12))
sub_title_label.pack(pady=(0,10))
dos_toggle.pack(pady=(5,0))
bf_toggle.pack(pady=0)
sql_toggle.pack(pady=(0))
fle_toggle.pack(pady=(0,5))

output_label.pack(pady=(20,0))  # Section heading for output panel
output_text.pack(padx=20, pady=10)

# Content section at the bottom
content_label = tk.Label(root, text="Project by:", font=("Arial", 8))
content_label.pack(pady=(10,0))
content_label = tk.Label(root, text="Dhruthi\tNikita\tNikhita\tSamarth", font=("Arial", 8))
content_label.pack(pady=(0,0))

# Run the GUI loop
root.mainloop()
