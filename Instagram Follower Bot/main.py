#

# ! Project on Instagram Follow Bot
# ? which automatically follows accounts
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementClickInterceptedException,
)
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time
import random


INSTA_URL = "https://instagram.com"
INSTA_USERNAME = "flame_kaiser_official"
INSTA_PASSWORD = "<pYL):qI<3@!^Duo2>Im"
CHEFSTEPS_ACCOUNT = "/chefsteps/"

chrome_options = ChromeOptions()
chrome_options.add_experimental_option("detach", True)


class InstaFollower:

    def __init__(self):
        # Optional - Keep browser open (helps diagnose issues during a crash)
        chrome_options = ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        self.driver = Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 5)

    def login(self):

        self.driver.maximize_window()
        self.driver.get(INSTA_URL)

        time.sleep(random.uniform(3, 5))

        username = self.wait.until(
            ec.presence_of_element_located((By.NAME, "username"))
        )

        for ch in INSTA_USERNAME:
            username.send_keys(ch)
            time.sleep(random.uniform(0.5, 0.7))  # human like typing speed

        password = self.driver.find_element(By.NAME, "password")

        for ch in INSTA_PASSWORD:
            password.send_keys(ch)
            time.sleep(random.uniform(0.7, 1))

        time.sleep(random.uniform(3.2, 5.2))

        password.send_keys(Keys.ENTER)

        time.sleep(random.uniform(4.3, 7.3))

        try:
            save_login_prompt = self.driver.find_element(
                By.XPATH, '//div[contains(text(), "Not now")]'
            )
            if save_login_prompt:
                save_login_prompt.click()
        except (NoSuchElementException, Exception):
            pass

        time.sleep(random.uniform(3.7, 5.7))

    def find_followers(self):

        time.sleep(random.uniform(5.5, 10.5))

        target_url = INSTA_URL + CHEFSTEPS_ACCOUNT
        self.driver.get(target_url)

        time.sleep(random.uniform(5.2, 7.2))

        self.wait.until(
            ec.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[2]/div[2]/section/main/div/div/header/div/section[2]/div[1]/div[3]/div[2]/a",
                )
            )
        ).click()

        time.sleep(random.uniform(2.2, 4.4))

        scrollable_popup = self.driver.find_element(
            by=By.XPATH,
            value="/html/body/div[4]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]",
        )

        for i in range(20):
            self.driver.execute_script(
                "arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_popup
            )
            time.sleep(random.uniform(2.7, 3.1))

    def follow(self):

        time.sleep(random.uniform(2, 4))

        modal = self.driver.find_element(
            By.XPATH,
            "/html/body/div[4]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]",
        )

        all_follow_button = modal.find_elements(
            by=By.CSS_SELECTOR, value='button[type="button"]'
        )

        for btns in all_follow_button:
            try:
                btns.click()
                time.sleep(random.uniform(2.2, 3.2))
            except (Exception, ElementClickInterceptedException):
                time.sleep(random.uniform(2.2, 3.2))

                try:
                    # cancel to unfollow
                    cancel_unfollow = self.wait.until(
                        ec.element_to_be_clickable(
                            (
                                By.XPATH,
                                "/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div/div/button[2]",
                            )
                        )
                    )
                    if cancel_unfollow:
                        cancel_unfollow.click()
                except Exception:
                    pass


bot = InstaFollower()
bot.login()
bot.find_followers()
bot.follow()
