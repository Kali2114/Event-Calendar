"""
Tests for models.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model


def create_user(**params):
    """Create and return a new user."""
    default_user = {
        "email": "test@example.com",
        "password": "Test123",
        "name": "TestName",
    }
    default_user.update(**params)

    return get_user_model().objects.create_user(**default_user)


def create_instructor(**params):
    """Create and return a new instructor."""
    default_user = {
        "email": "instructor@example.com",
        "password": "testpass123",
        "name": "Instructor",
    }
    default_user.update(params)

    return get_user_model().objects.create_superuser(**default_user)


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with email is successful."""
        email = "test@example.com"
        password = "Test123"

        user = create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email is normalized for new users."""
        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@ExAmple.com", "Test2@example.com"],
            ["Test3@example.COM", "Test3@example.com"],
        ]
        for idx, (email, expected) in enumerate(sample_emails):
            user = create_user(
                email=email,
                password="Test123",
                name=f"User{idx}",
            )
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raise_error(self):
        """Test raises ValueError when creating user without email."""
        with self.assertRaises(ValueError):
            create_user(email="")

    def test_new_user_without_name_raise_error(self):
        """Test raises ValueError when creating user without email."""
        with self.assertRaises(ValueError):
            create_user(name="")

    def test_create_superuser(self):
        """Test creating a superuser successful."""
        user = get_user_model().objects.create_superuser(
            email="example@test.com",
            password="Test123",
            name="Test_Name",
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
