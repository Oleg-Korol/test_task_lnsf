import time
import logging
import random
from dotenv import load_dotenv
from selenium.webdriver import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from google.logs.logging_settings import setup_logging
from config import LIST_OF_ACCAUNTS_TWITTER as list_of_tuples_accaunts



load_dotenv()
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


def edit_twitter_accaunt():


    with (webdriver.Chrome(options=chrome_options) as driver):

        actions = ActionChains(driver)
        wait =  WebDriverWait(driver, 10)

        for accaunt in list_of_tuples_accaunts:
            try:
                login, username,passw,new_password = accaunt[0], accaunt[1], accaunt[2], accaunt[3]


                #вводим логин
                driver.get('https://twitter.com/i/flow/login')
                driver.refresh()
                time.sleep(10)
                input_element = driver.find_element(By.CSS_SELECTOR,
                    "input.r-30o5oe.r-1dz5y72.r-13qz1uu.r-1niwhzg.r-17gur6a.r-1yadl64.r-deolkf.r-homxoj.r-poiln3.r-7cikom.r-1ny4l3l.r-t60dpp.r-fdjqy7")
                input_element.send_keys(login)
                next_button = driver.find_element(By.XPATH,
                    "//div[contains(@class, 'css-175oi2r')]//span[contains(text(), 'Next')]")
                next_button.click()
                time.sleep(5)

                # enter username
                username_input = driver.find_element(By.CSS_SELECTOR, "input[data-testid='ocfEnterTextTextInput']")
                username_input.send_keys(username)
                time.sleep(5)
                next_button_2 = driver.find_element(By.XPATH,"//div[@role='button' and contains(@class, 'css-175oi2r') and contains(@class, 'r-sdzlij') and contains(@class, 'r-1phboty') and contains(@class, 'r-rs99b7') and contains(@class, 'r-lrvibr') and contains(@class, 'r-19yznuf') and contains(@class, 'r-64el8z') and contains(@class, 'r-1dye5f7') and contains(@class, 'r-1loqt21') and contains(@class, 'r-o7ynqc') and contains(@class, 'r-6416eg') and contains(@class, 'r-1ny4l3l')]")
                next_button_2.click()
                time.sleep(5)


                # вводим пароль
                password_input = driver.find_element(By.CSS_SELECTOR,"input.r-30o5oe.r-1dz5y72.r-13qz1uu.r-1niwhzg.r-17gur6a.r-1yadl64.r-deolkf.r-homxoj.r-poiln3.r-7cikom.r-1ny4l3l.r-t60dpp.r-fdjqy7")
                password_input.send_keys(passw)
                all_buttons = driver.find_elements(By.XPATH, "//div[@role='button']")
                all_buttons[-1].click()
                time.sleep(5)

                # публикуем пост
                driver.get('https://twitter.com/compose/post')
                time.sleep(5)
                text_area = driver.find_element(By.CSS_SELECTOR, 'div[data-testid="tweetTextarea_0"]')

                # Создаем список постов
                posts = [
                    "Сегодня отличный день!",
                    "Классная погода!",
                    "Улетел на отдых!",
                    "Отдыхаем на природе в выходные!",
                    "Собираемся на вечеринку в пятницу!"
                ]

                # Выбираем случайный пост из списка
                random_post = random.choice(posts)
                text_area.send_keys(random_post)
                time.sleep(3)
                button_post = post_button = driver.find_element(By.XPATH, "//div[@data-testid='tweetButton']")
                button_post.click()


                #изменяем пароль
                driver.get('https://twitter.com/settings/password')
                time.sleep(10)
                input_current_password = driver.find_element(By.CSS_SELECTOR, 'input[name="current_password"][type="password"][class="r-30o5oe r-1dz5y72 r-13qz1uu r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-fdjqy7"]')
                input_current_password.send_keys(passw)
                time.sleep(2)
                new_passw = driver.find_element(By.CSS_SELECTOR, 'input[name="new_password"][type="password"][autocomplete="on"][autocorrect="on"][spellcheck="true"][dir="auto"][class*="r-30o5oe"]')
                new_passw.send_keys(new_password)
                time.sleep(2)
                confirm_password = driver.find_element(By.CSS_SELECTOR,  'input[name="password_confirmation"][type="password"][class="r-30o5oe r-1dz5y72 r-13qz1uu r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-fdjqy7"]')
                confirm_password.send_keys(new_password)
                time.sleep(2)
                all_buttons = driver.find_elements(By.XPATH, "//div[@role='button']")
                all_buttons[-1].click()
                time.sleep(5)

                # Очистка куки
                driver.delete_all_cookies()

            except Exception as err:
                print(err)
                logging.warning(f'Произошла ошибка: {err}')




if __name__ == "__main__":
    edit_twitter_accaunt()










