# Example PyPI (Python Package Index) Package
import random
import string
import os
from datetime import datetime


class UserProfileGenerator(object):

    def __init__(self, min_age, max_age, gender=None):
        self.male_names = self.read_names_from_file(os.path.join(os.path.dirname(__file__), "data", "firstname_male.txt"))
        self.female_names = self.read_names_from_file(os.path.join(os.path.dirname(__file__), "data", "firstname_female.txt"))
        self.uni_names = self.read_names_from_file(os.path.join(os.path.dirname(__file__), "data", "firstname_uni.txt"))
        self.lastnames = self.read_names_from_file(os.path.join(os.path.dirname(__file__), "data", "lastname.txt"))
        self.min_age = min_age
        self.max_age = max_age
        self.genders = ['Male', 'Female']

        if gender is not None and gender.capitalize() in self.genders:
            self.gender = gender.capitalize()
        else:
            self.gender = random.choice(self.genders)

    def read_names_from_file(self, filename):
        with open(filename, 'r',encoding='utf-8') as file:
            return [name.strip() for name in file.readlines()]

    def generate_profile(self):
        firstname = self.get_firstname().lower()
        lastname = self.get_lastname().lower()
        current_year = datetime.now().year
        birth_year = random.randint(current_year - self.max_age, current_year - self.min_age)
        birth_month = random.randint(1, 12)
        birth_day = random.randint(1, 28)  # Assuming all months have 28 days
        birthday = f"{birth_year}-{birth_month:02d}-{birth_day:02d}"
        age = current_year - birth_year - ((birth_month, birth_day) > (datetime.now().month, datetime.now().day))
        email = self.get_email(firstname, lastname, birth_year)
        password = self.generate_password()

        return {
            'firstname': firstname,
            'lastname': lastname,
            'age': age,
            'birthday': birthday,
            'email': email,
            'password': password,
            'gender': self.gender
        }

    def generate_password(self):
        upper_case = random.choice(string.ascii_uppercase)
        random_character = random.choice("!'^+&/()=?")
        lower_case = ''.join(random.choices(string.ascii_lowercase, k=6))
        password = upper_case + random_character + lower_case
        password = ''.join(random.sample(password, len(password)))
        return password

    def get_firstname(self):
        if self.gender == 'Male':
            return random.choice(self.male_names)
        elif self.gender == 'Female':
            return random.choice(self.female_names)
        else:
            if random.randint(1, 100) <= 5:
                return random.choice(self.uni_names)
            else:
                return random.choice(self.male_names + self.female_names)

    def get_lastname(self):
        return random.choice(self.lastnames)

    @staticmethod
    def remove_turkish_characters(text):
        turkish_characters = {'ö': 'o', 'ü': 'u', 'ç': 'c', 'ğ': 'g', 'ş': 's', 'ı': 'i', 'Ö': 'O', 'Ü': 'U', 'Ç': 'C', 'Ğ': 'G', 'Ş': 'S', 'İ': 'I'}
        return ''.join(turkish_characters.get(char, char) for char in text)

    def get_email(self, firstname, lastname, birth_year):
        firstname = self.remove_turkish_characters(firstname)
        lastname = self.remove_turkish_characters(lastname)
        if random.choice([True, False]):
            return f"{firstname.lower().replace(' ', '_')}_{lastname.lower().replace(' ', '_')}_{birth_year}_{random.randint(10000, 99999)}"
        else:
            return f"{firstname.lower().replace(' ', '_')}_{lastname.lower().replace(' ', '_')}_{random.randint(10000, 99999)}_{birth_year}"

    def get_password(self):
        return self.generate_password()

    def get_birthday(self, min_age, max_age):
        age = random.randint(min_age, max_age)
        current_year = datetime.now().year
        birth_year = random.randint(current_year - age, current_year)
        birth_month = random.randint(1, 12)
        birth_day = random.randint(1, 28)  # Assuming all months have 28 days
        return f"{birth_year}-{birth_month}-{birth_day}"

    def reset(self, gender='None'):
        if gender.capitalize() in self.genders:
            self.gender = gender.capitalize()
        return self.generate_profile()
