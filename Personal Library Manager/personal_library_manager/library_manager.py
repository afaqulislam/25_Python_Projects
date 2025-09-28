import json  # JSON module for saving and loading data

# File name for storing data
FILE_NAME = "library.json"

# Global list to store books
library = []

def display_menu():
    """Function to display the menu options."""
    print("\n📚 Welcome to your Personal Library Manager!")
    print("1. Add a book")
    print("2. Remove a book")
    print("3. Search for a book")
    print("4. Display all books")
    print("5. Display statistics")
    print("6. Exit")

def add_book():
    """Function to add a book to the library."""
    title = input("Enter the book title: ").strip()
    author = input("Enter the author: ").strip()
    year = input("Enter the publication year: ").strip()
    genre = input("Enter the genre: ").strip()
    read_status = input("Have you read this book? (yes/no): ").strip().lower()

    if not title or not author or not year or not genre:
        print("⚠️ All fields are required!")
        return
    
    if not year.isdigit():
        print("⚠️ Publication year must be a number!")
        return

    book = {
        "title": title,
        "author": author,
        "year": int(year),
        "genre": genre,
        "read": True if read_status == "yes" else False
    }
    
    library.append(book)
    print(f"✅ '{title}' added successfully!")

def remove_book():
    """Function to remove a book by title."""
    title = input("Enter the title of the book to remove: ").strip()

    for book in library:
        if book["title"].lower() == title.lower():
            library.remove(book)
            print(f"✅ '{title}' removed successfully!")
            return
    
    print(f"❌ Book '{title}' not found!")

def search_book():
    """Function to search for a book by title or author."""
    print("\nSearch by:")
    print("1. Title")
    print("2. Author")
    choice = input("Enter your choice (1 or 2): ").strip()

    if choice == "1":
        keyword = input("Enter the book title: ").strip().lower()
        results = [book for book in library if keyword in book["title"].lower()]
    elif choice == "2":
        keyword = input("Enter the author's name: ").strip().lower()
        results = [book for book in library if keyword in book["author"].lower()]
    else:
        print("❌ Invalid choice!")
        return

    if results:
        print("\n🔎 Matching Books:")
        for idx, book in enumerate(results, start=1):
            status = "✅ Read" if book["read"] else "📖 Unread"
            print(f"{idx}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {status}")
    else:
        print("❌ No matching books found!")

def display_books():
    """Function to display all books in the library."""
    if not library:
        print("📖 Your library is empty!")
        return
    
    print("\n📚 Your Library:")
    for idx, book in enumerate(library, start=1):
        status = "✅ Read" if book["read"] else "📖 Unread"
        print(f"{idx}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {status}")

def display_statistics():
    """Function to display statistics of the library."""
    total_books = len(library)
    
    if total_books == 0:
        print("📊 Your library is empty! Add some books first.")
        return

    read_books = sum(1 for book in library if book["read"])
    read_percentage = (read_books / total_books) * 100

    print("\n📊 Library Statistics:")
    print(f"📚 Total books: {total_books}")
    print(f"✅ Books read: {read_books}")
    print(f"📖 Percentage read: {read_percentage:.2f}%")

def save_library():
    """Function to save the library data to JSON and a text file."""
    # Save as JSON
    with open("library.json", "w") as json_file:
        json.dump(library, json_file, indent=4)

    # Save as a readable text file
    with open("library.txt", "w") as txt_file:
        for book in library:
            book_data = f"Title: {book['title']} | Author: {book['author']} | Year: {book['year']} | Genre: {book['genre']} | Read: {'Yes' if book['read'] else 'No'}\n"
            txt_file.write(book_data)
    
    print("💾 Library saved to `library.json` & `library.txt` successfully!")

def load_library():
    """Function to load the library data from a JSON file."""
    global library
    try:
        with open("library.json", "r") as file:
            library = json.load(file)
        print("📂 Library loaded from library.json successfully!")
    except FileNotFoundError:
        library = []  # If file doesn't exist, start with an empty list
    except json.JSONDecodeError:
        print("⚠️ Error decoding JSON. Starting with an empty library.")
        library = []

def main():
    """Main function to run the library manager."""
    load_library()  # Load data at the start

    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_book()
        elif choice == "2":
            remove_book()
        elif choice == "3":
            search_book()
        elif choice == "4":
            display_books()
        elif choice == "5":
            display_statistics()
        elif choice == "6":
            save_library()  # Save data before exiting
            print("📌 Exiting... Goodbye!")
            break
        else:
            print("❌ Invalid choice! Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()
