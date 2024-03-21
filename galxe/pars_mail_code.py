import logging
import os
import easyimap
import html2text
from dotenv import load_dotenv
from logs.logging_settings import setup_logging


setup_logging()
load_dotenv()

# параметры подключения
mail_server = os.getenv('MAIL_SERVER')
mail_port =int(os.getenv('MAIL_PORT'))
username = os.getenv('USERNAME_MAIL')
password = os.getenv('PASSWORD')

def get_code()->str:
    """
    Получаем код из email
    :return: код
    """
    logging.info('Получаем код из email')
    # Подключение к почтовому серверу
    mail = easyimap.connect(mail_server, username, password, mailbox='inbox', port=mail_port, ssl=True)
    try:
        # Получение списка сообщений
        for mail_id in mail.listids(limit=5):  # Ограничиваем до 10 последних сообщений
            print(mail_id)
            email_message = mail.mail(mail_id)

            # Вывод информации о письме
            sender = email_message.from_addr
            title = email_message.title
            if sender=='Galxe <notify@email.galxe.com>' and title=='Please confirm your email on Galxe':
                text_content = html2text.html2text(email_message.body)
                start = text_content.find('#')
                code = (text_content[start+1:start+10]).strip()
                logging.info('Код из email получен успешно')
                return code

    except Exception as err:
        logging.warning(f'Notification not found: {err}')
        logging.info('Код из email не получен. Ошибка выполнения')
    finally:
        mail.quit()


