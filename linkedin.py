import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver.get("https://www.linkedin.com/")
driver.find_element(By.CSS_SELECTOR,"a[class='sign-in-form__sign-in-cta my-2 py-1 btn-md btn-secondary block min-h-[40px] babybear:w-full']").click()
username=driver.find_element(By.ID,'username').send_keys("username")
password=driver.find_element(By.ID,'password').send_keys("password")
driver.find_element(By.CSS_SELECTOR,"button[aria-label='Sign in']").click()
driver.maximize_window()
time.sleep(15)
post_data = {}
post_xpath = "(//div[@class='fie-impression-container'])[1]"
first_post = driver.find_element(By.XPATH, post_xpath)


# Extract the author name
try:
    post_data['post_author'] = first_post.find_element(By.XPATH, ".//span[@class='visually-hidden']").text
    print("Post Author:", post_data['post_author'])
except:
    post_data['post_author']=print("Could not extract the name.")


# Optionally, you can extract more information like comments, likes, or shares if needed.

try:
    # Adjusting the XPath for likes based on LinkedIn's structure
    likes_element = first_post.find_element(By.XPATH,".//span[contains(@class, 'social-details-social-counts__reactions-count')]")

   # likes_element = first_post.find_element(By.XPATH, "//span[contains(@aria-hidden,'true')][normalize-space()='']")
    post_data['likes_count'] = likes_element.text
    print("Number of Likes:", post_data['likes_count'])
except:
    post_data['likes_count']=print("Could not extract the number of likes.")

# Extracting the number of comments
try:

    comments_element = first_post.find_element(By.XPATH,"//button[contains(@aria-label,'comments')]")
    post_data['comments_count'] = comments_element.text
    print("Total Number of Comments:", post_data['comments_count'])
except:
    post_data['comments_count']=print("Could not extract the number of comments.")

# Click to expand the comments section (this is necessary to load all comments)
try:
    comment_section_button = first_post.find_element(By.XPATH, ".//button[contains(@aria-label,'comments')]")
    comment_section_button.click()  # This expands the comments section
    time.sleep(3)  # Wait for the comments to load
except:
    print("Could not expand the comments section.")

# Extract the latest comment (assuming comments are loaded)
try:
    post_data['latest_comment'] = first_post.find_element(By.XPATH, "(//div[@dir='ltr'])[2]").text
    print("Latest Comment:", post_data['latest_comment'])
except:
    post_data['latest_comment']=print("Could not extract the latest comment.")
# Close the browser after scraping
driver.quit()

df = pd.DataFrame([post_data])
excel_file = "linkedin_post_data.xlsx"
df.to_excel(excel_file, index=False)

print(f"Scraped data has been saved to {excel_file}")


