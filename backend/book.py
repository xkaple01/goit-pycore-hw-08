import re
from datetime import datetime, date, timedelta
from collections import UserDict


class Field:
    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)

    def __eq__(self, other: 'Field') -> bool:
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(str(self.value))


class Name(Field):
    def __init__(self, input_name: str) -> None:
        try:
            name_match: re.Match | None = re.fullmatch(
                pattern=r'[A-z]{2,20}', string=input_name
            )

            if name_match is None:
                raise ValueError('Name does not match the expected format.')

            super().__init__(value=input_name)

        except:
            raise ValueError('Name must consist of letters A-Z, a-z.')


class Phone(Field):
    def __init__(self, input_phone: str) -> None:
        try:
            phone_match: re.Match | None = re.fullmatch(
                pattern=r'[0-9]{10}', string=input_phone
            )

            if phone_match is None:
                raise ValueError('Phone does not match the expected format.')

            super().__init__(value=input_phone)

        except:
            raise ValueError(
                'Phone number must consist of 10 digits, example: 0971122333'
            )


class Birthday(Field):
    def __init__(self, input_birthday: str) -> None:
        try:
            birthday_date: date = datetime.strptime(
                input_birthday, r'%d.%m.%Y'
            ).date()

            super().__init__(value=birthday_date)

        except:
            raise ValueError(
                'Birthday must be in format: dd.mm.yyyy, example: 31.12.2024'
            )

    def __str__(self) -> str:
        date_birthday: date = self.value
        return date_birthday.strftime(r'%d.%m.%Y')


class Record:
    def __init__(self, name: Name) -> None:
        self.name: Name = name
        self.birthday: Birthday | None = None
        self.phones: list[Phone] = []

    def add_birthday(self, birthday: Birthday) -> None:
        self.birthday = birthday

    def add_phone(self, phone: Phone) -> None:
        if phone not in self.phones:
            self.phones.append(phone)
        else:
            raise ValueError(
                f'Phone {phone} is already present in contact {self.name} '
                'and can not be added twice.'
            )

    def remove_phone(self, phone: Phone) -> None:
        if phone in self.phones:
            self.phones.remove(phone)
        else:
            raise ValueError(
                f'Phone {phone} is absent in contact {self.name} '
                'and can not be removed.'
            )

    def edit_phone(self, phone: Phone, new_phone: Phone) -> None:
        if phone in self.phones:
            existing_phone: Phone = self.phones[self.phones.index(phone)]
            existing_phone.value = new_phone.value
        else:
            raise ValueError(
                f'Phone {phone} is absent in contact {self.name} '
                'and can not be edited.'
            )


class AddressBook(UserDict[Name, Record]):
    def __init__(self) -> None:
        self.__is_commit_required: bool = False
        super().__init__()

    def __getstate__(self) -> dict:
        self.__is_commit_required: bool = False
        return self.__dict__

    @property
    def is_commit_required(self) -> bool:
        return self.__is_commit_required
    
    def add_birthday(self, name: Name, birthday: Birthday) -> None:
        if name not in self.data:
            new_record: Record = Record(name=name)
            new_record.add_birthday(birthday=birthday)
            self.data[name] = new_record
        else:
            existing_record: Record = self.data[name]
            existing_record.add_birthday(birthday=birthday)

        self.__is_commit_required: bool = True

    def show_birthday(self, name: Name) -> str:
        if name not in self.data:
            raise ValueError(
                f'Contact {name} is absent in address book, '
                'birthday can not be displayed.'
            )

        existing_record: Record = self.data[name]
        birthday: Birthday = existing_record.birthday

        report: str = f'Contact {existing_record.name} \n\n'

        if birthday is None:
            report += f'Birthday: not entered yet. \n\n'
        else:
            report += f'Birthday: {birthday} \n\n'

        return report

    def show_birthdays(self) -> str:
        if len(self.data) == 0:
            raise ValueError(f'There are no contacts in address book yet.')

        start: date = datetime.now().date()
        end: date = start + timedelta(weeks=1)
        num_congratulations: int = 0
        report: str = 'Congratulations next week: \n\n'

        for record in self.data.values():
            birthday: Birthday = record.birthday
            if birthday is None:
                continue

            birthday_date: date = birthday.value
            birthday_this_year: date = birthday_date.replace(year=start.year)

            if birthday_this_year >= start and birthday_this_year <= end:
                congratulation_date: date = birthday_this_year
                congratulation_weekday: int = birthday_this_year.weekday()

                if congratulation_weekday == 5:
                    congratulation_date += timedelta(days=2)
                elif congratulation_weekday == 6:
                    congratulation_date += timedelta(days=1)

                num_congratulations += 1
                report += (
                    f'Contact: {record.name}, '
                    f'Congratulation: '
                    f'{congratulation_date.strftime(r"%d.%m.%Y")} \n\n'
                )

        if num_congratulations == 0:
            report += 'There are no congratulations next week. \n\n'

        return report

    def add_phone(self, name: Name, phone: Phone) -> None:
        if name not in self.data:
            new_record: Record = Record(name=name)
            new_record.add_phone(phone=phone)
            self.data[name] = new_record
        else:
            existing_record: Record = self.data[name]
            existing_record.add_phone(phone=phone)

        self.__is_commit_required: bool = True

    def edit_phone(self, name: Name, phone: Phone, new_phone: Phone) -> None:
        if name not in self.data:
            raise ValueError(
                f'Contact {name} is absent in address book, '
                'phone can not be edited.'
            )

        existing_record: Record = self.data[name]
        existing_record.edit_phone(phone=phone, new_phone=new_phone)

        self.__is_commit_required: bool = True

    def show_phones(self, name: Name) -> str:
        if name not in self.data:
            raise ValueError(
                f'Contact {name} is absent in address book, '
                'phones can not be displayed.'
            )

        existing_record: Record = self.data[name]
        phones: list[Phone] = existing_record.phones

        report: str = f'Contact: {name}: \n\n'
        if len(phones) == 0:
            report += 'Phones: not entered yet.'
        else:
            for phone in phones:
                report += f'Phone: {phone} \n\n'

        return report

    def show_all_phones(self) -> str:
        if len(self.data.values()) == 0:
            raise ValueError('There are no contacts in address book yet. \n\n')

        report: str = 'All phones in address book: \n\n'
        for record in self.data.values():
            report += self.show_phones(name=record.name)

        return report
