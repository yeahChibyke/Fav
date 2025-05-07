# pragma version ^0.4.0
# @license MIT

struct Person:
    name: String[10]
    fav_num: uint256 

list_of_fav_num: public(uint256[5])
list_of_persons: public(Person[5])
index: uint256 

name_to_fav_num: HashMap[String[10], uint256]
    
@external
def add_person(person_name: String[10], person_fav_num: uint256):
    new_person: Person = Person(name = person_name, fav_num = person_fav_num)
    self.list_of_persons[self.index] = new_person 
    self.list_of_fav_num[self.index] = person_fav_num
    self.name_to_fav_num[person_name] = person_fav_num
    self.index = self.index + 1
    

@external
@view 
def get_fav_num(person_name: String[10]) -> uint256:
    return self.name_to_fav_num[person_name]


