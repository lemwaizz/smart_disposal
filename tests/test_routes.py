# tests/test_routes.py

import unittest
from app import app, db
from app.models import User, WasteCollection
from datetime import datetime

class TestRoutes(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 302)  # Redirects to login when not authenticated

    def test_login(self):
        # Test login functionality
        response = self.app.post('/login', data=dict(
            username='testuser',
            password='password'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Home', response.data)

    def test_register(self):
        # Test user registration
        response = self.app.post('/register', data=dict(
            username='newuser',
            email='newuser@example.com',
            password='password',
            password2='password'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Congratulations, you are now a registered user!', response.data)

    def test_schedule_collection(self):
        # Test scheduling waste collection
        user = User(username='testuser', email='testuser@example.com')
        db.session.add(user)
        db.session.commit()

        with self.app.session_transaction() as session:
            session['user_id'] = user.id
        
        response = self.app.post('/schedule_collection', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Waste collection scheduled successfully!', response.data)

if __name__ == '__main__':
    unittest.main()
