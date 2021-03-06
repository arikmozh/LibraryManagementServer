from webbrowser import get
from Shelf import *
from Book import *
from Reader import * 
from Library import *

from pymongo import MongoClient
from bson import ObjectId
import requests
import json
import os 
import sys

client = MongoClient(port=27017)
db = client["Library"]
shelves_collection = db["Shelves"]
shelves = shelves_collection.find({}) # select * from shelves
library = Library()

shelf1 = Shelf()
shelf2 = Shelf()
shelf3 = Shelf()

def utilize_from_mongo():
  for book in shelves[0]["books"]:
    print(book)
    b = Book()
    b.author = book["author"]
    b.title = book["title"]
    b.num_of_pages = book["num_of_pages"]
    shelf1.books.append(b)
  shelf1.is_shelf_full = shelves[0]["is_shelf_full"]
  for book in shelves[1]["books"]:
    b = Book()
    b.author = book["author"]
    b.title = book["title"]
    b.num_of_pages = book["num_of_pages"]
    shelf2.books.append(b)
  shelf2.is_shelf_full = shelves[1]["is_shelf_full"]
  for book in shelves[2]["books"]:
    b = Book()
    b.author = book["author"]
    b.title = book["title"]
    b.num_of_pages = book["num_of_pages"]
    shelf3.books.append(b)
  shelf3.is_shelf_full = shelves[2]["is_shelf_full"]
  library.shelves.append(shelf1)
  library.shelves.append(shelf2)
  library.shelves.append(shelf3)

user_Names_Emails = []

def utilize_access():
  # #Get ALl users
  resp = requests.get("https://jsonplaceholder.typicode.com/users")
  pers = resp.json()
  user_Names_List = list(map(lambda x: x["username"],pers))
  user_Emails_List = list(map(lambda x: x["email"],pers))
  user_Names_Emails.append(user_Names_List)
  user_Names_Emails.append(user_Emails_List)

def check_username_email(user_name,user_email):
  if user_name in user_Names_Emails[0] and user_email in user_Names_Emails[1]:
    if user_Names_Emails[0].index(user_name) == user_Names_Emails[1].index(user_email):
      return True
    else:
      print("Invalid username or email. \nplease try again")
      return False
  else:
      print("Invalid username or email \nplease try again")
      return False

def switch(option):
  if option == 1:
    print("Option - 1: Adding a book to the library: ")
    obj = Book()
    obj.author = input("Enter book author name: ")
    obj.title = input("Enter book title: ")
    obj.num_of_pages = int(input("Enter book num of pages: "))
    library.add_new_book(obj)

  elif option == 2:
    print("Option - 2: deleting a book from the library: ")
    title = input("Enter book title you want to delete from the library: ")
    library.delete_book(title)

  elif option == 3:
    print("Option - 3: changing 2 books location in the library: ")
    title1 = input("Please enter book title - 1:")
    title2 = input("Please enter book title - 2:")
    library.change_locations(title1,title2)
  
  elif option == 4:
    print("Option - 4: registering a new reader to the library: ")
    reader_name = input("Please enter reader's name you want to add to the readers list of the library: ")
    library.register_reader(reader_name)

  elif option == 5:
    print("Option - 5: removing a reader from the library: ")
    reader_name = input("Please enter reader's name you want to remove from the readers list of the library: ")
    library.remove_reader(reader_name)

  elif option == 6:
    print("Option - 6: searching library books by author: ")
    author = input("Please enter author name: ")
    library.search_by_author(author)

  elif option == 7:
    print("Option - 7: reading a book by a reader: ")
    reader_name = input("Please enter reader name to add books to: ")
    book_title = input("Please enter book title to add: ")
    library.reader_read_book(book_title,reader_name)

  elif option == 8:
    print("Option - 8: ordering all books by page number: ")
    library.order_books()

  elif option == 9:
    print("Option - 9: For saving all data")
    l = {}
    shelves = []
    readers = []
    for shelf in library.shelves:
      obj_shelf = {}
      shelf_books = []
      # obj_shelf["is_shelf_full"] = shelf.is_shelf_full
      for book in shelf.books:
        obj_book = {}
        obj_book["author"] = book.author
        obj_book["title"] = book.title
        obj_book["num_of_pages"] = book.num_of_pages
        shelf_books.append(obj_book)
      obj_shelf["books"] = shelf_books
      obj_shelf["is_shelf_full"] = shelf.is_shelf_full

      shelves.append(obj_shelf)
    l["Shelves"] = shelves

    for reader_obj in library.readers:
      obj = {}
      obj["id"] = reader_obj
      obj_r_books = []
      for book in library.readers[reader_obj]["reader"].books:
        obj_b = {}
        obj_b["title"] = book
        obj_b["date"] = library.readers[reader_obj]["reader"].books[book]
        obj_r_books.append(obj_b)
      obj["books"] = obj_r_books
      readers.append(obj)
    l["Readers"] = readers
  
    file_name = input("Please enter file name: ")
    f = open(os.path.join(sys.path[0],file_name+".json"),'w')
    json.dump(l,f)

    f.close()

  elif option == 10:
    print("Option - 10: For loading library data from json file: ")

    library.shelves = []
    library.readers = {}
    shelf1 = Shelf()
    shelf2 = Shelf()
    shelf3 = Shelf()
    shelves_collection.drop()

    filename = input("please enter a file name: ")
    f = open(os.path.join(sys.path[0],filename+".json"),'r')
    data = json.load(f)
    f.close()

    shelves = data["Shelves"]

    for book in shelves[0]["books"]:
      b = Book()
      b.author = book["author"]
      b.title = book["title"]
      b.num_of_pages = book["num_of_pages"]
      shelf1.books.append(b)
    if len(shelf1.books)< 5:
      shelf1.is_shelf_full = False
    for book in shelves[1]["books"]:
      b = Book()
      b.author = book["author"]
      b.title = book["title"]
      b.num_of_pages = book["num_of_pages"]
      shelf2.books.append(b)  
    if len(shelf2.books)< 5:
      shelf2.is_shelf_full = False
    for book in shelves[2]["books"]:
      b = Book()
      b.author = book["author"]
      b.title = book["title"]
      b.num_of_pages = book["num_of_pages"]
      shelf3.books.append(b)
    if len(shelf3.books)< 5:
      shelf3.is_shelf_full = False
    
    library.shelves.append(shelf1)
    library.shelves.append(shelf2)
    library.shelves.append(shelf3)


    readers = data["Readers"]
    for reader in readers:
      r = Reader()
      print(reader)
      obj = {}
      for book in reader["books"]:
        r.books[book["title"]] = book["date"]
      obj["reader"] = r
      obj["id"] = r.id
      obj["reader_name"] = "reader from json"+str(r.id)
      library.readers[r.id] = obj

    shelves_collection.insert_many(shelves)
    ids = []
    for shelf in shelves_collection.find({}):
      ids.append(shelf["_id"])
    library.ids = ids

  else:
    print("Incorrect option")

  print("\nFor adding a book - Press 1."+
    "\nFor deleting a book - Press 2."+
    "\nFor changing books locations - Press 3."+
    "\nFor registering a new reader - Press 4."+
    "\nFor removing a reader - Press 5."+
    "\nFor searching books by author ??? Press 6."+
    "\nFor reading a book by a reader ??? Press 7."+
    "\nFor ordering all books ??? Press 8."+
    "\nFor saving all data ??? Press 9."+
    "\nFor loading data ??? Press 10."+
    "\nFor exit ??? Press 11.\n")

utilize_access()

username = input("Enter your username: ")
email = input("Enter your email address: ")

while check_username_email(username,email) == False:
  username = input("Enter your username: ")
  email = input("Enter your email address: ")
  check_username_email(username,email)
else:
  print("Ok, username and password matched")
  utilize_from_mongo()
  print("\nFor adding a book - Press 1."+
    "\nFor deleting a book - Press 2."+
    "\nFor changing books locations - Press 3."+
    "\nFor registering a new reader - Press 4."+
    "\nFor removing a reader - Press 5."+
    "\nFor searching books by author ??? Press 6."+
    "\nFor reading a book by a reader ??? Press 7."+
    "\nFor ordering all books ??? Press 8."+
    "\nFor saving all data ??? Press 9."+
    "\nFor loading data ??? Press 10."+
    "\nFor exit ??? Press 11.")
  option = int(input("Enter your option: "))
  while option != 11:
    switch(option)
    option = int(input("Enter your option: "))
  
print("finished")
