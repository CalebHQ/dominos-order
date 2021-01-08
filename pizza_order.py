from requests.api import get
from selenium import webdriver
from time import sleep
import requests
from bs4 import BeautifulSoup
from texttable import Texttable
from selenium.common.exceptions import NoSuchElementException

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-notifications")
options.add_argument("--incognito")
options.add_experimental_option("detach", True)

time = 1


def order(street_no, street, suburb, state, postcode, order_option, voucher, pizza1, pizza2, pizza3, name, phone, email, payment_method):
    driver = webdriver.Chrome(chrome_options=options)
    driver.get('https://www.dominos.com.au/')

    address = f'{street_no} {street} {suburb} {state} {postcode}'

    driver.find_element_by_xpath(
        f'//a[@class="{order_option} button"]').click()

    driver.find_element_by_xpath(
        '//input[@name="Customer.StreetNo"]').send_keys(street_no)
    driver.find_element_by_xpath(
        '//input[@name="Customer.Street"]').send_keys(street)
    driver.find_element_by_xpath(
        '//input[@name="Customer.Suburb"]').send_keys(suburb)
    driver.find_element_by_xpath(
        '//input[@name="Customer.Postcode"]').send_keys(postcode)

    driver.find_element_by_xpath('//button[@id="order-time-button"]').click()

    sleep(time)

    driver.find_element_by_xpath('//*[@id="no-button"]').click()

    sleep(time)

    search_results = driver.find_elements_by_xpath(
        "//button[@class='store-result btn next']")

    for i in range(len(search_results)):
        if search_results[i].text == address:
            if len(search_results) > 1:
                driver.find_element_by_xpath(
                    f"//*[@id='search-items']/li[{i+1}]/form/button").click()
            elif len(search_results) == 1:
                driver.find_element_by_xpath(
                    f"//*[@id='search-items']/li/form/button").click()
            break
        else:
            print(f'Attempt {i+1}')

        if i == len(search_results)-1:
            print('Dominos does not have your address in record')
            driver.quit()
            quit()

    sleep(time)

    driver.find_element_by_xpath('//button[@aria-label="Close"]').click()

    sleep(time)

    driver.find_element_by_xpath(
        '//input[@id="voucher_code"]').send_keys(voucher)
    driver.find_element_by_xpath('//button[@id="apply_voucher"]').click()

    sleep(time)

    driver.find_element_by_xpath(
        '//a[@class="btn at-voucher-fulfill"]').click()

    sleep(time)

    get_pizza(driver, pizza1)
    get_pizza(driver, pizza2)
    get_pizza(driver, pizza3)

    while True:
        if driver.current_url != 'https://order.dominos.com.au/estore/en/Checkout':
            next_button(driver)
        elif driver.current_url == 'https://order.dominos.com.au/estore/en/Checkout':
            break

    driver.find_element_by_xpath(
        '//input[@name="Customer.Name"]').send_keys(name)
    driver.find_element_by_xpath(
        '//input[@name="Customer.Phone"]').send_keys(phone)
    driver.find_element_by_xpath(
        '//input[@name="Customer.Email"]').send_keys(email)

    sleep(time)

    driver.find_element_by_xpath(
        '//input[@name="Customer.SubscribeToEClub"]').click()
    driver.find_element_by_xpath(
        '//input[@name="Customer.SubscribeToEClubSms"]').click()

    sleep(time)

    driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);")
    driver.find_element_by_xpath(
        '//button[@id="customer-details-submit"]').click()

    sleep(time)

    driver.find_element_by_xpath('//button[@id="no-button"]').click()

    sleep(time*2)

    try:
        driver.find_element_by_xpath(
            '//button[@id="offer-addtoyourorder-no-5607"]').click()
    except:
        print('No Ad')

    sleep(time)

    # payment_method(driver, payment_method)

    sleep(time)


def next_button(driver):
    sleep(time)
    try:
        driver.find_element_by_xpath(
            '//button[@id="offer-addtoyourorder-no-6273"]').click()
    except:
        print('No Ad')

    try:
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        driver.find_element_by_xpath('//a[@id="basket-next"]').click()
    except NoSuchElementException:
        print('Next')
    sleep(time)


def get_pizza(driver, pizza_name):
    driver.find_element_by_xpath(
        '//a[@class="btn at-voucher-fulfill"]').click()

    sleep(time)

    max = len(driver.find_elements_by_xpath(f'//span[@id="product-name"]'))

    for i in range(1, max):
        name = driver.find_element_by_xpath(
            f'//*[@id="product"]/section/div[{i}]/div/a/div[2]/div[1]/div/span')
        pizza = f'//*[@id="product"]/section/div[{i}]/div/a/div[2]/div[1]/div/span'
        if name.text.strip() == pizza_name:
            driver.find_element_by_xpath(pizza).click()
            break

    sleep(time)

    driver.find_element_by_xpath(
        "//select[@id='crust']/option[text()='New Deep Pan']").click()

    driver.find_element_by_xpath('//button[@id="add-product-button"]').click()

    sleep(time)


# def payment(driver, method):
#     driver.find_element_by_xpath(f'//a[@id="payment_method_{method}"]').click()


def get_vouchers():
    vouchers = []

    url = 'https://www.frugalfeeds.com.au/dominos'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    codes = soup.find_all('td', {'class': 'column-1'})
    titles = soup.find_all('td', {'class': 'column-2'})
    exp_dates = soup.find_all('td', {'class': 'column-3'})

    for i in range(len(codes)):
        if 'Delivered' in titles[i].text:
            code = codes[i].text.strip()
            title = titles[i].text.strip()
            exp_date = exp_dates[i].text.strip()

            vouchers.append((code, title, exp_date))

    return vouchers


def print_vouchers():
    vouchers = get_vouchers()
    t = Texttable()
    t.set_cols_align(["c", "c", "c", "c"])
    t.set_cols_width([2, 15, 50, 15])

    count = 0
    for voucher in vouchers:
        id = count
        code = voucher[0]
        title = voucher[1]
        exp_date = voucher[2]
        t.add_rows([['ID', 'Code', 'Title', 'Expiry Date'],
                    [id, code, title, exp_date]])
        count += 1
    print(t.draw())
