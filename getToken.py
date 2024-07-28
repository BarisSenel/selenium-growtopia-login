# Made by chaos_automation / spearofchaos
import argparse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import undetected_chromedriver as uc
import re
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from fake_useragent import UserAgent
import getLoginUrl
import os
import random
import string
import requests

# Generate random text for creating GID name
def generate_random_text(length=10):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Setup Chrome options
def setup_chrome_options(proxy):
    CAPSOLVER_EXTENSION_PATH = os.path.abspath("Capsolver")
    chrome_options = uc.ChromeOptions()
    ua = UserAgent()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument(f"--load-extension={CAPSOLVER_EXTENSION_PATH}")
    chrome_options.add_argument("--lang=en-EN")
    if proxy:
        chrome_options.add_argument(f'--proxy-server={proxy}')
    return chrome_options

# Initialize WebDriver
def init_driver(proxy):
    chrome_options = setup_chrome_options(proxy)
    driver = uc.Chrome(options=chrome_options)
    width = 1024
    height = 768
    driver.set_window_size(width, height)
    return driver

# Check for CAPTCHA
def captcha_check(driver):
    try:
        if "accounts.google.com/v3/signin/challenge/recaptcha" in driver.current_url:
            reCAPTCHA_frame = WebDriverWait(driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//iframe[@title="reCAPTCHA"]'))
            )
            print("Switched to reCAPTCHA frame")
            for _ in range(100):
                if "You are verified" in driver.page_source:
                    print("You are verified")
                    driver.switch_to.default_content()
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//*[text()="Next"]'))
                    ).click()
                    print("Submitted the form")
                    break
                else:
                    print("You are not verified yet. Retrying...")
                    sleep(1)
            else:
                print("Verification failed after multiple attempts.")
    except TimeoutException as e:
        print("Timeout occurred:", e)
    except NoSuchElementException as e:
        print("Element not found:", e)
    except Exception as e:
        print("An error occurred:", e)

# Login process
def login(driver, email, password, recovery_mail):
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="identifierId"]'))
        ).send_keys(email)
        print("Email sent")

        driver.switch_to.default_content()
        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="identifierNext"]/div/button/span'))
        ).click()
        sleep(5)
        captcha_check(driver)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input'))
        ).send_keys(password)
        print("Password sent")

        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="passwordNext"]/div/button/span'))
        ).click()
        sleep(5)

        if "Choose how you want to sign in:" in driver.page_source:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[text()="Confirm your recovery email"]'))
            ).click()
            sleep(3)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="knowledge-preregistered-email-response"]'))
            ).send_keys(recovery_mail)
            sleep(3)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[text()="Next"]'))
            ).click()
            sleep(3)
    except Exception as e:
        print("An error occurred during login:", e)
        driver.quit()

# Handle post-login process
def handle_post_login(driver):
    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[3]/div/div/div[2]/div/div/button/span'))
        ).click()
    except TimeoutException:
        print("Continue button not found")

    try:
        random_text = generate_random_text()

        if "Choose your name in Growtopia" in driver.page_source:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="login-name"]'))
            ).send_keys(random_text)
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="modalShow"]/div/div/div/div/section/div/div[2]/div/form/div[2]/input'))
            ).click()


        WebDriverWait(driver, 10).until(lambda d: "status\":\"success" in d.page_source)

        token_pattern = r'"token":"(.*?)"'
        match = re.search(token_pattern, driver.page_source)
        if match:
            token = match.group(1)
            print(f"Validated token: {token}")
            try:
                proxy = str(args.proxy).replace("socks5://", "")
                url = "http://localhost:80/addGmailBot"
                data = {'token': token, 'proxy': proxy}
                requests.post(url, data=data)
            except:
                print("Request not successfull")
        else:
            print("Token not found in the page source.")
    except TimeoutException:
        print("Token not found within the specified wait time.")
    finally:
        try:
            driver.quit()
        except OSError as e:
            print("Token process done")

# Main function
def main(proxy, email, password, recovery_mail):
    post_body = getLoginUrl.percent_encode()
    login_link = getLoginUrl.getUrl(post_body)
    print(f"Generated login link: {login_link}")  # Debugging statement

    while login_link is None:
        print("Error: The login link was not generated.")
        post_body = getLoginUrl.percent_encode()
        login_link = getLoginUrl.getUrl(post_body)
        print(f"Generated login link: {login_link}")  # Debugging statement
        
    driver = init_driver(proxy)
    driver.get(login_link)

    if "Use another account" in driver.page_source:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[text()="Use another account"]'))
        ).click()

    login(driver, email, password, recovery_mail)
    handle_post_login(driver)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Gmail Login Script')
    parser.add_argument('-proxy', type=str, help='Proxy information', required=False)
    parser.add_argument('-mail', type=str, help='Email address', required=True)
    parser.add_argument('-password', type=str, help='Password', required=True)
    parser.add_argument('-recoverymail', type=str, help='Recovery email address', required=True)
    
    args = parser.parse_args()

    main(args.proxy, args.mail, args.password, args.recoverymail)
