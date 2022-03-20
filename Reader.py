from datetime import datetime

class Reader:
  _id = 0
  def __init__(self):
    self.id = Reader._id
    Reader._id +=1
    self.books = {}

# read_book – receives a book title and adds it + the current date to the books list
  def read_book(self,book_title):
    date = datetime.today().strftime('%d-%m-%Y')
    self.books[book_title] = date