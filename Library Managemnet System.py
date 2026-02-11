import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime, timedelta

class LibraryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("1000x600")
        self.root.resizable(False, False)
        
        # Initialize database
        self.init_database()
        
        # Create GUI
        self.create_widgets()
        
    def init_database(self):
        """Initialize SQLite database and create tables"""
        self.conn = sqlite3.connect('library.db')
        self.cursor = self.conn.cursor()
        
        # Create Books table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                isbn TEXT UNIQUE,
                category TEXT,
                quantity INTEGER DEFAULT 1,
                available INTEGER DEFAULT 1
            )
        ''')
        
        # Create Members table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS members (
                member_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE,
                phone TEXT,
                join_date TEXT
            )
        ''')
        
        # Create Transactions table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER,
                member_id INTEGER,
                issue_date TEXT,
                due_date TEXT,
                return_date TEXT,
                status TEXT DEFAULT 'Issued',
                FOREIGN KEY (book_id) REFERENCES books(book_id),
                FOREIGN KEY (member_id) REFERENCES members(member_id)
            )
        ''')
        
        self.conn.commit()
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Title
        title_frame = tk.Frame(self.root, bg="#2C3E50", height=80)
        title_frame.pack(fill=tk.X)
        
        title_label = tk.Label(title_frame, text="📚 Library Management System", 
                              font=("Arial", 24, "bold"), bg="#2C3E50", fg="white")
        title_label.pack(pady=20)
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_books_tab()
        self.create_members_tab()
        self.create_transactions_tab()
        self.create_search_tab()
    
    def create_books_tab(self):
        """Create Books management tab"""
        books_frame = ttk.Frame(self.notebook)
        self.notebook.add(books_frame, text="Books")
        
        # Input frame
        input_frame = tk.LabelFrame(books_frame, text="Book Details", font=("Arial", 12, "bold"), padx=20, pady=20)
        input_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Book Title
        tk.Label(input_frame, text="Title:", font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.book_title_entry = tk.Entry(input_frame, width=30, font=("Arial", 10))
        self.book_title_entry.grid(row=0, column=1, pady=5, padx=10)
        
        # Author
        tk.Label(input_frame, text="Author:", font=("Arial", 10)).grid(row=0, column=2, sticky=tk.W, pady=5)
        self.book_author_entry = tk.Entry(input_frame, width=30, font=("Arial", 10))
        self.book_author_entry.grid(row=0, column=3, pady=5, padx=10)
        
        # ISBN
        tk.Label(input_frame, text="ISBN:", font=("Arial", 10)).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.book_isbn_entry = tk.Entry(input_frame, width=30, font=("Arial", 10))
        self.book_isbn_entry.grid(row=1, column=1, pady=5, padx=10)
        
        # Category
        tk.Label(input_frame, text="Category:", font=("Arial", 10)).grid(row=1, column=2, sticky=tk.W, pady=5)
        self.book_category_entry = tk.Entry(input_frame, width=30, font=("Arial", 10))
        self.book_category_entry.grid(row=1, column=3, pady=5, padx=10)
        
        # Quantity
        tk.Label(input_frame, text="Quantity:", font=("Arial", 10)).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.book_quantity_entry = tk.Entry(input_frame, width=30, font=("Arial", 10))
        self.book_quantity_entry.grid(row=2, column=1, pady=5, padx=10)
        
        # Buttons frame
        button_frame = tk.Frame(input_frame)
        button_frame.grid(row=3, column=0, columnspan=4, pady=20)
        
        tk.Button(button_frame, text="Add Book", command=self.add_book, 
                 bg="#27AE60", fg="white", font=("Arial", 10, "bold"), width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Update Book", command=self.update_book,
                 bg="#3498DB", fg="white", font=("Arial", 10, "bold"), width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Delete Book", command=self.delete_book,
                 bg="#E74C3C", fg="white", font=("Arial", 10, "bold"), width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Clear Fields", command=self.clear_book_fields,
                 bg="#95A5A6", fg="white", font=("Arial", 10, "bold"), width=15).pack(side=tk.LEFT, padx=5)
        
        # Treeview frame
        tree_frame = tk.Frame(books_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Scrollbars
        tree_scroll_y = tk.Scrollbar(tree_frame)
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree_scroll_x = tk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Books Treeview
        self.books_tree = ttk.Treeview(tree_frame, 
                                       columns=("ID", "Title", "Author", "ISBN", "Category", "Quantity", "Available"),
                                       yscrollcommand=tree_scroll_y.set,
                                       xscrollcommand=tree_scroll_x.set)
        self.books_tree.pack(fill=tk.BOTH, expand=True)
        
        tree_scroll_y.config(command=self.books_tree.yview)
        tree_scroll_x.config(command=self.books_tree.xview)
        
        # Configure columns
        self.books_tree['show'] = 'headings'
        self.books_tree.heading("ID", text="ID")
        self.books_tree.heading("Title", text="Title")
        self.books_tree.heading("Author", text="Author")
        self.books_tree.heading("ISBN", text="ISBN")
        self.books_tree.heading("Category", text="Category")
        self.books_tree.heading("Quantity", text="Quantity")
        self.books_tree.heading("Available", text="Available")
        
        self.books_tree.column("ID", width=50)
        self.books_tree.column("Title", width=200)
        self.books_tree.column("Author", width=150)
        self.books_tree.column("ISBN", width=120)
        self.books_tree.column("Category", width=100)
        self.books_tree.column("Quantity", width=80)
        self.books_tree.column("Available", width=80)
        
        self.books_tree.bind("<ButtonRelease-1>", self.select_book)
        
        self.display_books()
    
    def create_members_tab(self):
        """Create Members management tab"""
        members_frame = ttk.Frame(self.notebook)
        self.notebook.add(members_frame, text="Members")
        
        # Input frame
        input_frame = tk.LabelFrame(members_frame, text="Member Details", font=("Arial", 12, "bold"), padx=20, pady=20)
        input_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Member Name
        tk.Label(input_frame, text="Name:", font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.member_name_entry = tk.Entry(input_frame, width=30, font=("Arial", 10))
        self.member_name_entry.grid(row=0, column=1, pady=5, padx=10)
        
        # Email
        tk.Label(input_frame, text="Email:", font=("Arial", 10)).grid(row=0, column=2, sticky=tk.W, pady=5)
        self.member_email_entry = tk.Entry(input_frame, width=30, font=("Arial", 10))
        self.member_email_entry.grid(row=0, column=3, pady=5, padx=10)
        
        # Phone
        tk.Label(input_frame, text="Phone:", font=("Arial", 10)).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.member_phone_entry = tk.Entry(input_frame, width=30, font=("Arial", 10))
        self.member_phone_entry.grid(row=1, column=1, pady=5, padx=10)
        
        # Buttons frame
        button_frame = tk.Frame(input_frame)
        button_frame.grid(row=2, column=0, columnspan=4, pady=20)
        
        tk.Button(button_frame, text="Add Member", command=self.add_member,
                 bg="#27AE60", fg="white", font=("Arial", 10, "bold"), width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Update Member", command=self.update_member,
                 bg="#3498DB", fg="white", font=("Arial", 10, "bold"), width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Delete Member", command=self.delete_member,
                 bg="#E74C3C", fg="white", font=("Arial", 10, "bold"), width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Clear Fields", command=self.clear_member_fields,
                 bg="#95A5A6", fg="white", font=("Arial", 10, "bold"), width=15).pack(side=tk.LEFT, padx=5)
        
        # Treeview frame
        tree_frame = tk.Frame(members_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Scrollbars
        tree_scroll_y = tk.Scrollbar(tree_frame)
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree_scroll_x = tk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Members Treeview
        self.members_tree = ttk.Treeview(tree_frame,
                                        columns=("ID", "Name", "Email", "Phone", "Join Date"),
                                        yscrollcommand=tree_scroll_y.set,
                                        xscrollcommand=tree_scroll_x.set)
        self.members_tree.pack(fill=tk.BOTH, expand=True)
        
        tree_scroll_y.config(command=self.members_tree.yview)
        tree_scroll_x.config(command=self.members_tree.xview)
        
        # Configure columns
        self.members_tree['show'] = 'headings'
        self.members_tree.heading("ID", text="ID")
        self.members_tree.heading("Name", text="Name")
        self.members_tree.heading("Email", text="Email")
        self.members_tree.heading("Phone", text="Phone")
        self.members_tree.heading("Join Date", text="Join Date")
        
        self.members_tree.column("ID", width=50)
        self.members_tree.column("Name", width=200)
        self.members_tree.column("Email", width=250)
        self.members_tree.column("Phone", width=150)
        self.members_tree.column("Join Date", width=150)
        
        self.members_tree.bind("<ButtonRelease-1>", self.select_member)
        
        self.display_members()
    
    def create_transactions_tab(self):
        """Create Transactions tab for issuing/returning books"""
        trans_frame = ttk.Frame(self.notebook)
        self.notebook.add(trans_frame, text="Issue/Return Books")
        
        # Input frame
        input_frame = tk.LabelFrame(trans_frame, text="Transaction Details", font=("Arial", 12, "bold"), padx=20, pady=20)
        input_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Book ID
        tk.Label(input_frame, text="Book ID:", font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.trans_book_id_entry = tk.Entry(input_frame, width=30, font=("Arial", 10))
        self.trans_book_id_entry.grid(row=0, column=1, pady=5, padx=10)
        
        # Member ID
        tk.Label(input_frame, text="Member ID:", font=("Arial", 10)).grid(row=0, column=2, sticky=tk.W, pady=5)
        self.trans_member_id_entry = tk.Entry(input_frame, width=30, font=("Arial", 10))
        self.trans_member_id_entry.grid(row=0, column=3, pady=5, padx=10)
        
        # Due Days
        tk.Label(input_frame, text="Due Days:", font=("Arial", 10)).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.trans_due_days_entry = tk.Entry(input_frame, width=30, font=("Arial", 10))
        self.trans_due_days_entry.insert(0, "14")  # Default 14 days
        self.trans_due_days_entry.grid(row=1, column=1, pady=5, padx=10)
        
        # Buttons frame
        button_frame = tk.Frame(input_frame)
        button_frame.grid(row=2, column=0, columnspan=4, pady=20)
        
        tk.Button(button_frame, text="Issue Book", command=self.issue_book,
                 bg="#27AE60", fg="white", font=("Arial", 10, "bold"), width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Return Book", command=self.return_book,
                 bg="#3498DB", fg="white", font=("Arial", 10, "bold"), width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Clear Fields", command=self.clear_transaction_fields,
                 bg="#95A5A6", fg="white", font=("Arial", 10, "bold"), width=15).pack(side=tk.LEFT, padx=5)
        
        # Treeview frame
        tree_frame = tk.Frame(trans_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Scrollbars
        tree_scroll_y = tk.Scrollbar(tree_frame)
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree_scroll_x = tk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Transactions Treeview
        self.trans_tree = ttk.Treeview(tree_frame,
                                      columns=("Trans ID", "Book ID", "Member ID", "Issue Date", "Due Date", "Return Date", "Status"),
                                      yscrollcommand=tree_scroll_y.set,
                                      xscrollcommand=tree_scroll_x.set)
        self.trans_tree.pack(fill=tk.BOTH, expand=True)
        
        tree_scroll_y.config(command=self.trans_tree.yview)
        tree_scroll_x.config(command=self.trans_tree.xview)
        
        # Configure columns
        self.trans_tree['show'] = 'headings'
        self.trans_tree.heading("Trans ID", text="Trans ID")
        self.trans_tree.heading("Book ID", text="Book ID")
        self.trans_tree.heading("Member ID", text="Member ID")
        self.trans_tree.heading("Issue Date", text="Issue Date")
        self.trans_tree.heading("Due Date", text="Due Date")
        self.trans_tree.heading("Return Date", text="Return Date")
        self.trans_tree.heading("Status", text="Status")
        
        self.trans_tree.column("Trans ID", width=80)
        self.trans_tree.column("Book ID", width=80)
        self.trans_tree.column("Member ID", width=100)
        self.trans_tree.column("Issue Date", width=120)
        self.trans_tree.column("Due Date", width=120)
        self.trans_tree.column("Return Date", width=120)
        self.trans_tree.column("Status", width=100)
        
        self.trans_tree.bind("<ButtonRelease-1>", self.select_transaction)
        
        self.display_transactions()
    
    def create_search_tab(self):
        """Create Search tab"""
        search_frame = ttk.Frame(self.notebook)
        self.notebook.add(search_frame, text="Search")
        
        # Search frame
        input_frame = tk.LabelFrame(search_frame, text="Search Books", font=("Arial", 12, "bold"), padx=20, pady=20)
        input_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(input_frame, text="Search by:", font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.search_option = ttk.Combobox(input_frame, width=15, font=("Arial", 10), state="readonly")
        self.search_option['values'] = ("Title", "Author", "ISBN", "Category")
        self.search_option.current(0)
        self.search_option.grid(row=0, column=1, pady=5, padx=10)
        
        tk.Label(input_frame, text="Search term:", font=("Arial", 10)).grid(row=0, column=2, sticky=tk.W, pady=5)
        self.search_entry = tk.Entry(input_frame, width=30, font=("Arial", 10))
        self.search_entry.grid(row=0, column=3, pady=5, padx=10)
        
        tk.Button(input_frame, text="Search", command=self.search_books,
                 bg="#3498DB", fg="white", font=("Arial", 10, "bold"), width=15).grid(row=0, column=4, padx=10)
        tk.Button(input_frame, text="Show All", command=self.display_books,
                 bg="#95A5A6", fg="white", font=("Arial", 10, "bold"), width=15).grid(row=0, column=5, padx=10)
        
        # Results frame
        tree_frame = tk.Frame(search_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Scrollbars
        tree_scroll_y = tk.Scrollbar(tree_frame)
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree_scroll_x = tk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Search Results Treeview
        self.search_tree = ttk.Treeview(tree_frame,
                                       columns=("ID", "Title", "Author", "ISBN", "Category", "Quantity", "Available"),
                                       yscrollcommand=tree_scroll_y.set,
                                       xscrollcommand=tree_scroll_x.set)
        self.search_tree.pack(fill=tk.BOTH, expand=True)
        
        tree_scroll_y.config(command=self.search_tree.yview)
        tree_scroll_x.config(command=self.search_tree.xview)
        
        # Configure columns
        self.search_tree['show'] = 'headings'
        self.search_tree.heading("ID", text="ID")
        self.search_tree.heading("Title", text="Title")
        self.search_tree.heading("Author", text="Author")
        self.search_tree.heading("ISBN", text="ISBN")
        self.search_tree.heading("Category", text="Category")
        self.search_tree.heading("Quantity", text="Quantity")
        self.search_tree.heading("Available", text="Available")
        
        self.search_tree.column("ID", width=50)
        self.search_tree.column("Title", width=200)
        self.search_tree.column("Author", width=150)
        self.search_tree.column("ISBN", width=120)
        self.search_tree.column("Category", width=100)
        self.search_tree.column("Quantity", width=80)
        self.search_tree.column("Available", width=80)
    
    # Book operations
    def add_book(self):
        """Add a new book to the library"""
        title = self.book_title_entry.get().strip()
        author = self.book_author_entry.get().strip()
        isbn = self.book_isbn_entry.get().strip()
        category = self.book_category_entry.get().strip()
        quantity = self.book_quantity_entry.get().strip()
        
        if not title or not author:
            messagebox.showerror("Error", "Title and Author are required!")
            return
        
        try:
            quantity = int(quantity) if quantity else 1
            
            self.cursor.execute('''
                INSERT INTO books (title, author, isbn, category, quantity, available)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (title, author, isbn, category, quantity, quantity))
            
            self.conn.commit()
            messagebox.showinfo("Success", "Book added successfully!")
            self.clear_book_fields()
            self.display_books()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "ISBN already exists!")
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a number!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def update_book(self):
        """Update selected book"""
        selected = self.books_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a book to update!")
            return
        
        book_id = self.books_tree.item(selected[0])['values'][0]
        title = self.book_title_entry.get().strip()
        author = self.book_author_entry.get().strip()
        isbn = self.book_isbn_entry.get().strip()
        category = self.book_category_entry.get().strip()
        quantity = self.book_quantity_entry.get().strip()
        
        if not title or not author:
            messagebox.showerror("Error", "Title and Author are required!")
            return
        
        try:
            quantity = int(quantity) if quantity else 1
            
            self.cursor.execute('''
                UPDATE books 
                SET title=?, author=?, isbn=?, category=?, quantity=?
                WHERE book_id=?
            ''', (title, author, isbn, category, quantity, book_id))
            
            self.conn.commit()
            messagebox.showinfo("Success", "Book updated successfully!")
            self.clear_book_fields()
            self.display_books()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def delete_book(self):
        """Delete selected book"""
        selected = self.books_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a book to delete!")
            return
        
        book_id = self.books_tree.item(selected[0])['values'][0]
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this book?"):
            try:
                self.cursor.execute("DELETE FROM books WHERE book_id=?", (book_id,))
                self.conn.commit()
                messagebox.showinfo("Success", "Book deleted successfully!")
                self.clear_book_fields()
                self.display_books()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def display_books(self):
        """Display all books in the treeview"""
        for item in self.books_tree.get_children():
            self.books_tree.delete(item)
        
        self.cursor.execute("SELECT * FROM books")
        books = self.cursor.fetchall()
        
        for book in books:
            self.books_tree.insert('', tk.END, values=book)
    
    def select_book(self, event):
        """Fill entry fields when a book is selected"""
        selected = self.books_tree.selection()
        if selected:
            values = self.books_tree.item(selected[0])['values']
            self.clear_book_fields()
            self.book_title_entry.insert(0, values[1])
            self.book_author_entry.insert(0, values[2])
            self.book_isbn_entry.insert(0, values[3])
            self.book_category_entry.insert(0, values[4])
            self.book_quantity_entry.insert(0, values[5])
    
    def clear_book_fields(self):
        """Clear all book entry fields"""
        self.book_title_entry.delete(0, tk.END)
        self.book_author_entry.delete(0, tk.END)
        self.book_isbn_entry.delete(0, tk.END)
        self.book_category_entry.delete(0, tk.END)
        self.book_quantity_entry.delete(0, tk.END)
    
    # Member operations
    def add_member(self):
        """Add a new member"""
        name = self.member_name_entry.get().strip()
        email = self.member_email_entry.get().strip()
        phone = self.member_phone_entry.get().strip()
        join_date = datetime.now().strftime("%Y-%m-%d")
        
        if not name:
            messagebox.showerror("Error", "Name is required!")
            return
        
        try:
            self.cursor.execute('''
                INSERT INTO members (name, email, phone, join_date)
                VALUES (?, ?, ?, ?)
            ''', (name, email, phone, join_date))
            
            self.conn.commit()
            messagebox.showinfo("Success", "Member added successfully!")
            self.clear_member_fields()
            self.display_members()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Email already exists!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def update_member(self):
        """Update selected member"""
        selected = self.members_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a member to update!")
            return
        
        member_id = self.members_tree.item(selected[0])['values'][0]
        name = self.member_name_entry.get().strip()
        email = self.member_email_entry.get().strip()
        phone = self.member_phone_entry.get().strip()
        
        if not name:
            messagebox.showerror("Error", "Name is required!")
            return
        
        try:
            self.cursor.execute('''
                UPDATE members 
                SET name=?, email=?, phone=?
                WHERE member_id=?
            ''', (name, email, phone, member_id))
            
            self.conn.commit()
            messagebox.showinfo("Success", "Member updated successfully!")
            self.clear_member_fields()
            self.display_members()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def delete_member(self):
        """Delete selected member"""
        selected = self.members_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a member to delete!")
            return
        
        member_id = self.members_tree.item(selected[0])['values'][0]
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this member?"):
            try:
                self.cursor.execute("DELETE FROM members WHERE member_id=?", (member_id,))
                self.conn.commit()
                messagebox.showinfo("Success", "Member deleted successfully!")
                self.clear_member_fields()
                self.display_members()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def display_members(self):
        """Display all members in the treeview"""
        for item in self.members_tree.get_children():
            self.members_tree.delete(item)
        
        self.cursor.execute("SELECT * FROM members")
        members = self.cursor.fetchall()
        
        for member in members:
            self.members_tree.insert('', tk.END, values=member)
    
    def select_member(self, event):
        """Fill entry fields when a member is selected"""
        selected = self.members_tree.selection()
        if selected:
            values = self.members_tree.item(selected[0])['values']
            self.clear_member_fields()
            self.member_name_entry.insert(0, values[1])
            self.member_email_entry.insert(0, values[2])
            self.member_phone_entry.insert(0, values[3])
    
    def clear_member_fields(self):
        """Clear all member entry fields"""
        self.member_name_entry.delete(0, tk.END)
        self.member_email_entry.delete(0, tk.END)
        self.member_phone_entry.delete(0, tk.END)
    
    # Transaction operations
    def issue_book(self):
        """Issue a book to a member"""
        book_id = self.trans_book_id_entry.get().strip()
        member_id = self.trans_member_id_entry.get().strip()
        due_days = self.trans_due_days_entry.get().strip()
        
        if not book_id or not member_id:
            messagebox.showerror("Error", "Book ID and Member ID are required!")
            return
        
        try:
            book_id = int(book_id)
            member_id = int(member_id)
            due_days = int(due_days) if due_days else 14
            
            # Check if book exists and is available
            self.cursor.execute("SELECT available FROM books WHERE book_id=?", (book_id,))
            result = self.cursor.fetchone()
            
            if not result:
                messagebox.showerror("Error", "Book ID not found!")
                return
            
            if result[0] <= 0:
                messagebox.showerror("Error", "Book is not available!")
                return
            
            # Check if member exists
            self.cursor.execute("SELECT member_id FROM members WHERE member_id=?", (member_id,))
            if not self.cursor.fetchone():
                messagebox.showerror("Error", "Member ID not found!")
                return
            
            # Issue the book
            issue_date = datetime.now().strftime("%Y-%m-%d")
            due_date = (datetime.now() + timedelta(days=due_days)).strftime("%Y-%m-%d")
            
            self.cursor.execute('''
                INSERT INTO transactions (book_id, member_id, issue_date, due_date, status)
                VALUES (?, ?, ?, ?, 'Issued')
            ''', (book_id, member_id, issue_date, due_date))
            
            # Update book availability
            self.cursor.execute('''
                UPDATE books SET available = available - 1 WHERE book_id=?
            ''', (book_id,))
            
            self.conn.commit()
            messagebox.showinfo("Success", f"Book issued successfully!\nDue date: {due_date}")
            self.clear_transaction_fields()
            self.display_transactions()
            self.display_books()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def return_book(self):
        """Return a book"""
        selected = self.trans_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a transaction from the list!")
            return
        
        trans_id = self.trans_tree.item(selected[0])['values'][0]
        
        try:
            # Get transaction details
            self.cursor.execute('''
                SELECT book_id, status FROM transactions WHERE transaction_id=?
            ''', (trans_id,))
            result = self.cursor.fetchone()
            
            if not result:
                messagebox.showerror("Error", "Transaction not found!")
                return
            
            book_id, status = result
            
            if status == 'Returned':
                messagebox.showerror("Error", "Book already returned!")
                return
            
            # Update transaction
            return_date = datetime.now().strftime("%Y-%m-%d")
            self.cursor.execute('''
                UPDATE transactions 
                SET return_date=?, status='Returned'
                WHERE transaction_id=?
            ''', (return_date, trans_id))
            
            # Update book availability
            self.cursor.execute('''
                UPDATE books SET available = available + 1 WHERE book_id=?
            ''', (book_id,))
            
            self.conn.commit()
            messagebox.showinfo("Success", "Book returned successfully!")
            self.display_transactions()
            self.display_books()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def display_transactions(self):
        """Display all transactions in the treeview"""
        for item in self.trans_tree.get_children():
            self.trans_tree.delete(item)
        
        self.cursor.execute("SELECT * FROM transactions ORDER BY transaction_id DESC")
        transactions = self.cursor.fetchall()
        
        for trans in transactions:
            self.trans_tree.insert('', tk.END, values=trans)
    
    def select_transaction(self, event):
        """Fill entry fields when a transaction is selected"""
        selected = self.trans_tree.selection()
        if selected:
            values = self.trans_tree.item(selected[0])['values']
            self.clear_transaction_fields()
            self.trans_book_id_entry.insert(0, values[1])
            self.trans_member_id_entry.insert(0, values[2])
    
    def clear_transaction_fields(self):
        """Clear all transaction entry fields"""
        self.trans_book_id_entry.delete(0, tk.END)
        self.trans_member_id_entry.delete(0, tk.END)
        self.trans_due_days_entry.delete(0, tk.END)
        self.trans_due_days_entry.insert(0, "14")
    
    # Search operations
    def search_books(self):
        """Search for books"""
        search_by = self.search_option.get()
        search_term = self.search_entry.get().strip()
        
        if not search_term:
            messagebox.showerror("Error", "Please enter a search term!")
            return
        
        # Clear search results
        for item in self.search_tree.get_children():
            self.search_tree.delete(item)
        
        # Map search option to column name
        column_map = {
            "Title": "title",
            "Author": "author",
            "ISBN": "isbn",
            "Category": "category"
        }
        
        column = column_map[search_by]
        
        try:
            query = f"SELECT * FROM books WHERE {column} LIKE ?"
            self.cursor.execute(query, (f"%{search_term}%",))
            results = self.cursor.fetchall()
            
            if results:
                for book in results:
                    self.search_tree.insert('', tk.END, values=book)
                messagebox.showinfo("Success", f"Found {len(results)} book(s)!")
            else:
                messagebox.showinfo("No Results", "No books found matching your search!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def __del__(self):
        """Close database connection when application closes"""
        if hasattr(self, 'conn'):
            self.conn.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryManagementSystem(root)
    root.mainloop()