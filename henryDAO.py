import mysql.connector

class HenryDAO:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                user='root',
                passwd='xxx', #replace with your root password
                database='xxx', #replace with the database you donwloaded Henry.sql into
                host='127.0.0.1')
            self.cursor = self.connection.cursor()
            print("Database connection successful.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    
    def get_author_data(self):
        query = "SELECT author_num, author_first, author_last FROM HENRY_AUTHOR"
        self.cursor.execute(query)
        authors = self.cursor.fetchall()
        return authors

    def get_books_by_author(self, author_num):
        query = """
        SELECT b.book_code, b.title, b.price
        FROM HENRY_BOOK b
        JOIN HENRY_WROTE w ON b.book_code = w.book_code
        WHERE w.author_num = %s
        """
        self.cursor.execute(query, (author_num,))
        books = self.cursor.fetchall()
        return books

    def get_category_data(self):
        query = "SELECT DISTINCT type FROM HENRY_BOOK"
        self.cursor.execute(query)
        categories = self.cursor.fetchall()
        return categories

    def get_books_by_category(self, category_type):
        query = """
        SELECT book_code, title, price 
        FROM HENRY_BOOK 
        WHERE type = %s
        """
        self.cursor.execute(query, (category_type,))
        books = self.cursor.fetchall()
        return books

    def get_publisher_data(self):
        query = "SELECT publisher_code, publisher_name FROM HENRY_PUBLISHER"
        self.cursor.execute(query)
        publishers = self.cursor.fetchall()
        return publishers

    def get_books_by_publisher(self, publisher_code):
        query = """
        SELECT DISTINCT book_code, title, price 
        FROM HENRY_BOOK 
        WHERE publisher_code = %s
        """
        self.cursor.execute(query, (publisher_code,))
        books = self.cursor.fetchall()
        return books

    def get_branch_data_for_book(self, book_code):
        query = """
        SELECT branch.branch_name, inventory.on_hand 
        FROM HENRY_BRANCH AS branch
        JOIN HENRY_INVENTORY AS inventory ON branch.branch_num = inventory.branch_num
        WHERE inventory.book_code = %s
        """
        self.cursor.execute(query, (book_code,))
        branch_data = self.cursor.fetchall()
        return branch_data

    def close_connection(self):
        self.cursor.close()
        self.connection.close()
        print("Database connection closed.")
