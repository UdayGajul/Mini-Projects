"""
Internet Speed Twitter (X) Complaint Bot
----------------------------------------
This script automatically checks your internet speed using speedtest.net
and tweets a complaint to @your_isp if the speed is below the promised values.

Features:
- Measures download and upload speed
- Compares with promised speeds (example speed - 150 Mbps down / 10 Mbps up)
- Automatically posts complaint on X (Twitter) if speed is insufficient

Note: Twitter/X login is currently commented out / not implemented due to
anti-bot detection issues with Selenium.
In order to Tweet I've created a new file called - 'tweet.py'.
"""

# ! Internet Speed Twitter (X) Complaint Bot

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time
import tweet
from dotenv import load_dotenv
import os

load_dotenv()

# CONSTANTS
PROMIS_DOWN = 150
PROMIS_UP = 10
SPEED_TEST_URL = "https://speedtest.net"
X_URL = "https://x.com"

class InternetSpeedXBot:
    """A bot that measures internet speed and complains to the ISP on X/Twitter when speeds are below promised values."""

    def __init__(self):
        """Initialize the Selenium WebDriver with Chrome and set up wait utility."""
        chrome_options = ChromeOptions()
        chrome_options.add_experimental_option("detach", True)

        self.driver = Chrome(chrome_options)
        self.wait = WebDriverWait(self.driver, 5)
        self.down = 0
        self.up = 0

    # ----------------------------------
    def get_internet_speed(self):
        """
        Navigate to speedtest.net, run the speed test,
        and extract download & upload speeds.

        Updates instance variables:
            self.down (float): Download speed in Mbps
            self.up (float): Upload speed in Mbps

        Note: Waits approximately 60 seconds for the test to complete.
        """

        # go to speedtest website
        self.driver.get(SPEED_TEST_URL)
        self.driver.maximize_window()

        time.sleep(3)

        # click on continue button i.e. privacy
        self.wait.until(
            ec.presence_of_element_located((By.ID, "onetrust-accept-btn-handler"))
        ).click()

        # click on go button
        self.driver.find_element(By.CLASS_NAME, value="start-text").click()

        time.sleep(60)

        # finding the elements
        down_up_result = self.wait.until(
            ec.presence_of_all_elements_located(
                (By.CSS_SELECTOR, ".result-data-large.number.result-data-value")
            )
        )

        # getting hold of the data i.e. down and up
        self.down = float(down_up_result[0].text)
        self.up = float(down_up_result[1].text)
        print(f"down: {self.down}")
        print(f"up: {self.up}")
        time.sleep(3)
        self.driver.quit()

    # ----------------------------------
    def tweet_at_provider(self):
        """
        Check if measured speeds are below promised values.
        If yes, prepare and post a complaint tweet to @reliancejio.

        Note: Actual tweeting is delegated to external tweet.tweet_a_post() function.
        Currently login implementation is skipped due to X anti-bot measures.
        """
        if self.down < PROMIS_DOWN or self.up < PROMIS_UP:
            your_isp = "example"
            complaint_msg = f"Hey @ {your_isp} ISP, why is my internet speed {self.down} down/{self.up} up when I pay for {PROMIS_DOWN} down/{PROMIS_UP} up?"
            tweet.tweet_a_post(complaint_msg)


bot = InternetSpeedXBot()

bot.get_internet_speed()
bot.tweet_at_provider()
