# Learn-PyTest

Learning PyTest and Selenium to create unit test and other automation. Starting right from setting up pytest till its common use cases.

## Technology Used

- Python
- Django
- PyTest

## Index

1. [Intro to PyTest](#PyTest)
2. [What are Fixtures and how to use them](#states-of-fixtures-and-factories)  
  2.1 Fixtures  
  2.2 Accessing Database in Unit Test

## Resources and Credits

- [Very Academy YouTube Playlist](https://www.youtube.com/playlist?list=PLOLrQ9Pn6caw3ilqDR8_qezp76QuEOlHY)
- [PyTest Official Doc](https://docs.pytest.org/en/6.2.x/)

## Setup

- Load `.env` using `pipenv shell`. Then start django app.
- Install `pytest` as dev package. `pipenv install --dev pytest`
- Update Pipfile.lock `pipenv lock`
- Install packages in production `pipenv install --ignore-pipfile`
- Install dev packages using `pipenv install --dev`
- Install pytest for django using `pipenv install --dev pytest-django`

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

1. Arrange  - prepare everything for our test
2. Act      - state-changing action that kicks off the behavior we want to test
3. Assert   - where we look at that resulting state and check if it looks how we’d expect
4. CleanUp  - where the test clean up after execution, so other tests aren’t being accidentally influenced by it.

### Fixtures

- **Fixtures**: they are used to feed data to the tests such as databases connections, URLs or input data. Fixtures can be used at start and end of the test.
- Fixture can be defined in 4 ways.
  
  - **Function**:   Run once per test
  - **Class**:      Run once per class of test
  - **Module**:     Run once per module
  - **Session**:    Run once per session

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

### `conftest.py` - Making fixture common for several modules.

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
