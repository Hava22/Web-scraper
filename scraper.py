import requests
from bs4 import BeautifulSoup
import csv

URL = "https://example.com/products"  # <-- Replace with your target URL

def scrape_products(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    products = []

    # Adjust selectors to fit the target website
    for item in soup.select(".product-item"):
        title = item.select_one(".product-title")
        price = item.select_one(".product-price")
        link = item.select_one("a")

        products.append({
            "Title": title.get_text(strip=True) if title else "N/A",
            "Price": price.get_text(strip=True) if price else "N/A",
            "Link": link["href"] if link and link.has_attr("href") else "N/A"
        })

    return products

def save_to_csv(products, filename="products.csv"):
    if not products:
        print("No products found to save.")
        return
    keys = products[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(products)
    print(f"Saved {len(products)} products to {filename}")

if __name__ == "__main__":
    product_list = scrape_products(URL)
    save_to_csv(product_list)

