from selenium import webdriver
import time

chrome_driver_path = ""
driver = webdriver.Chrome(chrome_driver_path)

driver.get("http://orteil.dashnet.org/experiments/cookie/")
cookie = driver.find_element_by_id("cookie")

shop_items = driver.find_elements_by_css_selector("html body#whole div#game div#rightPanel div#store *")

shop_items = [shop_items[num].text.split("\n")[0] for num in range(0, len(shop_items), 2)
              if shop_items[num].text != ""][:8]

cookie_upgrades = {}
for item in shop_items:
    lst = item.split(" - ")
    upg_id = f"buy{lst[0]}"
    upg_cost = int(lst[1].strip().replace(",", ""))
    cookie_upgrades[upg_cost] = upg_id

timeout = time.time() + 5
five_min = time.time() + 60*5

while True:
    cookie.click()

    if time.time() > timeout:
        money_el = driver.find_element_by_id("money").text
        if "," in money_el:
            money_el = money_el.replace(",", "")
        cookie_count = int(money_el)

        affordable_upgrades = {}
        for upg_cost, upg_id in cookie_upgrades.items():
            if cookie_count > upg_cost:
                affordable_upgrades[upg_cost] = upg_id

        highest_affordable_upgrade_price = max(affordable_upgrades)
        upgrade_to_purchase = affordable_upgrades[highest_affordable_upgrade_price]
        driver.find_element_by_id(upgrade_to_purchase).click()

        timeout = time.time() + 5

    if time.time() > five_min:
        cookie_per_s = driver.find_element_by_id("cps").text
        print(cookie_per_s)
        break

driver.quit()
