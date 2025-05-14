from library.book import Book
from library.library import Library

if __name__ == "__main__":

    #the main database for the cart to pass to the class
    database = "./database.json"
    my_library = Library(database)

    # search for an item
    print("Searching item...")
    results = my_library.search_book("relentless")
    print("------------------------")

    # Create an Item object so it can be added to the cart
    print("Adding books to the library:...")
    print("------------------------")
    book_one = Book("Repertoire", "Asi Wind")
    my_library.add_book_to_library(book_one)
    book_two = Book("Prism", "Max Maven")
    my_library.add_book_to_library(book_two)

    # get all the books in the library
    print("------------------------")
    print("Getting all the books in the library:")
    print("------------------------")
    my_library.get_all_books(verbose=1)

    print("------------------------")

    # remove all items by name or type
    print("Removing all instances of an item:")
    print("------------------------")
    my_library.remove_books_from_library_by_query("Repertoire")
    my_library.remove_books_from_library_by_query("Prism")

    print("------------------------")
    print("\n")
    # removes a selected item
    print("Removing a specific item by selection:")
    print("------------------------")
    my_library.remove_books_from_library_by_selection()
    print("------------------------")

    print("All the current items in the cart:")
    my_library.get_all_books(verbose=1)
    print("------------------------")

