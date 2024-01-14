from behave import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = None


@given("I am a user of the nbastore.eu")
def step_start_driver(context):
    options = Options()
    options.add_experimental_option("detach", False)
    context.driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    context.driver.maximize_window()

    global wait
    wait = WebDriverWait(context.driver, 5)


@when("I visit the nbastore.eu")
def step_visit_website(context):
    context.driver.get("https://www.nbastore.eu/en/")
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    assert (
        context.driver.title
        == "NBA Gear at NBA Store - The NBA Store. One Store, Every Team"
    )


@when("I search for a product using the term {term}")
def step_search_term(context, term):
    discount_box = context.driver.find_element(
        By.XPATH,
        "//*[@class='modal-backdrop']",
    )
    wait.until(EC.invisibility_of_element_located(discount_box))

    search_box = context.driver.find_element(
        By.XPATH,
        "//*[@id='typeahead-input-desktop']",
    )

    assert search_box is not None
    search_box.send_keys(term)

    search_button = context.driver.find_element(
        By.CSS_SELECTOR, "[aria-label='Search Product']"
    )
    assert search_button is not None
    search_button.click()


@then("I should see the search results")
def step_load_searched_page(context):
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    print(context.driver.title)
    assert context.driver.title == "| www.nbastore.eu"


@then("there should be at least {num_products} products in the search results")
def step_load_searched_page(context, num_products):
    products = context.driver.find_elements(By.CLASS_NAME, "column")
    assert len(products) > int(
        num_products
    ), f"Expected at least {num_products} products, but found {len(products)}"


@when("I click on the first product in the results")
def step_click_first_product(context):
    first_product = context.driver.find_element(
        By.XPATH,
        "//*[@alt='Chicago Bulls Michael Jordan Hardwood Classics Jersey - Michael Jordan - Youth']",
    )

    assert first_product is not None
    first_product.click()


@then("I should be taken to the details page for that product")
def step_first_product_page(context):
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    assert (
        context.driver.title
        == "Chicago Bulls Michael Jordan Hardwood Classics Jersey - Michael Jordan - Youth"
    )


@then("I close the browser")
def step_then_close_browser(context):
    context.driver.quit()
