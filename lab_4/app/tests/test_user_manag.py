import pytest
from app import db
from app.models import User, Role


class TestMainPage:
    """Tests for main page"""

    def test_main_page_accessible(self, client):
        """Test main page is accessible"""
        response = client.get('/')
        assert response.status_code == 200
        assert 'Список пользователей' in response.get_data(as_text=True)

    def test_main_page_shows_users(self, client):
        """Test main page shows users"""
        response = client.get('/')
        assert response.status_code == 200
        assert 'Тестов Тест Тестович' in response.get_data(as_text=True)


class TestAuthentication:
    """Tests for authentication"""

    def test_login_page_accessible(self, client):
        """Test login page is accessible"""
        response = client.get('/auth/login')  # ← Исправлено: /auth/login
        assert response.status_code == 200
        assert 'Вход в систему' in response.get_data(as_text=True)

    def test_successful_login(self, client):
        """Test successful login"""
        response = client.post('/auth/login', data={  # ← Исправлено: /auth/login
            'login': 'testuser',
            'password': 'TestPass123'
        }, follow_redirects=True)

        assert response.status_code == 200
        assert 'Вы успешно вошли в систему' in response.get_data(as_text=True)

    def test_failed_login_wrong_password(self, client):
        """Test failed login with wrong password"""
        response = client.post('/auth/login', data={  # ← Исправлено: /auth/login
            'login': 'testuser',
            'password': 'WrongPass'
        }, follow_redirects=True)

        assert response.status_code == 200
        assert 'Неверный логин или пароль' in response.get_data(as_text=True)

    def test_logout(self, authenticated_client):
        """Test logout"""
        response = authenticated_client.get('/auth/logout', follow_redirects=True)  # ← Исправлено: /auth/logout
        assert response.status_code == 200
        assert 'Вы вышли из системы' in response.get_data(as_text=True)


class TestViewUser:
    """Tests for viewing user details"""

    def test_view_user_accessible_to_all(self, client):
        """Test view user page is accessible to anonymous users"""
        response = client.get('/user/1')  # ← Исправлено: /user/1
        assert response.status_code == 200

    def test_view_user_shows_details(self, client):
        """Test view user shows correct details"""
        response = client.get('/user/1')  # ← Исправлено: /user/1
        assert response.status_code == 200
        assert 'Тестов' in response.get_data(as_text=True)


class TestCreateUser:
    """Tests for creating users"""

    def test_create_user_requires_auth(self, client):
        """Test create user requires authentication"""
        response = client.get('/user/create')  # ← Исправлено: /user/create
        assert response.status_code == 302

    def test_create_user_success(self, authenticated_client):
        """Test successful user creation"""
        response = authenticated_client.post('/user/create', data={  # ← Исправлено: /user/create
            'login': 'newuser123',
            'password': 'NewUser123',
            'first_name': 'New',
            'last_name': 'User',
            'middle_name': 'Test',
            'role_id': 1  # ← Исправлено: role_id вместо role
        }, follow_redirects=True)

        assert response.status_code == 200
        assert 'успешно создан' in response.get_data(as_text=True)

    def test_create_user_empty_login(self, authenticated_client):
        """Test create user with empty login"""
        response = authenticated_client.post('/user/create', data={  # ← Исправлено
            'login': '',
            'password': 'TestPass123',
            'first_name': 'Test',
            'last_name': 'User',
            'role_id': 1
        })

        assert response.status_code == 200
        assert 'Поле не может быть пустым' in response.get_data(as_text=True)

    def test_create_user_invalid_login_format(self, authenticated_client):
        """Test create user with invalid login format"""
        response = authenticated_client.post('/user/create', data={  # ← Исправлено
            'login': 'invalid-login!',
            'password': 'TestPass123',
            'first_name': 'Test',
            'last_name': 'User',
            'role_id': 1
        })

        assert response.status_code == 200
        assert 'Логин должен состоять только из латинских букв и цифр' in response.get_data(as_text=True)

    def test_create_user_short_login(self, authenticated_client):
        """Test create user with short login"""
        response = authenticated_client.post('/user/create', data={  # ← Исправлено
            'login': 'test',
            'password': 'TestPass123',
            'first_name': 'Test',
            'last_name': 'User',
            'role_id': 1
        })

        assert response.status_code == 200
        assert 'Логин должен содержать не менее 5 символов' in response.get_data(as_text=True)

    def test_create_user_weak_password(self, authenticated_client):
        """Test create user with weak password"""
        response = authenticated_client.post('/user/create', data={  # ← Исправлено
            'login': 'newuser456',
            'password': 'weak',
            'first_name': 'Test',
            'last_name': 'User',
            'role_id': 1
        })

        assert response.status_code == 200
        assert 'Пароль должен содержать не менее 8 символов' in response.get_data(as_text=True)

    def test_create_user_password_no_uppercase(self, authenticated_client):
        """Test create user with password without uppercase"""
        response = authenticated_client.post('/user/create', data={  # ← Исправлено
            'login': 'newuser789',
            'password': 'testpass1',
            'first_name': 'Test',
            'last_name': 'User',
            'role_id': 1
        })

        assert response.status_code == 200
        assert 'Пароль должен содержать как минимум одну заглавную букву' in response.get_data(as_text=True)


class TestEditUser:
    """Tests for editing users"""

    def test_edit_user_requires_auth(self, client):
        """Test edit user requires authentication"""
        response = client.get('/user/1/edit')  # ← Исправлено: /user/1/edit
        assert response.status_code == 302

    def test_edit_user_success(self, authenticated_client):
        """Test successful user edit"""
        response = authenticated_client.post('/user/1/edit', data={  # ← Исправлено
            'first_name': 'Updated',
            'last_name': 'Name',
            'middle_name': 'Test',
            'role_id': 1  # ← Исправлено: role_id
        }, follow_redirects=True)

        assert response.status_code == 200
        assert 'обновлены' in response.get_data(as_text=True)

    def test_edit_user_form_prefilled(self, authenticated_client):
        """Test edit user form is prefilled"""
        response = authenticated_client.get('/user/1/edit')  # ← Исправлено
        assert response.status_code == 200
        assert 'Тестов' in response.get_data(as_text=True)


class TestDeleteUser:
    """Tests for deleting users"""

    def test_delete_user_requires_auth(self, client):
        """Test delete user requires authentication"""
        response = client.post('/user/2/delete')  # ← Исправлено: /user/2/delete
        assert response.status_code == 302

    def test_delete_user_success(self, authenticated_client):
        """Test successful user deletion"""
        # Сначала создадим второго пользователя для удаления
        with authenticated_client.session_transaction() as sess:
            pass

        # Создаем тестового пользователя для удаления
        user = User.query.filter_by(login='testuser').first()
        if user:
            # Создаем ещё одного пользователя
            new_user = User(
                login='todelete',
                first_name='Удалить',
                last_name='Меня',
                middle_name='Пожалуйста'
            )
            new_user.set_password('TestPass123')
            db.session.add(new_user)
            db.session.commit()
            user_id = new_user.id
        else:
            user_id = 2

        response = authenticated_client.post(f'/user/{user_id}/delete', follow_redirects=True)  # ← Исправлено
        assert response.status_code == 200

    def test_cannot_delete_self(self, authenticated_client):
        """Test cannot delete yourself"""
        response = authenticated_client.post('/user/1/delete', follow_redirects=True)  # ← Исправлено
        assert response.status_code == 200
        assert 'Нельзя удалить самого себя' in response.get_data(as_text=True)


class TestChangePassword:
    """Tests for password change"""

    def test_change_password_requires_auth(self, client):
        """Test change password requires authentication"""
        response = client.get('/change-password')  # ← Исправлено: /change-password
        assert response.status_code == 302

    def test_change_password_success(self, authenticated_client):
        """Test successful password change"""
        response = authenticated_client.post('/change-password', data={  # ← Исправлено
            'old_password': 'TestPass123',
            'new_password': 'NewPass123',
            'confirm_password': 'NewPass123'
        }, follow_redirects=True)

        assert response.status_code == 200
        assert 'Пароль успешно изменен' in response.get_data(as_text=True)

    def test_change_password_wrong_old(self, authenticated_client):
        """Test change password with wrong old password"""
        response = authenticated_client.post('/change-password', data={  # ← Исправлено
            'old_password': 'WrongPass',
            'new_password': 'NewPass123',
            'confirm_password': 'NewPass123'
        })

        assert response.status_code == 200
        assert 'Неверный старый пароль' in response.get_data(as_text=True)

    def test_change_password_mismatch(self, authenticated_client):
        """Test change password with mismatched passwords"""
        response = authenticated_client.post('/change-password', data={  # ← Исправлено
            'old_password': 'TestPass123',
            'new_password': 'NewPass123',
            'confirm_password': 'DifferentPass456'
        })

        assert response.status_code == 200
        assert 'Пароли не совпадают' in response.get_data(as_text=True)


class TestNavbar:
    """Tests for navbar elements"""

    def test_navbar_shows_login_for_anonymous(self, client):
        """Test navbar shows login for anonymous users"""
        response = client.get('/')
        assert 'Войти' in response.get_data(as_text=True)  # ← Исправлено: decode

    def test_navbar_shows_logout_for_authenticated(self, authenticated_client):
        """Test navbar shows logout for authenticated users"""
        response = authenticated_client.get('/')
        assert 'Выйти' in response.get_data(as_text=True)  # ← Исправлено: decode

    def test_navbar_shows_change_password_for_authenticated(self, authenticated_client):
        """Test navbar shows change password for authenticated users"""
        response = authenticated_client.get('/')
        assert 'Изменить пароль' in response.get_data(as_text=True)  # ← Исправлено: decode

    def test_create_button_only_for_authenticated(self, client):
        """Test create user button only shown for authenticated users"""
        response = client.get('/')
        assert 'Создание пользователя' not in response.get_data(as_text=True)  # ← Исправлено: decode


class TestValidation:
    """Tests for input validation"""

    def test_password_with_spaces_invalid(self, authenticated_client):
        """Test password with spaces is invalid"""
        response = authenticated_client.post('/user/create', data={  # ← Исправлено
            'login': 'newuser999',
            'password': 'Test Pass 123',
            'first_name': 'Test',
            'last_name': 'User',
            'role_id': 1
        })

        assert response.status_code == 200
        assert 'Пароль не должен содержать пробелы' in response.get_data(as_text=True)

    def test_password_too_long(self, authenticated_client):
        """Test password longer than 128 chars is invalid"""
        long_password = 'A' * 129 + '1'
        response = authenticated_client.post('/user/create', data={  # ← Исправлено
            'login': 'newuser888',
            'password': long_password,
            'first_name': 'Test',
            'last_name': 'User',
            'role_id': 1
        })

        assert response.status_code == 200
        assert 'Пароль должен содержать не более 128 символов' in response.get_data(as_text=True)