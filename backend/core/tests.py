from django.test import Client, TestCase
from rest_framework.authtoken.models import Token

from core.models import User

# Create your tests here.


class LoginTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@example.com", "rightpassword")

    def test_login_with_correct_credentials(self):
        client = Client()
        login_response = client.post(
            "/api/login/", {"username": "testuser", "password": "rightpassword"}, "application/json"
        )
        self.assertEqual(login_response.status_code, 200)
        self.assertIn("token", login_response.json())
        self.assertEqual(login_response.json()["token"], Token.objects.get(user=self.user).key)

    def test_login_with_incorrect_credentials(self):
        client = Client()
        failed_login_response = client.post(
            "/api/login/", {"username": "testuser", "password": "wrongpassword"}, "application/json"
        )
        self.assertEqual(failed_login_response.status_code, 400)
        self.assertNotIn("token", failed_login_response.json())


class RegisterTestCase(TestCase):
    def setUp(self):
        User.objects.create_user("existing")

    def test_registration(self):
        c = Client()
        registration_response = c.post(
            "/api/register/",
            {
                "username": "IvanIvanov",
                "password": "ivanspassword",
                "first_name": "Иван",
                "patronymic": "Иванович",
                "last_name": "Иванов",
            },
            "application/json",
        )
        self.assertEqual(registration_response.status_code, 201)
        registration_json = registration_response.json()
        self.assertEqual(registration_json["first_name"], "Иван")
        self.assertEqual(registration_json["patronymic"], "Иванович")
        self.assertEqual(registration_json["last_name"], "Иванов")
        self.assertIn("token", registration_json)

        login_response = c.post(
            "/api/login/", {"username": "IvanIvanov", "password": "ivanspassword"}, "application/json"
        )
        self.assertEqual(login_response.json()["token"], registration_json["token"])

    def test_registration_with_existing_username(self):
        c = Client()
        response = c.post(
            "/api/register/",
            {
                "username": "existing",
                "password": "somepassword",
                "first_name": "Иван",
                "patronymic": "Иванович",
                "last_name": "Иванов",
            },
            "application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("username", response.json())

    def test_registration_with_invalid_username(self):
        c = Client()
        response = c.post(
            "/api/register/",
            {
                "username": "~!@#",
                "password": "somepassword",
                "first_name": "Иван",
                "patronymic": "Иванович",
                "last_name": "Иванов",
            },
            "application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("username", response.json())

    def test_registration_without_first_name(self):
        c = Client()
        response = c.post(
            "/api/register/",
            {"username": "p.petrov", "password": "petrovspassword", "patronymic": "Петрович", "last_name": "Петров"},
            "application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("first_name", response.json())

    def test_registration_without_last_name(self):
        c = Client()
        response = c.post(
            "/api/register/",
            {
                "username": "a.alekseev",
                "password": "alekseevspassword",
                "first_name": "Алексей",
                "patronymic": "Алексеевич",
            },
            "application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("last_name", response.json())

    def test_registration_without_patronymic(self):
        c = Client()
        registration_response = c.post(
            "/api/register/",
            {"username": "johnjohnson", "password": "johnspassword", "first_name": "Джон", "last_name": "Джонсон"},
            "application/json",
        )
        self.assertEqual(registration_response.status_code, 201)
        registration_json = registration_response.json()
        self.assertEqual(registration_json["first_name"], "Джон")
        self.assertEqual(registration_json["patronymic"], "")
        self.assertEqual(registration_json["last_name"], "Джонсон")
        self.assertIn("token", registration_json)

        login_response = c.post(
            "/api/login/", {"username": "johnjohnson", "password": "johnspassword"}, "application/json"
        )
        self.assertEqual(login_response.json()["token"], registration_json["token"])

    def test_registration_with_short_password(self):
        c = Client()
        response = c.post(
            "/api/register/",
            {
                "username": "Nikolai1940",
                "password": "short",
                "first_name": "Николай",
                "patronymic": "Николаевич",
                "last_name": "Николаев",
            },
            "application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("password", response.json())

    def test_registration_with_numeric_password(self):
        c = Client()
        response = c.post(
            "/api/register/",
            {
                "username": "lvov",
                "password": "31415926535",
                "first_name": "Лев",
                "patronymic": "Львович",
                "last_name": "Львов",
            },
            "application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("password", response.json())


# class EmployeeTestCase(TestCase):
#
#     def test_get_employee_with_valid_fullname(self):
#         c = Client()
#         response = c.get(
#             "/api/employee/",
#             {
#                 "full_name": "7e4f5484 7e4f54bf 7e4f54cb",
#             },
#             "application/json",
#         )
#
#         self.assertEqual(response.status_code, 200)
