from django.test import TestCase

class HelloWorldTest(TestCase):
    def test_hello(self):
        print("Hello, World!")
        self.assertEqual(1, 1)
