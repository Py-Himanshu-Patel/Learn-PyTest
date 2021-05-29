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

