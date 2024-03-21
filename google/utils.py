from password_generator import PasswordGenerator


pwo = PasswordGenerator()
pwo.minlen = 10
pwo.maxlen = 12
pwo.minuchars = 2
pwo.minlchars = 3
pwo.minnumbers = 1
pwo.minschars = 1



def generate_password()->str:

    """Генератор пароля"""
    password = pwo.generate()
    return password