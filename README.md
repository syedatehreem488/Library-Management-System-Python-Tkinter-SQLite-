# 📚 Library Management System (Python + Tkinter + SQLite)

A desktop-based **Library Management System** built with **Python Tkinter** for the GUI and **SQLite** for the database.  
This project allows librarians to manage books, members, and transactions (issue/return) with an intuitive interface.

---

## ✨ Features

- **Books Management**
  - Add, update, delete books
  - Track quantity and availability
- **Members Management**
  - Register new members
  - Update or delete member details
- **Transactions**
  - Issue books with due dates
  - Return books and update status
- **Search**
  - Search books by Title, Author, ISBN, or Category
- **GUI**
  - Tabbed interface using Tkinter Notebook
  - Treeview tables for displaying records

---

## 🛠️ Tech Stack

- **Python 3.x**
- **Tkinter** (GUI)
- **SQLite3** (Database)
- **Datetime** (Issue/Return tracking)

---

## 📂 Project Structure

Library-Management-System:
- library_management.py   # Main application code
- library.db              # SQLite database (auto-generated)
- requirements.txt        # Dependencies
- screenshots/            # GUI screenshots
- README.md               # Documentation
- LICENSE                 # License file

---

🔮 Future Improvements:

- Fine calculation for late returns
- Export reports to CSV/PDF
- User authentication (admin login)
- Cloud database integration
- Dark mode UI
