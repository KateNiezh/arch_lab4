import booksupfunc as bsf

print("Welcome to the Home Library Catalogue(HLC v0.04.0-alpha)")
book_catalogue = bsf.Support()

while True:
    book_catalogue.print_menu()
    ch = input()
    if ch == '1':
        book_catalogue.catalogue.add_book(book_catalogue.get_book())
    elif ch == '2':
        book_catalogue.catalogue.edit_book(
            input("Title: "),
            input("Author: "), book_catalogue.get_book())
    elif ch == '3':
        book_catalogue.catalogue.delete_book(
            input("Title: "),
            input("Author: "))
    elif ch == '4':
        year_f, year_t, desc = book_catalogue.get_optional_values()
        book_catalogue.pprint(
            book_catalogue.catalogue.filter_books(
                input("Filter key(author, genre or year): "),
                input("Enter key value: "),
                year_f,
                year_t,
                desc))
    elif ch == '5':
        book_catalogue.print_authors(
            book_catalogue.catalogue.get_authors(book_catalogue.get_genre()))
    elif ch == '6':
        book_catalogue.load_library()
    elif ch == '7':
        book_catalogue.dump_into_library()
    elif ch == '0':
        break
