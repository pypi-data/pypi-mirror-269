# Turkish Profile Generator

Turkish Profile Generator is a Python package used to generate random Turkish user profiles. This package creates realistic Turkish user profiles using random names and other attributes.

## Installation

You can easily install the package using pip:

```bash
pip install turkish-profile-generator


from turkish_profile_generator import UserProfileGenerator

# Create an instance of UserProfileGenerator class
generator = UserProfileGenerator(min_age=18, max_age=50)
#generator = UserProfileGenerator(min_age=18, max_age=50, gender='Female')
#generator = UserProfileGenerator(min_age=18, max_age=50, gender='Male')

# Generate a random user profile
profile = generator.generate_profile()

# Print the generated profile attributes
print("Generated Profile:")
print("First Name:", profile['firstname'])
print("Last Name:", profile['lastname'])
print("Age:", profile['age'])
print("Birthday:", profile['birthday'])
print("Email:", profile['email'])
print("Password:", profile['password'])
print("Gender:", profile['gender'])

profile.reset()

Features
Generates random Turkish names.
Generates random age, birth date, email address, and password.
Generates names compatible with the Turkish alphabet.
Can generate user profiles in the desired age range.
Contributing
If you'd like to contribute to this project, please visit the GitHub repository: https://github.com/bossturk/turkish-profile-generator

We welcome any feedback, suggestions, or contributions!

License
This project is licensed under the MIT License - see the LICENSE file for details.

