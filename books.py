
import mysql.connector


def get_db_connection():
    try:
        con = mysql.connector.connect(
            user="root",
            password="root",
            host="localhost",
            database="bookstore"
        )
        print(con)
        print("working 1")
        return con

    except:
        print("not working")
        return None


def create_book(book_id, title, author, category, price, stock):
    con = get_db_connection()
    if con is None:
        return

    c = None
    try:
        c = con.cursor()

        query = """ insert into books (book_id, title ,author,
        category, price, stock )
        values(%s, %s, %s, %s, %s, %s)"""

        data = (book_id, title, author, category, price, stock)
        c.execute(query, data)
        con.commit()

        print("created")

    except:
        print("not working")

    finally:
        if c:
            c.close()
        con.close()


def read_books():
    con = get_db_connection()
    if con is None:
        return

    c = None
    try:
        c = con.cursor()
        query = "select * from books"
        c.execute(query)
        records = c.fetchall()

        if records:
            for row in records:
                print(row)
        else:
            print("no such records")

    except:
        print("try failed")

    finally:
        if c:
            c.close()
        con.close()


def read_book(book_id):
    con = get_db_connection()
    if con is None:
        return

    c = None
    try:
        c = con.cursor()
        query = "select * from books where book_id=%s"
        data = (book_id,)
        c.execute(query, data)
        record = c.fetchone()

        if record:
            print(record)
        else:
            print("no such book")

    except:
        print("try failed to work")

    finally:
        if c:
            c.close()
        con.close()


# updateing

def update_book(book_id, price):
    con = get_db_connection()
    if con is None:
        return

    c = None
    try:
        c = con.cursor()
        query = "update books set price=%s where book_id=%s "
        data = (price, book_id)
        c.execute(query, data)
        con.commit()

        if c.rowcount > 0:
            print("succesfully updated")
            print(c.rowcount)
        else:
            print("not updated")

    except:
        print("failed to update, try failed")

    finally:
        if c:
            c.close()
        con.close()


# deleting the book

def delete_book(book_id):
    con = get_db_connection()
    if con is None:
        return

    c = None
    try:
        c = con.cursor()
        query = "delete from books where book_id = %s"
        data = (book_id,)
        c.execute(query, data)
        con.commit()

        if c.rowcount > 0:
            print("deleted succesfully")
        else:
            print("no book deleted")

    except:
        print("try didnt work")

    finally:
        if c:
            c.close()
        con.close()


def read_books_below_500():
    con = get_db_connection()
    if con is None:
        return

    c = None
    try:
        c = con.cursor()
        query = "select * from books where price < 500"
        c.execute(query)
        records = c.fetchall()

        if records:
            for row in records:
                print(row)
        else:
            print("if not working")

    except:
        print("try not working")

    finally:
        if c:
            c.close()
        con.close()


def count_books_category():
    con = get_db_connection()
    if con is None:
        return

    c = None
    try:
        c = con.cursor()
        query = "select category , count(*) from books group by category"
        c.execute(query)
        records = c.fetchall()

        if records:
            for row in records:
                print(row)
        else:
            print("not found, if not working")

    except:
        print("failed, try not working")

    finally:
        if c:
            c.close()
        con.close()


def second_highest_price():
    con = get_db_connection()
    if con is None:
        return

    c = None
    try:
        c = con.cursor()

        query = "select max(price) from books where price < (select max(price) from books)"
        c.execute(query)
        record = c.fetchone()

        if record[0] is not None:
            print(record[0])
        else:
            print("if not working")

    except:
        print("try not working")

    finally:
        if c:
            c.close()
        con.close()


def purchase_book(book_id, quantity):
    con = get_db_connection()
    if con is None:
        return

    c = None
    try:
        c = con.cursor()

        query = "select stock from books where book_id = %s"
        data = (book_id,)
        c.execute(query, data)
        record = c.fetchone()

        if record:
            stock = record[0]

            if quantity > 0 and stock >= quantity:
                query = "update books set stock=%s where book_id=%s"
                data = (stock - quantity, book_id)
                c.execute(query, data)
                con.commit()
                print("Book purchased successfully")

            else:
                con.rollback()
                print("Insufficient stock")

        else:
            print("Book not found")

    except:
        con.rollback()
        print("Failed to purchase book")

    finally:
        if c:
            c.close()
        con.close()


while (1):

    print("1, create")
    print("2 Display ")
    print("3 search book by ID")
    print("4 update price")
    print("5 Delete")
    print("6 Display books below 500")
    print("7 Count books in each category")
    print("8 Find second highest book price")
    print("9 Purchase book")
    print("10Exit")

    ch = int(input("Enter choice: "))

    if ch == 1:
        book_id = int(input("book ID"))
        title = input("book title ")
        author = input("author name ")
        category = input("category")
        price = float(input("price "))
        stock = int(input(" "))

        create_book(book_id, title, author, category, price, stock)

    elif ch == 2:
        read_books()

    elif ch == 3:
        book_id = int(input("Enter id"))
        read_book(book_id)

    elif ch == 4:
        book_id = int(input("Enter id"))
        price = float(input("enter new price: "))
        update_book(book_id, price)

    elif ch == 5:
        book_id = int(input("id "))
        delete_book(book_id)

    elif ch == 6:
        read_books_below_500()

    elif ch == 7:
        count_books_category()

    elif ch == 8:
        second_highest_price()

    elif ch == 9:
        book_id = int(input("id "))
        quantity = int(input("quantity"))
        purchase_book(book_id, quantity)

    elif ch == 10:
        print("Thank you")
        exit()

    else:
        print("no choise available")
