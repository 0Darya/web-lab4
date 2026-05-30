from app import create_app, db
from app.models import User, Role

app = create_app()

with app.app_context():
    # Create roles
    admin_role = Role(name='Администратор', description='Полный доступ к системе')
    user_role = Role(name='Пользователь', description='Обычный пользователь')
    db.session.add_all([admin_role, user_role])
    db.session.commit()

    # Create admin user
    admin = User(
        login='admin',
        first_name='Иван',
        last_name='Иванов',
        middle_name='Иванович',
        role_id=admin_role.id
    )
    admin.set_password('AdminPass123')
    db.session.add(admin)

    # Create test user
    test_user = User(
        login='user',
        first_name='Петр',
        last_name='Петров',
        middle_name='Петрович',
        role_id=user_role.id
    )
    test_user.set_password('UserPass123')
    db.session.add(test_user)

    db.session.commit()
    print("База данных инициализирована!")
    print("Админ: login=admin, password=AdminPass123")
    print("Пользователь: login=user, password=UserPass123")