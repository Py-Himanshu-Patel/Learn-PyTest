# Learn-PyTest

Learning PyTest and Selenium to create unit test and other automation

## Resources

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

xfailed : expected to fail
xpassed: exceptionally pass

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

    ```bash
    (Learn-PyTest)  src : pytest -m "slow"
    ================ test session starts =================
    collected 3 items / 2 deselected / 1 selected        

    apps/MyApp/tests.py .                          [100%]

    ========== 1 passed, 2 deselected in 0.04s ===========
    ```

## States of Fixtures and Factories

1. Arrange
2. Act
3. Assert

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
