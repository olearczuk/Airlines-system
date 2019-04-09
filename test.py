import json
from datetime import datetime, timedelta
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from system.flights.models import Flight, Airplane, Crew, Airport


class ApiTest(TestCase):
    date = datetime.strptime('2018-12-22', '%Y-%m-%d').astimezone(timezone.utc)

    def setUp(self):
        start_airport = Airport.objects.create(city='Warsaw', country='Poland')
        final_airport = Airport.objects.create(city='Cracow', country='Poland')
        user = User.objects.create(username="username")
        user.set_password("password")
        user.save()
        for i in range(3):
            airplane = Airplane.objects.create(official_number=i, capacity=3)
            crew = Crew.objects.create(captainsName='Name{}'.format(i), captainsSurname='Surname{}'.format(i))
            Flight.objects.create(start_airport=start_airport, final_airport=final_airport, crew=crew,
                                  airplane=airplane, departure_time=self.date,
                                  arrival_time=self.date + timedelta(hours=4))

    def testCrews(self):
        response = self.client.get('/api/crew/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'[{"captainsName":"Name0","captainsSurname":"Surname0","id":1},' +
                                           b'{"captainsName":"Name1","captainsSurname":"Surname1","id":2},' +
                                           b'{"captainsName":"Name2","captainsSurname":"Surname2","id":3}]')

    def testCorretChangeCrew(self):
        client = Client()
        client.login(username="username", password="password")
        new_crew = Crew.objects.create(captainsName="testName", captainsSurname="testSurname").id
        flight_id = Flight.objects.get(airplane__official_number=0).id
        response = client.patch('/api/flights/{}/'.format(flight_id), content_type='application/json',
                                data=json.dumps({"crew": new_crew}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Flight.objects.get(id=flight_id).crew.id, new_crew)

    def testErrorChangeCrew(self):
        client = Client()
        client.login(username="username", password="password")
        flight = Flight.objects.get(airplane__official_number=0)
        new_crew = Crew.objects.last().id
        old_crew = flight.crew.id
        flight_id = flight.id
        response = client.patch('/api/flights/{}/'.format(flight_id), content_type='application/json',
                                data=json.dumps({"crew": new_crew}))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Flight.objects.get(id=flight_id).crew.id, old_crew)

    def testNoAuthChangeCrew(self):
        new_crew = Crew.objects.create(captainsName="testName", captainsSurname="testSurname").id
        flight_id = Flight.objects.get(airplane__official_number=0).id
        response = self.client.patch('/api/flights/{}/'.format(flight_id), content_type='application/json',
                                     data=json.dumps({"crew": new_crew}))
        self.assertEqual(response.status_code, 401)


class SeleniumTest(StaticLiveServerTestCase):
    date = datetime.strptime('2018-12-22', '%Y-%m-%d').astimezone(timezone.utc)

    def procedure(self, driver, crew_num, flightNum):
        # Logging in
        driver.get("{}/auth/login".format(self.live_server_url))
        # driver.find_element_by_id("login_link").click()
        driver.find_element_by_id("login_username").send_keys("username")
        driver.find_element_by_id("login_password").send_keys("password")
        driver.find_element_by_id("login_button").click()

        # Try to change crew
        select = "select{}".format(flightNum)
        button = "select_button{}".format(flightNum)
        driver.get("{}/static/crews_vue.html".format(self.live_server_url))
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, select))
        )
        Select(driver.find_element_by_id(select)).select_by_index(crew_num)
        driver.find_element_by_id(button).click()

    def test(self):
        start_airport = Airport.objects.create(city='Warsaw', country='Poland')
        final_airport = Airport.objects.create(city='Cracow', country='Poland')
        driver = WebDriver()
        for i in range(3):
            airplane = Airplane.objects.create(official_number=i, capacity=3)
            airplane.save()
            crew = Crew.objects.create(captainsName='Name{}'.format(i), captainsSurname='Surname{}'.format(i))
            crew.save()
            flight = Flight.objects.create(start_airport=start_airport, final_airport=final_airport, crew=crew,
                                           airplane=airplane, departure_time=self.date,
                                           arrival_time=self.date + timedelta(hours=4))
            flight.save()
        crew = Crew.objects.create(captainsName='NewName', captainsSurname='NewSurname')
        crew.save()
        user = User.objects.create(username="username")
        user.set_password("password")
        user.save()

        self.procedure(driver, 3, 1)

        driver1 = webdriver.Firefox()

        self.procedure(driver1, 4, 1)
