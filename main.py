from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
import pandas as pd

ser = Service('drivers/chrome/chromedriver')
opts = webdriver.ChromeOptions()
opts.headless = True
assert opts.headless


def data_scrapping(data):
    global books_df
    for book in data:
        # print(book.text)
        try:
            name = book.find_element(By.CLASS_NAME, 'title').text
            try:
                author = book.find_element(By.CLASS_NAME, 'subtitle').text
            except:
                author = 'Not availbale'
            try:
                date = book.find_element(By.CLASS_NAME, 'extra').text
            except:
                date = 'Not availbale'
            print('name:', name)
            print('author :', author)
            print('date :', date)
            print('_' * 100)
            #     Form a dataframe
            books_df = books_df.append(pd.DataFrame({'name': [name], 'author': author, 'date':date}))
        except Exception as e:
            print(e)
            pass


if __name__ == '__main__':
    driver = webdriver.Chrome()
    url = 'https://www.gutenberg.org/ebooks/search/?sort_order=release_date'
    driver.get(url)
    driver.maximize_window()
    books_df = pd.DataFrame()
    for _ in range(5):
        next_button = driver.find_element(By.XPATH, ".//a[contains(text(), 'Next')]")
        books = driver.find_elements(By.CLASS_NAME, 'booklink')
        data_scrapping(books)
        next_button.click()
    books_df.to_excel('output/extracted.xlsx')
    driver.close()