import argparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


def take_screenshot(width, height, theme_name, pathname, delay, filename):
    try:
        chrome_options = Options()
        chrome_options.add_argument(f"--window-size={width},{height}")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--hide-scrollbars")

        driver = webdriver.Chrome(options=chrome_options)
        driver.get(f"https://www.zimoluo.me/{pathname}")

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "menu-button"))).click()

        time.sleep(0.4)

        button_xpath = f"//button[.//img[@alt='Use {theme_name} theme']]"
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, button_xpath))).click()
        time.sleep(0.4)

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "menu-button"))).click()

        time.sleep(1)

        time.sleep(delay)

        driver.save_screenshot(f'{filename}.png')
    except KeyboardInterrupt:
        print("Screenshot taking was aborted by the user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()


def main():
    parser = argparse.ArgumentParser(
        description="Take a screenshot of a Zimo Web's page with specified settings.")
    parser.add_argument('-w', '--width', type=int,
                        default=1600, help='Width of the browser window')
    parser.add_argument('-H', '--height', type=int,
                        default=900, help='Height of the browser window')
    parser.add_argument('-t', '--theme', type=str,
                        default="pixelland", help='Theme name to apply')
    parser.add_argument('-p', '--pathname', type=str,
                        default="design", help='Path within Zimo Web')
    parser.add_argument('-d', '--delay', type=float,
                        default=0, help='Delay before taking the screenshot')
    parser.add_argument('-f', '--filename', type=str,
                        default='webpage_screenshot', help='Output filename without suffix')

    args = parser.parse_args()

    try:
        take_screenshot(args.width, args.height, args.theme,
                        args.pathname, args.delay, args.filename)
    except Exception as e:
        print(f"Failed to take screenshot: {e}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Program was interrupted by the user.")
