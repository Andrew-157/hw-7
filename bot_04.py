from collections import UserDict
from datetime import datetime
import re
import pickle


class Field:
    pass


class Birthday:
    def __init__(self, birth_day):
        self.__value = None
        self.value = birth_day

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, birth_day):
        check_match = re.search(r"[0-9]{4}\-[0-9]{2}\-[0-9]{2}", birth_day)
        if check_match:
            self.__value = birth_day
        else:
            self.__value = None


class Phone(Field):
    def __init__(self, phone):
        self.__value = None
        self.value = phone

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, phone):
        check_match = re.search(
            r"\([0-9]{2}\)\-[0-9]{3}\-[0-9]{1}\-[0-9]{3}|\([0-9]{2}\)\-[0-9]{3}\-[0-9]{2}\-[0-9]{2}", phone)
        if check_match:
            self.__value = phone
        else:
            self.__value = None


class Name(Field):
    def __init__(self, name):
        self.value = name


class Record:
    def __init__(self, name, phone=None, birth_day=None):
        self.name = Name(name)

        if phone and birth_day:

            self.phones = [Phone(phone)]
            self.birth_day = Birthday(birth_day)

        elif not phone and not birth_day:

            self.phones = []
            self.birth_day = None

        elif not phone and birth_day:

            self.phones = []
            self.birth_day = Birthday(birth_day)

        elif phone and not birth_day:

            self.phones = [Phone(phone)]
            self.birth_day = None

    def add_phone(self, name, value, address_book):
        address_book[name].phones.append(Phone(value))

    def change_birthday(self, name, value, address_book):
        address_book[name].birth_day = Birthday(value)

    def change_phones(self, name, old_phone, new_phone, address_book):
        phones = [phone.value for phone in address_book[name].phones]
        index = phones.index(old_phone)
        phones.insert(index, new_phone)
        phones.remove(old_phone)
        address_book[name].phones = []
        for value in phones:
            address_book[name].phones.append(Phone(value))

    def delete_phones(self, name, address_book):
        address_book[name].phones.clear()

    def days_to_birthday(self, date):
        date_list = date.split("-")
        reference_date = datetime(year=int(date_list[0]), month=int(
            date_list[1]), day=int(date_list[2]))
        days_to_birthday = reference_date - datetime.now()
        return days_to_birthday.days


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
        return self.data

    def iterator(self, start, N):
        keys = list(self.data.keys())
        while int(start) < int(N):
            yield self.data[keys[start]]
            start += 1

    def load_address_book(self):
        try:
            object = self
            with open("address_book.txt", "rb") as file:
                object = pickle.load(file)
            return object
        except FileNotFoundError:
            object = self
            return object

    def dump_address_book(self, address_book):
        with open("address_book.txt", "wb") as file:
            pickle.dump(address_book, file)


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return "Try again, please"
        except ValueError:
            return "Try again, please"
        except TypeError:
            return "Try again, please"

    return inner


@input_error
def add(data, address_book):
    info = data.split(" ")
    name = info[1]

    if name not in address_book:
        if len(info) == 4:
            phone = info[2]
            birth_day = info[3]
            if not Phone(phone).value and Birthday(birth_day).value:

                record = Record(name=name, phone=None, birth_day=birth_day)
                address_book.add_record(record)

                return f"{name} with {birth_day} birthday was added to Address Book,to add phone use these formats: (00)-000-0-000 or (00)-000-00-00"

            elif not Birthday(birth_day).value and Phone(phone).value:

                record = Record(name=name, phone=phone, birth_day=None)
                address_book.add_record(record)

                return f"{name} with {phone} phone was added to Address Book,to add birthday use this format: yyyy-mm-dd"

            elif not Birthday(birth_day).value and not Phone(phone).value:

                record = Record(name)
                address_book.add_record(record)

                return f"{name} was added to Address Book,to add phone use these formats: (00)-000-0-000 or (00)-000-00-00,to add birthday use this format: yyyy-mm-dd"

            elif Birthday(birth_day).value and Phone(phone).value:

                record = Record(name=name, phone=phone, birth_day=birth_day)
                address_book.add_record(record)

                return f"{name} with {phone} phone and {birth_day} birthday was added to Address Book"

        elif len(info) == 3:

            phone = info[2]

            if Phone(phone).value:

                record = Record(name, phone)
                address_book.add_record(record)

                return f"{name} with {phone} phone was added to Address Book"

            elif not Phone(phone).value and Birthday(phone).value:

                record = Record(name, phone=None, birth_day=phone)
                address_book.add_record(record)

                return f"{name} with {phone} birthday was added to Address Book"

            else:
                record = Record(name)
                return f"{name} was added, but {phone} phone cannot be added because of the wrong format, use these formats: (00)-000-0-000 or (00)-000-00-00"

        elif len(info) == 2:

            record = Record(name)
            address_book.add_record(record)

            return f"{name} was added to Address Book"

        else:

            return "Please, enter this command using one of the following formats:'Add name phone birthday', 'Add name phone', 'Add name'"

    elif name in address_book:

        if len(info) == 2:
            return f"{name} is already in Address Book, add some information to {name}"

        elif len(info) == 3:
            phone = info[2]

            if not Phone(phone).value and Birthday(phone).value:

                return f"You cannot add {phone} birthday to {name},use 'change_birthday' command, if you want to change it for {name}"

            elif Phone(phone).value:

                Record(name).add_phone(name, phone, address_book)
                return f"{phone} phone was added to {name} in Address Book"

            elif not Phone(phone).value:

                return f"To add phone to {name} in Address Book use these formats: (00)-000-0-000 or (00)-000-00-00"

        elif len(info) == 4:
            phone = info[2]

            if not Phone(phone).value:
                return f"{phone} is of the wrong format and {info[3]} cannot be added to {name}"

            elif Phone(phone).value:
                Record(name).add_phone(name, phone, address_book)
                return f"{phone} was added to {name}, but {info[3]} cannot be added"


@input_error
def change_birthday(data, address_book):

    name = data.split(" ")[1]
    birth_day = data.split(" ")[2]

    if name not in address_book:
        return f"{name} doesn't have aby information in Address Book,you can't change it's birthday"
    else:
        if Birthday(birth_day).value:

            Record(name).change_birthday(name, birth_day)
            return f"{name} contact's birthday was changed to {birth_day}"

        else:
            return f"{birth_day} is of the wrong format,use this format: yyyy-mm-dd"


@input_error
def change_phones(data, address_book):

    name = data.split(" ")[1]

    if len(data.split(" ")) < 4:
        return "Enter this command with the phone number you want to change and its new value"
    elif len(data.split(" ")) > 4:
        return "Enter this command with the phone number you want to change and its new value"
    else:
        phone_to_change = data.split(" ")[2]
        new_phone = data.split(" ")[3]

        if Phone(phone_to_change).value in [phone.value for phone in address_book[name].phones]:
            if Phone(new_phone):
                Record(name).change_phones(name, phone_to_change, new_phone)
                return f"{name} contact's {phone_to_change} phone was changed to {new_phone}"
            else:
                return f"{new_phone} is of the wrong format, use these formats: (00)-000-0-000 or (00)-000-00-00"

        else:
            return f"{name} doesn't have this phone: {phone_to_change}"


@input_error
def delete_phones(data, address_book):
    name = data.split(" ")[1]

    if name not in address_book:
        return f"{name} doesn't have any information in Address Book, you can't delete it's phones"

    else:

        Record(name).delete_phones(name)
        return f"{name} contact's phones were deleted"


def say_hello():
    return "How can I help you?"


@input_error
def show_all(data, address_book):
    number = data.split(" ")[1]
    info_dict = {}
    if int(number) > len(address_book):
        generator = address_book.iterator(start=0, N=len(address_book))
        for info in generator:
            try:
                info_dict[info.name.value] = f"{[phone.value for phone in info.phones]}--{info.birth_day.value}"
            except AttributeError:
                info_dict[info.name.value] = f"{[phone.value for phone in info.phones]}"

    else:
        generator = address_book.iterator(start=0, N=number)
        for info in generator:
            try:
                info_dict[info.name.value] = f"{[phone.value for phone in info.phones]}--{info.birth_day.value}"
            except AttributeError:
                info_dict[info.name.value] = f"{[phone.value for phone in info.phones]}"

    return info_dict


@input_error
def phones(data, address_book):
    name = data.split(" ")[1]

    if name not in address_book:
        return f"{name} doesn't have any information"
    else:
        phones_list = []
        for phone in address_book[name].phones:
            phones_list.append(phone.value)
        return phones_list


@input_error
def birthday(data, address_book):
    name = data.split(" ")[1]

    if name not in address_book:
        return f"{name} doesn't have any information"
    else:
        if not address_book[name].birth_day:
            return f"Birthday for {name} was not defined"
        else:
            return address_book[name].birth_day.value


@input_error
def days_to_birthday(data, address_book):
    name = data.split(" ")[1]

    if name not in address_book:
        return f"{name} doesn't have any information in Address Book, you can't use this command"
    else:
        if not address_book[name].birth_day:
            return f"You can't use this command, because {name} contact doesn't have birthday data in Address Book,use 'change_birthday' command"

        else:

            birth_date = address_book[name].birth_day.value
            days = Record(name).days_to_birthday(birth_date)
            return f"{days} days left to {name} contact's birthday"


@input_error
def find(data, address_book):
    hint = data.split(" ")[1]
    list_to_user = []

    for name in address_book.keys():
        if hint.lower() in name.lower():
            list_to_user.append(name)
        else:
            continue

    for name, value in address_book.items():
        if name in list_to_user:
            continue
        else:
            for phone in [phone.value for phone in value.phones]:
                if hint in phone:
                    list_to_user.append(name)

    if not list_to_user:
        return "No matches were found"
    else:
        return list_to_user


COMMANDS = {"add": add,
            "change_birthday": change_birthday,
            "change_phones": change_phones,
            "delete_phones": delete_phones,
            "days_to_birthday": days_to_birthday,
            "hello": say_hello,
            "show_all": show_all,
            "phones": phones,
            "birthday": birthday,
            "find": find}


def handler(comm):
    return COMMANDS[comm]


def main():

    address_book = AddressBook().load_address_book()
    while True:

        user_command = input("Enter a command: ")

        if user_command.lower() == "hello":
            print(handler(user_command.lower())())

        elif user_command.split(" ")[0].lower() not in list(COMMANDS.keys()) + ["exit", "close", "goodbye", "commands"]:
            print("No such a command\nCheck all the commands using 'commands' command")

        elif user_command == "commands":

            commands = ["exit", "close", "goodbye", "commands"]
            for key in COMMANDS.keys():
                commands.append(key)
            print(f"Here are the commands this bot can do:\n{commands}")

        elif user_command.lower() in ["exit", "close", "goodbye"]:
            AddressBook().dump_address_book(address_book)
            print("Address Book was saved to file: 'address_book.txt'")
            print("Goodbye")
            break

        else:
            print(handler(user_command.split(" ")[0].lower())(
                user_command, address_book))


if __name__ == "__main__":
    main()
