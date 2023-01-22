from tkinter import *
import tkinter as tk
from tkinter import messagebox

import common
import db_operations


class ItemDetailPage:
    def __init__(self, list_page, is_edit, db_name, selected_item=None):
        self.is_edit = is_edit
        self.list_page = list_page
        self.selected_item = selected_item
        self.db_name = db_name

        self.item_detail_page = tk.Toplevel(self.list_page)
        self.take_focus()
        self.item_detail_page.bind('<Return>', self.save_process)
        self.make_form_page()

        self.item_detail_page.protocol("WM_DELETE_WINDOW", self.close_process) 


    def make_form_page(self):
        if self.is_edit:
            title_label_text = 'Edit an Item'
        else:
            title_label_text = 'Add an Item'

        self.item_detail_page.geometry('400x430+450+70')
        self.item_detail_page.title(title_label_text)

        title_label = Label(self.item_detail_page, text=title_label_text, width=20, font=('bold', 14))
        title_label.place(x=100, y=30)

        label_x = 2
        entry_x = 130
        entry_width = 40
        initial_y = 70
        vertical_gap = 60

        url_label = Label(self.item_detail_page, text='URL', width=15, font=('bold', 10))
        url_label.place(x=label_x, y=(initial_y + 1 * vertical_gap))
        self.url_entry = Entry(self.item_detail_page, width=entry_width)
        self.url_entry.place(x=entry_x, y=(initial_y + 1 * vertical_gap)) 

        username_label = Label(self.item_detail_page, text='Username', width=15, font=('bold', 10))
        username_label.place(x=label_x, y=(initial_y + 2 * vertical_gap))
        self.username_entry = Entry(self.item_detail_page, width=entry_width)
        self.username_entry.place(x=entry_x, y=(initial_y + 2 * vertical_gap))

        password_label = Label(self.item_detail_page, text='Password', width=15, font=('bold', 10))
        password_label.place(x=label_x, y=(initial_y + 3 * vertical_gap))
        self.password_entry = Entry(self.item_detail_page, width=entry_width)
        self.password_entry.place(x=entry_x, y=(initial_y + 3 * vertical_gap))

        save_button = Button(self.item_detail_page, text='Save', command=self.save_process, width=10) 
        save_button.place(x=295, y=(initial_y + 4 * vertical_gap + 35))

        cancel_button = Button(self.item_detail_page, text='Cancel', command=self.close_process, width=10)
        cancel_button.place(x=25, y=(initial_y + 4 * vertical_gap + 35))

        if self.is_edit:
            self.set_entry_values()
    

    def set_entry_values(self):
        self.url_entry.insert(END, self.selected_item[0])
        self.username_entry.insert(END, self.selected_item[1])
        self.password_entry.insert(END, self.selected_item[3])


    def save_process(self, event=None):
        is_form_valid, item = self.validate_form()  

        if is_form_valid:
            if self.is_edit:
                item_id = self.selected_item[4]
                common.CommonClass().decrypt_db(self.db_name)
                is_successful = db_operations.DbOperations(self.db_name).update_item(item, item_id)
                common.CommonClass().encrypt_db(self.db_name)
            else:
                common.CommonClass().decrypt_db(self.db_name)
                is_successful = db_operations.DbOperations(self.db_name).insert_item(item)
                common.CommonClass().encrypt_db(self.db_name)

            if is_successful:
                self.close_process()
            else:
                messagebox.showerror('Error', 'Error occured while saving to Database', parent=self.item_detail_page)


    def validate_form(self):
        is_form_valid = False
        item = []

        url_value = self.url_entry.get()
        if not url_value:
            messagebox.showerror('Error', 'URL can not be empty', parent=self.item_detail_page)
            return is_form_valid, item

        username_value = self.username_entry.get()
        if not username_value:
            messagebox.showerror('Error', 'Username can not be empty', parent=self.item_detail_page)
            return is_form_valid, item
        
        password_value = self.password_entry.get()
        if not password_value:
            messagebox.showerror('Error', 'Password can not be empty', parent=self.item_detail_page)
            return is_form_valid, item

        is_form_valid = True
        item = [url_value, username_value, password_value]

        return is_form_valid, item
    

    def take_focus(self):
        self.item_detail_page.focus_set()
        self.list_page.attributes('-disabled', True)
    

    def close_process(self, event=None):
        self.list_page.attributes('-disabled', False)         
        self.item_detail_page.destroy()   