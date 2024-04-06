from collections import defaultdict, UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    # реалізація класу
		pass


class Phone(Field):
    def __init__(self, value):
        if len(value) == 10 and value.isdigit():
            super().__init__(value)
	    else:
            raise ValueError("Phone not valid")
        

class Birthday(Field):
    def __init__(self, value):
        try:
            self.date = datetime.strptime(value, "%d.%m.%Y").date()
            super().__init__(value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))
        
    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p != phone]

    def edit_phone(self, phone, new_phone):
        for p in self.phones:
            Phone(new_phone)
            if p == phone:
                p.value = new_phone
                break
            else:
                 raise ValueError

    def find_phone(self, phone):
        for p in self.phones:
            if str(p) == phone:
                return p
        return None
    
    def add_birthday(self, birthday): 
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
    
    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        del self.data[name]
    
    def find_next_birthday(self, weekday):
        for record in self.data.values():
            if record.birthday:
                next_birthday = record.birthday.replace(year=datetime.today().year)
                if next_birthday.weekday() == weekday:
                    return next_birthday
        return None
        
    def get_upcoming_birthdays(self, days=7):
        uncoming_birthdays = []
        current_date = datetime.today().date()
        for record in self.data.values():
            if record.birthday:
                next_birthday = record.birthday.replace(year=current_date.year + 1)
                if current_date <= next_birthday <= current_date + timedelta(days=days):
                    if next_birthday.weekday() >= 5:
                        next_birthday += timedelta(days = 7 - next_birthday.weekday())
            uncoming_birthdays.append(f"{record.name.value}: {next_birthday.strftime("%d,%m,%Y")}")
        return uncoming_birthdays 
    

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "Сheck the validity of the entered data"
        except IndexError:
            return "Enter user name"
    return inner


@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message
     

@input_error
def show_phone(args,book: AddressBook):
        name = args[0]
        if name in book:
            return (book[name])
        else: 
            return "Користувача з таким іменем не знайдено, перевірте вірність введених даних"
    

@input_error
def show_all(book: AddressBook):
    result = []
    if book:
        for name, phone in book.items():
            result.append(f"{name}: {phone}")
        return result
    else:
        result.append("Список контактів порожній")
        return result

@input_error
def add_birthday(args, book: AddressBook):
    name, birthday = args
    record = book.find(name)
    if record is None:
        record = Record(name)
        book.add_record(record)
        record.add_birthday(birthday) 
        return "Birthday added."
    else:
        return "Перевірте вірність введених даних"
       
@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return record.birthday
    else: 
        return "Користувача з таким іменем не знайдено, перевірте вірність введених даних"

@input_error
def birthdays(args, book: AddressBook):
    birthdays = []
    for record in book.values():
        if record.birthday:
            birthdays.append(f"{record.name.value}: {record.birthday}")
        return birthdays
    else:
        birthdays.append("Список днів народжень порожній")
    return birthdays
    

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)
        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(add_contact(args, book))
        elif command == "phone":
            print(show_phone(args,book))
        elif command == "all":
            contact_list = show_all(book)
            for contact in contact_list:
                 print(contact)
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args,book))
        elif command == "birthdays":  
            birthdays_list = birthdays(book)
            for birthday in birthdays_list:
                 print(birthday)  
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()