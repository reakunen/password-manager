import os
import json
import bcrypt
from tkinter.constants import BOTH, CENTER, END, LEFT, RIGHT, VERTICAL, Y
from generator import PasswordGenerator
from functools import partial
from password import PasswordMethods
from tkinter import PhotoImage
from customtkinter import * 

MASTER_PASSWORD_FILE = './passwords/master_password.json'

class PasswordManager:
    def __init__(self):
        self.window = CTk()
        self.window.update()
        self.window.title("Password Manager")
        self.window.geometry("1250x400")
        self.vault_methods = None

    def welcome_new_user(self):
        self.window.geometry("550x300")
        self.window.iconbitmap('./media/logo.ico')  # Set window icon
        logo = PhotoImage(file="./media/logo.png")  # Load logo image
        smaller_logo = logo.subsample(2, 2)  # resize
        logo_label = CTkLabel(self.window, image=smaller_logo, text="")
        logo_label.pack()

        label1 = CTkLabel(self.window, text="Sign Up: Create New Master Password")
        label1.configure(anchor=CENTER)
        label1.pack(pady=0)

        mp_entry_box = CTkEntry(self.window, width=200, show="*")
        mp_entry_box.pack()
        mp_entry_box.focus()

        label2 = CTkLabel(self.window, text="Enter the password again")
        label2.configure(anchor=CENTER)
        label2.pack(pady=0)

        rmp_entry_box = CTkEntry(self.window, width=200, show="*")
        rmp_entry_box.pack()

        self.feedback = CTkLabel(self.window, text_color="red", text="Must be a strong password")
        self.feedback.pack()

        save_btn = CTkButton(self.window, text="Create Password",
                          command=partial(self.save_master_password, mp_entry_box, rmp_entry_box))
        save_btn.pack(pady=0)

    def login_user(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        self.window.geometry("550x230")
        self.window.iconbitmap('./media/logo.ico')  # Set window icon
        logo = PhotoImage(file="./media/logo.png")  # Load logo image
        smaller_logo = logo.subsample(2, 2)  # resize
        logo_label = CTkLabel(self.window, image=smaller_logo, text="")
        logo_label.pack()

        label1 = CTkLabel(self.window, text="Login: Enter your master password")
        label1.configure(anchor=CENTER)
        label1.place(relx=0.5, rely=0.35, anchor=CENTER)  # Center horizontally

        self.password_entry_box = CTkEntry(self.window, width=200, show="*")
        self.password_entry_box.place(relx=0.5, rely=0.49, anchor=CENTER)  # Center horizontally
        self.password_entry_box.focus()

        self.feedback = CTkLabel(self.window, text="")
        self.feedback.place(relx=0.5, rely=0.55, anchor=CENTER)  # Center horizontally

        login_btn = CTkButton(self.window, text="Log In", command=partial(
            self.check_master_password, self.password_entry_box))
        login_btn.place(relx=0.5, rely=0.66, anchor=CENTER)  # Center horizontally

    def save_master_password(self, eb1, eb2):
        password1 = eb1.get()
        password2 = eb2.get()
        if password1 == password2:
            hashed_password = bcrypt.hashpw(password1.encode(), bcrypt.gensalt(rounds=13))
            with open(MASTER_PASSWORD_FILE, 'w') as file:
                json.dump({"password": hashed_password.decode()}, file)
            self.login_user()
        else:
            self.feedback.configure(text="Passwords do not match", fg="red")

    def check_master_password(self, eb):
        input_password = eb.get()
        with open(MASTER_PASSWORD_FILE, 'r') as file:
            stored_password = json.load(file)["password"].encode()
        if bcrypt.checkpw(input_password.encode(), stored_password):
            self.vault_methods = PasswordMethods(input_password)
            self.password_vault_screen()
        else:
            self.password_entry_box.delete(0, END)
            self.feedback.configure(text="Incorrect password", fg="red")

    def password_vault_screen(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        self.window.geometry("850x350")
        main_frame = CTkFrame(self.window)
        main_frame.pack(fill=BOTH, expand=1)

        main_canvas = CTkCanvas(main_frame)
        main_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        # main_scrollbar = CTkScrollbar(
        #     main_frame, direction='vertical', command=main_canvas.yview)
        # main_scrollbar.pack(side=RIGHT, fill=Y)

        # main_canvas.configureure(yscrollcommand=main_scrollbar.set)
        # main_canvas.bind('<configureure>', lambda e: main_canvas.configureure(
        #     scrollregion=main_canvas.bbox("all")))

        second_frame = CTkFrame(main_canvas)
        main_canvas.create_window((0, 0), window=second_frame, anchor="nw")

        generate_password_btn = CTkButton(second_frame, text="Generate Password", fg_color="green",
                                       command=PasswordGenerator)
        generate_password_btn.grid(row=1, column=2, pady=10, padx=10)

        add_password_btn = CTkButton(
            second_frame, text="Add New Password", fg_color="green", command=partial(self.vault_methods.add_password, self.password_vault_screen))
        add_password_btn.grid(row=1, column=3, pady=10, padx=10)

        lbl = CTkLabel(second_frame, text="Website", text_color="gray75")
        lbl.grid(row=2, column=0, padx=40, pady=10)
        lbl = CTkLabel(second_frame, text="Username", text_color="gray75")
        lbl.grid(row=2, column=1, padx=40, pady=10)
        lbl = CTkLabel(second_frame, text="Password", text_color="gray75")
        lbl.grid(row=2, column=2, padx=40, pady=10)

        for i, entry in enumerate(self.vault_methods.vault_data['vault']):
            platform_label = CTkLabel(second_frame, text=entry["platform"])
            platform_label.grid(column=0, row=i + 3)

            account_label = CTkLabel(second_frame, text=entry["userid"])
            account_label.grid(column=1, row=i + 3)

            decrypted_password = self.vault_methods.decrypt_password(entry["password"])
            password_label = CTkLabel(second_frame, text=decrypted_password)
            password_label.grid(column=2, row=i + 3)

            copy_btn = CTkButton(second_frame, text="Copy Password",
                              command=partial(self.copy_text, decrypted_password))
            copy_btn.grid(column=3, row=i + 3, pady=10, padx=10)
            update_btn = CTkButton(second_frame, text="Update Password",
                                command=partial(self.vault_methods.update_password, entry["id"], self.password_vault_screen))
            update_btn.grid(column=4, row=i + 3, pady=10, padx=10)
            remove_btn = CTkButton(second_frame, text="Delete Password", fg_color="red",
                                command=partial(self.vault_methods.remove_password, entry["id"], self.password_vault_screen))
            remove_btn.grid(column=5, row=i + 3, pady=10, padx=10)

    def copy_text(self, text):
        self.window.clipboard_clear()
        self.window.clipboard_append(text)


if __name__ == '__main__':
    if not os.path.exists(MASTER_PASSWORD_FILE):
        manager = PasswordManager()
        manager.welcome_new_user()
    else:
        manager = PasswordManager()
        manager.login_user()
    manager.window.mainloop()