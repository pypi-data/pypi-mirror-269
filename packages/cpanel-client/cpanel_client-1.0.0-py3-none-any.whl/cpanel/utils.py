import string
import random


def generate_random_password() -> string:
    chars = string.ascii_letters + string.digits + string.punctuation
    pwd_size = random.randint(15, 20)

    return ''.join((random.choice(chars)) for x in range(pwd_size))


def convert_domain_to_username(domain) -> string:
    return domain.replace('.', '')