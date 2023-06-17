from collections import UserDict


class Field:
    def __init__(self, value=None):
        self.value = value

    def add_to_record(self, record):
        pass

    def remove_from_record(self, record):
        passgit 

    def edit_record(self, record, new_value):
        pass


class Name(Field):
    def __init__(self, value):
        self.value = value


class Phone(Field):
    def __init__(self):
        self.numbers = []

    def add_number(self, number):
        self.numbers.append(number)

    def remove_number(self, number):
        if number in self.numbers:
            self.numbers.remove(number)

    def edit_number(self, old_number, new_number):
        if old_number in self.numbers:
            index = self.numbers.index(old_number)
            self.numbers[index] = new_number        


class Record:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone


class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record

    def show_contacts(self):
        for record_name, record_phone in self.data.items():
            print(f"Name: {record_name}")
            for phone in record_phone.phone.numbers:
                print(f" -> {phone}")
            


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

if __name__ == "__main__":
    main()