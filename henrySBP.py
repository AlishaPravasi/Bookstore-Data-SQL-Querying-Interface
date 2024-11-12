import tkinter as tk
from tkinter import ttk
from henryDAO import HenryDAO

class HenrySBP:
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

        publisher_label = tk.Label(self.frame, text="Publisher Selection:")
        publisher_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        self.publisher_combo = ttk.Combobox(self.frame, values=self.get_publishers())
        self.publisher_combo.bind("<<ComboboxSelected>>", self.on_publisher_selected)
        self.publisher_combo.grid(row=2, column=0, sticky="w", padx=10, pady=5)

        book_label = tk.Label(self.frame, text="Book Selection:")
        book_label.grid(row=1, column=1, sticky="w", padx=10, pady=5)

        self.book_combo = ttk.Combobox(self.frame)
        self.book_combo.bind("<<ComboboxSelected>>", self.on_book_selected)
        self.book_combo.grid(row=2, column=1, sticky="w", padx=10, pady=5)

    def get_publishers(self):
        publishers = self.dao.get_publisher_data()
        return [publisher[1] for publisher in publishers]  
        
    def on_publisher_selected(self, event):
        selected_publisher = self.publisher_combo.get()
        publisher_data = self.dao.get_publisher_data()
        publisher_code = [publisher[0] for publisher in publisher_data if publisher[1] == selected_publisher][0]
        books = self.dao.get_books_by_publisher(publisher_code)
        self.book_combo.set('')  
        self.book_combo['values'] = [] 
        self.books_by_code = {book[1]: book for book in books} 
        self.book_combo['values'] = [book[1] for book in books]  
        if books:
            self.book_combo.current(0)
            self.update_book_info(books[0])

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


