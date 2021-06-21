# Learn-PyTest

Learning PyTest and Selenium to create unit test and other automation. Starting right from setting up pytest till its common use cases.

## Technology Used

- Python
- Python-Decouple
- Django
- PyTest
- PyTest-Factory Boy
- Faker
- Django REST Framework
- Selenium
- pytest-cov
- model-bakery
- pytest-mock

In case Pipfile do not work

```bash
pipenv install django
pipenv install python-decouple
pipenv install djangorestframework
pipenv install pytest
pipenv install pytest-django
pipenv install selenium
pipenv install pytest-factoryboy
pipenv install Faker
pipenv install pytest-cov
pipenv install pytest-mock
```

## Index

1. [Intro to PyTest](#PyTest)
2. [What are Fixtures and how to use them](#states-of-fixtures-and-factories)  
   2.1 [Fixtures](#Fixtures)  
   2.2 [Accessing Database in Unit Test](#access-database)  
   2.3 [conftest.py file](#`conftest.py`---making-fixture-common-for-several-modules)  
   2.4 [Factory](#factory-as-a-fixture)
3. [Factory Boy and Faker](#factory-boy-and-faker)
4. [Parametrizing Test](#parametrizing-fixtures-and-test-functions)  
5. [Pytest in Selenium](#intro-to-selenium)
6. [Pytest with Unit, Integration and End to End tests](#payment-unit-integration-and-end-to-end-testing)

## Resources and Credits

- [Very Academy YouTube Playlist](https://www.youtube.com/playlist?list=PLOLrQ9Pn6caw3ilqDR8_qezp76QuEOlHY)
- [PyTest Official Doc](https://docs.pytest.org/en/6.2.x/)

## Setup

- To run all test `src $ : pytest`
- To run a specific test `src $ pytest apps/SeleniumApp/Test/test_2.py::BrowserTest`
- Load `.env` using `pipenv shell`. To load the env variables from `.env` file.
- Install `pytest` as dev package. `pipenv install --dev pytest`
- Update Pipfile.lock `pipenv lock`
- Install packages in production `pipenv install --ignore-pipfile`
- Install dev packages using `pipenv install --dev`
- Install pytest for django using `pipenv install --dev pytest-django`
- To create new app in nested folder user. (do not put trailing / after end of path )

    ```bash
    (Learn-PyTest)  src : ./manage.py startapp RegisterUser apps/RegisterUser
    ```

## PyTest

- Run `pytest` from dir where `pytest.ini` is located.

- `pytest -x` Prevent Further execution of other test when one test fails.

- By default pytest do not print any print statement inside unit test. We can do that by using `pytest -rP`

  ```python
  import pytest

  def test_example1():
      print('Inside string test')
      assert 1 == 1
  ```

  Before

  ```bash
  (Learn-PyTest)  src : pytest
  ============== test session starts ==============
  collected 2 items

  apps/MyApp/tests.py ..                    [100%]

  =============== 2 passed in 0.05s ===============
  ```

  After

  ```bash
  collected 2 items

  apps/MyApp/tests.py ..                    [100%]

  ==================== PASSES =====================
  _________________ test_example2 _________________
  ------------- Captured stdout call --------------
  Inside string test
  =============== 2 passed in 0.04s ===============
  ```

- Running a specific folder, app, file or test case

  ```bash
  (Learn-PyTest)  src : pytest apps/MyApp/tests.py::test_example2
  =================== test session starts ===========
  collected 1 item

  apps/MyApp/tests.py .                               [100%]

  ==================== 1 passed in 0.03s ===========
  ```

- We can skip some test cases or mark them as expected fail.

  ```python
  import pytest

  @pytest.mark.skip
  def test_example2():
      print("Inside string test")
      assert 'Hi' == 'Hi'

  @pytest.mark.xfail
  def test_example1():
      assert 1 == 1

  @pytest.mark.xfail
  def test_example3():
      assert 1 == 2
  ```

  ```bash
  (Learn-PyTest)  src : pytest
  =================== test session starts ==============
  collected 3 items

  apps/MyApp/tests.py sXx                        [100%]

  ======== 1 skipped, 1 xfailed, 1 xpassed in 0.08s =====
  ```

  **xfailed** : expected to fail  
   **xpassed**: exceptionally pass

- Put custom marker in `pytest.ini` file

  ```ini
  [pytest]
  DJANGO_SETTINGS_MODULE = MyProject.settings
  # -- recommended but optional:
  python_files = tests.py test_*.py *_tests.py

  markers =
      slow: slow running test
  ```

  Under marker a marker (**slow**) with description (**slow running test**). Now we can use this marker to run only those test cases which are marked with this marker.

  ```python
  import pytest

  @pytest.mark.slow
  def test_example1():
      assert 1 == 1

  def test_example2():
      assert 2 == 2
  ```

  ```bash
  (Learn-PyTest)  src : pytest -m "slow"
  ================ test session starts =================
  collected 3 items / 2 deselected / 1 selected

  apps/MyApp/tests.py .                          [100%]

  ========== 1 passed, 2 deselected in 0.04s ===========
  ```

## States of Fixtures and Factories

1. `Arrange` - prepare everything for our test
2. `MockUp` - mock the database, external code or third party API request
3. `Act` - state-changing action that kicks off the behavior we want to test
4. `Assert` - where we look at that resulting state and check if it looks how we’d expect
5. `CleanUp` - where the test clean up after execution, so other tests aren’t being accidentally influenced by it.

### Fixtures

- **Fixtures**: they are used to feed data to the tests such as databases connections, URLs or input data. Fixtures can be used at start and end of the test.
- Fixture can be defined in 4 ways.

  - **Function**: Run once per test
  - **Class**: Run once per class of test
  - **Module**: Run once per module
  - **Session**: Run once per session

```python
# fixture with scope of function (default)
import pytest

@pytest.fixture()
def fixture_1():
    print('Fixture 1')
    return 1

def test_example1(fixture_1):
    print('Example 1')
    assert 1 == fixture_1

def test_example2(fixture_1):
    print('Example 2')
    assert 1 == fixture_1
```

```bash
======================= PASSES =======================
___________________ test_example1 ____________________
--------------- Captured stdout setup ----------------
Fixture 1
---------------- Captured stdout call ----------------
Example 1
___________________ test_example2 ____________________
--------------- Captured stdout setup ----------------
Fixture 1
---------------- Captured stdout call ----------------
Example 2
================= 2 passed in 0.04s ==================
```

Changing the scope of fixture

```python
# scope of session
@pytest.fixture(scope="session")
def fixture_1():
    print('Fixture 1')
    return 1
```

```bash
======================= PASSES =======================
___________________ test_example1 ____________________
--------------- Captured stdout setup ----------------
Fixture 1
---------------- Captured stdout call ----------------
Example 1
___________________ test_example2 ____________________
---------------- Captured stdout call ----------------
Example 2
================= 2 passed in 0.04s ==================
```

Lets see how we can use fixtures to be used before and after a test.

```python
import pytest

@pytest.fixture
def yield_fixture():
    print("Start Test Phase")
    yield 1
    print("End Test Phase")

def test_example(yield_fixture):
    print('Example Test Case')
    assert 1 == yield_fixture
```

```bash
===================== PASSES =====================
__________________ test_example __________________
------------- Captured stdout setup --------------
Start Test Phase
-------------- Captured stdout call --------------
Example Test Case
------------ Captured stdout teardown ------------
End Test Phase
=============== 1 passed in 0.08s ================
```

### Access Database

```python
import pytest
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_user_create1():
    User.objects.create_user(
        username='test',
        email='test@email.com',
        password='abcd@1234'
    )
    count = User.objects.count()
    print(count)
    assert  count == 1


@pytest.mark.django_db
def test_user_create2():
    count = User.objects.count()
    print(count)
    assert  count == 0
```

```bash
===================== PASSES =====================
_______________ test_user_create1 ________________
-------------- Captured stdout call --------------
1
_______________ test_user_create2 ________________
-------------- Captured stdout call --------------
0
_________________ test_example1 __________________
```

This shows the database is seperate for two unit test cases that is both are supposed to run in isolation. Execution or failure of one should not prevent another from passing.

In case we want to access the very same data from database in two tests then we must go for fixtures. Where we infact put same data in database for each test case. Or think of it as each test case access same state of database. Since fixture access the database we don't need to access it in our test cases.

```python
import pytest
from django.contrib.auth.models import User

@pytest.fixture
def create_user(db):
    return User.objects.create_user(
        username='test',
        email='test@email.com'
    )

def test_set_check_password(create_user):
    create_user.set_password('new-password')
    assert create_user.check_password('new-password') == True
```

But here we addressed only one problem that is **we don't write data creation code repeatedly in each test** but what if we want that that data to be accessible by each of the test.py file or each of the test module in same or in sub dir of where the fixture is present. then we must declare the fixture on module level i.e. seperate module for fixture with name `conftest.py` file and that fixture will be available for all the test in same or in sub directory.

```bash
(Learn-PyTest)  src : pytest -rP apps/MyApp/tests/test_8.py
```

See the repeated execution of fixture for same data, Also this is accessible for test in this file only.

```python
import pytest
from django.contrib.auth.models import User

@pytest.fixture
def create_user(db):
    user = User.objects.create_user(
        username='test',
        email='test@email.com'
    )
    print('Creating User')
    return user

def test_set_check_password1(create_user):
    print("Set Password 1")
    create_user.set_password('new-password1')
    assert create_user.check_password('new-password1') == True

def test_set_check_password2(create_user):
    print("Set Password 2")
    create_user.set_password('new-password2')
    assert create_user.check_password('new-password2') == True
```

```bash
======================= PASSES =======================
______________ test_set_check_password1 ______________
--------------- Captured stdout setup ----------------
Creating User
---------------- Captured stdout call ----------------
Set Password 1
______________ test_set_check_password2 ______________
--------------- Captured stdout setup ----------------
Creating User
---------------- Captured stdout call ----------------
Set Password 2
================= 2 passed in 0.87s ==================
```

Modifyig above code to something below won't fix the problem but infact gives an error.

```python
@pytest.fixture(scope="session")
def create_user(db):
    user = User.objects.create_user(
        username='test',
        email='test@email.com'
    )
    print('Creating User')
    return user
```

```bash
======================== ERRORS =========================
______ ERROR at setup of test_set_check_password1 _______
ScopeMismatch: You tried to access the 'function' scoped fixture 'db' with a 'session' scoped request object, involved factories
______ ERROR at setup of test_set_check_password2 _______
... same
=================== 2 errors in 0.05s ===================
```

### `conftest.py` - Making fixture common for several modules

To fix this we create a file `conftest.py` in same dir where the test modules are located which shares the same fixture.

```bash
apps/MyApp/tests/
├── conftest.py
├── __pycache__
├── test_1.py
├── test_2.py
├── test_3.py
├── test_4.py
├── test_5.py
├── test_6.py
├── test_7.py
├── test_8.py
└── test_9.py
```

```python
# conftest.py
import pytest
from django.contrib.auth.models import User


@pytest.fixture()
def create_user(db):
    user = User.objects.create_user(
        username='test',
        email='test@email.com'
    )
    print('Creating User')
    return user
```

```python
# test_9.py
import pytest

def test_set_check_password1(create_user):
    print("Test 1")
    assert create_user.username == 'test'

def test_set_check_password2(create_user):
    print("Test 2")
    assert create_user.username == 'test'
```

```bash
================ PASSES =================
_______ test_set_check_password1 ________
--------- Captured stdout setup ---------
Creating User
--------- Captured stdout call ----------
Test 1
_______ test_set_check_password2 ________
--------- Captured stdout setup ---------
Creating User
--------- Captured stdout call ----------
Test 2
=========== 2 passed in 0.57s ===========
```

Now we can access module level fixture in each test in same or sub dir without importing it.

### Factory as a fixture

This factory will produce many different user which can be obtained using many different fixtures. Factory returns a function which can be used to create new user in minimal possible way.

```python
@pytest.fixture()
def new_user_factory(db):
    # inner function
    def create_app_user(
        username: str,
        password: str = None,
        first_name: str = "firstname",
        last_name: str = "lastname",
        email: str = "user@email.com",
        is_staff: bool = False,
        is_superuser: bool = False,
        is_active: bool = True
    ):
        user = User.objects.create(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=is_active
        )
        return user
    return create_app_user

@pytest.fixture
def create_new_user(db, new_user_factory):
    return new_user_factory(
            'Test User',
            'password',
            'user_firstname',
            is_staff=True
        )
```

```python
import pytest

def test_create_user_factory(create_new_user):
    print(create_new_user.first_name)
    assert  create_new_user.first_name == "user_firstname"
```

```bash
collected 1 item

apps/MyApp/tests/test_10.py .               [100%]

===================== PASSES ======================
____________ test_create_user_factory _____________
-------------- Captured stdout call ---------------
user_firstname
================ 1 passed in 0.25s ================
```

## Factory Boy and Faker

For the purpose of generating fake data. Factory Boy is basically fixture replacement tool. Factories are defined in a nice, clean and readable manner.

Make a new App and Test folder inside it. make a `factory.py` file to declare a factory class and a `conftest.py` file. Don't forget to include a `__init__.py` file inside `Test` dir of each App.

```python
# factory.py

import factory
from django.contrib.auth.models import User
from faker import Faker
fake = Faker()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    # specifing some default args to user model
    username = fake.name()
    is_staff = True
```

Register this factory in `conftest.py` file in same test folder. We will be running test cases for both the app seperately to avoid conflict in naming of `test_*` modules and other settings, factory and fixtures.

```python
# conftest.py
import pytest

from pytest_factoryboy import register
from .factory import UserFactory

register(UserFactory)   # now fixture to access this factory is user_factory
```

```python
# test 1
import  pytest

def test_new_user(user_factory):
    print(user_factory.username)
    assert True
```

```bash
(Learn-PyTest)  src : pytest -rP apps/FactoryApp/Tests/
================ test session starts =================
apps/FactoryApp/Tests/test_1.py .              [100%]

======================= PASSES =======================
___________________ test_new_user ____________________
---------------- Captured stdout call ----------------
Julie Arnold
================= 1 passed in 0.06s ==================
```

Here we created user but we don't add this user to database hence we are not required to add any decorator of pytest to test function. Do repeat this we can use `build` option of factory. `create` make entry to test database and not actual database. The obj which gets saved remains in test db until all test runs.
`create` is better as it gives error if obj created cannot be saved to database may be due to foreign key constraint or not null constraint.

```python
import  pytest

def test_new_user(user_factory):
    user = user_factory.build()
    print(user.username)
    assert True
```

```bash
======================= PASSES =======================
___________________ test_new_user ____________________
---------------- Captured stdout call ----------------
Amber Ritter
================= 1 passed in 0.07s ==================
```

Now if we try to create a user i.e. create a new user and save it to database we gets an error.

```python
import  pytest

def test_new_user(user_factory):
    # can not access database to save created user
    user = user_factory.create()
    print(user.username)
    assert True
```

We can remove the error by one of the following ways (first is prefered). Till now we use only `build` thus the object do not gets into database but using `create` we can save them into test database.

```python
import  pytest
from django.contrib.auth.models import User

def test_new_user(db, user_factory):
    user = user_factory.create()
    print(User.objects.count())
    print(user.username)
    assert True
```

```bash
--------------- Captured stdout call ----------------
0
Meghan Johnson
```

```python
import  pytest
from django.contrib.auth.models import User

# we can check the obj we create using factory
# is actually got saved into User table
@pytest.mark.django_db
def test_new_user(user_factory):
    user = user_factory.create()
    print(User.objects.count())
    print(user.username)
    assert True
```

```bash
--------------- Captured stdout call ----------------
1
Ryan Hubbard
```

Instead creating user in test case we prefer to introduce fixture here.

```python
# update conftest.py
import pytest

from pytest_factoryboy import register
from .factory import UserFactory

# now fixture will access this factory as user_factory
register(UserFactory)

# use a fixture to access datanase while using
# factory and prepare data for test
@pytest.fixture
def create_user(db, user_factory):
    user = user_factory.create()
    return user
```

```python
import  pytest
from django.contrib.auth.models import User

def test_new_user(create_user):
    user = create_user
    print(User.objects.count())
    print(user.username)
    assert True
```

```bash
apps/FactoryApp/Tests/test_1.py .           [ 50%]
apps/FactoryApp/Tests/test_2.py .           [100%]

===================== PASSES ======================
__________________ test_new_user __________________
-------------- Captured stdout call ---------------
1
Vincent Page
__________________ test_new_user __________________
-------------- Captured stdout call ---------------
1
Vincent Page
================ 2 passed in 0.25s ================
```

A more advanced use of factory is when model have foreign key dependency of each other. Let consider a Product model which refer to Category model. Then our factory will looks something like.

```python
class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = 'django'


class  ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    title = "product_title"
    category = factory.SubFactory(CategoryFactory)
    description = fake.text()
    slug = "product_slug"
    regular_price = 9.99
    discount_price = 4.99
```

Register the factories in conftest.py

```python
import pytest
from pytest_factoryboy import register
from .factory import ProductFactory, CategoryFactory

# now fixture will access this factory as user_factory
register(ProductFactory)
register(CategoryFactory)
```

```python
import pytest

def test_product_creation(product_factory):
    product = product_factory.build()
    print(product.description)
    print(product.category)
    assert True
```

```bash
===================== PASSES =====================
_____________ test_product_creation ______________
-------------- Captured stdout call --------------
Young soon support assume score. Task force energy financial if push town.
django
=============== 1 passed in 0.06s ================
```

```python
import pytest
from apps.FactoryApp.models import Product

def test_product_creation(db, product_factory):
    product = product_factory.create()
    print(product.description)
    print(product.category)
    print(Product.objects.count())
    assert True
```

```bash
_____________ test_product_creation ______________
-------------- Captured stdout call --------------
Enough involve talk head address. Feeling early trial resource. Capital writer finally give culture green field oil.
Protect career course can anyone. Ago space discuss old.
django
1
=============== 1 passed in 0.29s ================
```

## Parametrizing Fixtures and Test functions

Provide data to be passed to test in parameters itself. For each new parameter a new database is created and one test run do not interfer another one.

```python
import pytest
from apps.FactoryApp.models import Product


@pytest.mark.parametrize(
    "title, category, description, slug, regular_price, discount_price, validity",
    [
        ("NewProduct1", 1, "NewDesc", "slug", 2.99, 5.99, True),
        ("", 1, "NewDesc", "slug", 2.99, 5.99, True),
        # ("NewProduct3", 0, "NewDesc", "slug", 2.99, 5.99, False),      # can't test as None can't be given in Foreign Key
        ("NewProduct4", 1, "", "slug", 2.99, 5.99, True),
        ("NewProduct5", 1, "NewDesc", "", 2.34, 5.99, True),
        # ("NewProduct6", 1, "NewDesc", "slug", 2.99, None, False)            # Can't give none in float field
    ]
)
def test_product_instance(
    db,                     # to access database
    product_factory,        # to access factory
    title,
    category,
    description,
    slug,
    regular_price,
    discount_price,
    validity
):
    test = product_factory(
        title=title,
        category_id=category,
        description=description,
        slug=slug,
        regular_price=regular_price,
        discount_price=discount_price,
    )

    item = Product.objects.count()
    print(item)
    assert item == validity
```

```bash
============================= PASSES =============================
_ test_product_instance[NewProduct1-1-NewDesc-slug-2.99-5.99-True] _
---------------------- Captured stdout call ----------------------
1
_____ test_product_instance[-1-NewDesc-slug-2.99-5.99-True] ______
---------------------- Captured stdout call ----------------------
1
___ test_product_instance[NewProduct4-1--slug-2.99-5.99-True] ____
---------------------- Captured stdout call ----------------------
1
__ test_product_instance[NewProduct5-1-NewDesc--2.34-5.99-True] __
---------------------- Captured stdout call ----------------------
1
======================= 4 passed in 0.29s ========================
```

But notice we can't test API's of some input for which data is invalid like `pk` of `Category` which do not exists. So we will use `client` to make this request. This `client` request can be made on django forms or API's.

- We made a `not null` restriction on `slug` field of `Product` and it is available on `api/product/`.

```python
import pytest


@pytest.mark.parametrize(
    "title, category, description, slug, regular_price, discount_price, validity",
    [
        ("Netflix", 3, "New Series", "", 50.99, 45.99, 400),
        ("Netflix", 3, "New Series", "netflix", "", 45.99, 400),
    ]
)
@pytest.mark.django_db
def test_product_instance(
    client,    # client to make request
    title,
    category,
    description,
    slug,
    regular_price,
    discount_price,
    validity
):
    response = client.post(
        '/api/product/',
        data = {
            'title': title,
            'category': category,
            'description': description,
            'slug': slug,
            'regular_price': regular_price,
            'discount_price': discount_price,
        }
    )

    print(response.status_code)
    print(response.data)

    assert response.status_code == validity
```

Lets see the response

```bash
============================ PASSES =============================
_ test_product_instance[Netflix-3-New Series--50.99-45.99-400] __
--------------------- Captured stdout call ----------------------
400
{'slug': [ErrorDetail(string='This field may not be blank.', code='blank')], 'category': [ErrorDetail(string='Invalid pk "3" - object does not exist.', code='does_not_exist')]}
----------------------- Captured log call -----------------------
WARNING  django.request:log.py:224 Bad Request: /api/product/
_ test_product_instance[Netflix-3-New Series-netflix--45.99-400] _
--------------------- Captured stdout call ----------------------
400
{'regular_price': [ErrorDetail(string='A valid number is required.', code='invalid')], 'category': [ErrorDetail(string='Invalid pk "3" - object does not exist.', code='does_not_exist')]}
----------------------- Captured log call -----------------------
WARNING  django.request:log.py:224 Bad Request: /api/product/
======================= 2 passed in 0.31s =======================
```

## Intro to Selenium

```bash
# create a new app
(Learn-PyTest)  src : mkdir apps/SeleniumApp
(Learn-PyTest)  src : ./manage.py startapp SeleniumApp apps/SeleniumApp
```

Download `chromedriver` as per your browser version.

Put `chromedriver` inside project and let the instance refer to its location in project. Or include its location in environment PATH for discovery without explict declaration. Server need not to be in running state to check these selenium tests.

```python
import pytest
from django.test import LiveServerTestCase
from selenium import webdriver


class AdminTest(LiveServerTestCase):
    def test_admin_page(self):
        # locate the chromedriver (relative to root/manage.py of project )
        driver = webdriver.Chrome('./chromedriver')
        # get the page via url provided
        driver.get(f"{self.live_server_url}/admin/")
        # check if 'Log in | Django site admin' is present in page title
        assert  "Log in | Django site admin" in driver.title

```

Another way to do the same without opening a browser window is to use `headless` flag.

```python
import pytest
from django.test import LiveServerTestCase
from selenium import webdriver


class BrowserTest(LiveServerTestCase):
    def test_headless(self):
        options = webdriver.ChromeOptions()
        options.headless = True
        driver = webdriver.Chrome(
            executable_path=r"./chromedriver",
            options=options
        )
        driver.get(f"{self.live_server_url}/admin/")
        assert "Log in | Django site admin" in driver.title
```

Now we can move this chromedriver init code to a fixture with class scope that is it will run one time for each class. How many test method we may call inside that class.

```python
import pytest
from selenium import webdriver


@pytest.fixture(scope="class")
def chrome_driver_init(request):

    options = webdriver.ChromeOptions()
    options.headless = True
    chrome_driver = webdriver.Chrome(
        executable_path="./chromedriver",
        options=options
    )
    request.cls.driver = chrome_driver
    yield 
    chrome_driver.close()
```

Note in below code we access driver using `self` and not directly.

```bash
import pytest
from django.test import LiveServerTestCase


@pytest.mark.usefixtures("chrome_driver_init")
class BrowserTest(LiveServerTestCase):
    def test_admin_page(self):
        # the driver we access using self is headless already
        # conftest.py file run before any test hence update the 
        # driver attribute of class 
        self.driver.get(f"{self.live_server_url}/admin/")
        assert "Log in | Django site admin" in self.driver.title
```

Also we can make a generic fixture for chrome and firefox both. This will check the web page for both the browsers.

```python
# conftest.py

# a more generic fixture can be used for both chrome as well firefox
@pytest.fixture(params=["chrome", "firefox"], scope="class")
def driver_init(request):
    if request.param == "chrome":
        options = webdriver.ChromeOptions()
        options.headless = True
        web_driver = webdriver.Chrome(
            executable_path="./chromedriver",
            options=options
        )
    if request.param == "firefox":
        options = webdriver.FirefoxOptions()
        options.headless = True
        web_driver = webdriver.Firefox(
            executable_path="./geckodriver",
            options=options
        )
    request.cls.driver = web_driver
    yield 
    web_driver.close()
```

```python
# test_4.py
import pytest


@pytest.mark.usefixtures("driver_init")
class TestAdminPage:
    # instead of live_server_url from django test class we use
    # live_server from webdriver 
    def test_admin_page(self, live_server):
        self.driver.get(f"{live_server.url}/admin/")
        assert "Log in | Django site admin" in self.driver.title
```

See the test getting passed in both the browser conditions.

```bash
collected 2 items                                 

apps/SeleniumApp/Test/test_4.py::TestAdminPage::test_admin_page[chrome] PASSED [ 50%]
apps/SeleniumApp/Test/test_4.py::TestAdminPage::test_admin_page[firefox] PASSED [100%]
```

## Take screenshot with selenium while testing

```python
# fixture to run for each type of ss
@pytest.fixture(params=["chrome1980", "chrome411", "firefox"], scope="class")
def driver_init_screenshot(request):
    if request.param == "chrome1980":
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument("--window-size=1920,1080")
        web_driver = webdriver.Chrome(
            executable_path="./chromedriver",
            options=options
        )
        request.cls.browser = "Chrome1920x1080"
    if request.param == "chrome411":
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument("--window-size=411,823")
        web_driver = webdriver.Chrome(
            executable_path="./chromedriver",
            options=options
        )
        request.cls.browser = "Chrome411x823"
    if request.param == "firefox":
        options = webdriver.FirefoxOptions()
        options.headless = True
        web_driver = webdriver.Firefox(
            executable_path="./geckodriver",
            options=options
        )
        request.cls.browser = "Firefox"

    request.cls.driver = web_driver
    yield 
    web_driver.close()
```

```python
import os
import pytest


def take_screenshot(driver, name):
    # first make the required dir
    os.makedirs(
        os.path.join("screenshot",  # path where to make directory
        os.path.dirname(name)       # name of new dir
        ),
        exist_ok=True               # no error if already exists
    )
    # now save the image to given dir with given name
    driver.save_screenshot(
        # fullname of path where to save ss
        os.path.join("screenshot", name)
    )


@pytest.mark.usefixtures("driver_init_screenshot")
class TestScreenshot:
    def test_screenshot_admin(self, live_server):
        self.driver.get(f"{live_server.url}/admin/")
        take_screenshot(self.driver, "admin/" +
                        "admin_" + self.browser + ".png")
        assert "Log in | Django site admin" in self.driver.title
```

Saving screenshot for three different type

```bash
apps/SeleniumApp/Test/test_5.py::TestScreenshot::test_screenshot_admin[chrome1980] PASSED [ 33%]
apps/SeleniumApp/Test/test_5.py::TestScreenshot::test_screenshot_admin[chrome411] PASSED [ 66%]
apps/SeleniumApp/Test/test_5.py::TestScreenshot::test_screenshot_admin[firefox] PASSED [100%]
```

## Payment: Unit, Integration and End-to-End testing

### Benefits and point to remember

- Have fast enough tests for both efficient code-and-test flows for developers and for CI/CD pipelines.
- Have comprehensive enough tests to isolate what breaks in the piece of code and what breaks in external/internal code the code we are testing depends on.
- Leave a clear set of useful tools to pinpoint relevant individual or multiple tests resulting in a rocket-fast workflow for the developer.

### How to structure tests

```bash
...
├── tests
│   ├── __init__.py
│   ├── test_app1
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── factories.py
│   │   ├── e2e_tests.py
│   │   ├── test_models.py
│   │   ├── test_signals.py
│   │   ├── test_serializers.py
│   │   ├── test_utils.py
│   │   ├── test_views.py
│   │   └── test_urls.py
│   │
│   └── ...
└── ...
```

### PyTest Settings

PyTest settings configurations can be set in `pytest.ini` files under `[pytest]` or in `setup.cfg` files under `[tool:pytest]`:

```bash
:in pytest.ini
[pytest]
DJANGO_SETTINGS_MODULE = MyProject.settings
markers = slow: slow running test
python_files = tests.py test_*.py *_tests.py
addopts = --cov=apps/ --cov-report html

:in setup.cfg
[tool:pytest]
DJANGO_SETTINGS_MODULE = MyProject.settings
markers = slow: slow running test
python_files = tests.py test_*.py *_tests.py
addopts = --cov=apps/ --cov-report html

[coverage:run]
omit = */migrations/*, 
        tests/*, 
        */test.py, 
        */__init__.py
```

From now we are using `setup.cfg` and not `pytest.ini`. As `pytest.ini` only usefull for pytest while `setup.cfg` is usefull for various types of plugins.

- `DJANGO_SETTINGS_MODULE`: indicates where in the working dir are the settings located.
- `python_files`: indicates the patterns pytest will use to match test files.
- `addopts`: indicates the command line arguments pytest should run with whenever we run pytest .
- `markers`: here we define the markers we and our team may later agree to use for categorizing tests (i.e: "unit", "integration", "e2e", "regression", etc.).

**Note**: Mind the `,` after each omit argument

### Types of Tests

- `Unit Tests`: test of a relevant piece of code isolated (mostly by mocking external code to the code tested) from interactions with other units of code. Be it internal code like a helper function we made to clean the code, a call to the database or a call to an external API.
- `Integration Tests`: tests that test a piece of code without isolating them from interactions with other units.
- `E2E Tests`: e2e stands for “end to end”, this tests are integration tests that test the end to end flows of the Django app we are testing.
- `Regression Tests`: a kind of test that, be it integration or unit, was originated by a bug that was covered right after fixing it by a test to expect it in the future.

### A Proper Test Flow

There are two main code testing flows for testing developers:

- `TDD (Test Driven Development)`: making tests before asserting them through code.
- `Testing after developing`: testing the piece of code right after creating it.

But I’ll recommend a mix of them:

- `Make end-to-end tests`: this should be the TDD component of our final test-suite. This tests will help you first and foremost to layout beforehand what each endpoint should return, and to have a preliminary vission of how the rest of the code of your app should follow.
- `Create Unit Tests`: write code and create the isolated tests for each of the parts of the Django app. This will not only help the developer through the development process but will also be extremely helpful to pinpoint where the problem is happening.

The only `integration tests` in our test suite should be the e2e ones. This tests should not be part of our team's testing flow while developing and, given integration tests take time, this should not even form part of the CI/CD pipeline we set up.

### What should I test in my unit tests?

Models should only be used for data representation. The logic we may need for a model should be stored in either signals or model managers. Thus we don't test models in unit testing.

Since we are avoiding database access for our main tests, we'll leave the job of making sure we built our models correctly to the e2e tests.

Thus a unit test could be of a:

- Model (model methods/model managers)
- Signal
- Serializer
- Helper Object a.k.a "utils" (functions, classes, method, etc.)
- View/Viewset
- URL Configuration

## Common Testing Utilities

### Markers

Markers are just decorators with the format `@pytest.mark.<marker>` we set wrapping our test functions.

- `@pytest.mark.parametrize()`: this marker will be used to run the same test several times with different values, working as a for loop.
- `@pytest.mark.django_db`: if we don’t give a test access to the db, it will by default not be able to access the db.

### Mocking

When making unit tests, we will want to mock access to external APIs, to the db and to internal code. That’s where the following libraries will be helpful:

- `pytest-mock`: to provide `unittest.mock` objects like a mock object and a non invasive patch function through the mocker fixture.
- `requests-mock` : to provide a requests factory through the `rf` fixture and also the ability to mock requests objects.
- `django-mock-queries`: provides the ability to mock a queryset object and fill it with non persistend object instances.

### PyTest Commands

- `-k <expression>`: matches a file, class or function name inside the tests folder that contains the indicated expression. Below test run only `test_6.py` from MyApp.

  ```bash
  pytest -k 'create1'
  ```

- `-m <marker>`: will run all tests with the inputed marker.

- `-m "not <marker>"`: will run all tests that don’t have the inputed marker.

  ```bash
  pytest -m "slow"
  pytest -m "not slow"
  ```

- `-x`: stops running tests suit as soon one test fails.

- `--lf`: starts running the test suite from the last failed test, perfect to avoid continiously running tests we already know pass when debuggin.

- `-vv`: shows a more detailed version of a failed assertion.

- `--cov`: show % of tests covered by tests (depends on `pytest-cov` plugin).

- `--reruns <num_of_reruns>`: used for dealing with flaky tests, tests that fail when run in the test suite but pass when run alone.

#### Coverage

The complete list of command line options is:

`--cov=PATH`
Measure coverage for filesystem path. (multi-allowed)

`--cov-report=type`
Type of report to generate: term, term-missing, annotate, html, xml (multi-allowed). term, term- missing may be followed by `:skip-covered`. annotate, html and xml may be followed by `:DEST` where DEST specifies the output location. Use `–cov-report=` to not generate any output.

`--cov-config=path`
Config file for coverage. Default: .coveragerc

`--no-cov-on-fail`
Do not report coverage if test run fails. Default: False

`--no-cov`
Disable coverage report completely (useful for debuggers). Default: False

`--cov-fail-under=MIN`
Fail if the total coverage is less than MIN.

`--cov-append`
Do not delete coverage but append to current. Default: False

`--cov-branch`
Enable branch coverage.

`--cov-context`
Choose the method for setting the dynamic context.

### Addopts

Addopts are PyTest commands that will want to run every time we run the `pytest` command so we don't have to input it every time.

```conf
DJANGO_SETTINGS_MODULE = ...
markers = ...
python_files = ...
addopts = -vv -x --lf --cov
```

### Pinpoint Tests

If we want to instead run a set of tests with something in common, we can run pytest using the `-k` command to select all `test_*.py` files, all `Test*` classes or all `test_*` functions with the inserted expression.
A good way to group tests, is to set custom markers in our `pytest.ini/setup.cfg`file and share the markers across our team.

```conf
[tool:pytest]
markers =
    # Define our new marker
    unit: tests that are isolated from the db, external api calls and other mockable internal code.
```

we can mark it like this:

```python
import pytest

@pytest.mark.unit
def test_something(self):
    pass
```

we can avoid the tediousity of making a marker for each function by setting a global marker for all the file by declaring the pytestmark variable in the top of the file right after the imports, which will contain a singular pytest marker or a list of markers:

```python
# (imports)

# Only one global marker (most commonly used)
pytestmark = pytest.mark.unit
# Several global markers
pytestmark = [pytest.mark.unit, pytest.mark.other_criteria]

# (tests)
```

If we want to go further and set a global marker for all the tests, pytest creates a fixtures called items that represents all PyTest test objects inside the containing directory. marker `all` here

```conf
# in conftest.py
def pytest_collection_modifyitems(items):
    for item in items:
        item.add_marker('all')
```

### Factories

Factories are pre-filled model instances. Instead of manually making model instances by hand, factories will do the work for us. The main modules for creating factories are `factory_boy` and `model_bakery`.

Instances that are saved into the db are called `persistent instances` in contrast with `non persistent`, which are the ones we will use to mock the response of database calls.

```python
from model_bakery import baker

from apps.my_app.models import MyModel

# create and save to the database
baker.make(MyModel) # --> One instance
baker.make(MyModel, _quantity=3) # --> Batch of 3 instances

# create and don't save
baker.prepare(MyModel) # --> One instance
baker.prepare(MyModel, _quantity=3) # --> Batch of 3 instances
```

If we want to have other than random data we can write factories with `factory_boy` and `faker` in the following way:

```python
# factories.py
import factory
from faker import Faker
fake = Faker()
from apps.Payment.models import Currency


class CurrencyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Currency
    name, code = fake.currency()

CurrencyFactory()

# Save to db
CurrencyFactory() # --> One instance
CurrencyFactory.create_batch(3) # --> Batch of 3 instances

# Do not save to db
CurrencyFactory.build() # --> One instance
CurrencyFactory.build_batch() # --> Batch of 3 instances
```

### How to Organize a Test

- `Arrange`: set everything needed for the test
- `Mock`: mock everything needed to isolate your test
- `Act`: trigger your code unit.
- `Assert`: assert the outcome is exactly as expected to avoid any unpleasant surprises later.

### Test Examples

And inside `tests/test_app/conftest.py` we'll set our factories as fixtures to later access them as a param in our test functions.

### E2E Tests

Once we already have our models and their factories created go for end to end tests.

```text
GET     api/transactions        List all transaction objects
POST    api/transactions        Create a transaction object
GET     api/transactions        Retrieve a transaction object
PUT     api/transactions/hash   Update a transaction object
PATCH   api/transactions/hash   Update a field of a transaction object
DELETE  api/transactions/hash   Delete a transaction object  
```

Lets make a DRF API client as a fixture for later use.

```python
# in root level tests/conftest.py

@pytest.fixture
def api_client():
    return APIClient
```

Now write End to End test as in **test_E2E.py** then we can proceed with building the rest of the app from the models up. First create the models and then the factory to access them.

```python
import factory

from apps.Payment.models import Transaction, Currency
from faker import Faker
fake = Faker()


class CurrencyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Currency
        # this make sure that if a repeated value is 
        # passed in these two fields then same obj is returned
        # without causing any duplicacy error

        # django_get_or_create = ('name', 'code')


    # code and name get assigned when the class is called hence if we use
    # create_batch(n) we get all n object same
 
    # code, name = fake.currency() 

    code = factory.LazyAttribute(lambda _: fake.currency()[0]) 
    name = factory.LazyAttribute(lambda _: fake.currency()[1]) 
    symbol = '$'


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transaction
    
    # if we do not assign these attributes here then they will remain blank
    
    # currency is auto generated on creation of transaction
    currency = factory.SubFactory(CurrencyFactory)
    payment_intent_id = None
    email = factory.LazyAttribute(lambda _: fake.email())
    name = factory.LazyAttribute(lambda _: fake.name())
```

- In `TransactionFactory` we assign all possible fields with fake data those who are left will have blank or null value.

- In `CurrencyFactory` since we need to create multiple `Currency` object using `create_batch()` we can not assign a value which is constant to any of the field since that will be same each time we call `CurrencyFactory` as hence will produce `UNIQUE CONSTRAINT FAIL`. Also we can use `LazyAttribute` to assign some fields when other are already assigned and argument of `lambda` is the object which is going to be saved.

### Utils

To understand it better we need to know `mock` and `patch`.

- [Medium Blog for patch](https://medium.com/@durgaswaroop/writing-better-tests-in-python-with-pytest-mock-part-2-92b828e1453c)
- [Patching, Mock and Dependency Injection](https://levelup.gitconnected.com/unit-testing-in-python-mocking-patching-and-dependency-injection-301280db2fed)

Utils are helper functions that will be spreaded all along our code. Like one field we can fill on the backend is the `payment_intent_id` field

The first util we are going to make, is a `fill_transaction` function that , given an `Transaction` model's instance, will fill the fields that are not intended to be filled by the user.

```python
import string
import random


class Stripe:
    # to represent a call to strip API
    @staticmethod
    def create(length):
        chars = string.ascii_letters + string.digits
        return ''.join(random.choices(chars, k=length))


def fill_transaction(transaction):
    # get a transaction id before making an transaction
    payment_intent_id = Stripe.create(6)

    # get the queryset of all those transaction with this id
    t = transaction.__class__.objects.filter(id=transaction.id)

    # We use update not to trigger a save-signal recursion Overflow
    t.update(
        payment_intent_id=payment_intent_id,
    )
```

In conftest.py of Payment tests

```python
import pytest

@pytest.fixture
def get_payment_id():
    return "tnMMv6"
```

A test for this util should mock the API call and the 2 db calls:

```python
from .factory import TransactionFactory
from apps.Payment.utils import Stripe
from apps.Payment.models import Transaction
from apps.Payment.utils import fill_transaction


class TestUtilFunctions:

    def test_fill_transaction(self, mocker, get_payment_id):

        transaction = TransactionFactory.build()
        strip_intent_id = get_payment_id

        # mocking API call
        payment_intent_mock = mocker.Mock(return_value=strip_intent_id)
        Stripe.create = payment_intent_mock

        # mocking DB calls
        filter_call_mock = mocker.Mock()
        Transaction.objects.filter = filter_call_mock
        update_call_mock = mocker.Mock()
        filter_call_mock.return_value.update = update_call_mock

        # call the function to be tested
        fill_transaction(transaction)

        filter_call_mock.assert_called_with(id=transaction.id)
        update_call_mock.assert_called_with(
            payment_intent_id=strip_intent_id
        )
```

### Signals

Write a signal to fill some field in model post save.

```python
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.Payment.models import Transaction
from apps.Payment.utils import fill_transaction


@receiver(post_save, sender=Transaction)
def transaction_filler(sender, instance, created, *args, **kwargs):
    ''' fill 'payment_intent_id' field in a transacton before saving '''

    if created:
        fill_transaction(instance)
```

This signal update the `payment_intent_id` field on payment model. Lets try to test this signal. We will send a `post_save` signal with a instance which is not yet saved in DB and hence the signal calls `fill_transaction`.

```python
import pytest

from django.db.models.signals import post_save

from apps.Payment.models import Transaction
from tests.Payment.factory import TransactionFactory


pytestmark = pytest.mark.unit

class TestTransactionFiller:

    def test_post_save(self, mocker):
        instance = TransactionFactory.build()
        mock = mocker.patch(
            'apps.Payment.signals.fill_transaction'
        )

        post_save.send(Transaction, instance=instance, created=True)
        mock.assert_called_with(instance)
```

Some points about `mocker`:

1. When we do the patch, we create a new mocked function that gets called, bypassing the original function. Thus original `fill_transaction` function do not get called instead a mock `fill_transaction` is called.
2. We mocked `fill_transaction` in `signal.py` file where it is used and not the file from where it is imported.

### Serializers
