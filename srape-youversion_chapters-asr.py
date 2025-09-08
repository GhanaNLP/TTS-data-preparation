import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Chrome setup (not headless, so you can see browser)
options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 15)

# Start URL
start_url = "https://www.bible.com/bible/2717/MAT.1.NB"
driver.get(start_url)

# Output CSV file
output_file = "bible_chapters_output-nzema.csv"

# Create CSV file and write headers
with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Content", "URL"])

    chapter_count = 0

    while True:
        try:
            # Wait for title and content
            title_elem = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div[2]/main/div[1]/div[2]/div[1]/div[1]/div[1]/h1")))
            content_elem = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div[2]/main/div[1]/div[2]/div[1]/div[1]/div[1]/div")))

            # Extract data
            title = title_elem.text
            content = content_elem.text
            url = driver.current_url

            # Write to CSV
            writer.writerow([title, content, url])
            file.flush()  # Save immediately

            # Print status
            chapter_count += 1
            print(f"\n✅ Scraped Chapter {chapter_count}")
            print("Title:", title)
            print("URL:", url)
            print("Content snippet:", content[:200], "...")

            # Try clicking next button
            try:
                next_btn_xpath = "/html/body/div/div[2]/main/div[1]/div[3]/div[2]/a/div"
                next_button = wait.until(EC.element_to_be_clickable((By.XPATH, next_btn_xpath)))
                next_button.click()
                time.sleep(3)
            except Exception as e:
                print("🔁 Retry clicking next button...")
                try:
                    time.sleep(2)
                    next_button = wait.until(EC.element_to_be_clickable((By.XPATH, next_btn_xpath)))
                    next_button.click()
                    time.sleep(3)
                except:
                    print("❌ No more 'Next' button or failed twice. Ending.")
                    break

        except Exception as e:
            print(f"❌ Error while scraping Chapter {chapter_count + 1}: {e}")
            break

# Done
driver.quit()
print(f"\n✅ Finished scraping {chapter_count} chapters. Data saved to '{output_file}'.")

