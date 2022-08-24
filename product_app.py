#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tkinter import ttk
from tkinter import *
import sqlite3

class Product:

    db_name = 'database.db'

    def __init__(self,window):
        self.wind = window
        self.wind.title('products Application')

        #CREATING A FRAME CONTAINER

        frame = LabelFrame(self.wind, text = 'Register a new Product')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)

        #name input
        Label(frame, text = 'Name: ').grid(row = 1, column = 0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row = 1, column = 1)

        #price input
        Label(frame, text = 'Price: ').grid(row = 2, column = 0)
        self.price = Entry(frame)
        self.price.grid(row = 2, column = 1)

        #button add product
        ttk.Button(frame, text = 'Save Product', command=self.add_product).grid(row = 3, columnspan = 2, sticky = W + E)

        self.message = Label(text="", fg = "red")
        self.message.grid(row=3, column=0, columnspan=2, sticky=W + E)
        
        #table
        self.tree = ttk.Treeview(height = 10, columns = 2)
        self.tree.grid(row = 4, column = 0, columnspan = 2)
        self.tree.heading('#0', text = 'Name', anchor = CENTER)
        self.tree.heading('#1', text = 'Price', anchor = CENTER)

        ttk.Button(text = 'DELETE').grid(row = 5, column = 0, sticky = W + E)
        ttk.Button(text = 'EDIT').grid(row = 5, column = 1, sticky = W + E)
        
        self.get_products()

    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def get_products(self):
        records = self.tree.get_children()
        for e in records:
            self.tree.delete(e)
        query = 'SELECT * FROM product ORDER BY name DESC'
        db_rows = self.run_query(query)
        for i in db_rows:
            self.tree.insert('',0,text=i[1], values = i[2])

    def validation(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0
            

    def add_product(self):
        if self.validation():
            query = 'INSERT INTO product VALUES(NULL, ?, ?)'
            parameters = (self.name.get(), self.price.get())
            self.run_query(query, parameters)
            self.message['text'] = 'Product {} added Successfully'.format(self.name.get())
            self.name.delete(0, END)
            self.price.delete(0, END)
        else:
            self.message['text'] = 'Name and price are required.'
        self.get_products()

    def delete_product(self):
        pass
            

if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()


