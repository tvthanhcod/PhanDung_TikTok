import argparse
import asyncio
import contextlib
import os
import sys
from concurrent.futures import ThreadPoolExecutor
import threading
import logging
import aiofiles
from colorama import Fore, init

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

init(autoreset=True)

drivers = {}

selenium_logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
selenium_logger.setLevel(logging.ERROR)  # Chỉ hiển thị log error của Selenium


def create_driver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    options.add_experimental_option("prefs", prefs)
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    options.add_argument("--no-sandbox")
    options.set_capability('goog:loggingPrefs', {'browser': 'OFF', 'driver': 'OFF'}) 
    options.add_argument('--log-level=3')
    return webdriver.Chrome(options=options)

def split_text(input, character):
    input_split = input.split(character)
    return input_split


def get_user_status(username, driver, execution_time_hasProfile, execution_time_noProfile):
    
    url = f"https://www.tiktok.com/@{username}"
    driver.get(url)
        
    for i in range(15):
        try:
            userdata = WebDriverWait(driver, execution_time_hasProfile).until(EC.element_to_be_clickable((By.CLASS_NAME, "css-1h3j14u-DivFollowButtonWrapper")))
            return 0
        except:
            try:
                usertitle=WebDriverWait(driver, execution_time_noProfile).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".css-1osbocj-DivErrorContainer")))
                return 1
            except:
                pass
    return 2



def ensure_outfile() -> None:
    if not os.path.exists("./results"):
        os.mkdir("./results")
        open("./results/banned.txt", 'w')
        open("./results/living.txt", 'w')


def output_available(result: tuple[str, int]) -> None:
    username, status = result
    u_name, u_auth, u_hasphone = split_text(username, "|")
    if u_hasphone == "False":
        if (status == 1 or status==2):
            print(f"{Fore.LIGHTRED_EX}[ DIE OR NOT INFO ]{Fore.RESET}{Fore.LIGHTRED_EX} -> {u_name} - {u_auth}{Fore.RESET}")
            with open("./results/banned.txt", 'a') as of:
                of.write(str(username + '\n'))
                of.close()
        else:
            print(f"{Fore.LIGHTGREEN_EX}[ LIVE ]{Fore.RESET}{Fore.LIGHTGREEN_EX} -> {u_name} - {u_auth}{Fore.RESET}")
            with open("./results/living.txt", 'a') as of:
                of.write(str(username + '\n'))
                of.close()


def check_user(usernames: list[str]) -> None:
    current_thread = threading.current_thread()
    driver = drivers.get(current_thread)
    if driver is None:
        driver = create_driver()
        drivers[current_thread] = driver
    
    for username in usernames:
        u_name, _ , _ = split_text(username, "|")
        statusCode = get_user_status(u_name, driver, 1, 1)
        output_available((username, statusCode))

    if current_thread in drivers:
        drivers[current_thread].quit()
        del drivers[current_thread]



async def start() -> None:
    global USERNAMES
    async with aiofiles.open(WORDLIST, mode='r') as infile:
        USERNAMES = [line.strip() for line in await infile.readlines()]
        USERNAMES = [USERNAMES[x:x + int(THREADS + 1)]
                     for x in range(0, len(USERNAMES), int(THREADS + 1))]
    ensure_outfile()
    with ThreadPoolExecutor(max_workers=int(THREADS)) as executor:
        for sublist in USERNAMES:
            executor.submit(check_user, sublist)
            

if __name__ == "__main__":
    parser = argparse.ArgumentParser(sys.argv[0], description="github.com/9sv")
    parser.add_argument("wordlist", action="store")
    WORDLIST = (parser.parse_args()).wordlist
    THREADS = int(
        input(f"[{Fore.LIGHTBLUE_EX} Thread Count {Fore.RESET}] -> "))
    THREADS = 5 if THREADS >= 5 else THREADS 
    asyncio.run(start())
