from dbm.ndbm import library
import shelve
from flask import jsonify
from pymongo import MongoClient
from bson import ObjectId
from Book import *
from Reader import Reader
from Shelf import *
class Library:
  def __init__(self):
    self.__client = MongoClient(port=27017)
    self.__db = self.__client["Library"] 
    self.shelves_collection = self.__db["Shelves"]
    self.shelvesDB = self.shelves_collection.find({}) # select * from shelves
    self.ids = self.get_ids()
    self.shelves = []
    self.readers = {}

  def get_ids(self):
    ids = []
    for shelf in self.shelvesDB:
      ids.append(shelf["_id"])
    return ids
    
  
# is_there_place_for_new_book - Returns a Boolean indicates if there is a place for inserting a new book to the library
  def is_there_place_for_new_book(self):
    for shelf in self.shelves:
      if shelf.is_shelf_full == False:
        return True
      else:
        continue

# add_new_book - receives a new Book object and add it to the first Shelf with a free space
  def add_new_book(self,new_Book_obj):
    obj = {"author" : new_Book_obj.author,
            "title" : new_Book_obj.title,
            "num_of_pages" : new_Book_obj.num_of_pages}
    if self.is_there_place_for_new_book() == True:
      for shelf_num in range(len(self.shelves)):
        id = self.ids[shelf_num]
        if self.shelves[shelf_num].is_shelf_full == False:
          self.shelves[shelf_num].add_book(new_Book_obj)
          self.shelves_collection.update_one({"_id" : id},{"$push" : {"books" : obj}})
          if self.shelves[shelf_num].is_shelf_full == True:
            self.shelves_collection.update_one({"_id" : id},{"$set" : {"is_shelf_full" : True}})
          print("The book is added")
          break
        continue
    else:
      print("All of The shelf's are full there is no more space for adding books")       
  
# delete_book – receives a book title and delete the Book object from the library.
  def delete_book(self,book_title):
    flag = False
    for shelf_num in range(len(self.shelves)):
      id = self.ids[shelf_num]
      for book_num in range(len(self.shelves[shelf_num].books)):
        if self.shelves[shelf_num].books[book_num].title == book_title:
          del self.shelves[shelf_num].books[book_num]
          self.shelves_collection.update_one({"_id" : id},{"$pull": {"books": {"title":  book_title}}})
          print("The book was deleted from shelf number: "+str(shelf_num))
          flag = True
          break
    if flag == False:
      print("There is no book called: "+book_title+" in the library")

  def change_locations(self,title1,title2):
    b1 = []
    b2 = []

    for shelf in self.shelves:
      s1 = list(filter(lambda x: x.title == title1 ,shelf.books))
      s2 = list(filter(lambda x: x.title == title2 ,shelf.books))
      b1.append(s1)
      b2.append(s2)

    if b1.index(s1) == b2.index(s2):
      print("same shelf")
      for shelf in self.shelves:
        for index in range(len(shelf.books)):
          if shelf.books[index].title == title1:
            i1 = index
          elif shelf.books[index].title == title2:
            i2 = index
      self.change_location_in_same_shelf(b1.index(s1)+1,i1,i2)
    else:
      print("Not Same Shelf")
      self.change_locations_different_shelves(title1,title2)

# change_locations – receives 2 books titles, and replace between these 2 Books objects (their locations in the shelves).
  def change_locations_different_shelves(self,title1,title2):
    shelf_index_book1 = -1
    shelf_index_book2 = -1
    book1_index = -1
    book2_index = -1
    for shelf_num in range(len(self.shelves)):
      for book_num in range(len(self.shelves[shelf_num].books)):
        if self.shelves[shelf_num].books[book_num].title == title1:
          book1_index = book_num
          shelf_index_book1 = shelf_num
        elif self.shelves[shelf_num].books[book_num].title == title2:
          book2_index = book_num
          shelf_index_book2 = shelf_num
        else:
          continue
    if book1_index > -1 and book2_index > -1:
      self.change_loc(shelf_index_book1,book1_index,shelf_index_book2,book2_index)
    else:
      print("Book location's not changed, something is wrong.")

  def change_loc(self,s1,b1,s2,b2):
    id1 = self.ids[s1]
    id2 = self.ids[s2]
    book1 = self.shelves[s1].books[b1]
    obj1 = {"author" : book1.author,
            "title" : book1.title,
            "num_of_pages" : book1.num_of_pages}
    book2 = self.shelves[s2].books[b2]
    obj2 = {"author" : book2.author,
            "title" : book2.title,
            "num_of_pages" : book2.num_of_pages}
    self.shelves[s1].books.remove(book1)
    self.shelves[s1].books.insert(b1,book2)
    self.shelves[s2].books.remove(book2)
    self.shelves[s2].books.insert(b2,book1)
    self.shelves_collection.update_one({"_id" : id1 , "books.title": obj1["title"] } , {"$set" : {"books.$": obj2}})
    self.shelves_collection.update_one({"_id" : id2 , "books.title": obj2["title"] } , {"$set" : {"books.$": obj1}})
    print("Book location's changed.")

# change_locations_in_same_shelf – receives a shelf number, and books locations, and replace between these 2 Books objects.
  def change_location_in_same_shelf(self,shelf_number,location1,location2):#->1,0,1
    books_array = []
    for i in self.shelves[shelf_number].books:
      print(i.title)
    id = self.ids[shelf_number] #    id = self.ids[shelf_number-1]
    if shelf_number < len(self.shelves) and location1 < len(self.shelves[shelf_number].books) and location2 < len(self.shelves[shelf_number].books):
      book1 = self.shelves[shelf_number].books[location1]
      book2 = self.shelves[shelf_number].books[location2]
      self.shelves[shelf_number].books.remove(book1)
      self.shelves[shelf_number].books.insert(location1,book2)
      self.shelves[shelf_number].books.remove(book2)
      self.shelves[shelf_number].books.insert(location2,book1)
      for book in self.shelves[shelf_number].books:
        obj = {}
        obj["author"] = book.author
        obj["title"] = book.title
        obj["num_of_pages"] = book.num_of_pages
        books_array.append(obj)
      print(books_array)
      self.shelves_collection.update_one({"_id" : id} , {"$set" : {"books": books_array}})
      print("Book location's changed.")
    else:
      print("Book location's not changed, something is wrong.")

# order_books – order all books in each shelf by their num_of_pages
  def order_books(self):
    print("Before ordering by num_of_pages:")
    for shelf in self.shelves:
      for book in shelf.books:
        print(book.title)
        print(book.num_of_pages)
    print()

    for shelf in self.shelves:
        shelf.books.sort(key = lambda x: x.num_of_pages)
    print("After ordering by num_of_pages:")
    for shelf in self.shelves:
      for book in shelf.books:
        print(book.title)
        print(book.num_of_pages)
    self.shelves_collection.update_one({"_id": self.ids[0]},{"$push" : {"books": {"$each": [],"$sort": {"num_of_pages": 1}}}})
    self.shelves_collection.update_one({"_id": self.ids[1]},{"$push" : {"books": {"$each": [],"$sort": {"num_of_pages": 1}}}})
    self.shelves_collection.update_one({"_id": self.ids[2]},{"$push" : {"books": {"$each": [],"$sort": {"num_of_pages": 1}}}})
    print("Each shelf is ordered by num_of_pages.")

# register_reader – receives a new reader name and id and add it to the readers list.
  def register_reader(self,new_reader_name):
    r = Reader()
    obj = {"reader": r,"id": r.id, "reader_name":new_reader_name}
    self.readers[r.id] = obj
    print("Reader name: " + self.readers[r.id]["reader_name"] + " was added to the readers dictionarie with the Id: " + str(r.id))
    print("Library readers dictionary: ")
    print(self.readers)
    print()

# remove_reader – receives a new reader name and removes it from the readers list.
  def remove_reader(self,reader_name):
    flag = False
    values = list(self.readers.values())
    for i in range(len(values)):
      if values[i]["reader_name"] == reader_name:
        flag = True
        del self.readers[i]
        break
      else:
        continue
    if flag == True:
      print("Reader name: "+reader_name+" was deleted from Readers dictionarie.")
    else:
      print("No Reader name: "+reader_name+" was found in Readers dictionarie.")

# reader_read_book – receives a book title and a reader name and add this book title to the reader’s books list
  def reader_read_book(self,book_title,reader_name):
    flag = False
    print("All reader's list's before inserting: ")
    for reader_obj in self.readers:
      print(self.readers[reader_obj]["reader"].books)
    print()
    
    for s in self.shelves:
      for b in s.books:
        if book_title == b.title:
          for key, value in dict(self.readers).items():
            if value["reader_name"] == reader_name:
              self.readers[key]["reader"].read_book(book_title)
              flag = True
              # print(self.readers[key]["reader"].books)
              break
        else:
          continue

    if flag == True:
      print("Book named: "+book_title+" was added successfully to Reader name: "+reader_name+" books list.")
    else:  
      print("There is no book named: "+book_title+" in the Library please check the name of the book again.")

    print()
    print("All reader's list's after inserting: ")
    for reader_obj in self.readers:
      print(self.readers[reader_obj]["reader_name"]+":")
      print(self.readers[reader_obj]["reader"].books)

# search_by_author – receives an author name and returns all books titles this author wrote
  def search_by_author(self,author_name):
    b = []
    for shelf in self.shelves:
      s = list(filter(lambda x: x.author == author_name ,shelf.books))
      if len(s)>0:
        b.append(s) # b = [[book.book],[book.book]]
    if len(b)>0:
      print(b)
      print(author_name + " wrote this books:")
      for i in range(len(b)):
        for j in b[i]:
          print(j.title)
    else:
      print("There is no books that author named: " + author_name + " wrote, \nplease check author name again.") 

