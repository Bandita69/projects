from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time


def find_song_on_website(filepath, website_url):
    """
    Reads song titles from a file, searches them on a website, and stops 
    when a non-empty search result is found.
    
    Args:
        filepath (str): Path to the text file containing song titles (one per line).
        website_url (str): The URL of the website with the search functionality.
    """

    try:
      driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

      driver.get(website_url)

      with open(filepath, "r", encoding="utf-8") as file:
          for song_title in file:
              song_title = song_title.strip()
              if not song_title: #Skip empty lines.
                continue

              # Add quotations around the song title
              quoted_song_title = f'"{song_title}"'
              print(f"Searching for: {quoted_song_title}")
              
              #Find the search bar
              search_bar = driver.find_element(By.XPATH, "//input[@type='search']")
              search_bar.clear() #clear the previous query
              search_bar.send_keys(quoted_song_title)
              
              #Find the search button
              search_button = driver.find_element(By.XPATH, "//button[@type='submit']")
              search_button.click()

              # Wait for the search results to load
              WebDriverWait(driver, 10).until(
                  EC.presence_of_element_located((By.CLASS_NAME, "search-results"))
              )
              time.sleep(1) # give the page a moment to update the results in the DOM.
              search_results = driver.find_element(By.CLASS_NAME, "search-results")

              # Check if results are not empty.
              if search_results.text.strip():
                  print(f"Found a non-empty result for: {quoted_song_title}")
                  input("Press Enter to continue with the next song...")  # Wait for user input
              else:
                print(f"No result found for: {quoted_song_title}")


    except Exception as e:
       print(f"An error occurred: {e}")
    finally:
        # Close the browser after finishing or incase of an error
       if 'driver' in locals() and driver:
            driver.quit()


if __name__ == "__main__":
    song_file = "song_titles.txt" # Path to your song titles text file
    website = "https://beatsaver.com/?q=asdasad"  # Replace with the website's URL

    find_song_on_website(song_file, website)