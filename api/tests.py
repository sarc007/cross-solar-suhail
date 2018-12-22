from rest_framework.test import APITestCase,APIClient
from rest_framework import status
from rest_framework.exceptions import ValidationError
from .models import Panel, OneHourElectricity
from django.db.utils import IntegrityError
from .serializers import PanelSerializer, OneHourElectricitySerializer





class PanelTestCase(APITestCase):
    def setUp(self):
        """ Setting up initial data and variables to be used"""
        self.client = APIClient()
        self.uri = '/panel/'
        Panel.objects.create(brand="Areva", serial="AAAA1111BBBB2222", latitude=12.345678, longitude=98.765543)

    def test_model_Panel_str(self):
        panel_str = Panel.objects.create(brand="Areva", serial="ZZZZ1111BBBB2222", latitude=12.345678, longitude=98.765543)
        self.assertEqual(Panel.__str__(panel_str), "Brand: Areva, Serial: ZZZZ1111BBBB2222")

    def test_panel_listing(self):
        """ Testing the panel listing"""
        response = self.client.get(self.uri, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_panel_get(self):
        """Testing the get functionality for the specific panel"""
        response = self.client.get(self.uri+'1/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([response.data["serial"], response.data["brand"],
                          response.data["latitude"], response.data["longitude"]],
                         ["AAAA1111BBBB2222", "Areva", "12.345678", "98.765543"])

    def test_panel_partial_update_fail(self):
        """ Patching is not allowed hence testing the update fail confirmation """
        params = {
            "id" : 1,
            "brand": "BMW",
            "serial": "DMWHHBBJJDDTTM11",
            "latitude": 19.689385,
            "longitude": 148.356699
        }
        response = self.client.patch(self.uri, params)
        self.assertEqual(response.status_code, 405,
                         'Expected Response Code 405, received {0} instead.'
                         .format(response.status_code))

    def test_panel_post_fail(self):
        """ Post fails with wrong data, testing the post fail confirmation"""
        params = {
            "brand": "BMW",
            "serial": "WHHBBJJDDTTM11",
            "latitude": 19.689385,
            "longitude": 148.356699
        }
        response = self.client.post(self.uri, params)
        self.assertEqual(response.status_code, 400,
                         'Expected Response Code 400, received {0} instead.'
                         .format(response.status_code))


    def test_panel_put(self):
        """ Testing the put functionality on a specific panel"""
        params = {
            "id": 1,
            "brand": "BMW",
            "serial": "BMWHHBBJJDDTTM11",
            "latitude": 19.689385,
            "longitude": 1.356699
        }
        response = self.client.put(self.uri+'1/', params)
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, received {0} instead.'
                         .format(response.status_code))

    def test_panel_brand_serial_unique(self):
        """ Checking the uniqueness in combination of brand and serial
        as there cannot be 2 of same serial and brand"""
        with self.assertRaises(Exception) as raised:
            Panel.objects.create(brand="Areva", serial="AAAA1111BBBB2222", latitude=12.345678, longitude=98.765543)
        self.assertEqual(IntegrityError, type(raised.exception))

    def test_panel_validate_serial_multiple(self):
        """
        I had to use this method as paramterized decorator
         of pytest does not work with functions under a class

        Check - length greater than 16 and length less than 16 for serial
         """
        test_expected = {}
        test_raised_exception = {}
        serial_values = [[1, "AAAA1111BBBB22222", ValidationError], [2, "AAAA1111BBBB22222", ValidationError]]

        def test_panel_validate_serial(value):
            with self.assertRaises(Exception) as raised:
                PanelSerializer.validate_serial(PanelSerializer, value)
            return type(raised.exception)

        for key_value, value, expected in serial_values:
            test_raised_exception.update({key_value: test_panel_validate_serial(value)})
            test_expected.update({key_value: expected})

        self.assertDictEqual(test_expected, test_raised_exception)

    def test_panel_validate_latitude_multiple(self):
        """
        I had to use this method as paramterized decorator
         of pytest does not work with functions under a class

        Check -
        latitude is between 90 to - 90 assertion of failure if more than 90
        latitude is between 90 to - 90 assertion of failure if less than - 90
        latitude decimal values length more than 6 assertion is failure


         """
        test_expected = {}
        test_raised_exception = {}
        latitude_values = [[1, 127.368988, ValidationError],
                           [2, -90.01, ValidationError],
                           [3, 90.01, ValidationError],
                           [4, -127.368988, ValidationError],
                           [5, 45.8988664317, ValidationError]]

        def test_panel_validate_latitude(value):
            with self.assertRaises(Exception) as raised:
                PanelSerializer.validate_latitude(PanelSerializer, value)
            return type(raised.exception)

        for key_value, value, expected in latitude_values:
            test_raised_exception.update({key_value: test_panel_validate_latitude(value)})
            test_expected.update({key_value: expected})

        self.assertDictEqual(test_expected, test_raised_exception)

    def test_panel_validate_longitude_multiple(self):
        """
        I had to use this method as paramterized decorator
         of pytest does not work with functions under a class

        Check -
        longitude is between 180 to - 180 assertion of failure if more than 180
        longitude is between 180 to - 180 assertion of failure if less than - 180
        longitude decimal values length more than 6 assertion is failure


         """
        test_expected = {}
        test_raised_exception = {}
        longitude_values = [[1, 197.368988, ValidationError],
                            [2, -180.01, ValidationError],
                            [3, 180.01, ValidationError],
                            [4, -197.368988, ValidationError],
                            [5, 45.8988664317, ValidationError]]

        def test_panel_validate_longitude(value):
            with self.assertRaises(Exception) as raised:
                PanelSerializer.validate_latitude(PanelSerializer, value)
            return type(raised.exception)

        for key_value, value, expected in longitude_values:
            test_raised_exception.update({key_value: test_panel_validate_longitude(value)})
            test_expected.update({key_value: expected})

        self.assertDictEqual(test_expected, test_raised_exception)

    def test_panel_del(self):
        """ Checking panel deletion functionality for a specific panel"""
        params = {
            "id": 1
        }
        response = self.client.delete(self.uri+'1/', params)
        self.assertEqual(response.status_code, 204,
                         'Expected Response Code 204, received {0} instead.'
                         .format(response.status_code))

    def test_panel_get_invalid_id(self):
        """ Checking the get functionality for invalid panel """
        response = self.client.get(self.uri+'10/', format='json')
        self.assertEqual(response.status_code, 404,
                         'Expected Response Code 404, received {0} instead.'
                         .format(response.status_code))

class OneHourTestCase(APITestCase):
    def setUp(self):
        """ Set up of initial data and variables """
        self.client = APIClient()
        self.uri = '/panel/1/analytics/'
        Panel.objects.create(brand="BMW", serial="AAAA1111BBBB2222", latitude=12.345678, longitude=98.765543)
        OneHourElectricity.objects.create(panel_id=1, kilo_watt=1.2, date_time="2018-10-24T07:00:00Z")
        OneHourElectricity.objects.create(panel_id=1, kilo_watt=1.4, date_time="2018-10-24T08:00:00Z")
        OneHourElectricity.objects.create(panel_id=1, kilo_watt=1.6, date_time="2018-10-24T09:00:00Z")

    def test_model_OneHourElectricity_str(self):
        onehourelectricity_str = OneHourElectricity.objects.create(panel_id=1, kilo_watt=1.2,
                                                                   date_time="2018-10-24T07:00:00Z")
        self.assertEqual(OneHourElectricity.__str__(onehourelectricity_str),
                         "Hour: 2018-10-24T07:00:00Z - 1.2 KiloWatt")

    def test_OneHourElectricity_listing(self):
        """ Checking the listing functionality of 'One Hour Electricity Listing' """
        response = self.client.get(self.uri, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_HourAnalyticsView_post(self):
        """ Checking the post functionality of post"""
        params = {
            "panel": 1,
            "kilo_watt": 1.2,
            "date_time": "2018-12-01T09:00:00Z"
        }
        response = self.client.post(self.uri, params, format='json')
        self.assertEqual(response.status_code, 201,
                         'Expected Response Code 201, received {0} instead.'
                         .format(response.status_code))

    def test_HourAnalyticsView_post_fail(self):
        """ Checking the confirmation of post failing"""
        params = {
            "panel": 1,
            "kilo_watt": 1.2,
            "date_time": "2018-12-01T09:01:00Z"
        }
        response = self.client.post(self.uri, params, format='json')
        self.assertEqual(response.status_code, 400,
                         'Expected Response Code 400, received {0} instead.'
                         .format(response.status_code))


    def test_OneHourElectricity_panel_date_time_unique(self):
        """ Checking the uniqueness of panel and the hourly date """
        with self.assertRaises(Exception) as raised:
            OneHourElectricity.objects.create(panel_id=1, date_time="2018-10-24T09:00:00Z")
        self.assertEqual(IntegrityError, type(raised.exception))

    def test_OneHourElectricitySerializer_validate_kilo_watt(self):
        """ Checking the value of kilo watts if negative raises an exception """
        with self.assertRaises(Exception) as raised:
            OneHourElectricitySerializer.validate_kilo_watt(OneHourElectricitySerializer, -0.01)
        self.assertEqual(ValidationError, type(raised.exception))

    def test_OneHourElectricitySerializer_validate_date_time_multiple(self):
        """
                I had to use this method as paramterized decorator
                 of pytest does not work with functions under a class

                Check -
                Date time values are hourly and not in additional minutes
                Date time values are hourly and not in additional seconds
                Date time values are not greater than current datetime
                 """
        test_expected = {}
        test_raised_exception = {}
        date_time_values = [[1, "2018-10-24T11:01:00Z", ValidationError],
                            [2, "2018-10-24T11:00:01Z", ValidationError],
                            [3, "2025-10-24T11:00:00Z", ValidationError],
                            [4, "2020-10-24T08:00:00Z", ValidationError]]

        def test_OneHourElectricity_validate_date_time(value):
            with self.assertRaises(Exception) as raised:
                OneHourElectricitySerializer.validate_date_time(OneHourElectricitySerializer, value)
            return type(raised.exception)

        for key_value, value, expected in date_time_values:
            test_raised_exception.update({key_value: test_OneHourElectricity_validate_date_time(value)})
            test_expected.update({key_value: expected})

        self.assertDictEqual(test_expected, test_raised_exception)

    def test_OneHourElectricity_del_fail(self):
        """ delete method is not allowed hence testing the confirmation"""
        params = {
            "id": 1
        }
        response = self.client.delete(self.uri, params)
        self.assertEqual(response.status_code, 405,
                         'Expected Response Code 405, received {0} instead.'
                         .format(response.status_code))


class OneHourDayTestCase(APITestCase):
    def setUp(self):
        """ Setting up initial data and variable """
        self.client = APIClient()
        self.uri = '/panel/1/analytics/day/'
        Panel.objects.create(brand="Areva", serial="AAAA1111BBBB2222", latitude=12.345678, longitude=98.765543)
        OneHourElectricity.objects.create(panel_id=1, kilo_watt=1.2, date_time="2018-10-24T07:00:00Z")
        OneHourElectricity.objects.create(panel_id=1, kilo_watt=1.4, date_time="2018-10-24T08:00:00Z")
        OneHourElectricity.objects.create(panel_id=1, kilo_watt=1.6, date_time="2018-10-24T09:00:00Z")

        OneHourElectricity.objects.create(panel_id=1, kilo_watt=1.2, date_time="2018-10-20T07:00:00Z")
        OneHourElectricity.objects.create(panel_id=1, kilo_watt=1.4, date_time="2018-10-20T08:00:00Z")
        OneHourElectricity.objects.create(panel_id=1, kilo_watt=1.6, date_time="2018-10-20T09:00:00Z")

    def test_OneHourDayElectricity_listing(self):
        """ Checking the values are returned """
        response = self.client.get(self.uri, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)








