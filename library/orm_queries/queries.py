# -*- coding: utf-8 -*-
""" Module to do some transactions with the library database

This script contains all the code details required to perform the
orm_queries based SQL operations, and do some transactions on the
library database, it contains the following functions

    * log
    * student_issue
    * professor_issue
    * professor_returning
    * student_returning
    * impact
    * check_status
    * test
    * main

This script requires that the following packages be installed within the Python
environment you are running this script in.

    * sqlalchemy - Package used to connect to a database and do SQL
      operations using orm_queries.
    * library_class - orm_queries classes for the library database.
    * json - To deal with Json Files.
    * logging - To log Errors.
    * datetime - To deal with datetime objects.

"""

# Standard import
from datetime import date
import json
import logging
import logging.config

# External import
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# User Import
from library.orm_queries.models import Staffs, Department, \
    Students, Professors, Books, BookItem, MyEnum, StudentActivity, \
    ProfessorActivity, StudentBorrow, ProfessorBorrow, Base


__author__ = 'praveen@gyandata.com'


def log():
    """
    Creates a custom logger from the configuration dictionary
    """
    with open('D:\\Profession\\Intern\\Assignments\\master_repo\\'
              'pythonProjects\\configs\\analyse_log.json', 'r') as file:
        config = json.load(file)
        logging.config.dictConfig(config)
    global logger
    logger = logging.getLogger(__name__)


def student_issue(session, staff, s_id, b_id):
    """
    Function to issues books to student

    Parameters
    ----------
    session: Session

    staff : int
        Staff id who handled the issue.
    s_id : int
        Students id.
    b_id : list
        list of book-item bar codes being borrowed
    """

    print("\nIssuing\n")

    # Asserting the parameters
    assert isinstance(staff, int), "Staff ID should be integer"
    assert isinstance(s_id, int), "Student ID should be integer"
    assert isinstance(b_id, list), "Books should be a list"

    # Getting Student object
    student = session.query(Students).filter_by(reg_id=s_id).first()

    if not student:
        # If student id is not in database, then raises attribute error
        raise AttributeError("Student not in DB")

    # Getting staff object
    staff = session.query(Staffs).filter_by(staff_id=staff).first()

    if not staff:
        # If staff id is not in database, raise attribute error
        raise AttributeError("Staff not in DB")

    # Getting all book-item objects
    book_list = session.query(BookItem). \
        filter(BookItem.bar_code.in_(b_id)).all()

    if (not book_list) or (len(b_id) != len(book_list)):
        # If books not in database, then raise attribute error
        raise AttributeError("Book item not in DB")

    for book_item in book_list:
        if book_item.status != MyEnum.AVAILABLE:
            # If book is not available then raise attribute error
            raise AttributeError("Book item not Available")
        # If all books are available, then their status are changed
        book_item.status = MyEnum.UNAVAILABLE

    # Creating a student activity object to enter transaction details
    student_activity = StudentActivity(doi=date.today(),
                                       student=student,
                                       staff=staff)
    session.add(student_activity)

    # Adding all the book items to student activity
    student_activity.book_items = book_list
    session.flush()

    # Printing all details
    print(f"Student: {student.name}\n")
    print(f"Student_ Activity Id: {student_activity.trans_id}\n")
    print(f"Date Of Issue: {student_activity.doi}\n")
    for book_item in book_list:
        print("Name of book: ", book_item.book.name)


def professor_issue(session, staff, p_id, b_id):
    """
    Function to issues books to professor

    Parameters
    ----------
    session: Session

    staff : int
        Staff id who handled the issue.
    p_id : int
        Professor id.
    b_id : list
        list of book-item bar codes being borrowed
    """

    print("\nIssuing\n")

    # Asserting the parameters
    assert isinstance(staff, int), "Staff ID should be integer"
    assert isinstance(p_id, int), "Professor ID should be integer"
    assert isinstance(b_id, list), "Books should be a list"

    # Getting Professor object
    professor = session.query(Professors).\
        filter_by(employee_code=p_id).first()

    if not professor:
        # If Professor id is not in database, then raises attribute error
        raise AttributeError("Professor not in DB")

    staff = session.query(Staffs).filter_by(staff_id=staff).first()
    if not staff:
        # If staff id is not in database, raise attribute error
        raise AttributeError("Staff not in DB")

    # Getting all book-item objects
    book_list = session.query(BookItem).\
        filter(BookItem.bar_code.in_(b_id)).all()

    if (not book_list) or (len(b_id) != len(book_list)):
        # If books not in database, then raise attribute error
        raise AttributeError("Book item not in DB")

    for book_item in book_list:
        if book_item.status != MyEnum.AVAILABLE:
            # If book is not available then raise attribute error
            raise AttributeError("Book item not Available")
        # If all books are available, then their status are changed
        book_item.status = MyEnum.UNAVAILABLE

    # Creating a professor activity object to enter transaction details
    professor_activity = ProfessorActivity(doi=date.today(),
                                           professor=professor,
                                           staff=staff)
    session.add(professor_activity)

    # Adding all the book items to student activity
    professor_activity.book_items = book_list
    session.flush()

    # Printing all details
    print(f"Professor: {professor.name}\n")
    print(f"Professor_ Activity Id: {professor_activity.trans_id}\n")
    print(f"Date Of Issue: {professor_activity.doi}\n")
    for book_item in book_list:
        print("Name of book: ", book_item.book.name)


def student_returning(session, b_id, lost=False, tampered=False):
    """
    Function to return books from student.

    Parameters
    ----------
    session: Session

    b_id : list
        list of book-item bar codes being returned.
    lost : bool
        True if the students has lost the book.
    tampered : bool
        True if the book was tampered while returning.

    """
    print("\nReturning\n")

    # Asserting the parameters
    assert isinstance(b_id, list), "Books should be a list"
    assert isinstance(lost, bool), "Lost has to be boolean"
    assert isinstance(tampered, bool), "Tampered has to be boolean"

    # Getting list of book objects
    book_list = session.query(BookItem).\
        filter(BookItem.bar_code.in_(b_id)).all()
    if (not book_list) or (len(b_id) != len(book_list)):
        # If books not in database, then raise attribute error
        raise AttributeError("Book item not in DB")

    for i in range(len(book_list)):
        # Getting list of student borrow where the given book item occurred
        student_borrow = session.query(StudentBorrow).\
            filter(StudentBorrow.book_item == book_list[i]). \
            order_by(StudentBorrow.student_trans_id.desc()).first()
        if not student_borrow:
            # If book did not occur in any previous transaction,
            # then raise an attribute error
            raise AttributeError("Book Not Found in Any Borrowed Transaction")
        if lost:
            # If book is lost then, status is changed to lost and
            # student has to pay fine
            book_list[i].status = MyEnum.LOST
            print("\npay Fine\n")
        else:
            # If book is not lost, then status is changed to available
            book_list[i].status = MyEnum.AVAILABLE

        if tampered:
            # If book is tampered
            if not book_list[i].tampered:
                # if the book item was not tampered previously,
                # then the tampered is changed to true
                print("\npay Fine\n")
                book_list[i].tampered = True

        # Assigning the return date to today
        student_borrow.rd = date.today()
        session.flush()

        print("Books are returned")


def professor_returning(session, b_id, lost=False, tampered=False):
    """
    Function to return books from professor.

    Parameters
    ----------
    session: Session

    b_id : list
        list of book-item bar codes being returned.
    lost : bool
        True if the professor has lost the book.
    tampered : bool
        True if the book was tampered while returning.

    """
    print("\nReturning\n")

    # Asserting the parameters
    assert isinstance(b_id, list), "Books should be a list"
    assert isinstance(lost, bool), "Lost has to be boolean"
    assert isinstance(tampered, bool), "Tampered has to be boolean"

    # Getting list of book objects
    book_list = session.query(BookItem).\
        filter(BookItem.bar_code.in_(b_id)).all()
    if (not book_list) or (len(b_id) != len(book_list)):
        # If books not in database, then raise attribute error
        raise AttributeError("Book item not in DB")

    for i in range(len(book_list)):
        # Getting list of professor borrow where the given book item occurred
        professor_borrow = session.query(ProfessorBorrow).\
            filter(ProfessorBorrow.book_item == book_list[i]). \
            order_by(ProfessorBorrow.professor_trans_id.desc()).first()
        if not professor_borrow:
            # If book did not occurred in any previous transaction,
            # then raise an attribute error
            raise AttributeError("Book Not Found in Any Borrowed Transaction")
        if lost:
            # If book is lost then, status is changed to lost and
            # professor has to pay fine
            book_list[i].status = MyEnum.LOST
        else:
            # If book is not lost, then status is changed to available
            book_list[i].status = MyEnum.AVAILABLE

        if tampered:
            # If book is tampered
            if not book_list[i].tampered:
                # if the book item was not tampered previously,
                # then the tampered is changed to true
                print("\npay Fine\n")
                book_list[i].tampered = True

        # Assigning the return date to today
        professor_borrow.rd = date.today()
        session.flush()
        print("Books are returned")


def impact(session, dep):
    """
    Function to check the impact on a department.

    Parameters
    ----------
    session: Session
    dep : int
        Department Id

    """

    # Asserting parameters
    assert isinstance(dep, int), "Department Id should be integer"

    # Getting department object
    department = session.query(Department).filter_by(dept_id=dep).first()
    if not department:
        # If department is not in database, raise attribute error
        raise AttributeError("Department not in DB")

    # Finding transactions in which the book of given department occurRed, using join
    query = session.query(Books.isbn_id, Books.name,
                          Department.name, BookItem.bar_code,
                          StudentBorrow.student_trans_id)
    query = query.join(Department).join(BookItem).join(StudentBorrow)
    results = query.filter(Department.dept_id == dep).all()
    if not results:
        # If no activity was found, it raise an attribute error
        raise AttributeError("No Activity For this Department's Books")

    data = []
    for result in results:
        trans = session.query(StudentActivity).\
            filter_by(trans_id=result[-1]).first()
        if trans.student.department.dept_id != dep:
            # Looping through the results and getting details
            # Of those students who are not from the given department
            data.append((trans.trans_id, trans.student.name,
                         trans.student.department.name))

    for i in data:
        print(f"Transaction Id: {i[0]}, Student name: {i[1]},"
              f" student department: {i[2]}")


def check_status(session, book_id):
    """
    Function to check the status of a given book

    Parameters
    ----------
    session: Session

    book_id : int
        Primary Key/ Isbn code of Book.
    """
    print("\nChecking\n")

    # Asserting the parameters
    assert isinstance(book_id, int), "Book Id should be integer"

    # Getting the book object
    book_object = session.query(Books).\
        filter(Books.isbn_id == book_id).first()
    if not book_object:
        # If book id is not in database, raise an attribute error
        raise AttributeError("Book not in DB")

    # Getting list of all book items associated with the given book object
    book_items = book_object.book_items
    for item in book_items:
        # Setting due date to none
        due_date = None
        if item.status == MyEnum.UNAVAILABLE:
            # If status of book is unavailable, getting student borrow object
            student_borrow = session.query(StudentBorrow).\
                filter(StudentBorrow.book_item == item). \
                order_by(StudentBorrow.student_trans_id.desc()).first()
            if student_borrow:
                # if student borrow is not none, then
                # assigning the due date to the due date from the student borrow
                due_date = student_borrow.dd
            else:
                # If student borrow is none, then checking with the professor borrow
                professor_borrow = session.query(ProfessorBorrow). \
                    filter(ProfessorBorrow.book_item == item). \
                    order_by(ProfessorBorrow.professor_trans_id.desc()).first()
                if professor_borrow:
                    # if professor borrow is not none, then
                    # assigning the due date to the due date from the professor borrow
                    due_date = professor_borrow.dd

            print(
                f"\nBook Name: {book_object.name} - Bard Code: {item.bar_code}"
                f" is {item.status.name} and is due return on: {due_date}\n")
        else:
            print(f"\nBook Name: {book_object.name} - Bard Code: {item.bar_code}"
                  f" is {item.status.name}\n")


def test(session_factory):
    """
    Function to do some testing with random issues and returns

    """
    # pylint: disable=too-many-branches
    # pylint: disable=too-many-statements
    session = session_factory()
    try:
        # Issuing book (id-[1]) to student (id-1) by staff (id-1)
        student_issue(session, 1, 1, [1])
        # Committing all changes
        session.commit()
    except AssertionError as err:
        logger.error(err)
    except AttributeError as err:
        session.rollback()
        logger.error(err)
    finally:
        session.close()

    session = session_factory()
    try:

        student_issue(session, 1, 2, [3, 5])
        # Committing all changes
        session.commit()
    except AssertionError as err:
        logger.error(err)
    except AttributeError as err:
        session.rollback()
        logger.error(err)
    finally:
        session.close()

    session = session_factory()
    try:

        student_issue(session, 1, 2, [2])
        # Committing all changes
        session.commit()
    except AssertionError as err:
        logger.error(err)
    except AttributeError as err:
        session.rollback()
        logger.error(err)
    finally:
        session.close()

    session = session_factory()
    book = session.query(BookItem).filter_by(bar_code=2).first()
    print(book.status)
    session.close()

    session = session_factory()
    try:

        student_returning(session, [2])
        # Committing all changes
        session.commit()
    except AssertionError as err:
        logger.error(err)
    except AttributeError as err:
        session.rollback()
        logger.error(err)
    finally:
        session.close()

    session = session_factory()
    try:

        student_returning(session, [6])
        # Committing all changes
        session.commit()
    except AssertionError as err:
        logger.error(err)
    except AttributeError as err:
        session.rollback()
        logger.error(err)
    finally:
        session.close()

    session = session_factory()
    try:

        student_issue(session, 1, 3, [1])
        # Committing all changes
        session.commit()
    except AssertionError as err:
        logger.error(err)
    except AttributeError as err:
        session.rollback()
        logger.error(err)
    finally:
        session.close()

    print("\nTesting Tampering----------------\n")
    session = session_factory()
    try:

        student_issue(session, 1, 3, [22])
        # Committing all changes
        session.commit()
    except AssertionError as err:
        logger.error(err)
    except AttributeError as err:
        session.rollback()
        logger.error(err)
    finally:
        session.close()

    session = session_factory()
    try:

        student_returning(session, [22], tampered=True)
        # Committing all changes
        session.commit()
    except AssertionError as err:
        logger.error(err)
    except AttributeError as err:
        session.rollback()
        logger.error(err)
    finally:
        session.close()

    session = session_factory()
    try:

        student_issue(session, 1, 3, [22])
        # Committing all changes
        session.commit()
    except AssertionError as err:
        logger.error(err)
    except AttributeError as err:
        session.rollback()
        logger.error(err)
    finally:
        session.close()

    session = session_factory()
    try:

        student_returning(session, [22], tampered=True)
        # Committing all changes
        session.commit()
    except AssertionError as err:
        logger.error(err)
    except AttributeError as err:
        session.rollback()
        logger.error(err)
    finally:
        session.close()

    session = session_factory()
    try:

        student_issue(session, 1, 3, [22])
        # Committing all changes
        session.commit()
    except AssertionError as err:
        logger.error(err)
    except AttributeError as err:
        session.rollback()
        logger.error(err)
    finally:
        session.close()

    session = session_factory()
    try:

        student_returning(session, [22], lost=True)
        # Committing all changes
        session.commit()
    except AssertionError as err:
        logger.error(err)
    except AttributeError as err:
        session.rollback()
        logger.error(err)
    finally:
        session.close()

    session = session_factory()
    try:

        student_issue(session, 1, 3, [22])
        # Committing all changes
        session.commit()
    except AssertionError as err:
        logger.error(err)
    except AttributeError as err:
        session.rollback()
        logger.error(err)
    finally:
        session.close()

    print("\nIssuing to check Analysis----------\n")

    session = session_factory()
    try:

        student_issue(session, 1, 2, [24])
        # Committing all changes
        session.commit()
    except AssertionError as err:
        logger.error(err)
    except AttributeError as err:
        session.rollback()
        logger.error(err)
    finally:
        session.close()

    session = session_factory()
    try:

        student_issue(session, 1, 3, [26])
        # Committing all changes
        session.commit()
    except AssertionError as err:
        logger.error(err)
    except AttributeError as err:
        session.rollback()
        logger.error(err)
    finally:
        session.close()

    session = session_factory()
    try:

        student_issue(session, 1, 13, [28])
        # Committing all changes
        session.commit()
    except AssertionError as err:
        logger.error(err)
    except AttributeError as err:
        session.rollback()
        logger.error(err)
    finally:
        session.close()

    session = session_factory()
    try:
        student_returning(session, [28])
        # Committing all changes
        session.commit()
    except AssertionError as err:
        logger.error(err)
    except AttributeError as err:
        session.rollback()
        logger.error(err)
    finally:
        session.close()

    session = session_factory()
    try:
        student_issue(session, 1, 28, [29])
        # Committing all changes
        session.commit()
    except AssertionError as err:
        logger.error(err)
    except AttributeError as err:
        session.rollback()
        logger.error(err)
    finally:
        session.close()

    print("\nAnalysing--------------------\n")
    session = session_factory()
    try:
        impact(session, 2)
        # Committing all changes
        session.commit()
    except AssertionError as err:
        logger.error(err)
    except AttributeError as err:
        session.rollback()
        logger.error(err)
    finally:
        session.close()

    session = session_factory()
    try:
        check_status(session, 15)
        # Committing all changes
        session.commit()
    except AssertionError as err:
        logger.error(err)
    except AttributeError as err:
        session.rollback()
        logger.error(err)
    finally:
        session.close()


def main():
    """
    Main function to call the required functions and do some testing
    """

    # pylint: disable=no-member
    # pylint: disable=invalid-name

    # Creating the logging object
    log()
    url = "mysql+pymysql://root:nebula@localhost/library1?charset=utf8mb4"
    engine = create_engine(url)

    # Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)

    # calling test function to do some transaction
    test(Session)

    # Deleting all tables
    Base.metadata.drop_all(engine)


if __name__ == '__main__':
    main()
