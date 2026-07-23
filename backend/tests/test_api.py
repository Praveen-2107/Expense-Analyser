import csv
import io
import os
import tempfile
import unittest

from fastapi import Depends
from fastapi.testclient import TestClient
from pypdf import PdfWriter

from app.auth import dependencies as auth_dependencies
from app.core import config as core_config
from app.database import session as db_session
from app.main import app
from app.models.category import Category
from app.models.user import User


class ExpenseAnalyserApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.database_path = os.path.join(cls.temp_dir.name, 'test_expense_analyzer.db')
        cls.database_url = f'sqlite:///{cls.database_path}'
        cls.uploads_dir = os.path.join(cls.temp_dir.name, 'uploads')
        os.makedirs(cls.uploads_dir, exist_ok=True)

        core_config.settings.database_url = cls.database_url
        core_config.settings.uploads_dir = cls.uploads_dir
        core_config.settings.gemini_api_key = None

        db_session.engine.dispose()
        db_session.engine = db_session.create_engine(
            cls.database_url,
            future=True,
            pool_pre_ping=True,
            connect_args={"check_same_thread": False},
        )
        db_session.SessionLocal.configure(bind=db_session.engine)
        db_session.Base.metadata.create_all(bind=db_session.engine)

        app.dependency_overrides[auth_dependencies.get_current_user] = cls._override_current_user
        cls.client = TestClient(app)

        cls.test_user_email = 'tester@example.com'
        cls.test_user_password = 'strongpassword123'
        cls.current_user_id = None

    @classmethod
    def tearDownClass(cls):
        app.dependency_overrides.clear()
        db_session.Base.metadata.drop_all(bind=db_session.engine)
        db_session.engine.dispose()
        cls.temp_dir.cleanup()

    @classmethod
    def _override_current_user(cls, db=Depends(db_session.get_db)):
        if cls.current_user_id is None:
            raise RuntimeError('current_user_id not initialized')
        user = db.query(User).filter(User.id == cls.current_user_id).first()
        if user is None:
            raise RuntimeError('current_user not found')
        return user

    def setUp(self):
        self._create_user_if_needed()
        self._seed_categories_if_needed()

    def _create_user_if_needed(self):
        if self.__class__.current_user_id is not None:
            return

        response = self.client.post(
            '/api/v1/auth/register',
            json={
                'full_name': 'Test User',
                'email': self.test_user_email,
                'password': self.test_user_password,
            },
        )
        self.assertEqual(response.status_code, 201)
        self.__class__.current_user_id = response.json()['id']

    def _seed_categories_if_needed(self):
        with db_session.SessionLocal() as db:
            existing = db.query(Category).filter(Category.user_id == self.current_user_id).count()
            if existing > 0:
                return

            db.add_all(
                [
                    Category(user_id=self.current_user_id, name='Housing', color='#0b5cab', icon='home'),
                    Category(user_id=self.current_user_id, name='Food & Dining', color='#16a34a', icon='utensils'),
                ]
            )
            db.commit()

    def test_auth_register_login_and_me(self):
        login_response = self.client.post(
            '/api/v1/auth/login',
            data={'username': self.test_user_email, 'password': self.test_user_password},
        )
        self.assertEqual(login_response.status_code, 200)
        token = login_response.json()['access_token']

        me_response = self.client.get('/api/v1/auth/me', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(me_response.status_code, 200)
        self.assertEqual(me_response.json()['email'], self.test_user_email)

    def test_expense_crud(self):
        create_response = self.client.post(
            '/api/v1/expenses',
            json={
                'title': 'Monthly rent',
                'description': 'Apartment rent',
                'amount': '1200.50',
                'expense_date': '2026-07-01',
                'payment_method': 'Bank Transfer',
                'merchant_name': 'Landlord',
                'is_recurring': True,
                'category_id': 1,
            },
        )
        self.assertEqual(create_response.status_code, 201)
        expense_id = create_response.json()['id']

        list_response = self.client.get('/api/v1/expenses')
        self.assertEqual(list_response.status_code, 200)
        self.assertGreaterEqual(len(list_response.json()), 1)

        update_response = self.client.put(
            f'/api/v1/expenses/{expense_id}',
            json={'title': 'Updated rent', 'amount': '1250.00'},
        )
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.json()['title'], 'Updated rent')

        delete_response = self.client.delete(f'/api/v1/expenses/{expense_id}')
        self.assertEqual(delete_response.status_code, 204)

    def test_income_crud(self):
        create_response = self.client.post(
            '/api/v1/incomes',
            json={
                'title': 'Salary',
                'description': 'Monthly salary',
                'amount': '4500.00',
                'income_date': '2026-07-01',
                'source': 'Employer',
                'is_recurring': True,
                'category_id': None,
            },
        )
        self.assertEqual(create_response.status_code, 201)
        income_id = create_response.json()['id']

        list_response = self.client.get('/api/v1/incomes')
        self.assertEqual(list_response.status_code, 200)

        update_response = self.client.put(
            f'/api/v1/incomes/{income_id}',
            json={'source': 'Updated Employer'},
        )
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.json()['source'], 'Updated Employer')

        delete_response = self.client.delete(f'/api/v1/incomes/{income_id}')
        self.assertEqual(delete_response.status_code, 204)

    def test_ai_insights_endpoint(self):
        response = self.client.post('/api/v1/ai/insights', json={'focus': 'savings opportunities'})
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn('summary', payload)
        self.assertIn('insights', payload)
        self.assertIn('recommendations', payload)

    def test_prediction_endpoint(self):
        self.client.post(
            '/api/v1/expenses',
            json={
                'title': 'Expense 1',
                'amount': '100.00',
                'expense_date': '2026-01-01',
                'is_recurring': False,
                'category_id': 1,
            },
        )
        self.client.post(
            '/api/v1/expenses',
            json={
                'title': 'Expense 2',
                'amount': '200.00',
                'expense_date': '2026-02-01',
                'is_recurring': False,
                'category_id': 1,
            },
        )
        self.client.post(
            '/api/v1/expenses',
            json={
                'title': 'Expense 3',
                'amount': '300.00',
                'expense_date': '2026-03-01',
                'is_recurring': False,
                'category_id': 1,
            },
        )

        response = self.client.post('/api/v1/predictions/expense-forecast', json={'months_ahead': 3})
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn(payload['method'], ['linear_regression', 'moving_average', 'no_history'])
        self.assertEqual(len(payload['forecast']), 3)

    def test_upload_csv_and_pdf(self):
        csv_buffer = io.StringIO()
        writer = csv.DictWriter(csv_buffer, fieldnames=['Date', 'Description', 'Amount'])
        writer.writeheader()
        writer.writerow({'Date': '2026-07-01', 'Description': 'Grocery Mart', 'Amount': '-45.50'})
        writer.writerow({'Date': '2026-07-02', 'Description': 'Salary', 'Amount': '4500.00'})

        csv_response = self.client.post(
            '/api/v1/uploads/csv',
            files={'file': ('statement.csv', csv_buffer.getvalue().encode('utf-8'), 'text/csv')},
        )
        self.assertEqual(csv_response.status_code, 200)
        self.assertEqual(csv_response.json()['parser_type'], 'csv')
        self.assertEqual(csv_response.json()['total_transactions'], 2)

        pdf_buffer = io.BytesIO()
        writer = PdfWriter()
        writer.add_blank_page(width=72, height=72)
        writer.write(pdf_buffer)
        pdf_bytes = pdf_buffer.getvalue()
        pdf_response = self.client.post(
            '/api/v1/uploads/pdf',
            files={'file': ('statement.pdf', pdf_bytes, 'application/pdf')},
        )
        self.assertEqual(pdf_response.status_code, 200)
        self.assertEqual(pdf_response.json()['parser_type'], 'pdf')

        history_response = self.client.get('/api/v1/uploads/statements')
        self.assertEqual(history_response.status_code, 200)
        self.assertGreaterEqual(len(history_response.json()), 2)


if __name__ == '__main__':
    unittest.main()
