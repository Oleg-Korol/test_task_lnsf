import os
import time
import logging
from collections import namedtuple

from dotenv import load_dotenv
from selenium.webdriver.support import expected_conditions as EC
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from faker import Faker
from google.database import db_add_account, create_db
from google.logs.logging_settings import setup_logging
from google.utils import generate_password
from config import LIST_OF_ACCAUNTS_GOOGLE as list_of_tuples_accaunts, url, url_edit_name, url_info, url_edit_password


load_dotenv()
setup_logging()


fake = Faker()
Accaunt = namedtuple('Accaunt', ['first_name', 'last_name','login','password','email'])


# options = {
#     "proxy": {
#         "http": f"socks5://{os.getenv('LOGIN_PROXY')}:{os.getenv('PASSWORD_PROXY')}"
#         f"@{os.getenv('HOST_PROXY')}:{os.getenv('PORT_PROXY')}",
#         "https": f"socks5://{os.getenv('LOGIN_PROXY')}:{os.getenv('PASSWORD_PROXY')}"
#         f"@{os.getenv('HOST_PROXY')}:{os.getenv('PORT_PROXY')}",
#     }
# }
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-blink-features=AutomaticControlled')




def edit_google_accaunt():
    with webdriver.Chrome(options=chrome_options) as driver:
        for accaunt in list_of_tuples_accaunts:
            try:
                login, passw = accaunt[0], accaunt[1]
                name, second_name,new_password = fake.first_name(), fake.last_name(), generate_password()


                #вводим логин
                driver.get(url)
                email_input = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, 'identifierId'))
                )
                email_input.send_keys(login)
                next_button = driver.find_element(By.ID, "identifierNext")
                next_button.click()

                # вводим пароль
                password_1 = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "password")))
                password = password_1.find_element(By.NAME, "Passwd")
                driver.execute_script("arguments[0].scrollIntoView();", password)
                password.send_keys(passw)
                time.sleep(3)
                password_next = driver.find_element(By.ID, 'passwordNext')
                password_next.click()
                time.sleep(3)


                #меняем имя и фамилию
                driver.get(url_edit_name)
                first_name = driver.find_element(By.ID, "i6")
                first_name.clear()
                first_name.send_keys(name)
                last_name= driver.find_element(By.ID, "i11")
                last_name.clear()
                last_name.send_keys(second_name)
                button_save = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'UywwFc-LgbsSe')]"))
                )
                button_save.click()
                time.sleep(3)


                #получаем резервный email
                driver.get(url_info)
                time.sleep(3)
                try:
                    email_input = driver.find_element(By.ID, 'i5')
                    email = email_input.get_attribute("value")
                except Exception as err:
                    logging.warning(f'Ошибка при парсинге резервной почты {err}')
                    email = 'отсутствует'

                user = Accaunt(first_name=name, last_name=second_name, login=login, password=new_password,
                               email=email)


                # изменяем пароль
                driver.get(url_edit_password)
                time.sleep(3)
                input_new_password = driver.find_element(By.ID, "i5")
                input_new_password.send_keys(new_password)
                confirm_password = driver.find_element(By.ID, "i11")
                confirm_password.send_keys(new_password)
                time.sleep(2)
                button_edit_password = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'UywwFc-LgbsSe')]"))
                )
                button_edit_password.click()

                #проверяем что не появилось уведомление о некорректном пароле
                bad_password = driver.find_element(By.ID, "i7")
                if bad_password.is_displayed() and bad_password.text.strip() != "":
                    user = Accaunt(first_name=name, last_name=second_name, login=login, password=passw,
                                   email=email)
                    logging.info(f'Пароль не был измнен так как он не соответствует')
                else:
                    logging.info('Пароль соответствует')

                if os.path.exists('user_db'):
                        db_add_account(user)
                else:
                    create_db('user_db')
                    db_add_account(user)

                # Очистка куки
                driver.delete_all_cookies()

            except Exception as err:
                logging.warning(f'Произошла ошибка: {err}')




if __name__ == "__main__":
    edit_google_accaunt()










