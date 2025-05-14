import json
from dataclasses import dataclass, field
from library.book import Book
from library.random_number_utils import RandomUtils
from library.file_io import Fstream

@dataclass
class Library:
    database_path: str
    isEmpty: bool = True
    isActive: bool = False
    id: str = field(init=False, default_factory=RandomUtils.generate_random_id)

    def get_all_books(self, verbose=0)->dict:
        """
        Reads and returns a has map with all the available items

        Args:
            if verbose is set to 1, it will print all the items.

        Returns:
            dict: a hash map with all the items in the database.
        """
        data_file = Fstream.load_json_files(self.database_path)

        if len(data_file.items()) > 0:
            self.isEmpty = False
            self.isActive = True

        try:
            if verbose == 1:
                Fstream.print_from_structure(data_file)
                return data_file
            else:
                return data_file

        except:
            raise ValueError("The value for the verbose as to be 0 or 1")

    def search_book(self, query: str)->list[Book]:
        """
        """
        data = Fstream.load_json_files(self.database_path)
        matching_items = []
        for item_id, item_data in data["Books"].items():
            item = Book(name=item_data["name"], author=item_data["author"])
            if query.lower() in item.search_string.lower():
                matching_items.append(item)

        if len(matching_items) == 0:
            print("Not items found")

        else:
            for item in matching_items:
                print(f"Found: {item.name} {item.author}")

        return matching_items

    def add_book_to_library(self, book: Book):
        """
        Adds an item to the cart and updates the database.json file.

        Args:
            item (Item): The item to add to the cart.
        """
        data = self.get_all_books()

        new_book = {
            "name": book.name,
            "author": book.author
        }

        data["Books"][book.id] = new_book

        with open(self.database_path, 'w') as file:
            json.dump(data, file, indent=4)

        self.isEmpty = False
        self.isActive = True

        print(f"Added {book.name} to the cart.")

    def remove_books_from_library_by_query(self, query: str):
        """
        Removes all the instances of an item from the cart based on a query.

        Args:
            query (str): The search query to find the item to remove.
        """
        data = self.get_all_books()
        books_to_remove = []

        for book_id, item_data in data["Books"].items():
            if query.lower() in item_data["name"].lower() or query.lower() in item_data["author"].lower():
                books_to_remove.append(book_id)

        if not books_to_remove:
            print(f"No items found matching '{query}'")
            return

        for book_id in books_to_remove:
            book_name = data["Books"][book_id]["name"]
            del data["Books"][book_id]
            print(f"Removed {book_name} from the cart.")

        with open(self.database_path, 'w') as file:
            json.dump(data, file, indent=4)

        if not data["Books"]:
            self.isEmpty = True
            self.isActive = False

    def remove_books_from_library_by_selection(self):
        """
        Removes the selected item by index.
        """

        data = self.get_all_books()
        items = []
        i = 1
        for book_id, book_data in data["Books"].items():
            items.append(book_id)
            print(f"{i}: {book_data}")
            i += 1
        try:
            usr_choice = int(input("Select the book to delete by number, example: 0: ")) - 1
        except:
            raise ValueError("You must select a valid number!")

        if usr_choice > len(items):
            print("Book not found!")
            return

        book_to_delete = items[usr_choice]
        book_name = data["Books"][book_to_delete]["name"]
        del data["Books"][book_to_delete]
        print(f"Removed {book_name} from the cart.")

        with open(self.database_path, 'w') as file:
            json.dump(data, file, indent=4)

        if not data["Books"]:
            self.isEmpty = True
            self.isActive = False

    def empty_library(self):
        """
        Clear all the books in the library.
        """
        data = self.get_all_books()
        if len(data["Books"].items()) > 0:
            data = {"Books": {}}

            with open(self.database_path, 'w') as file:
                json.dump(data, file, indent=4)

            if not data["Books"]:
                self.isEmpty = True
                self.isActive = False
            print("The cart is empty")
        else:
            print("The cart is already empty")

