##Class library->book,librarins,members
## book->book_id,name,author,category,avaliabilty,stock,
##User->libarain,student,faculty/prof
##librarian-id,name,
##libarary-add,remove,register,fetchbook,issue,return
##borrowrecord-book,student,issue_date,return ,status
#TOMORROWS-TASK->
## things i have to complete->duplicate books handling
## borrowing limits-done
## enforce the user type -done
## add one more status overdue and check who haven't returned the book yet means due date!!
## dunder methods!!-done
## multilevel inheritance+access_modifiers_revision

from abc import ABC,abstractmethod
from enum import Enum
from datetime import timedelta,date

class Library:

    def __init__(self):
        self.books = []
        self.members = []
        self.librarians = []
        self.borrow_records = []


    def add_book(self,book):
        self.books.append(book)

    def remove_book(self,book_id):
        for book in self.books:
            if book_id==book.book_id:
                self.books.remove(book)
                return

        raise ValueError("Book not found!!")

    def register_member(self,user):
        if user in self.members:
            raise ValueError("Member already registered")

        self.members.append(user)

    def register_librarian(self, librarian):

        if librarian in self.librarians:
            raise ValueError("Librarian already registered")

        self.librarians.append(librarian)


    def fetch_book(self,book_id):

        for book in self.books:

            if book.book_id == book_id:
                return book

        raise ValueError("Book not found")
    def issue_book(self,user,book_id,issue_date):
        book=self.fetch_book(book_id)
        active_borrowings=0
        for record in self.borrow_records:
            if record.user==user and record.status==BorrowStatus.ISSUED:
                active_borrowings+=1
        
        if active_borrowings>=user.borrowing_limit():
            raise ValueError(
            f"{user.user_name} has reached the borrowing limit"
        )
        if not book.is_available:
            raise ValueError("Book is not available!!")

        record=BorrowRecord(
            record_id=len(self.borrow_records)+1,
            user=user,
            book=book,
            issue_date=issue_date,
            return_date=None,
            status=BorrowStatus.ISSUED
        )
        book.remove_stock(1)
        self.borrow_records.append(record)
        return record
    def return_book(self,user,book_id,return_date):
        book=self.fetch_book(book_id)
        for record in self.borrow_records:
            if record.user==user and record.book==book and record.status in[ BorrowStatus.ISSUED,BorrowStatus.OVERDUE]:
                
                record.return_date=return_date
                record.fine=record.calculate_fine(return_date)
                record.status=BorrowStatus.RETURNED
                book.add_stock(1)
                return record
            
        raise ValueError("No active borrowing record found")

   
class BorrowStatus(Enum):
    ISSUED = "ISSUED"
    RETURNED = "RETURNED"
    OVERDUE = "OVERDUE"




class Book:
    def __init__(self,book_id,book_name,author,category,stock):
        self.book_id=book_id
        self.book_name=book_name
        self.author=author
        self.category=category
        self.stock=stock


    def display(self):

        print("=" * 60 + "BOOK_DETAILS" + "=" * 60)
        print(f"Book ID-->{self.book_id}")
        print(f"Book Name-->{self.book_name}")
        print(f"Author-->{self.author}")
        print(f"Category-->{self.category}")
        print(f"Stock-->{self.stock}")
        print(f"Is Available-->{self.is_available}")

    @property
    def is_available(self):
        return self.stock>0

    def add_stock(self,quantity):
        if quantity<0:
            raise ValueError("Quantity must be gerater than zero!!")

        self.stock+=quantity
    


        
    def remove_stock(self,quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")

        if quantity > self.stock:
            raise ValueError("Not enough books available")

        self.stock -= quantity

        
class User(ABC):
    def __init__(self,user_id,user_name,user_email,user_no):
        self.user_id=user_id
        self.user_name=user_name
        self.user_email=user_email
        self.user_no=user_no


    @abstractmethod
    def user_type(self):
        pass

    @abstractmethod
    def user_details(self):
         
         pass
    
    @abstractmethod
    def borrowing_limit(self):
        pass

    def borrowing_history(self, library):
        print("=" * 60)
        print(f"BORROWING HISTORY - {self.user_name}")
        print("=" * 60)

        found = False

        for record in library.borrow_records:
            if record.user == self:
                found = True

                print(f"Record ID   --> {record.record_id}")
                print(f"Book        --> {record.book.book_name}")
                print(f"Issue Date  --> {record.issue_date}")
                print(f"Return Date --> {record.return_date}")
                print(f"Status      --> {record.status.value}")
                print("-" * 60)

        if not found:
            print("No borrowing history found.")
class Student(User):
    def __init__(self,user_id,user_name,user_email,user_no,dept):
        self.dept=dept
        super().__init__(user_id,user_name,user_email,user_no)

    def borrowing_limit(self):
        return 3
    def user_type(self):
        return "USER_TYPE-->STUDENT"

    def user_details(self):
        print("="*60+"STUDENT_DETAILS"+"="*60)
        print(f"User ID-->{self.user_id}")
        print(f"User Name-->{self.user_name}")
        print(f"Email-->{self.user_email}")
        print(f"Phone-->{self.user_no}")
        print(f"Department-->{self.dept}")
    
   

    def borrow_book(self,library,book_id,issue_date):
        return library.issue_book(self,book_id,issue_date)
       

    def return_book(self,library,book_id,return_date):
        return library.return_book(self,book_id,return_date)
        
    def pay_extra_fee(self,amount):
        if amount<=0:
            raise ValueError("Fee must be greater than 0")

        print(f"{self.user_name} paid extra fee of ${amount}")


class Faculty(User):
    def __init__(self, user_id, user_name, user_email, user_no, department):
        self.department = department
        super().__init__(user_id, user_name, user_email, user_no)

    def user_type(self):
        return "USER_TYPE-->FACULTY"
    def borrowing_limit(self):
        return 5

    def user_details(self):
        print("=" * 60 + "FACULTY_DETAILS" + "=" * 60)
        print(f"User ID-->{self.user_id}")
        print(f"Name-->{self.user_name}")
        print(f"Email-->{self.user_email}")
        print(f"Phone-->{self.user_no}")
        print(f"Department-->{self.department}")

    def borrow_book(self, library, book_id, issue_date):
        return library.issue_book(
            self,
            book_id,
            issue_date
        )

    def return_book(self, library, book_id, return_date):
        return library.return_book(
            self,
            book_id,
            return_date
        )

    def pay_extra_fee(self, amount):
        if amount <= 0:
            raise ValueError("Fee must be greater than 0")

        print(f"{self.user_name} paid extra fee of ₹{amount}")


class Librarian(User):
    def __init__(self,user_id,user_name,user_email,user_no):
        
        super().__init__(user_id,user_name,user_email,user_no)

    def user_type(self):
        return "USER_TYPE-->LIBRARIAN"

    def user_details(self):
        print("="*60+"LIBRARIAN_DETAILS"+"="*60)
        print(f"User ID-->{self.user_id}")
        print(f"User Name-->{self.user_name}")
        print(f"Email-->{self.user_email}")
        print(f"Phone-->{self.user_no}")

    def borrowing_limit(self):
        return 0

    def add_book(self, library, book):
        library.add_book(book)

    def remove_book(self, library, book_id):
        library.remove_book(book_id)

    def fetch_book(self, library, book_id):
        return library.fetch_book(book_id)


class BorrowRecord:
    def __init__(self,record_id,user,book,issue_date,return_date,status):
        self.record_id=record_id
        self.user=user
        self.book=book
        self.issue_date=issue_date
        self.return_date=return_date
        self.due_date=issue_date+timedelta(days=10)
        self.status=status
        self.fine=0
    def calculate_fine(self,current_date):
            if current_date<=self.due_date:
                return 0
            extra_days=(current_date-self.due_date).days
            return extra_days*1

    def check_overdue(self,current_date):
        if self.status==BorrowStatus.RETURNED:
            return
        if current_date>self.due_date:
            self.status=BorrowStatus.OVERDUE
            
    def display(self):
        print("=" * 60 + "BORROW_RECORD_DETAILS" + "=" * 60)
        print(f"Record ID-->{self.record_id}")
        print(f"User-->{self.user.user_name}")
        print(f"Book Name-->{self.book.book_name}")
        print(f"Issue Date-->{self.issue_date}")
        print(f"Due Date    --> {self.due_date}")
        print(f"Return Date --> {self.return_date}")
        print(f"Status      --> {self.status.value}")
        print(f"Fine        --> ₹{self.fine}")

library = Library()

# Books
book1 = Book(
    101,
    "Clean Code",
    "Robert C. Martin",
    "Programming",
    3
)

book2 = Book(
    102,
    "Python Crash Course",
    "Eric Matthes",
    "Programming",
    2
)

library.add_book(book1)
library.add_book(book2)


# Students
student1 = Student(
    1,
    "Rahul",
    "rahul@gmail.com",
    "9876543210",
    "Computer Engineering"
)

student2 = Student(
    3,
    "Raaahul",
    "raddhul@gmail.com",
    "9816543210",
    "ENTC Engineering"
)


# Faculty
faculty1 = Faculty(
    2,
    "Dr. Sharma",
    "sharma@college.edu",
    "9876543211",
    "Computer Engineering"
)


# Librarian
librarian1 = Librarian(
    101,
    "Amit",
    "amit@library.com",
    "9876543212"
)


# Registration
library.register_member(student1)
library.register_member(student2)
library.register_member(faculty1)

library.register_librarian(librarian1)


# Borrow books
record1 = student1.borrow_book(
    library,
    101,
    date(2026, 10, 3)
)

record2 = student2.borrow_book(
    library,
    101,
    date(2026, 10, 3)
)

record3 = faculty1.borrow_book(
    library,
    101,
    date(2026, 10, 3)
)
student1.return_book(
    library,
    101,
    date(2026, 10, 16)
)
student2.return_book(
    library,
    101,
    date(2026, 10, 11)
)

# Display
records = [record1, record2, record3]

for record in records:
    record.display()
members=[student1,student2,faculty1]

for member in members:
    member.borrowing_history(library)

