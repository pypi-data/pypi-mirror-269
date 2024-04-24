import subprocess
import json
import pkg_resources
import os
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from tkinter import filedialog


def send_email():
    # Function to send the email
    def send():
        sender_name = sender_entry.get()
        receiver_email = receiver_entry.get()
        subject = subject_entry.get()
        message = message_entry.get("1.0", "end-1c")
        attachment = attachment_entry.get()
        tls = tls_var.get()

        sendemail_command = f"sendemail -xu {config['username']} -xp {config['password']} -s {config['smtp_server']} -o tls={tls} -f '{sender_name}' -t {receiver_email} -u '{subject}' -m '{message}'"
        
        if attachment:
            sendemail_command += f" -a '{attachment}'"

        try:
            subprocess.run(sendemail_command, shell=True, check=True)
            CTkMessagebox(title="Success", message="Email sent successfully!", icon="info", option_1="ok")
        except subprocess.CalledProcessError as e:
            CTkMessagebox(title="Error", message=f"\n{e}", icon="warning", option_1="ok")

    def select_attachment():
        filename = filedialog.askopenfilename()
        if filename:  # Check if a file was selected
            basename = os.path.basename(filename)  # Extract the filename from the full path
            attachment_entry.delete(0, ctk.END)
            attachment_entry.insert(0, basename)  # Display only the filename
            attachment_entry.filename = filename  # Store the full path in a new attribute


    # Function to open dialog box to edit config
    def edit_config():
        edit_window = ctk.CTkToplevel(root)
        edit_window.title("Edit Configuration")

        # Read configuration from file
        config = load_config()

        # Create text box to display converted text
        text_box = ctk.CTkTextbox(edit_window, wrap="word", height=150, width=400)
        text_box.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        text_box.insert(ctk.END, json.dumps(config, indent=4))  # Insert JSON content into text box

        # Save button to overwrite config file
        def save_config():
            new_config = json.loads(text_box.get("1.0", "end-1c"))  # Get JSON content from text box
            config_path = get_config_path()
            with open(config_path, "w") as config_file:
                json.dump(new_config, config_file, indent=4)
            CTkMessagebox(title="Success", message="Configuration saved successfully.", icon="info", option_1="ok")
            edit_window.destroy()
            # Reload the configuration
            global config
            config = load_config()

        save_button = ctk.CTkButton(edit_window, text="Save", command=save_config)
        save_button.grid(row=1, column=0, pady=10)

    root = ctk.CTk()
    root.title("Email Spoofer from AKM KORISHEE APURBO")
    root.geometry("800x550+500+0")
    root.resizable(False, False)

    # Read configuration from file
    global config
    config = load_config()

    if config:
        
        # Create a label with text "KORISHEE THE CYBERMASTER"
        label = ctk.CTkLabel(root, text="KORISHEE THE CYBERMASTER", font=("Comic Sans MS", 18 , "bold"))
        # Use sticky option to center the label horizontally
        label.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")
            
        sender_label = ctk.CTkLabel(root, text="Sender's Email:  ",font=("Latin Modern Mono Slanted", 16))
        sender_label.grid(row=1, column=0, sticky="w")
        
        sender_entry = ctk.CTkEntry(root, width=600,border_color="blue",font=("Latin Modern Mono Slanted", 16))
        sender_entry.grid(row=1, column=1, sticky="e")
    
        receiver_label = ctk.CTkLabel(root, text="Recipient's Email:  ",font=("Latin Modern Mono Slanted", 16))
        receiver_label.grid(row=2, column=0, sticky="w")

        receiver_entry = ctk.CTkEntry(root, width=600,border_color="red",font=("Latin Modern Mono Slanted", 16))
        receiver_entry.grid(row=2, column=1, sticky="e")

        subject_label = ctk.CTkLabel(root, text="Subject:  ", font=("Latin Modern Mono Slanted", 16))
        subject_label.grid(row=3, column=0, sticky="w")

        subject_entry = ctk.CTkEntry(root, width=600,border_color="blue",font=("Latin Modern Mono Slanted", 16))
        subject_entry.grid(row=3, column=1, sticky="e")

        message_label = ctk.CTkLabel(root, text="Message:  ",font=("Latin Modern Mono Slanted", 16))
        message_label.grid(row=4, column=0, sticky="w")

        message_entry = ctk.CTkTextbox(root, width=600, height=250,font=("TeX Gyre Pagella", 14,"bold"))
        message_entry.grid(row=4, column=1, sticky="e")

        # Add attachment entry and button
        attachment_label = ctk.CTkLabel(root, text="Attachment: ", font=("Latin Modern Mono Slanted", 16))
        attachment_label.grid(row=5, column=0, sticky="w")
        
        attachment_entry = ctk.CTkEntry(root, width=500, border_color="blue",text_color="red", font=("Latin Modern Mono Slanted", 16))
        attachment_entry.grid(row=5, column=1, sticky="w")

        attachment_button = ctk.CTkButton(root,width=100,border_color="red",hover_color="black", border_width=3,fg_color="blue", text="📎", command=select_attachment)
        attachment_button.grid(row=5, column=1, sticky="e")
        
        send_button = ctk.CTkButton(root, text="Send Email",font=("MathJax_Main", 16,"italic"),fg_color="blue",hover_color="purple",command=send)
        send_button.grid(row=7, column=0, columnspan=2, pady=10)






        
        # Add TLS toggle
        tls_var = ctk.StringVar(value="no")  # Default to TLS on
        tls_checkbutton = ctk.CTkCheckBox(root, text="Use TLS", variable=tls_var, onvalue="yes", offvalue="no")
        tls_checkbutton.grid(row=6, column=1, sticky="w")

    

        # Button to edit config
        edit_button = ctk.CTkButton(root, text="Edit Config",text_color="black", font=("MathJax_Main", 16, "italic"),fg_color="red",hover_color="green", command=edit_config)
        edit_button.grid(row=6, column=0, columnspan=2, pady=10,sticky="se")
    
        root.mainloop()
    else:
        CTkMessagebox(title="Error", message="Failed to load configuration.", icon="warning", option_1="ok")

def load_config():
    try:
        # Load the config.json file from the package data
        config_path = get_config_path()
        with open(config_path) as config_file:
            config = json.load(config_file)
        return config
    except FileNotFoundError:
        CTkMessagebox(title="Error", message="Config file not found or invalid.", icon="warning", option_1="ok")
        return None

def get_config_path():
    # Get the directory of the package data
    data_dir = pkg_resources.resource_filename("emailspoofergui", "data")
    # Construct the path to the config.json file
    config_path = os.path.join(data_dir, "config.json")
    return config_path

if __name__ == "__main__":
    send_email()
