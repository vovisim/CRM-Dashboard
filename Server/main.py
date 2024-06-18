from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


# Определение класса конфигурации
class Config:
    SQLALCHEMY_BINDS = {
        'user_data': 'sqlite:///UserData.db',
        'client_data': 'sqlite:///ClientData.db'
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app = Flask(__name__)
api = Api(app)
CORS(app)
# Установка конфигурации Flask
app.config.from_object(Config)

# Создание экземпляра SQLAlchemy и привязка его к Flask
db = SQLAlchemy(app)

# Определение парсера для ClientData
client_parser = reqparse.RequestParser()
client_parser.add_argument("AccountNumber", type=int, required=True, help="Account number cannot be blank!")
client_parser.add_argument("Surname", type=str, required=True, help="Surname cannot be blank!")
client_parser.add_argument("Name", type=str, required=True, help="Name cannot be blank!")
client_parser.add_argument("Patronymic", type=str, required=True, help="Patronymic cannot be blank!")
client_parser.add_argument("Birthday", type=str, required=True, help="Birthday cannot be blank!")
client_parser.add_argument("TIN", type=int, required=True, help="TIN cannot be blank!")
client_parser.add_argument("FullNameResponsible", type=str, required=True,
                           help="Full name of the responsible person cannot be blank!")
client_parser.add_argument("Status", type=str, default="Не в работе")

# Определение парсера для UserData
user_parser = reqparse.RequestParser()
user_parser.add_argument("Fullname", type=str, required=True, help="Fullname cannot be blank!")
user_parser.add_argument("Login", type=str, required=True, help="Login cannot be blank!")
user_parser.add_argument("Password", type=str, required=True, help="Password cannot be blank!")

status_parser = reqparse.RequestParser()
status_parser.add_argument("Status", type=str, default="Не в работе")

# Определение модели данных для ClientData
class ClientData(db.Model):
    __bind_key__ = 'client_data'
    __tablename__ = 'ClientData'

    id = db.Column(db.Integer, primary_key=True)
    AccountNumber = db.Column(db.Integer, nullable=False)
    Surname = db.Column(db.String(100), nullable=False)
    Name = db.Column(db.String(100), nullable=False)
    Patronymic = db.Column(db.String(100), nullable=False)
    Birthday = db.Column(db.String(100), nullable=False)
    TIN = db.Column(db.Integer, nullable=False)
    FullNameResponsible = db.Column(db.String(100), nullable=False)
    Status = db.Column(db.String(100), server_default="Не в работе")

    def __repr__(self):
        return (f"ClientData(id={self.id}, AccountNumber={self.AccountNumber}, Surname={self.Surname}, Name={self.Name}"
                f", Patronymic={self.Patronymic}, Birthday={self.Birthday}, TIN={self.TIN}, FullNameResponsible="
                f"{self.FullNameResponsible}, Status={self.Status})")


# Определение модели данных для UserData
class UserData(db.Model):
    __bind_key__ = 'user_data'
    __tablename__ = 'UserData'

    id = db.Column(db.Integer, primary_key=True)
    Fullname = db.Column(db.String(100), nullable=False)
    Login = db.Column(db.String(100), nullable=False)
    Password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"UserData(id={self.id}, Fullname={self.Fullname}, Login={self.Login}, Password={self.Password})"


# Определение ресурса для ClientData

class ClientResource(Resource):
    def get(self, client_id, fullnameresponsible=''):
        if client_id == 0 and fullnameresponsible == '':
            clients = ClientData.query.all()
            result = {}
            for client in clients:
                result[client.id] = {
                    "id": client.id,
                    "AccountNumber": client.AccountNumber,
                    "Surname": client.Surname,
                    "Name": client.Name,
                    "Patronymic": client.Patronymic,
                    "Birthday": client.Birthday,
                    "TIN": client.TIN,
                    "FullNameResponsible": client.FullNameResponsible,
                    "Status": client.Status
                }
            print(result)
            return result
        elif fullnameresponsible != '':
            clients = ClientData.query.filter_by(FullNameResponsible=fullnameresponsible).all()
            if clients:
                result = {}
                for client in clients:
                    result[client.id] = {
                        "id": client.id,
                        "AccountNumber": client.AccountNumber,
                        "Surname": client.Surname,
                        "Name": client.Name,
                        "Patronymic": client.Patronymic,
                        "Birthday": client.Birthday,
                        "TIN": client.TIN,
                        "FullNameResponsible": client.FullNameResponsible,
                        "Status": client.Status
                    }
                print(result)
                return result
            else:
                return f"Client not found: {clients}", 404
        else:
            client = ClientData.query.get(client_id)
            if client:
                print(client)
                return {
                    "id": client.id,
                    "AccountNumber": client.AccountNumber,
                    "Surname": client.Surname,
                    "Name": client.Name,
                    "Patronymic": client.Patronymic,
                    "Birthday": client.Birthday,
                    "TIN": client.TIN,
                    "FullNameResponsible": client.FullNameResponsible,
                    "Status": client.Status
                }
            else:
                return "Client not found", 404

    def delete(self, client_id):
        client = ClientData.query.get(client_id)
        if client:
            db.session.delete(client)
            db.session.commit()
            return {"message": "Client deleted successfully"}
        else:
            return "Client not found", 404


    def post(self):
        args = client_parser.parse_args()
        client = ClientData(
            AccountNumber=args["AccountNumber"],
            Surname=args["Surname"],
            Name=args["Name"],
            Patronymic=args["Patronymic"],
            Birthday=args["Birthday"],
            TIN=args["TIN"],
            FullNameResponsible=args["FullNameResponsible"],
            Status=args["Status"]
        )
        db.session.add(client)
        db.session.commit()
        return {"message": "Client created successfully"}, 201

    def put(self, client_id, fullnameresponsible="False"):
        if fullnameresponsible == "False":
            args = client_parser.parse_args()
        else:
            args = status_parser.parse_args()
        client = ClientData.query.get(client_id)
        if client and fullnameresponsible == "True":
            client.Status = args["Status"]
            db.session.commit()
            return {"message": "Client updated successfully"}
        elif client:

            client.AccountNumber = args["AccountNumber"]
            client.Surname = args["Surname"]
            client.Name = args["Name"]
            client.Patronymic = args["Patronymic"]
            client.Birthday = args["Birthday"]
            client.TIN = args["TIN"]
            client.FullNameResponsible = args["FullNameResponsible"]
            client.Status = args["Status"]
            db.session.commit()
            return {"message": "Client updated successfully"}
        else:
            return "Client not found", 404


# Определение ресурса для UserData
class UserResource(Resource):
    def get(self, user_id):
        if user_id == 0:
            users = UserData.query.all()
            result = {}
            for user in users:
                result[user.id] = {
                    "Fullname": user.Fullname,
                    "Login": user.Login,
                    "Password": user.Password
                }
            return result
        else:
            user = UserData.query.get(user_id, )
            if user:
                return {
                    "Fullname": user.Fullname,
                    "Login": user.Login,
                    "Password": user.Password
                }
            else:
                return "User not found", 404

    def delete(self, user_id):
        user = UserData.query.get(user_id, )
        if user:
            db.session.delete(user)
            db.session.commit()
            return {"message": "User deleted successfully"}
        else:
            return "User not found", 404

    def post(self, user_id):
        args = user_parser.parse_args()
        user = UserData(
            Fullname=args["Fullname"],
            Login=args["Login"],
            Password=args["Password"]
        )
        db.session.add(user)
        db.session.commit()
        return {"message": "User created successfully"}, 201

    def put(self, user_id):
        args = user_parser.parse_args()
        user = UserData.query.get(user_id, )
        if user:
            user.Fullname = args["Fullname"]
            user.Login = args["Login"]
            user.Password = args["Password"]
            db.session.commit()
            return {"message": "User updated successfully"}
        else:
            return "User not found", 404


# Добавление ресурсов в API
api.add_resource(ClientResource, "/api/clients/<int:client_id>", "/api/clients/<int:client_id>/<string:fullnameresponsible>")

api.add_resource(UserResource, "/api/users/<int:user_id>", "/api/users/<int:user_id>")

if __name__ == "__main__":
    with app.app_context():
        db.create_all(bind_key='client_data')
        db.create_all(bind_key='user_data')
    app.run(debug=True, port=2266, host="127.0.0.1")
