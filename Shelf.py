from pymongo import MongoClient
from bson import ObjectId

class Shelf:
  def __init__(self):
    self.__client = MongoClient(port=27017)
    self.__db = self.__client["Library"] 
    self.shelves_collection = self.__db["Shelves"]
    self.books = []
    self.is_shelf_full = False

#addBook – receives a Book object and add it to the books list in the first
# available. If there is no more space , a proper message will be printed. If the shelf become full (with 5 Book objects), than the “is_shelf_full” will be set to True. Otherwise, will be set to False.
  def add_book(self,new_Book_obj):
    if len(self.books) < 5:
      self.books.append(new_Book_obj)
    if len(self.books) == 5:
      self.is_shelf_full = True
      print("The shelf is full there is no more space for adding books")

# replace_books – receives 2 numbers between 1 and 5 and replace between the
# Books in these locations. If one of the location is empty, a proper message will
# be printed.

  #def replace_books(self,num1,num2):
      #Done it in Library class
# order_books – order the books by their num_of_pages in ascending order.

  #def order_books(self):
      #Done it in Library class
