from bs4 import BeautifulSoup

# Read the prettified HTML file
with open('C:\\Users\\hp\\Documents\\DAO\\Backup\\formatted_html.txt', 'r', encoding='utf-8') as file:
    html_data = file.read()

# Create a BeautifulSoup object
soup = BeautifulSoup(html_data, 'html.parser')

# Work with the HTML using BeautifulSoup
# For example, let's extract all the <a> tags and print their href attributes
data = soup.find('tbody', class_='topic-list-body').find_all('tr')
for discussion in data:
    print("https://gov.uniswap.org"+discussion.find('a', class_='title raw-link raw-topic-link')['href'])
