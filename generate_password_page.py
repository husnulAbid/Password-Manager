from tkinter import *
import tkinter as tk
from tkinter import messagebox

import common
import db_operations


class GeneratePasswordPage:
    def __init__(self, login_page, db_name):
        self.login_page = login_page
        self.db_name = db_name

        self.generate_password_page = tk.Toplevel(self.login_page)
        self.take_focus()
        self.make_generate_password_page()
        self.generate_password_page.bind('<Return>', self.generate_process)
        self.generate_password_page.protocol("WM_DELETE_WINDOW", self.close_process)   

    def make_generate_password_page(self):
        self.generate_password_page.geometry('480x380+350+130')
        self.generate_password_page.title('Generate New Password')

        label_x = 2            
        entry_x = 130
        entry_width = 40
        initial_y = 40
        vertical_gap = 50

        title_label = Label(self.generate_password_page, text='Generate New Password', width=20, font=('bold', 14))
        title_label.place(x=label_x+130, y=initial_y-25)

        old_user_name_label = Label(self.generate_password_page, text="Old Username", width=15, font=('bold', 10))
        old_user_name_label.place(x=label_x, y=(initial_y + 1 * vertical_gap))
        self.old_user_name_entry = Entry(self.generate_password_page, width=entry_width)
        self.old_user_name_entry.place(x=entry_x, y=(initial_y + 1 * vertical_gap))  

        old_password_label = Label(self.generate_password_page, text="Old Password", width=15, font=('bold', 10))
        old_password_label.place(x=label_x, y=(initial_y + 2 * vertical_gap))
        self.old_password_entry = Entry(self.generate_password_page, show='*', width=entry_width)
        self.old_password_entry.place(x=entry_x, y=(initial_y + 2 * vertical_gap))

        new_user_name_label = Label(self.generate_password_page, text="New Username", width=15, font=('bold', 10))
        new_user_name_label.place(x=label_x, y=(initial_y + 3 * vertical_gap))
        self.new_user_name_entry = Entry(self.generate_password_page, width=entry_width)
        self.new_user_name_entry.place(x=entry_x, y=(initial_y + 3 * vertical_gap))  

        new_password_label = Label(self.generate_password_page, text="New Password", width=15, font=('bold', 10))
        new_password_label.place(x=label_x, y=(initial_y + 4 * vertical_gap))
        self.new_password_entry = Entry(self.generate_password_page, show='*', width=entry_width)
        self.new_password_entry.place(x=entry_x, y=(initial_y + 4 * vertical_gap))

        confirm_password_label = Label(self.generate_password_page, text="Confirm Password", width=15, font=('bold', 10))
        confirm_password_label.place(x=label_x, y=(initial_y + 5 * vertical_gap))
        self.confirm_password_entry = Entry(self.generate_password_page, show='*', width=entry_width)
        self.confirm_password_entry.place(x=entry_x, y=(initial_y + 5 * vertical_gap))

        generate_new_password_button = Button(self.generate_password_page, text='Generate', command=self.generate_process, width=15)  
        generate_new_password_button.place(x=165, y=(initial_y + 6 * vertical_gap))

        cancel_button = Button(self.generate_password_page, text='Cancel', command=self.close_process, width=10) 
        cancel_button.place(x=295, y=(initial_y + 6 * vertical_gap))
    

    def generate_process(self, event=None):
        old_user_name_value = self.old_user_name_entry.get()
        old_password_value = self.old_password_entry.get()

        new_user_name_value = self.new_user_name_entry.get()
        new_password_value = self.new_password_entry.get()
        confirm_password_value = self.confirm_password_entry.get()

        if not old_password_value or not old_user_name_value or not new_password_value or not new_user_name_value or not confirm_password_value:
            messagebox.showerror('Error', 'Please fill all fields', parent=self.generate_password_page)
        elif new_password_value != confirm_password_value:
            messagebox.showerror('Error', 'New Passwords Do not match', parent=self.generate_password_page)
        else:
            common.CommonClass().decrypt_db(self.db_name)
            item = db_operations.DbOperations(self.db_name).fetch_item_from_master_table()
            common.CommonClass().encrypt_db(self.db_name)
            user_name_from_item = item[0][0][0]
            password_from_item = item[0][0][1]

            if old_user_name_value == user_name_from_item and old_password_value == password_from_item:
                common.CommonClass().decrypt_db(self.db_name)
                db_operations.DbOperations(self.db_name).update_item_from_master_table(old_user_name_value, old_password_value, new_user_name_value, new_password_value)
                common.CommonClass().encrypt_db(self.db_name)
                
                self.close_process()
                messagebox.showinfo('Success', 'New Password Generated')
            else:
                messagebox.showerror('Error', 'Old Username or Password Invalid', parent=self.generate_password_page)
    
    def take_focus(self):
        self.generate_password_page.focus_set()
        self.login_page.attributes('-disabled', True)

    def close_process(self, event=None):
        self.login_page.attributes('-disabled', False)
        self.generate_password_page.destroy()