import time
import logging
import random
from selenium.webdriver import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from galxe.pars_mail_code import get_code
from google.logs.logging_settings import setup_logging
from config import LIST_OF_ACCAUNTS_GALXE as list_of_accaunts




setup_logging()



HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/95.0.4638.69 Safari/537.36',
        'accept': '*/*'
    }

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-blink-features=AutomaticControlled')
chrome_options.add_argument("user-agent=" + HEADERS['User-Agent'])
chrome_options.add_argument("accept-language=" + HEADERS['accept'])



# options = {
#     "proxy": {
#         "http": f"socks5://{os.getenv('LOGIN_PROXY')}:{os.getenv('PASSWORD_PROXY')}"
#         f"@{os.getenv('HOST_PROXY')}:{os.getenv('PORT_PROXY')}",
#         "https": f"socks5://{os.getenv('LOGIN_PROXY')}:{os.getenv('PASSWORD_PROXY')}"
#         f"@{os.getenv('HOST_PROXY')}:{os.getenv('PORT_PROXY')}",
#     }
# }



def galxe_accaunt():


    with (webdriver.Chrome(options=chrome_options) as driver):

        actions = ActionChains(driver)

        driver.maximize_window()

        for accaunt in list_of_accaunts:
            try:

                #вводим логин
                driver.get('https://galxe.com')
                time.sleep(5)
                button_login = driver.find_element(By.XPATH, "//div[@class='login-btn clickable text-14-bold rounded-pill']")
                button_login.click()
                time.sleep(5)
                button_log_for_mail = driver.find_element(By.XPATH, "//li[@class='login-item-wrapper email clickable']")
                button_log_for_mail.click()

                #вводим email
                time.sleep(3)
                input_email = driver.find_element(By.XPATH,"//input[@data-v-a82c81cc]")
                input_email.send_keys(accaunt)

                #отправить код на почту
                time.sleep(3)
                send_code_button = driver.find_element(By.XPATH,"//a[@data-v-a82c81cc]")
                input_code = driver.find_element(By.XPATH, "//input[@data-v-a82c81cc and @placeholder='Enter code']")
                input_code.send_keys('3drvf43fd2')
                input_code.clear()


                # Случайная задержка перед кликом
                time.sleep(random.uniform(1, 2))
                send_code_button.click()
                time.sleep(15)


                #достаем код из письма
                code = get_code()
                print(code)

                #вводим код
                input_code = driver.find_element(By.XPATH,"//input[@data-v-a82c81cc and @placeholder='Enter code']")
                input_code.send_keys(code)
                time.sleep(3)

                #подтверждаем вход
                ok_button = driver.find_element(By.XPATH,"//button[@data-v-1db972f4]")
                ok_button.click()


                #TODO доделать. Видит автоматизацию и не отпраляет код на почту


                time.sleep(500)

            except Exception as  err:
                logging.warning(f'Произошла ошибка {err}')



if __name__ == "__main__":
    galxe_accaunt()

