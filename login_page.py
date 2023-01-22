import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import common
import list_page
import db_operations
import generate_password_page


class LoginPage:
    def __init__(self, db_name):
        self.db_name = db_name
        self.login_page = Tk()
        self.make_landing_page()
        self.login_page.bind('<Return>', self.login_process)
        self.login_page.mainloop()

    def make_landing_page(self):
        self.login_page.geometry('480x380+350+130')       
        self.login_page.title('Password Storage')

        self.make_page_frame()
        self.make_login_frame()

    def make_page_frame(self):
        list_frame = Frame(self.login_page)                     
        list_frame.grid(row=0, column=0, sticky='nsew', pady=5, padx=5)

    def make_login_frame(self):
        label_x = 2             
        entry_x = 130
        entry_width = 40
        initial_y = 40
        vertical_gap = 50

        title_label = Label(self.login_page, text='Login Page', width=20, font=('bold', 14))
        title_label.place(x=label_x+130, y=initial_y-25)

        user_name_label = Label(self.login_page, text="Username", width=15, font=('bold', 10))
        user_name_label.place(x=label_x, y=(initial_y + 1 * vertical_gap))
        self.user_name_entry = Entry(self.login_page, width=entry_width)
        self.user_name_entry.place(x=entry_x, y=(initial_y + 1 * vertical_gap))  

        password_label = Label(self.login_page, text="Password", width=15, font=('bold', 10))
        password_label.place(x=label_x, y=(initial_y + 2 * vertical_gap))
        self.password_entry = Entry(self.login_page, show='*', width=entry_width)
        self.password_entry.place(x=entry_x, y=(initial_y + 2 * vertical_gap))

        generate_password_button = Button(self.login_page, text='Generate Password', command=self.generate_password_process, width=15)  # declaring the buttons
        generate_password_button.place(x=165, y=(initial_y + 3.5 * vertical_gap))

        login_button = Button(self.login_page, text='Login', command=self.login_process, width=10)  # declaring the buttons
        login_button.place(x=295, y=(initial_y + 3.5 * vertical_gap))

    def generate_password_process(self):
        temp = generate_password_page.GeneratePasswordPage(self.login_page, self.db_name)
        self.login_page.wait_window(temp.generate_password_page)


    def login_process(self, event=None):
        user_name_value = self.user_name_entry.get()
        password_value = self.password_entry.get()

        common.CommonClass().decrypt_db(self.db_name)
        item = db_operations.DbOperations(self.db_name).fetch_item_from_master_table()
        common.CommonClass().encrypt_db(self.db_name)

        user_name_from_item = item[0][0][0]
        password_from_item = item[0][0][1]

        if user_name_value == user_name_from_item and password_value == password_from_item:
            for widget in self.login_page.winfo_children():
                widget.destroy()

            list_page.ListPage(self.login_page, self.db_name)
        else:
            messagebox.showerror('Error', 'Access Denied', parent=self.login_page)