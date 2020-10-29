from bs4 import BeautifulSoup as soup  # Library for HTML data structures
from urllib.request import urlopen as uReq  # Library for opening URLs
import re  # Library for regular expressions
import pandas as pd  # Library for data structures and data analysis tools

page_url = "https://lifeinformatica.com/categoria-producto/family-componentes/family-procesadores/"

uClient = uReq(page_url)

page_soup = soup(uClient.read(), "html.parser")
uClient.close()

containers = page_soup.findAll("div", {"class": "product-inner product-item__inner"})

out_filename = "cpu.csv"
headers = "manufacturer,product_name,speed,price \n"

f = open(out_filename, "w")
f.write(headers)

for container in containers:

    # Variables
    element = container.findAll("h2", {"class": "woocommerce-loop-product__title"})[0]
    split_word = "ghz"
    amd = "amd"
    intel = "intel"
    full_title = element.text.lower()

    # Manufacturer
    manufacturer = element.text.split(" ", 1)[0].lower()

    # Speed
    if manufacturer == amd and split_word in full_title:
        speed = full_title.partition(split_word)[0].split(" ", 4)[4]
    if manufacturer == intel:
        speed = re.search("([^\s]+)" + split_word, full_title).group(1)

    # Product Name
    if manufacturer == amd:
        product_name = re.search(manufacturer + "(.*?)" + speed, full_title).group(1)
    elif manufacturer == intel and "núcleos" in full_title:
        product_name = re.search(manufacturer + "(.*?)" + "núcleos", full_title).group(
            1
        )[:-3]

    # Price
    price = (
        container.findAll("span", {"class": "woocommerce-Price-amount amount"})[0]
        .text.strip()
        .replace("€", "")
        .replace(",", ".")
    )

    # Write the data into respective columns
    f.write(
        manufacturer
        + ", "
        + product_name.replace(",", "|")
        + ", "
        + speed
        + ", "
        + price
        + "\n"
    )

# Lastly, the file must be closed
f.close()

data = pd.read_csv("cpu.csv")
data.head()
