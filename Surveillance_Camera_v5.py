#Author: Zachary Williams
# VERSION 5 added timer that waits for webpage 
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

# Step 1: Set up Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run browser in headless mode
driver = webdriver.Chrome(options=chrome_options)

# Step 2: Navigate to the website
base_url = "http://insecam.org/en/bynew/"
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

# Extract the page numbers and select a random page
page_numbers = [int(page.text) for page in page_elements if page.text.isdigit()]
if not page_numbers:
    print("No page numbers found on the page.")
    driver.quit()
    exit()

random_page = random.choice(page_numbers)

## print random page selected
print('Random page selected: ' + str(random_page))

# Navigate to the selected random page with a delay
random_page_url = f"{base_url}?page={random_page}"
driver.get(random_page_url)

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

max_retry_attempts = 3  # Adjust the number of retry attempts as needed
for attempt in range(max_retry_attempts):
    try:
        # Set a longer timeout for accessing the camera feed (adjust as needed)
        driver.set_page_load_timeout(60)  # 60 seconds
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

# Step 8: Generate a unique filename with the title
screenshot_file = f"{selected_camera_title}.png"

# Step 9: Save Screenshot
with open(screenshot_file, "wb") as file:
    file.write(screenshot)

print(f"Screenshot saved as {screenshot_file}")

# Clean up
driver.quit()


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

# # Step 5: Random Selection
# selected_camera_url, selected_camera_title = random.choice(camera_info)

# # Step 6: Access Camera Feed with Retry
# print(f"Selected camera URL: {selected_camera_url}")

# max_retry_attempts = 3  # Adjust the number of retry attempts as needed
# for attempt in range(max_retry_attempts):
#     try:
#         # Set a longer timeout for accessing the camera feed (adjust as needed)
#         driver.set_page_load_timeout(60)  # 60 seconds
#         driver.get(selected_camera_url)
#         break  # Exit the loop if successful
#     except TimeoutException:
#         if attempt == max_retry_attempts - 1:
#             print("Timeout: Camera feed didn't load within the specified time after retries.")
#             driver.quit()
#             exit()
#         else:
#             print(f"Retry attempt {attempt + 1}...")
#             time.sleep(5)  # Wait for a few seconds before retrying



# # Step 7: Generate a unique filename with the title
# screenshot_file = f"{selected_camera_title}.png"

# # Step 7.5: Capture Screenshot
# screenshot = driver.get_screenshot_as_png()

# # Step 8: Save Screenshot
# with open(screenshot_file, "wb") as file:
#     file.write(screenshot)

# print(f"Screenshot saved as {screenshot_file}")

# # Step 9: Upload the screenshot to Twitter using Bearer Token
# try:
#     print('Entered try to upload screenshot to Twitter')
#     # Prepare the headers for the media upload
#     headers = {
#         'Authorization': f'Bearer {bearer_token}',
#         'Content-Type': 'multipart/form-data',
#     }

#     # Upload the media (screenshot)
#     with open(screenshot_file, 'rb') as media_file:
#         media_data = media_file.read()
#         media_response = requests.post(
#             'https://upload.twitter.com/1.1/media/upload.json',
#             headers=headers,
#             data=media_data
#         )
#     print('made it to 146')
#     if media_response.status_code == 201:
#         media_id = media_response.json()['media_id']
#         # Tweet with the uploaded media
#         tweet_text = f"Live camera screenshot: {selected_camera_title}"
#         tweet_params = {
#             'status': tweet_text,
#             'media_ids': [media_id],
#         }
#         print('155 - tweet_text worked')
#         tweet_response = requests.post(
#             'https://api.twitter.com/1.1/statuses/update.json',
#             headers=headers,
#             params=tweet_params,
#         )

#         if tweet_response.status_code == 200:
#             print("Screenshot uploaded to Twitter successfully.")
#         else:
#             print(f"Error uploading screenshot to Twitter: {tweet_response.text}")
#             print(f"Response Text: {tweet_response.text}")
#     else:
#         print(f"Error uploading media to Twitter: {media_response.text}")

# except Exception as e:
#     print(f"An error occurred: {str(e)}")
#     print(f"Response content: {media_response.text}")  # Add this line

# # Clean up
# driver.quit()