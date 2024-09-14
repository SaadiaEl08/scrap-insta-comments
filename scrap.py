from selenium import webdriver
from selenium.webdriver.common.by import By
import json
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
import logging
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from dotenv import load_dotenv

load_dotenv()


output = {}
logging.basicConfig(level=logging.INFO)


def prepare_browser():
    logging.info("Preparing browser...")
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--headless=new")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    )

    # Setup ChromeDriver service
    service = Service(ChromeDriverManager().install())
    # Launch Chrome browser
    chrome = webdriver.Chrome(service=service, options=options)
    # # Navigate to Instagram before adding cookies
    # chrome.get("https://www.instagram.com")
    # # Pause for the page to load fully
    # time.sleep(5)
    # # add_login_cookie(chrome)
    print("prepare browser ended....")
    return chrome


def login(chrome):
    try:
        # waiting the page load
        WebDriverWait(chrome, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']"))
        )
        print("start login .....")
        username_value = os.getenv("instagram_username")
        password_value = os.getenv("instagram_password")
        username_input = chrome.find_element(By.CSS_SELECTOR, "input[name='username']")
        password_input = chrome.find_element(By.CSS_SELECTOR, "input[name='password']")

        # clear inputs
        username_input.clear()
        password_input.clear()

        # fill data
        username_input.send_keys(username_value)
        password_input.send_keys(password_value)

        # git the btn login
        login_btn = chrome.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_btn.click()
        time.sleep(15)
        print("finish login .....")

    except KeyboardInterrupt as e:
        print("finish login .....", e)


def add_login_cookie(chrome):
    # Define the expiration date and time
    expiration_date = datetime.now() + timedelta(days=1)
    # Convert to Unix timestamp
    expiration_timestamp = time.mktime(expiration_date.timetuple())
    logging.info("Adding login cookies...")
    with open("cookies.json", "r") as file:
        cookies = json.load(file)
        for cookie in cookies:
            cookie["expiry"] = expiration_timestamp
            chrome.add_cookie(cookie)
    chrome.refresh()
    time.sleep(10)
    logging.info("finished adding login cookies...")

def get_comments(chrome):
    print("start getting comments ....")
    WebDriverWait(chrome, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "h3._a9zc"))
    )
    comments_count = len(chrome.find_elements(By.CSS_SELECTOR, "h3._a9zc"))
    for i in range(comments_count):
        comment_text = chrome.find_elements(
            By.CSS_SELECTOR, "span._ap3a._aaco._aacu._aacx._aad7._aade"
        )[i].text
        comment_writer = chrome.find_elements(By.CSS_SELECTOR, "h3._a9zc a")[i].text
        comment = {"comment_tex": comment_text, "comment_writer": comment_writer}
        # Read existing data from the JSON file
        try:
            with open("instagram_comments.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            # If the file doesn't exist, start with an empty list
            data = []
        data.append(comment)

        with open("instagram_comments.json", "w") as file:
            json.dump(data, file, indent=4)
    close = chrome.find_element(
        By.CSS_SELECTOR,
        "body > div.x17hbii1.xyq6agu.x13ywhbb.xqlh4rs.x1n2onr6.xzkaem6 > div.x9f619.x1n2onr6.x1ja2u2z > div > div.x160vmok.x10l6tqk.x1eu8d0j.x1vjfegm > div > div",
    )
    close.click()
    print("end getting comments ....")

def scrape_instagram(username):
    chrome = prepare_browser()
    logging.info(f"Scraping Instagram for user: {username}")
    url = f"https://www.instagram.com/accounts/login/?next=https%3A%2F%2Fwww.instagram.com%2F{username}%2F&source=logged_out_half_sheet"
    chrome.get(url)
    # Wait until the page has finished loading
    WebDriverWait(chrome, 10).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete"
    )
    profile_url = f"https://www.instagram.com/{username}/"
    if "login" in chrome.current_url:
        login(chrome)
    if "challenge/" in chrome.current_url:
        print("oooooops")
    chrome.get(profile_url)
    time.sleep(10)
    if profile_url == chrome.current_url:
        logging.info("Successfully navigated to user profile.")
        try:
            WebDriverWait(chrome, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="tablist"]'))
            )
            all_posts_div = chrome.execute_script(
                "return document.querySelector('div[role=\"tablist\"]').nextElementSibling;"
            )
            actions = ActionChains(chrome)
            time.sleep(5)
            post_links = []
            # scroll to the end of all posts
            while True:
                all_links = all_posts_div.find_elements(By.TAG_NAME, "a")
                links = (
                    all_links
                    if len(post_links) == 0
                    else [item for item in all_links if item not in post_links]
                )
                if len(links) == 0:
                    print("reached the end of posts ....")
                    break
                for link in links:
                    post_links.append(link)
                    actions.move_to_element(link).perform()
                    time.sleep(3)
                    WebDriverWait(chrome, 20).until(
                        EC.presence_of_element_located(
                            (
                                By.CSS_SELECTOR,
                                "div:nth-child(3) li:nth-child(2)>span:nth-child(1)>span",
                            )
                        )
                    )
                    comment_count = link.find_element(
                        By.CSS_SELECTOR,
                        "div:nth-child(3) li:nth-child(2)>span:nth-child(1)>span",
                    ).text
                    if comment_count != "0":
                        link.click()
                        time.sleep(3)
                        get_comments(chrome)
                time.sleep(2)
        except Exception as e:
            logging.error(f"Error while scraping posts: {e} ")
    else:
        logging.warning("Failed to load profile.")


if __name__ == "__main__":
    instagram_profile = input("Enter instagram username to get its comments : ")
    start = time.time()
    scrape_instagram(instagram_profile)
    print("start time :", start)
    print("end time :", time.time())
