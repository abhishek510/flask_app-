import unittest
from myapp import *
import requests


class testClass(unittest.TestCase):
    def test_getstatus(self):
        headers = {'accept': 'application/json', 'Content-type:application/json'}
        data = '{"number":10}'
        response = requests.post('http://127.0.0.1:5000/calculate_factorial', headers=headers, data=data)
        self.assertEqual(response, 'SUCCESS')

    def test_getstatus_not_found(self):
        status = Getstatus.get(self, 'taskid-not-present')
        self.assertEqual(status, 'Not Found')


if __name__ == '__main__':
    unittest.main()
