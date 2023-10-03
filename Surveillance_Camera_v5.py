
# Author: Zachary Williams
# Version 8 : Added filename print loop / status messages / adjusted timers
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

# Define the number of times you want to repeat the process using prompt
num_iterations = int(input("Enter desired number of images: "))
counter = num_iterations # Counter for end message
png_arr_str = [] # Array of saved .png files to print at the completion of loop


# Step 1: Set up Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run browser in headless mode

for _ in range(num_iterations):
    driver = webdriver.Chrome(options=chrome_options)

    print('Driver initialized.')

    # roll for random page each iteration
    # random integer from 0 to 900 for page selection
    arrow_random = random.randint(1, 900)

    print('Connecting to website. \nThis may take awhile, please wait...\n')
    # Step 2: Navigate to the website page
    base_url = "http://insecam.org/en/bynew/?page=" + str(arrow_random)
    driver.get(base_url)

    # Wait for the page to load (adjust the wait time as needed)
    wait = WebDriverWait(driver, 5)  # Decrease the wait time to 5 seconds
    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "thumbnail-item__img")))
    except TimeoutException:
        print("Timeout: Page didn't load within the specified time.")
        driver.quit()
        exit()
    
    print(f"Attempting to navigate to page: {arrow_random}...\n")

    # Introduce a delay between page navigations
    # time.sleep(5)  # Adjust the sleep duration as needed

    print('Successfully navigated to selected random page\n')

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
                break
                # print("Timeout: Camera feed didn't load within the specified time after retries.")
                # driver.quit()
                # exit()
            else:
                print(f"Retry attempt {attempt + 1}...\n")
                time.sleep(5)  # Wait for a few seconds before retrying

    # Step 7: Capture Screenshot
    screenshot = driver.get_screenshot_as_png()

    # Step 8: Generate a unique filename with timestamp and the title
    current_timestamp = int(time.time())  # Get current timestamp
    screenshot_file = f"{selected_camera_title}_{current_timestamp}.png"

    # append screenshot name in .png filename array
    png_arr_str.append(screenshot_file)

    # Step 9: Save Screenshot
    with open(screenshot_file, "wb") as file:
        file.write(screenshot)

    print(f"Screenshot saved as {screenshot_file}\n")

    # Clean up
    driver.quit()

    # add delay between iterations 
    time.sleep(5)  # Adjust the sleep duration as needed

    counter-=1
    if (counter > 0):
        print(f"Success! \n\nIterations left: {counter}\n")

print('Here is a list of the images you saved:\n')

print(*png_arr_str, sep='\n')

print("\n")

print("Complete! Please come again!")
