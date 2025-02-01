from requests_html import HTMLSession

# Create a session
session = HTMLSession()

# Open the website
url = "https://economictimes.indiatimes.com/tech/it/articlelist/78570530.cms?from=mdr"  # Replace with the URL of the dynamic page
response = session.get(url)

# Execute JavaScript on the page
response.html.render()

# Get the rendered HTML
html_content = response.html.html

# Parse with BeautifulSoup or another tool
from bs4 import BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Example: Extracting all <h3> tags
headings = soup.find_all('h3')
for heading in headings:
    print(heading.text)

# Close the session once done
session.close()
