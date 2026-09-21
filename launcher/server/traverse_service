import time

import pyautogui

from base.login_one import GameTestLogin
from data.database import data_list

URL_MAP = {
    "test": "https://game_test.test928.xyz/#/start",
    "test4": "https://test4.bpapiglobal.com/",
    "demo": "https://game100.org/#/home",
}


def traverse_run(env: str, tasks: list):
    """遍历模式：单窗口内循环点击多个游戏"""
    for idx, win_config in enumerate(tasks, 1):
        country_cfg = next(
            (c for c in data_list if c["Country"] == win_config.country), None
        )
        if not country_cfg:
            print(f"[Traverse] 窗口{idx} 异常：找不到国家 {win_config.country}")
            continue

        start_y = int(win_config.y)
        bot = GameTestLogin()

        try:
            url = URL_MAP.get(env, URL_MAP["test"])
            bot.driver.get(url)

            # 登录流程（只执行一次）
            if env == "test4":
                bot.wallet_test4()
                bot.input_apihost_test4(country_cfg["apihost"])
            else:
                bot.wallet()
                bot.input_apihost()

            bot.input_id()
            bot.input_key()
            username = win_config.username or bot.random_username()
            if win_config.traverse_count > 1:
                username = f"{username}"
            bot.input_username(username)
            bot.input_rich(country_cfg["rich_code"])
            bot.input_region(country_cfg["region"])
            bot.input_language(win_config.language or country_cfg["language"])
            bot._win_rate = win_config.win_rate
            bot.input_win_probability_one()
            bot.input_balance()
            bot.click_login()
            time.sleep(1)

            # 选平台（只选一次）
            platform_xpath = bot.get_platform_xpath(win_config.x)
            bot.wait_click(platform_xpath).click()
            time.sleep(0.5)

            # 循环遍历游戏
            for offset in range(win_config.traverse_count):
                current_y = start_y + offset
                try:
                    game_xpath = bot.get_game_xpath(str(current_y))
                    bot.wait_click(game_xpath).click()
                    print(
                        f"[Traverse] 任务{idx}-{offset + 1} 成功：平台:{win_config.x}, 游戏={current_y}"
                    )

                    # bot.loading_wait(100)
                    time.sleep(60)

                    # bot.find_button_multiscale('D:\script\launcher\data\menu.png',matchvalue=0.4)
                    # bot.loading_wait(5)
                    # bot.find_button_multiscale('D:\script\launcher\data\gametable.png',matchvalue=0.3)
                    # time.sleep(3)
                    if offset < win_config.traverse_count - 1:
                        bot.driver.back()
                        time.sleep(2)

                except Exception as e:
                    print(f"[Traverse] 任务{idx}-{offset + 1} 异常(y={current_y})：{e}")
                    try:
                        bot.driver.get(url)
                        time.sleep(0.5)
                    except:
                        pass

        finally:
            try:
                bot.driver.quit()
            except:
                pass
