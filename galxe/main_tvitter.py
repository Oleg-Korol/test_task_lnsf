import time
import logging
from telnetlib import EC
from selenium.webdriver import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from google.logs.logging_settings import setup_logging
from config import LIST_OF_ACCAUNTS_GALXE as list_of_tuple_accaunts




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
        wait =  WebDriverWait(driver, 20)
        driver.maximize_window()

        for accaunt in list_of_tuple_accaunts:

            login, username, passw = accaunt[0], accaunt[1],accaunt[2]

            try:

                #вводим логин
                driver.get('https://twitter.com/i/flow/login?redirect_after_login=%2Fi%2Foauth2%2Fauthorize%3Fstate%3DSIGN_IN%253ATWITTER%26client_id%3DTmNyRlZveUpicFVNM1FxbW9VVjk6MTpjaQ%26redirect_uri%3Dhttps%253A%252F%252Fgalxe.com%252F%26response_type%3Dcode%26scope%3Dtweet.read%2520users.read%2520follows.read%2520like.read%2520offline.access%26code_challenge%3Dchallenge%26code_challenge_method%3Dplain')
                time.sleep(5)


                input_element = driver.find_element(By.CSS_SELECTOR,
                                                    "input.r-30o5oe.r-1dz5y72.r-13qz1uu.r-1niwhzg.r-17gur6a.r-1yadl64.r-deolkf.r-homxoj.r-poiln3.r-7cikom.r-1ny4l3l.r-t60dpp.r-fdjqy7")
                input_element.send_keys(login)
                next_button = driver.find_element(By.XPATH,
                                                  "//div[contains(@class, 'css-175oi2r')]//span[contains(text(), 'Next')]")
                next_button.click()
                time.sleep(5)

                # вводим имя пользователя
                username_input = driver.find_element(By.CSS_SELECTOR, "input[data-testid='ocfEnterTextTextInput']")
                username_input.send_keys(username)
                time.sleep(5)
                next_button_2 = driver.find_element(By.XPATH,
                                                    "//div[@role='button' and contains(@class, 'css-175oi2r') and contains(@class, 'r-sdzlij') and contains(@class, 'r-1phboty') and contains(@class, 'r-rs99b7') and contains(@class, 'r-lrvibr') and contains(@class, 'r-19yznuf') and contains(@class, 'r-64el8z') and contains(@class, 'r-1dye5f7') and contains(@class, 'r-1loqt21') and contains(@class, 'r-o7ynqc') and contains(@class, 'r-6416eg') and contains(@class, 'r-1ny4l3l')]")
                next_button_2.click()
                time.sleep(5)

                # вводим пароль
                password_input = driver.find_element(By.CSS_SELECTOR,
                                                     "input.r-30o5oe.r-1dz5y72.r-13qz1uu.r-1niwhzg.r-17gur6a.r-1yadl64.r-deolkf.r-homxoj.r-poiln3.r-7cikom.r-1ny4l3l.r-t60dpp.r-fdjqy7")
                password_input.send_keys(passw)
                all_buttons = driver.find_elements(By.XPATH, "//div[@role='button']")
                all_buttons[-1].click()
                time.sleep(5)


                ok_button = driver.find_element(By.XPATH,"//div[@data-testid='OAuth_Consent_Button']")
                ok_button.click()

                try:
                    wait.until(EC.url_contains("https://galxe.com"))
                    print("Переход на целевую страницу выполнен успешно.")

                except:
                    print("Ошибка: переход на целевую страницу не выполнен или время ожидания истекло.")


                time.sleep(500)



                #TODO доделать вход через твиттер.На данный момент сайт не поддерживает




            except Exception as err:
                logging.warning(f'Произошла ошибка {err}')


if __name__ == "__main__":
    galxe_accaunt()
