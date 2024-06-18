from faker import Faker
import random
from main import app, db, UserData, ClientData

fake = Faker()

# Создаем повторяющиеся значения для Fullname и FullNameResponsible
repeated_fullnames = [fake.name() for _ in range(5)]

# Функция для создания пользователей
def create_users(n):
    for i in range(n):
        fullname = random.choice(repeated_fullnames)
        user = UserData(
            Fullname=fullname,
            Login=fake.user_name(),
            Password=fake.password()
        )
        db.session.add(user)

# Функция для создания клиентов
def create_clients(n):
    for i in range(n):
        fullname_responsible = random.choice(repeated_fullnames)
        client = ClientData(
            AccountNumber=fake.random_number(digits=10),
            Surname=fake.last_name(),
            Name=fake.first_name(),
            Patronymic=fake.first_name(),
            Birthday=fake.date_of_birth().strftime('%Y-%m-%d'),
            TIN=fake.random_number(digits=12),
            FullNameResponsible=fullname_responsible,
            Status=random.choice(["Не в работе"])
        )
        db.session.add(client)

if __name__ == "__main__":
    with app.app_context():
        db.create_all(bind_key='user_data')
        db.create_all(bind_key='client_data')

        # Создаем синтетические данные
        create_users(100)  # Создаем 100 пользователей
        create_clients(100)  # Создаем 100 клиентов

        # Сохраняем изменения в базах данных
        db.session.commit()
