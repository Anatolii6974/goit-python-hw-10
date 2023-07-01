from collections import UserDict
from datetime import datetime
from faker import Faker, Factory
import json
import re




class Field:
    def __init__(self, value=None):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        # add your own logic
        self._value = new_value    

    def add_to_record(self, record):
        pass

    def remove_from_record(self, record):
        pass

    def edit_record(self, record, new_value):
        pass


class Name(Field):
    def __init__(self, value):
        self.value = value


class Phone(Field):  
    def __init__(self, value=None):
        super().__init__(value)

    @Field.value.setter
    def value(self, new_value):
        if not self._is_valid_phone(new_value):
            raise ValueError("Invalid phone number")
        self._value = new_value

    def _is_valid_phone(self, phone):
        return re.match(r'^[().\d+x-]+$', phone)


class Birthday(Field): 
    def __init__(self, value=None):
        super().__init__(value)    

    @property
    def value(self):
        return self._value        
   
    @value.setter
    def value(self, new_value):
        if isinstance(new_value, datetime):
            self._value = new_value
        else:
            raise ValueError("Expected datetime object.")

class Record:
    def __init__(self, name, phones=None, birthday=None):
        self.name = name
        if phones is None:
            self.phones = []
        elif isinstance(phones, Phone):
            self.phones = [phones]
        self.birthday = birthday


    def days_to_birthday(self):
        if self.birthday:
            today = datetime.today()
            next_birthday = datetime(today.year, self.birthday.value.month, self.birthday.value.day)
            if next_birthday < today:
                next_birthday = datetime(today.year + 1, self.birthday.value.month, self.birthday.value.day)
            days = (next_birthday - today).days
            return days
        else:
            return None
        
# class AddressBook
class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record
        self.save_to_file()

    def show_contacts(self):
        for record_name, record in self.data.items():
            print(f"Name: {record_name}")
            for phone in record.phone.numbers:
                print(f" -> {phone}")

    def iterator(self, page_size):
        record_keys = list(self.data.keys())
        num_records = len(record_keys)
        current_index = 0
        while current_index < num_records:
            page_records = []
            for i in range(current_index, min(current_index + page_size, num_records)):
                page_records.append(self.data[record_keys[i]])
            current_index += page_size
            yield page_records           
    
    
    # Save to JSON
    def save_to_file(self):
        with open("ab.json", 'w') as file:
            json.dump(self.data, file, default=self._serialize_record, indent=4)

    # Load from JSON
    def load_from_file(self):
        try:
            with open("ab.json", 'r') as file:
                data = json.load(file)
                for key, value in data.items():

                    name = Name(data[key]['name'])
                    phone = [Phone(phone) for phone in data[key]['phones']]
                    birthday = Birthday(datetime.strptime(data[key]['birthday'], "%Y-%m-%d"))
                    rec = Record(name, phone[0], birthday)
                    self.data[key] = rec  

        except FileNotFoundError:
            self.data = {}   


    @staticmethod
    def _serialize_record(record):
        serialized_phones = [phone.value for phone in record.phones]
        serialized_birthday = record.birthday.value.strftime('%Y-%m-%d') if record.birthday else None
        return {
            'name': record.name.value,
            'phones': serialized_phones,
            'birthday': serialized_birthday
        }
    
   
    # Search name by part of str
    def search_contacts(self, query):
        results = []
        for record in self.data.values():
            if query.lower() in record.name.value.lower():
                results.append(record)
            else:
                for phone in record.phones:
                    if query.lower() in phone.value.lower():
                        results.append(record)
                        break

        return results
 

def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except KeyError:
            return "Contact not found!"
        except ValueError:
            return "Invalid input!"
        except IndexError:
            return "Invalid command!"
    return inner

contacts = {}  
address_book = AddressBook()


@input_error
def hello_cmd():
    return "How can I help you?"


@input_error
def add_cmd(name, phone_number):
    contacts[name] = phone_number

    name = Name(name)
    phone = Phone()
    phone.add_number(phone_number)
    record = Record(name,phone)
    address_book.add_record(record)

    
    return "Contact added successfully!"

@input_error
def change_cmd(name,phone):
    print(name, phone)
    if not name and not phone:
        raise IndexError
    if name not in contacts:
        raise KeyError
    contacts[name] = phone
    return "Contact updated successfully!"

@input_error
def phone_cmd(name):
    if name not in contacts:
        raise KeyError
    return f"The phone number for {name} is {contacts[name]}"

@input_error
def show_all_cmd(): 
    if not contacts:
        return "Contact list is empty!"
    output = "Contacts:\n"
    for name, phone in contacts.items():
        output += f"{name}: {phone}\n"
    return output
  
    

def main():
    while True:
        user_input = input("> ").lower()
        user_list = user_input.split(' ')
        
        if user_input == "hello":
            print(hello_cmd())
        elif user_list[0] == "add":
            print(add_cmd(user_list[1], user_list[2]))
        elif user_list[0] == "change":
            print(change_cmd(user_list[1], user_list[2]))
        elif user_list[0] == "phone":
            print(phone_cmd(user_list[1]))
        elif user_input == "show all":
            print(show_all_cmd())
        elif user_input in ["good bye", "close", "exit"]:
            print("Good bye!")
            break
        else:
            print("Invalid command!")

fake = Factory.create() 
ab = AddressBook()

if __name__ == "__main__":
    
    # Create test AddressBook
    for _ in range(10):
        name = Name(fake.name())
        phone = Phone(fake.phone_number())
        birthday = Birthday(datetime.strptime(fake.date(), "%Y-%m-%d"))
        rec = Record(name, phone, birthday)

        ab.add_record(rec)
        # Save to ab.json
        ab.save_to_file()

    # Load from ab.json
    ab.data = {}
    print(f'AdressBook is empty {ab.data}')
    ab.load_from_file()
   
    # Test func search_contacts()
    while True:
        user_query = input("> ").lower()
        results = ab.search_contacts(user_query)
        
        if results:
            print("Search Results:")
            for record in results:
                print(f"Name: {record.name.value}")
                print("Phone Numbers:")
                for phone in record.phones:
                    print(f" - {phone.value}")
            break        
        else:
            print("No results found.")




