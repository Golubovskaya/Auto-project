# UI Test Automation: Cart & Checkout (YooKassa demo store)

E-commerce UI test automation built with **Python + Selenium + pytest**.
The tests cover the core user journey of an online store — from adding a
product to the cart through to order confirmation — against the demo
environment at [demo.yookassa.ru](https://demo.yookassa.ru/).

## Tech stack

- **Python 3.10+**
- **Selenium 4** — browser automation
- **pytest** — test runner and fixtures
- **Allure** — test reporting
- **GitHub Actions** — CI (linting + automated test runs)
- **Page Object Model** design pattern

## Test coverage

### 1. Cart operations (`test_cart_operations`)
- add a product to the cart and verify the cart counter;
- increase the quantity of a product;
- add a second product;
- verify both products are present in the cart;
- remove all products;
- verify the cart is empty and the counter is reset to zero.

### 2. Checkout process (`test_checkout_process`)
- navigate to the checkout page;
- verify the login modal window and its contents (email field, password field, "Log in" button);
- **negative testing** of the delivery city input (empty value, digits,
  special characters, non-existent city) with validation of the error messages;
- enter phone number and a valid city;
- verify that selecting a delivery option correctly increases the order total;
- enter the client's name and confirm the order.

## Architecture

The project follows the **Page Object Model** pattern: page interaction logic
is separated from the tests into dedicated classes.

```
bbe/
├── pages/
│   ├── base_page.py          # base actions: find, click, input, waits
│   ├── start_page.py         # home page and add-to-cart flow
│   ├── cart_page.py          # in-cart operations
│   └── order_status_page.py  # checkout flow
└── tests/
    ├── conftest.py           # driver fixtures, screenshot on test failure
    └── test_add_to_cart.py   # test scenarios
```

Implementation highlights:
- **explicit waits** (`WebDriverWait` + `expected_conditions`) instead of static sleeps;
- **automatic screenshot** on test failure, attached to the Allure report;
- structured reporting via `@allure.epic / feature / story / severity` and `allure.step`.

## Running the tests

```bash
# 1. Clone the repository
git clone https://github.com/Golubovskaya/Auto-project.git
cd Auto-project

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the tests
pytest bbe/tests --alluredir=allure-results
```

> Requires **Google Chrome** installed. The Selenium 4 driver is resolved
> automatically (Selenium Manager).

## Allure reports

```bash
# install the Allure CLI (example for macOS)
brew install allure

# generate and open the report
allure serve allure-results
```

## CI

On every push and pull request to the `main` branch, GitHub Actions:
1. installs dependencies;
2. runs the `flake8` linter;
3. runs the tests and stores the Allure results as a build artifact.
