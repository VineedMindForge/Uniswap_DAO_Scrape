from selenium import webdriver
from bs4 import BeautifulSoup
import time, openpyxl

geckodriver_path = 'C:/Users/hp/Documents/DAO/webdriver/geckodriver.exe'  # Update with the correct file name and extension

browser = webdriver.Firefox(executable_path=geckodriver_path)
browser.get("https://gov.uniswap.org/")

# Infinite scroll till the end of the page
first_run = 1
while True:
    # Execute JavaScript to scroll to the bottom
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait for some time for the new content to load
    # You can adjust the sleep duration based on the website and your internet speed
    time.sleep(5)  # Wait for 2 seconds

    # Check if the bottom of the page is reached
    current_height = browser.execute_script("return document.body.scrollHeight")
    if first_run ==1:
        prev_height = 0
        first_run =0
    if current_height == prev_height:
        break  # Reached the end of the page, exit the loop
    else:
        print(f"Current Height - {current_height}\t Prev Height - {prev_height}")
        prev_height = current_height
        print('Moving down')

print("Done scrolling", "\n**15")

# Get the HTML source of the page
html_source = browser.page_source

# Create a Beautiful Soup object
soup = BeautifulSoup(html_source, 'html.parser')
total_discussion_body = soup.find('tbody')
discussions = total_discussion_body.find_all('tr', class_='topic-list-item')

formatted_html = total_discussion_body.prettify()

with open('formatted_html.txt', 'w') as file:
    file.write(formatted_html)    


# Create new Excel workbook and schema design

sheet = openpyxl.Workbook().active
sheet.cell(row=1, column=1).value = 'Title'
sheet.cell(row=1, column=2).value = 'Description'
sheet.cell(row=1, column=3).value = 'Replies'
sheet.cell(row=1, column=4).value = 'Views'
sheet.cell(row=1, column=5).value = 'Date'

row = 2
for discussion in discussions:
    title = discussion.find('a', class_ = 'title raw-link raw-topic-link').text.strip()
    try:
        description = discussion.find('p', class_ = 'excerpt').text.strip()
    except:
        try:
            description = discussion.find('span', class_ = 'category-name').text.strip()        
        except:
            description = '*****No valid description extracted*****'
    reply = discussion.find('td', class_ = 'replies').text.strip()
    view = discussion.find('td', class_ = 'views').text.strip()
    date = discussion.find('td', class_ = 'views').find_next_sibling('td').text.strip()
    sheet.cell(row=row, column=1).value = title
    sheet.cell(row=row, column=2).value = description
    sheet.cell(row=row, column=3).value = reply
    sheet.cell(row=row, column=4).value = view
    sheet.cell(row=row, column=5).value = date
    print(f"Done Printing {row}")
    print('*'*15)
    row+=1
    
    
browser.quit()
sheet.parent.save("data.xlsx")





