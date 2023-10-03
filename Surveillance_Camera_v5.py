# Author: Zachary Williams
# Version 7 : Optimized randomization of page selection
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

# Define the number of times you want to repeat the process
num_iterations = 6  # Change this to the desired number of iterations

# random integer from 0 to 900 for page selection
arrow_random = random.randint(1, 900)

# Step 1: Set up Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run browser in headless mode

for _ in range(num_iterations):
    driver = webdriver.Chrome(options=chrome_options)

    # Step 2: Navigate to the website
    base_url = "http://insecam.org/en/bynew/?page=" + str(arrow_random)
    driver.get(base_url)

    # Wait for the page to load (adjust the wait time as needed)
    wait = WebDriverWait(driver, 20)  # Increased the wait time to 20 seconds
    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "thumbnail-item__img")))
    except TimeoutException:
        print("Timeout: Page didn't load within the specified time.")
        driver.quit()
        exit()

    # Step 3: Find the total number of pages
    page_elements = driver.find_elements(By.CSS_SELECTOR, "ul.pagination > li > a")
    if not page_elements:
        print("No pagination elements found on the page.")
        driver.quit()
        exit()

    # Extract the page numbers
    page_numbers = [int(page.text) for page in page_elements if page.text.isdigit()]
    
    # If there are page numbers, select a random page
    if page_numbers:
        random_page = random.choice(page_numbers)
        print('Random page selected: ' + str(random_page))

        # Navigate to the selected random page with a delay
        random_page_url = f"{base_url}?page={random_page}"
        driver.get(random_page_url)
        time.sleep(5)  # Adjust the sleep duration as needed


    # Introduce a delay between page navigations
    time.sleep(5)  # Adjust the sleep duration as needed

    print('Successfully navigated to selected random page')

    # Step 4: Find Camera Links with Title Attribute
    camera_elements = driver.find_elements(By.CLASS_NAME, "thumbnail-item")
    camera_info = []

    for camera_element in camera_elements:
        img_tag = camera_element.find_element(By.CLASS_NAME, "thumbnail-item__img")
        src_attr = img_tag.get_attribute("src")
        title_attr = img_tag.get_attribute("title")

        if src_attr and title_attr:
            camera_info.append((src_attr, title_attr))

    # Check if there are camera links
    if not camera_info:
        print("No camera links found on the page.")
        driver.quit()
        exit()

    # Step 5: Random Selection
    selected_camera_url, selected_camera_title = random.choice(camera_info)

    # Step 6: Access Camera Feed with Retry
    print(f"Selected camera URL: {selected_camera_url}")

    max_retry_attempts = 2  # Adjust the number of retry attempts as needed
    for attempt in range(max_retry_attempts):
        try:
            # Set a longer timeout for accessing the camera feed (adjust as needed)
            driver.set_page_load_timeout(10)  # 10 seconds
            driver.get(selected_camera_url)
            break  # Exit the loop if successful
        except TimeoutException:
            if attempt == max_retry_attempts - 1:
                print("Timeout: Camera feed didn't load within the specified time after retries.")
                driver.quit()
                exit()
            else:
                print(f"Retry attempt {attempt + 1}...")
                time.sleep(5)  # Wait for a few seconds before retrying

    # Step 7: Capture Screenshot
    screenshot = driver.get_screenshot_as_png()

    # Step 8: Generate a unique filename with timestamp and the title
    current_timestamp = int(time.time())  # Get current timestamp
    screenshot_file = f"{selected_camera_title}_{current_timestamp}.png"

    # Step 9: Save Screenshot
    with open(screenshot_file, "wb") as file:
        file.write(screenshot)

    print(f"Screenshot saved as {screenshot_file}")

    # Clean up
    driver.quit()

    # add delay between iterations 
    time.sleep(5)  # Adjust the sleep duration as needed


##

# # VERSION 6 with Twitter automation
# import random
# import time
# import requests
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException
# from bs4 import BeautifulSoup

# # Twitter Bearer Token
# bearer_token = ''  # Replace with your actual Bearer Token

# # Step 1: Set up Selenium WebDriver
# chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run browser in headless mode
# driver = webdriver.Chrome(options=chrome_options)

# # Step 2: Navigate to the website
# base_url = "http://insecam.org/en/bynew/"
# driver.get(base_url)

# print('Navigated to website')

# # Wait for the page to load (adjust the wait time as needed)
# wait = WebDriverWait(driver, 20)  # Increased the wait time to 20 seconds
# try:
#     wait.until(EC.presence_of_element_located((By.CLASS_NAME, "thumbnail-item__img")))
# except TimeoutException:
#     print("Timeout: Page didn't load within the specified time.")
#     driver.quit()
#     exit()

# # Step 3: Find the total number of pages
# page_elements = driver.find_elements(By.CSS_SELECTOR, "ul.pagination > li > a")
# if not page_elements:
#     print("No pagination elements found on the page.")
#     driver.quit()
#     exit()

# # Extract the page numbers and select a random page
# page_numbers = [int(page.text) for page in page_elements if page.text.isdigit()]
# if not page_numbers:
#     print("No page numbers found on the page.")
#     driver.quit()
#     exit()

# random_page = random.choice(page_numbers)

# ## print random page selected
# print('Random page selected: ' + str(random_page))

# # Navigate to the selected random page with a delay
# random_page_url = f"{base_url}?page={random_page}"
# driver.get(random_page_url)

# # Introduce a delay between page navigations
# time.sleep(5)  # Adjust the sleep duration as needed

# print('Successfully navigated to selected random page')

# # Step 4: Find Camera Links with Title Attribute
# camera_elements = driver.find_elements(By.CLASS_NAME, "thumbnail-item")
# camera_info = []

# for camera_element in camera_elements:
#     img_tag = camera_element.find_element(By.CLASS_NAME, "thumbnail-item__img")
#     src_attr = img_tag.get_attribute("src")
#     title_attr = img_tag.get_attribute("title")

#     if src_attr and title_attr:
#         camera_info.append((src_attr, title_attr))

# # Check if there are camera links
# if not camera_info:
#     print("No camera links found on the page.")
#     driver.quit()
#     exit()

