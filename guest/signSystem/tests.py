
from django.test import TestCase
from django.contrib.auth.models import User
from .models.event import Event
from .models.guest import Guest


# Create your tests here.

class ModelsTest(TestCase):
    '''UnitTest for models(Event, Guest)
    '''
    def setUp(self) -> None:
        Event.objects.create(id=1, name='MeetingTest', limit=256, status=True,
                            address='MeetingRoomTest', start_time='2025-01-10 10:30:30')
        Guest.objects.create(id=2, realname='Jennie', phone='13597038002', email='jennie@mail.com',
                            sign=False, event_id=1)

    def tearDown(self) -> None:
        pass

    def test_event_models(self):
        '''Test for Model Event
        '''
        e = Event.objects.get(name='MeetingTest')
        self.assertEqual(e.address, 'MeetingRoomTest')
        self.assertEqual(e.limit, 256)
        self.assertTrue(e.status)

    def test_guest_models(self):
        '''Test for Model Guest'''
        g = Guest.objects.get(phone='13597038002')
        self.assertEqual(g.realname, 'Jennie')
        self.assertEqual(g.email, 'jennie@mail.com')
        self.assertFalse(g.sign)


class UserModelsTest(TestCase):
    """Test for Model User
    """
    def setUp(self):
        User.objects.create_user("test01", "test01@mail.com", "test1232456")

    def test_user(self):
        user = User.objects.get(username="test01")
        self.assertEqual(user.username, "test01")
        self.assertEqual(user.email, "test01@mail.com")


class IndexPageTest(TestCase):
    """Test URL '/index'
    """
    def test_index_page_renders_index_template(self):
        """check if response uses the corresponding index.html
        """
        response = self.client.get('/index/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


class LoginActionTest(TestCase):
    """Test login operations
    """
    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')

    def test_login_action_get_user_email(self):
        """query email by username
        """
        user = User.objects.get(username="admin")
        self.assertEqual(user.username, "admin")
        self.assertEqual(user.email, "admin@mail.com")

    def test_login_action_username_password_null(self):
        """username or password null
        """
        response = self.client.post('/login/', {'username': '', 'password': ''})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"User name or Password error", response.content)

    def test_login_action_username_password_error(self):
        """username error/ password error
        """
        response = self.client.post('/login/', {'username': 'abc', 'password': '123'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"User name or Password error", response.content)

    def test_login_action_success(self):
        """login success
        """
        response = self.client.post('/login/', data={'username': 'admin', 'password': 'admin123456'})
        self.assertEqual(response.status_code, 302)


class EventManageTest(TestCase):
    """Test for Event operations
    """
    def setUp(self):
        User.objects.create_user(
                            'admin', 'admin@mail.com', 'admin123456')
        Event.objects.create(name="Meeting11", limit=20, address='Meeting Room11',
                            status=1, start_time='2023-02-01 12:30:00')
        login_user = {'username': 'admin', 'password': 'admin123456'}
        self.client.post('/login/', data=login_user)    # login before operations

    def test_add_event_data(self):
        """add an event
        """
        event = Event.objects.get(name="Meeting11")
        self.assertEqual(event.address, "Meeting Room11")

    def test_event_mange_success(self):
        """query event list
        """
        response = self.client.post('/event_manage/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Meeting11", response.content)
        self.assertIn(b"Meeting Room11", response.content)

    def test_event_mange_search_success(self):
        """query event list by name
        """
        response = self.client.post('/search_event_name/', {"name": "Meeting11"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Meeting11", response.content)
        self.assertIn(b"Meeting Room11", response.content)


class GuestManageTest(TestCase):
    """Test Guest operations
    """
    def setUp(self):
        User.objects.create_user(
                            'admin', 'admin@mail.com', 'admin123456')
        Event.objects.create(id=1, name="Meeting11", limit=2000,
                             address='Meeting Room11', status=1, start_time='2023-01-10 13:00:30')
        Guest.objects.create(realname="frank", phone=13597039990,
                             email='frank@mail.com', sign=0, event_id=1)
        login_user = {'username': 'admin', 'password': 'admin123456'}
        self.client.post('/login/', data=login_user)    # login before operations

    def test_add_guest_data(self):
        """add a guest
        """
        guest = Guest.objects.get(realname="frank")
        self.assertEqual(guest.phone, "13597039990")
        self.assertEqual(guest.email, "frank@mail.com")
        self.assertFalse(guest.sign)

    def test_event_mange_success(self):
        """query guest list
        """
        response = self.client.post('/guest_manage/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"frank", response.content)
        self.assertIn(b"13597039990", response.content)

    def test_guest_mange_search_success(self):
        """query guest info by realname
        """
        response = self.client.post('/search_guest_name/', {"realname": "frank"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"frank", response.content)
        self.assertIn(b"13597039990", response.content)


class SignIndexActionTest(TestCase):
    """Test User Sign in operations
    """
    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
        Event.objects.create(id=1, name="Meeting11", limit=20,
                             address='Meeting Room11', status=1, start_time='2023-01-10 11:30:00')
        Event.objects.create(id=2, name="Meeting12", limit=10,
                             address='Meeting Room11', status=1, start_time='2024-06-01 12:10:00')
        Guest.objects.create(realname="frank", phone=13597039998,
                             email='alen@mail.com', sign=0, event_id=1)
        Guest.objects.create(realname="hanna", phone=13597039999,
                             email='hanna@mail.com', sign=1, event_id=2)
        login_user = {'username': 'admin', 'password': 'admin123456'}
        self.client.post('/login/', data=login_user)

    def test_sign_index_action_phone_null(self):
        """phone null
        """
        response = self.client.post('/sign_index_action/1/', {"phone": ""})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"phone error.", response.content)

    def test_sign_index_action_phone_or_event_id_error(self):
        """phone error/ event_id error
        """
        response = self.client.post('/sign_index_action/2/', {"phone": "13597039998"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"event id or phone error.", response.content)

    def test_sign_index_action_user_sign_has(self):
        """User already signed
        """
        response = self.client.post('/sign_index_action/2/', {"phone": "13597039999"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"user has sign in.", response.content)

    def test_sign_index_action_sign_success(self):
        """User sign in success
        """
        response = self.client.post('/sign_index_action/1/', {"phone": "13597039998"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"sign in success!", response.content)


"""
Excecute all tests:
python3 manage.py test

Execute tests in app signSystem
python3 manage.py test sign

Execute tests in test.py of app signSystem
python3 manage.py test sign.tests

Execute test GuestManageTest in test.py of app signSystem
python3 manage.py test sign.tests.GuestManageTest
"""