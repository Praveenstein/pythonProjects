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
from contextlib import contextmanager

# User Import
from library.orm.models import Staffs, Department, \
    Students, Professors, Books, BookItem, MyEnum, StudentActivity, \
    ProfessorActivity, StudentBorrow, ProfessorBorrow, Base
from library.connections.get_connection import Session, config_session, engine


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except AssertionError as err:
        QUERY_LOGGER.error(err)
    except AttributeError as err:
        session.rollback()
        QUERY_LOGGER.error(err)
    finally:
        session.close()


__author__ = 'praveen@gyandata.com'

QUERY_LOGGER = logging.getLogger(__name__)


def config_log_query():
    with open('D:\\Profession\\Intern\\Assignments\\master_repo\\'
              'pythonProjects\\configs\\analyse_log.json', 'r') as file:
        config = json.load(file)

    logging.config.dictConfig(config)


def student_issue(staff, s_id, b_id):
    """
    Function to issues books to student

    Parameters
    ----------

    staff : int
        Staff id who handled the issue.
    s_id : int
        Students id.
    b_id : list
        list of book-item bar codes being borrowed
    """

    print("\nIssuing\n")

    with session_scope() as session:
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


def professor_issue(staff, p_id, b_id):
    """
    Function to issues books to professor

    Parameters
    ----------
    staff : int
        Staff id who handled the issue.
    p_id : int
        Professor id.
    b_id : list
        list of book-item bar codes being borrowed
    """

    print("\nIssuing\n")

    with session_scope() as session:
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


def student_returning(b_id, lost=False, tampered=False):
    """
    Function to return books from student.

    Parameters
    ----------

    b_id : list
        list of book-item bar codes being returned.
    lost : bool
        True if the students has lost the book.
    tampered : bool
        True if the book was tampered while returning.

    """
    print("\nReturning\n")

    with session_scope() as session:
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
            student_borrow.return_date = date.today()
            session.flush()

            print("Books are returned")


def professor_returning(b_id, lost=False, tampered=False):
    """
    Function to return books from professor.

    Parameters
    ----------

    b_id : list
        list of book-item bar codes being returned.
    lost : bool
        True if the professor has lost the book.
    tampered : bool
        True if the book was tampered while returning.

    """
    print("\nReturning\n")

    with session_scope() as session:
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
            professor_borrow.return_date = date.today()
            session.flush()
            print("Books are returned")


def impact(dep):
    """
    Function to check the impact on a department.

    Parameters
    ----------
    dep : int
        Department Id

    """
    with session_scope() as session:
        # Asserting parameters
        assert isinstance(dep, int), "Department Id should be integer"

        # Getting department object
        department = session.query(Department).filter_by(dept_id=dep).first()
        if not department:
            # If department is not in database, raise attribute error
            raise AttributeError("Department not in DB")

        # Getting list of students and their transactions who are from different
        # department but borrowed book from the given department
        query = session.query(StudentActivity.trans_id,
                              Books.name,
                              Students.name,
                              Department.name)
        query = query.join(StudentBorrow, StudentActivity.trans_id == StudentBorrow.student_trans_id)
        query = query.join(BookItem, StudentBorrow.book_bar_code_id == BookItem.bar_code)
        query = query.join(Books, BookItem.isbn_id == Books.isbn_id)
        query = query.join(Students, StudentActivity.student_id == Students.reg_id)
        query = query.join(Department, Students.dept_id == Department.dept_id)
        query = query.filter(Books.dept_id == dep).filter(Students.dept_id != dep)
        results = query.all()
        if not results:
            # If no activity was found, it raise an attribute error
            raise AttributeError("No Activity For this Department's Books")

        for row in results:
            print(f"Transaction Id: {row[0]}\tBook Name:{row[1]}\tStudent name: {row[2]},"
                  f"\tstudent department: {row[3]}")


def check_status(book_id):
    """
    Function to check the status of a given book

    Parameters
    ----------

    book_id : int
        Primary Key/ Isbn code of Book.
    """
    print("\nChecking\n")

    with session_scope() as session:
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
                    due_date = student_borrow.due_date
                else:
                    # If student borrow is none, then checking with the professor borrow
                    professor_borrow = session.query(ProfessorBorrow). \
                        filter(ProfessorBorrow.book_item == item). \
                        order_by(ProfessorBorrow.professor_trans_id.desc()).first()
                    if professor_borrow:
                        # if professor borrow is not none, then
                        # assigning the due date to the due date from the professor borrow
                        due_date = professor_borrow.due_date

                print(
                    f"\nBook Name: {book_object.name} - Bard Code: {item.bar_code}"
                    f" is {item.status.name} and is due return on: {due_date}\n")
            else:
                print(f"\nBook Name: {book_object.name} - Bard Code: {item.bar_code}"
                      f" is {item.status.name}\n")


def basic_trans():
    """
    Function to perform some basic book issue to students and showing how errors occur

    Returns
    -------
    None
    """

    # Issuing book (id-[1]) to student (id-1) by staff (id-1)
    student_issue(1, 1, [1])

    student_issue(1, 2, [3, 5])

    student_issue(1, 2, [2])

    # Student Returning [Session, Book_item bar code[2]]
    student_returning([2])

    # Student trying to return a book, which was never borrowed,
    # Hence will raise an error, saying it was not found in an borrows
    student_returning([6])

    # Trying to issue book to student of book-item bar code = 1,
    # Since that was previously issued, it raises an error that it is unavailable
    student_issue(1, 3, [1])


def test_tamper():
    """
    Function to show how security is enforced using tampered parameter

    Returns
    -------
    None
    """

    print("\nTesting Tampering----------------\n")

    # Issuing book to student
    student_issue(1, 3, [22])

    # Student returns the book tampered
    # Hence he will be asked to pay fine,
    # And the tampered attribute will be set to True
    student_returning([22], tampered=True)

    # Issuing the same book [bar_code = 22] to student
    student_issue(1, 3, [22])

    # Student returns the book tampered,
    # Since the book was previously tampered,
    # He will not be asked to pay fine
    student_returning([22], tampered=True)

    # Student is issued the same book
    student_issue(1, 3, [22])

    # Student lost the book bar_code = 22
    # He will be asked to pay fine and
    # The status will be changed to lost
    student_returning([22], lost=True)

    # When the lost book is tried to be issued to a student
    # It raises an error that the book is lost
    student_issue(1, 3, [22])


def impact_analysis():
    """
    Function to see the impact of new curriculum

    Returns
    -------
    None
    """

    print("\nIssuing to check Analysis----------\n")

    # Issuing some book to students who are
    # from the same department as the book and also from different department
    # Here a Computer science book is being issued to students
    student_issue(1, 2, [24])
    student_issue(1, 3, [26])
    student_issue(1, 13, [28])
    student_returning([28])
    student_issue(1, 28, [29])

    print("\nAnalysing--------------------\n")
    # Calling the impact function to see the impact
    # On computer science department [id=2]
    impact(2)

    print("\nChecking status of book -----------------------\n")
    # Checking the status of book of ISBN-15
    check_status(15)


def main():
    """
    Main function to call the required functions and do some testing
    """

    # Configuring the query log
    config_log_query()

    # Configuring the session factory
    config_session()

    # Calling the basic transaction to do some issues
    basic_trans()

    # calling test tamper function check the security activities
    test_tamper()

    # Calling impact analysis to issue to books and check the impact
    # On Computer science department
    impact_analysis()

    # Deleting all tables
    Base.metadata.drop_all(engine)


if __name__ == '__main__':
    main()
