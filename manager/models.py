from manager import bcrypt
from flask_login import UserMixin
from manager import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return Client.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship('Item', backref='owned_user', lazy=True)

    @property
    def prettier_budget(self):
        if len(str(self.budget)) >= 4:
            return f'{str(self.budget)[:-3]},{str(self.budget)[-3:]}$'
        else:
            return f"{self.budget}$"

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))
    def __repr__(self):
        return f'Item {self.name}'
    
class Client(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    dbs = db.relationship('Databases', backref='owned_user', lazy=True)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

class Databases(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    db_type = db.Column(db.String(length=12), nullable=False, unique=True)
    db_uri = db.Column(db.String(length=1024), nullable=False, unique=True)
    db_username = db.Column(db.String(length=60), nullable=False)
    db_password = db.Column(db.String(length=60), nullable=False)
    connection_test_result = db.Column(db.Boolean, nullable=False)
    tables = db.relationship('Tables', backref='owned_db', lazy=True)
    client_id = db.Column(db.Integer(), db.ForeignKey('client.id'))
    
    def __repr__(self):
        return f'Item {self.name}'
    
class Tables(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    db_type = db.Column(db.String(length=12), nullable=False, unique=True)
    db_uri = db.Column(db.String(length=1024), nullable=False, unique=True)
    db_password_hash = db.Column(db.String(length=60), nullable=False)
    # db = db.relationship('Databases', backref='owned_db', lazy=True)
    db_id = db.Column(db.Integer(), db.ForeignKey('databases.id'))
    
    def __repr__(self):
        return f'Item {self.name}'