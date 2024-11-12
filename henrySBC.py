import tkinter as tk
from tkinter import ttk
from henryDAO import HenryDAO

class HenrySBC:
    def __init__(self, frame):
        self.dao = HenryDAO()
        self.frame = frame

        self.frame.columnconfigure(0, weight=1)  
        self.frame.columnconfigure(1, weight=1)  
        
        self.tree = ttk.Treeview(self.frame, columns=("Branch", "Copies Available"), show="headings")
        self.tree.heading("Branch", text="Branch")
        self.tree.heading("Copies Available", text="Copies Available")
        self.tree.grid(row=0, column=0, sticky="nsew")  

        self.price_label = tk.Label(self.frame, text="Price: $0.00", font=("Arial", 12))
        self.price_label.grid(row=0, column=1, sticky="ne", padx=10, pady=5) 

        category_label = tk.Label(self.frame, text="Category Selection:")
        category_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        self.category_combo = ttk.Combobox(self.frame, values=self.get_categories())
        self.category_combo.bind("<<ComboboxSelected>>", self.on_category_selected)
        self.category_combo.grid(row=2, column=0, sticky="w", padx=10, pady=5)

        book_label = tk.Label(self.frame, text="Book Selection:")
        book_label.grid(row=1, column=1, sticky="w", padx=10, pady=5)

        self.book_combo = ttk.Combobox(self.frame)
        self.book_combo.bind("<<ComboboxSelected>>", self.on_book_selected)
        self.book_combo.grid(row=2, column=1, sticky="w", padx=10, pady=5)

    def get_categories(self):
        categories = self.dao.get_category_data()
        return [category[0] for category in categories] 

    def on_category_selected(self, event):
        selected_category = self.category_combo.get()
        books = self.dao.get_books_by_category(selected_category)
        self.books_by_code = {book[1]: book for book in books}  
        self.book_combo.set('')  
        self.book_combo['values'] = [] 
        self.book_combo['values'] = [book[1] for book in books]  
        if books:
            self.book_combo.current(0)
            self.update_book_info(books[0])
        else:
            self.price_label.config(text="Price: $0.00")  
            self.tree.delete(*self.tree.get_children())  

    def on_book_selected(self, event):
        selected_title = self.book_combo.get()
        book = self.books_by_code.get(selected_title)
        if book:
            self.update_book_info(book)

    def update_book_info(self, book):
        book_price = book[2]  
        self.price_label.config(text=f"Price: ${book_price:.2f}")
        branch_data = self.dao.get_branch_data_for_book(book[0])  
        self.tree.delete(*self.tree.get_children())  
        for branch in branch_data:
            self.tree.insert("", "end", values=(branch[0], branch[1]))
