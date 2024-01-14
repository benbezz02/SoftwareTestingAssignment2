from behave import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import re

wait = None


@given("I am a user of nbastore.eu")
def step_start_driver(context):
    options = Options()
    options.add_experimental_option("detach", False)
    context.driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    context.driver.maximize_window()

    global wait
    wait = WebDriverWait(context.driver, 5)


@when("I visit nbastore.eu")
def step_visit_website(context):
    context.driver.get("https://www.nbastore.eu/en/")
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    assert (
        context.driver.title
        == "NBA Gear at NBA Store - The NBA Store. One Store, Every Team"
    )


@when("I click on the {category} category")
def step_when_click_category(context, category):
    discount_box = context.driver.find_element(
        By.XPATH,
        "//*[@class='modal-backdrop']",
    )
    wait.until(EC.invisibility_of_element_located(discount_box))

    category_element = context.driver.find_element(
        By.CSS_SELECTOR,
        f"[aria-label='{category.lower()}']",
    )

    assert category_element is not None
    category_element.click()


@then("I should be taken to the {category} category")
def step_then_taken_to_category(context, category):
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    current_url = context.driver.current_url
    assert (
        category.lower() in current_url.lower()
    ), f"Expected {category} category in URL, but got {current_url}"


@then("the category should show at least {num_products} products")
def step_then_check_product_count(context, num_products):
    products = context.driver.find_elements(By.CLASS_NAME, "column")
    assert len(products) > int(
        num_products
    ), f"Expected at least {num_products} products, but found {len(products)}"


@when("I select the first product in the category")
def step_when_click_first_product(context):
    products = context.driver.find_elements(By.CLASS_NAME, "column")
    first_product = products[0]

    assert first_product is not None
    first_product.click()


@then("I should be taken to the details pageof the selected product")
def step_then_taken_to_product_details(context):
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    item = context.driver.find_element(
        By.CSS_SELECTOR, "[data-talos='labelPdpProductTitle']"
    )
    item_n = re.sub(r"\s+", "-", item.text.lower())
    item_name = re.sub(r"-+", "-", item_n)

    current_url = context.driver.current_url
    assert (
        item_name in current_url.lower()
    ), f"Expected {item_name} in URL, but got {current_url}"


@then("I should close the browser")
def step_then_close_browser(context):
    context.driver.quit()
