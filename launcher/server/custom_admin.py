import time
from controler.slote_admin import LoginSloteAdmin

def custom_admin_run(url: str, username: str, password: str, captcha: str):
    bot = LoginSloteAdmin()
    bot.slote.driver.get(url)
    time.sleep(2)
    bot.slote.input_username(username)
    bot.slote.input_password(password)
    bot.slote.input_verification_code(captcha)
    bot.slote.click_login()
