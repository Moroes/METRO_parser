import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


url = "https://online.metro-cc.ru/category/molochnye-prodkuty-syry-i-yayca/syry"

def get_data_with_selenium():
    opts = Options()
    opts.page_load_strategy = 'eager'
    opts.add_argument("User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")

    result_list = []
    progress = 0
    try:
        driver = webdriver.Chrome(options=opts)
        driver.get(url=url)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        count_page = int(soup.find_all("a", "v-pagination__item catalog-paginate__item")[-1].text)

        for i in range(1):
            current_url = f"https://online.metro-cc.ru/category/molochnye-prodkuty-syry-i-yayca/syry?page={i+1}"

            driver.get(url=current_url)
            soup = BeautifulSoup(driver.page_source, "html.parser")

            cards = soup.find_all("div", class_="product-card")

            for card in cards:
                progress += 1
                id = card.get("data-sku")
                title = card.find("a").get("title")
                href = "https://online.metro-cc.ru" + card.find("a").get("href")
                prices = card.find_all("span", class_="product-price__sum-rubles")
                if len(prices) == 0:
                    continue
                elif len(prices) > 1:
                    old_price = prices[1].text
                    new_price = prices[0].text
                else:
                    old_price = prices[0].text
                    new_price = None

                driver.get(url=href)
                soup = BeautifulSoup(driver.page_source, "html.parser")
                brand = soup.find("a", class_="product-attributes__list-item-link").text.strip()

                result_list.append(
                    {
                        "article": id,
                        "title": title,
                        "url": href,
                        "price": old_price,
                        "discout_price": new_price,
                        "brand": brand,
                    }
                )
                print(f"[+] Processed: {progress}/660")

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()
        with open("result2.json", "w", encoding="utf-8") as file:
            json.dump(result_list, file, indent=4, ensure_ascii=False)


def main():
    get_data_with_selenium()


if __name__ == '__main__':
    main()