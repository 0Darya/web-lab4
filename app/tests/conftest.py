import pytest
from app import create_app, db
from app.models import User, Role


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory DB
    app.config['WTF_CSRF_ENABLED'] = False

    with app.app_context():
        db.create_all()

        # Создаём роли, только если их нет
        admin_role = Role.query.filter_by(name='Администратор').first()
        if not admin_role:
            admin_role = Role(name='Администратор', description='Полный доступ')
            db.session.add(admin_role)
            db.session.commit()
        else:
            # Получаем существующую роль
            admin_role = Role.query.filter_by(name='Администратор').first()

        user_role = Role.query.filter_by(name='Пользователь').first()
        if not user_role:
            user_role = Role(name='Пользователь', description='Обычный пользователь')
            db.session.add(user_role)
            db.session.commit()
        else:
            user_role = Role.query.filter_by(name='Пользователь').first()

        # Создаём тестового пользователя
        test_user = User.query.filter_by(login='testuser').first()
        if not test_user:
            test_user = User(
                login='testuser',
                first_name='Тест',
                last_name='Тестов',
                middle_name='Тестович',
                role_id=user_role.id
            )
            test_user.set_password('TestPass123')
            db.session.add(test_user)
            db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def authenticated_client(client):
    client.post('/auth/login', data={
        'login': 'testuser',
        'password': 'TestPass123'
    }, follow_redirects=True)
    return client