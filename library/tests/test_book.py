from library.book import Book

def test_book_author()->None:
    book = Book("Never Split the Difference","Chris Voss")
    assert book.author != ""

def test_book_name()->None:
    item = Book("a", "b")
    assert len(item.name) > 0