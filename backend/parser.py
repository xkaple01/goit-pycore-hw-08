import pickle
import mesop.labs as mel
from pathlib import Path
from collections.abc import Callable
from backend.book import Name, Phone, Birthday, AddressBook


def handle_exceptions(func: Callable) -> str:
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as ex:
            return str(ex)

    return inner


def parse_input(user_input: str) -> tuple[str, list[str]]:
    cmd, *args = user_input.split()
    cmd: str = cmd.strip().lower()
    return cmd, args


def help() -> str:
    return '\n\n'.join(
        [
            'Available commands:',
            'hello',
            'add [name] [phone]',
            'change [name] [phone] [new_phone]',
            'phone [name]',
            'all',
            'add-birthday [name] [date]',
            'show-birthday [name]',
            'birthdays',
            'help',
            'close',
        ]
    )


def hello() -> str:
    return '\n\n'.join(
        [
            'Hi. How can i help you?',
            'Type "help" to get the list of available commands.',
        ]
    )


@handle_exceptions
def add(args: list[str], book: AddressBook) -> str:
    if len(args) != 2:
        raise ValueError(
            f'add: accepts 2 input arguments, '
            f'but {len(args)} were provided.'
        )

    name: Name = Name(input_name=args[0])
    phone: Phone = Phone(input_phone=args[1])

    book.add_phone(name=name, phone=phone)

    return 'Contact added.'


@handle_exceptions
def change(args: list[str], book: AddressBook) -> str:
    if len(args) != 3:
        raise ValueError(
            f'change: accepts 3 input arguments, '
            f'but {len(args)} were provided.'
        )

    name: Name = Name(input_name=args[0])
    phone: Phone = Phone(input_phone=args[1])
    new_phone: Phone = Phone(input_phone=args[2])

    book.edit_phone(name=name, phone=phone, new_phone=new_phone)

    return 'Contact updated.'


@handle_exceptions
def phone(args: list[str], book: AddressBook) -> str:
    if len(args) != 1:
        raise ValueError(
            f'phone: accepts 1 input argument, '
            f'but {len(args)} were provided.'
        )

    name: Name = Name(input_name=args[0])

    return book.show_phones(name=name)


@handle_exceptions
def all(args: list[str], book: AddressBook) -> str:
    if len(args) != 0:
        raise ValueError(
            f'all: accepts 0 input arguments, '
            f'but {len(args)} were provided.'
        )

    return book.show_all_phones()


@handle_exceptions
def add_birthday(args: list[str], book: AddressBook) -> str:
    if len(args) != 2:
        raise ValueError(
            f'add_birthday: accepts 2 input arguments, '
            f'but {len(args)} were provided.'
        )

    name: Name = Name(input_name=args[0])
    birthday: Birthday = Birthday(input_birthday=args[1])

    book.add_birthday(name=name, birthday=birthday)

    return 'Birthday added.'


@handle_exceptions
def show_birthday(args: list[str], book: AddressBook) -> str:
    if len(args) != 1:
        raise ValueError(
            f'show_birthday: accepts 1 input argument, '
            f'but {len(args)} were provided.'
        )

    name: Name = Name(input_name=args[0])

    return book.show_birthday(name=name)


@handle_exceptions
def birthdays(args: list[str], book: AddressBook) -> str:
    if len(args) != 0:
        raise ValueError(
            f'birthdays: accepts 0 input arguments, '
            f'but {len(args)} were provided.'
        )

    return book.show_birthdays()


def close() -> str:
    return 'Good bye!'


def load_data(filename: str) -> AddressBook:
    try:
        with open(file=filename, mode='rb') as f:
            book: AddressBook = pickle.load(file=f)
            return book
    except:
        return AddressBook()


def save_data(book: AddressBook, filename: str):
    with open(file=filename, mode='wb') as f:
        pickle.dump(obj=book, file=f)


def transform(input: str, history: list[mel.ChatMessage]) -> str:
    try:
        cmd, args = parse_input(user_input=input)

        match cmd:
            case 'hello' | 'hi':
                return hello()
            case 'add':
                return add(args=args, book=book)
            case 'change':
                return change(args=args, book=book)
            case 'phone':
                return phone(args=args, book=book)
            case 'all':
                return all(args=args, book=book)
            case 'add-birthday':
                return add_birthday(args=args, book=book)
            case 'show-birthday':
                return show_birthday(args=args, book=book)
            case 'birthdays':
                return birthdays(args=args, book=book)
            case 'close' | 'exit':
                return close()
            case 'help' | '"help"' | _:
                return help()
    except:
        return help()

    finally:
        if book.is_commit_required:
            save_data(book=book, filename=path_db)


path_db = Path(__file__).resolve().parent.joinpath('database/addressbook.pkl')
book: AddressBook = load_data(filename=path_db)
