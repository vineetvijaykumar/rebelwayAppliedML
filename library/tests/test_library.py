import pytest
from library.book import Book
from library.library import Library


@pytest.fixture
def library():
    database = "./tests/test_database.json"
    library = Library(database)
    library.empty_library()
    return library

def test_search_item(library):
    book = Book("Prism", "Max Maven")
    library.add_book_to_library(book)
    book_list = library.search_book("Prism")
    assert book_list[0].name == "Prism"

def test_empty_library(library):
    book = Book("Prism", "Max Maven")
    library.add_book_to_library(book)
    library.empty_library()
    assert len(library.get_all_books()["Books"].items()) == 0


def test_get_all_items(library):
    book1 = Book("Prism", "Max Maven")
    book2 = Book("Twilight", "Stephanie Meyer")
    library.add_book_to_library(book1)
    library.add_book_to_library(book2)
    retrieved_books = library.get_all_books()
    names_to_compare = [book1.name, book2.name]
    results = [book_data["name"] for book_id, book_data in retrieved_books["Books"].items()]
    assert names_to_compare == results
