import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

# List of websites to scrape with their respective tags
websites = [
    {"url": "https://economictimes.indiatimes.com/tech/it/articlelist/78570530.cms?from=mdr", "tags": "desc", "source": "economictimes"},
    {"url": "https://www.businesstoday.in/latest/corporate", "tags": "widget-listing-content-section", "source": "businesstoday"},
    {"url": "https://www.business-standard.com", "tags": "image-card", "source": "businessstandard"},
    {"url": "https://cio.economictimes.indiatimes.com/tag/it+companies", "tags": "", "source": "cioeconomictimes"}
]

# Headers to simulate a real browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

# HTML template for the output page
html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title> Corporate & IT News Scraper </title>
    <link rel="icon" href="https://icons.veryicon.com/png/o/miscellaneous/gu-bei-chen/it-4.png" type="image/x-icon">
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f9; margin: 0; padding: 20px; }
        h1 { color: #333; }
        .news-item { margin-bottom: 20px; padding: 10px; background-color: #fff; border: 1px solid #ddd; border-radius: 4px; }
        .news-item h4 { font-size: 1.2em; margin: 0; font-weight: bold; }
        .news-item p { font-size: 1em; color: #555; }
        .news-item a { color: #007BFF; text-decoration: none; }
        .news-item a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1> Corporate & IT Newsssss </h1>
    <div>"""

# Function to extract data from different websites based on the source
def extract_news_from_website(url, tag, source):
    try:
        req = requests.get(url, headers=headers)  # Pass headers to the request
        req.raise_for_status()
        soup = BeautifulSoup(req.content, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return []

    news_data = []

    if source == "economictimes":
        desc_divs = soup.find_all("div", class_=tag)
        for div in desc_divs:
            h4_tag = div.find("h4")
            if h4_tag and h4_tag.find("a"):
                anchor = h4_tag.find("a")
                title = anchor.get_text(strip=True)
                link = urljoin(url, anchor['href'])
                p_tag = div.find("p")
                description = p_tag.get_text(strip=True) if p_tag else "No description available."
                news_data.append((title, description, link))
    
    elif source == "businesstoday":
        section_divs = soup.find_all("div", class_=tag)
        for div in section_divs:
            h2_tag = div.find("h2")
            if h2_tag and h2_tag.find("a"):
                anchor = h2_tag.find("a")
                title = anchor.get_text(strip=True)
                link = urljoin(url, anchor['href'])
                p_tag = div.find("p")
                description = p_tag.get_text(strip=True) if p_tag else "No description available."
                news_data.append((title, description, link))

    elif source == "businessstandard":
        image_card_divs = soup.find_all("div", class_=tag)
        for div in image_card_divs:
            anchor = div.find("a", href=True)
            if anchor and anchor['href'].startswith("https://www.business-standard.com/companies"):
                link = anchor['href']
                title = anchor.get_text(strip=True)
                news_data.append((title, "", link))
    
    elif source == "cioeconomictimes":
        divs = soup.find_all("div", class_="")
        for div in divs:
            h3_tag = div.find("h3", class_="heading")
            if h3_tag and h3_tag.find("a"):
                anchor = h3_tag.find("a")
                title = anchor.get_text(strip=True)
                link = urljoin(url, anchor['href'])
                p_tag = div.find("p", class_="desktop-view")
                description = p_tag.get_text(strip=True) if p_tag else "No description available."
                news_data.append((title, description, link))

    return news_data

# Function to update HTML content
def update_html():
    global html_content
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title> Corporate & IT News Scraper </title>
    <link rel="icon" href="https://icons.veryicon.com/png/o/miscellaneous/gu-bei-chen/it-4.png" type="image/x-icon">
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f9; margin: 0; padding: 20px; }
        h1 { color: #333; }
        .news-item { margin-bottom: 20px; padding: 10px; background-color: #fff; border: 1px solid #ddd; border-radius: 4px; }
        .news-item h4 { font-size: 1.2em; margin: 0; font-weight: bold; }
        .news-item p { font-size: 1em; color: #555; }
        .news-item a { color: #007BFF; text-decoration: none; }
        .news-item a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1> Corporate & IT News </h1>
    <div>"""

    # Loop through each website and extract the data
    for website in websites:
        news_data = extract_news_from_website(website["url"], website["tags"], website["source"])
        for title, description, link in news_data:
            html_content += f'''
            <div class="news-item">
                <h4><a href="{link}" target="_blank">{title}</a></h4>
                <p>{description}</p>
            </div>
            '''

    # Close the HTML structure
    html_content += """
    </div>
</body>
</html>
    """

    # Write the updated HTML content to a file
    with open("extracted_news.html", "w", encoding="utf-8") as file:
        file.write(html_content)

    print("HTML file updated successfully: extracted_news.html")

# Run the update every 1 minute
while True:
    update_html()
    time.sleep(60)  # Wait for 1 minute before running again
