import pyperclip
import webbrowser
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import common
import db_operations
import item_detail_page


class ListPage:
    def __init__(self, list_page, db_name):
        self.db_name = db_name
        self.list_page = list_page

        self.list_page.bind('<a>', self.add_item)
        self.list_page.bind('<e>', self.edit_item)
        self.list_page.bind('<d>', self.delete_a_item)
        self.list_page.bind('<g>', self.go_to_web)
        self.list_page.bind('<q>', self.copy_username)
        self.list_page.bind('<w>', self.copy_password)

        common.CommonClass().decrypt_db(self.db_name)
        self.item_list = db_operations.DbOperations(self.db_name).fetch_items()
        common.CommonClass().encrypt_db(self.db_name)

        self.make_list_page()


    def make_list_page(self):
        self.list_page.geometry('920x275+200+170')
        self.list_page.title('Password List')
    
        self.make_button_frame()
        self.make_list_frame()


    def make_button_frame(self):
        button_frame = Frame(self.list_page)
        button_frame.grid(row=0, column=1, sticky='nswe')

        add_button = Button(button_frame, text='Add', font=('', 9, 'bold'), command=self.add_item, width=13, borderwidth=2)   
        edit_button = Button(button_frame, text='Edit', font=('', 9, 'bold'), command=self.edit_item, width=13, borderwidth=2)
        delete_button = Button(button_frame, text='Delete', font=('', 9, 'bold'), command=self.delete_a_item, width=13, borderwidth=2)
        copy_username_button = Button(button_frame, text='Copy Username', font=('', 9, 'bold'), command=self.copy_username , width=13, borderwidth=2)
        copy_password_button = Button(button_frame, text='Copy Password', font=('', 9, 'bold'), command=self.copy_password , width=13, borderwidth=2)
        goto_web_button = Button(button_frame, text='Go to Web', font=('', 9, 'bold'), command=self.go_to_web, width=13, borderwidth=2)
        delete_all_button = Button(button_frame, text='Delete All', font=('', 9, 'bold'), command=self.delete_all_item, width=13, borderwidth=2)

        add_button.grid(row=1, column=1, sticky='nswe', pady=(20, 5), padx=5)      
        edit_button.grid(row=2, column=1, sticky='nswe', pady=5, padx=5)
        delete_button.grid(row=3, column=1, sticky='nswe', pady=5, padx=5)
        copy_username_button.grid(row=4, column=1, sticky='nswe', pady=5, padx=5)
        copy_password_button.grid(row=5, column=1, sticky='nswe', pady=5, padx=5)
        goto_web_button.grid(row=6, column=1, sticky='nswe', pady=5, padx=5)
        delete_all_button.grid(row=7, column=1, sticky='nswe', pady=5, padx=5)
    

    def make_list_frame(self):
        list_frame = Frame(self.list_page)                      
        list_frame.grid(row=0, column=0, sticky='nsew', pady=5, padx=5)

        style = ttk.Style()
        style.configure('Treeview.Heading', font=('', 9, 'bold'))  

        self.item_list_gui = ttk.Treeview(list_frame, height=12, column=('c1', 'c2', 'c3'), show='headings', selectmode='browse')

        self.item_list_gui.column('#1', anchor=tk.CENTER, width=370)  
        self.item_list_gui.column('#2', anchor=tk.CENTER, width=210)
        self.item_list_gui.column('#3', anchor=tk.CENTER, width=170)

        self.item_list_gui.heading('#1', text='URL')      
        self.item_list_gui.heading('#2', text='Username')
        self.item_list_gui.heading('#3', text='Password')

        self.item_list_gui.bind('<<TreeViewSelect>>', self.on_tree_select)  
        self.item_list_gui.grid(row=0, column=0, sticky='nsew')

        self.insert_to_list()
        self.bind_scrollbar_with_list(list_frame)


    def on_tree_select(self, event):                 
        item_value = ''
        for item in self.item_list_gui.selection():
            item_value = self.item_list_gui.item(item, 'value')

        return item_value


    def add_item(self, event=None):
        is_edit = False
        temp = item_detail_page.ItemDetailPage(self.list_page, is_edit, self.db_name)
        self.list_page.wait_window(temp.item_detail_page)
        self.refresh_list()
    

    def edit_item(self, event=None):
        is_edit = True
        selected_item = self.on_tree_select('event')

        if selected_item:
            temp = item_detail_page.ItemDetailPage(self.list_page, is_edit, self.db_name, selected_item)
            self.list_page.wait_window(temp.item_detail_page)
            self.refresh_list()
        else:
            messagebox.showinfo('Info', 'Please select an item to Edit')
    

    def delete_a_item(self, event=None):
        selected_item = self.on_tree_select('event')

        if selected_item:
            response = messagebox.askyesno('Confirmation', "Are you sure that you want to Delete?", icon='warning')

            if response:
                item_id = selected_item[4]

                common.CommonClass().decrypt_db(self.db_name)
                is_successful = db_operations.DbOperations(self.db_name).delete_item(item_id)
                common.CommonClass().encrypt_db(self.db_name)

                if is_successful:
                    self.refresh_list()
                else:
                    messagebox.showerror('Error', 'Error occured while deleting from Db')
        else:
            messagebox.showinfo('Info', 'Please select an item to Remove')
    

    def copy_username(self, event=None):
        selected_item = self.on_tree_select('event')

        if selected_item:
            pyperclip.copy(selected_item[1])
        else:
            messagebox.showinfo('Info', 'Please select an item to Copy')
    

    def copy_password(self, event=None):
        selected_item = self.on_tree_select('event')

        if selected_item:
            pyperclip.copy(selected_item[3])
        else:
            messagebox.showinfo('Info', 'Please select an item to Copy')
    

    def go_to_web(self, event=None):
        selected_item = self.on_tree_select('event')

        if selected_item:
            webbrowser.open(selected_item[0])
        else:
            messagebox.showinfo('Info', 'Please select an item to Navigate to Web')
    

    def delete_all_item(self):
        response = messagebox.askyesno('Confirmation', "Are you sure that you want to Delete ALL?", icon='warning')

        if response:
            common.CommonClass().decrypt_db(self.db_name)
            is_successful = db_operations.DbOperations(self.db_name).delete_all_item()
            common.CommonClass().encrypt_db(self.db_name)

            if is_successful:
                self.refresh_list()
            else:
                messagebox.showerror('Error', 'Error occured while deleting all item from Db')


    def refresh_list(self):
        common.CommonClass().decrypt_db(self.db_name)
        self.item_list = db_operations.DbOperations(self.db_name).fetch_items()
        common.CommonClass().encrypt_db(self.db_name)
        self.insert_to_list()
    

    def insert_to_list(self):
        self.clear_list()

        for row in self.item_list:
            value_arr = [row[0], row[1], '*******', row[2], row[3]]
            self.item_list_gui.insert('', tk.END, values=value_arr) 

    def clear_list(self):  
        for i in self.item_list_gui.get_children():
            self.item_list_gui.delete(i)
    

    def bind_scrollbar_with_list(self, list_frame):  
        y_scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.item_list_gui.yview)

        self.item_list_gui.configure(yscrollcommand=y_scrollbar.set)
        y_scrollbar.configure(command=self.item_list_gui.yview)

        y_scrollbar.grid(row=0, column=1, sticky='nsew')
