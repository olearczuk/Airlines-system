from django.test import TestCase
from .flights.models import Flight, Airplane, Crew
from django.contrib.auth.models import User
from datetime import datetime as dt, timedelta
from django.utils import timezone
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


class TestSeleniu(StaticLiveServerTestCase):
    date = dt.strptime('2018-12-22', '%Y-%m-%d').astimezone(timezone.utc)

    def test(self):
        driver = WebDriver()
        database = {'planes': [], 'flights': [], 'crews': []}
        for i in range(5):
            airplane = Airplane(capacity=6, official_number=i + 1000)
            airplane.save()
            database['planes'].append(airplane)
            crew = Crew(captainsName="Name{}".format(i + 1000), captainsSurname="Sur{}".format(i + 1000))
            crew.save()
            database['crews'].append(crew)
