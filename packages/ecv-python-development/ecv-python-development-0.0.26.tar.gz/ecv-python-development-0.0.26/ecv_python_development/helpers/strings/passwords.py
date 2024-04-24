import random
import string


def generate_password(length: int = 12) -> str:
    # Define the characters for each category
    lowercase_letters = string.ascii_lowercase
    uppercase_letters = string.ascii_uppercase
    digits = string.digits
    special_characters = string.punctuation

    # Ensure each category is represented in the password
    password_chars = [
        random.choice(lowercase_letters),
        random.choice(uppercase_letters),
        random.choice(digits),
        random.choice(special_characters),
    ]

    # Fill the remaining characters using a mix of all categories
    remaining_length = length - len(password_chars)
    password_chars += random.choices(
        lowercase_letters + uppercase_letters + digits + special_characters,
        k=remaining_length,
    )

    # Shuffle the characters to create a random password
    random.shuffle(password_chars)

    return "".join(password_chars)
