import sqlalchemy
import databases
from settings import Settings

settings = Settings()

db = databases.Database(settings.DATABASE_URL)
meta = sqlalchemy.MetaData()

products = sqlalchemy.Table('products', meta,
                            sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
                            sqlalchemy.Column('title', sqlalchemy.String(80)),
                            sqlalchemy.Column('description', sqlalchemy.String(200)),
                            sqlalchemy.Column('price', sqlalchemy.Float))

users = sqlalchemy.Table('users', meta,
                         sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
                         sqlalchemy.Column('name', sqlalchemy.String(80)),
                         sqlalchemy.Column('surname', sqlalchemy.String(80)),
                         sqlalchemy.Column('email', sqlalchemy.String(120)),
                         sqlalchemy.Column('password', sqlalchemy.String(32)))

orders = sqlalchemy.Table('orders', meta,
                          sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
                          sqlalchemy.Column('user_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'),
                                            nullable=False),
                          sqlalchemy.Column('product_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('products.id'),
                                            nullable=False),
                          sqlalchemy.Column('order_date', sqlalchemy.Date),
                          sqlalchemy.Column('status', sqlalchemy.Enum('cancelled', 'in progress', 'done')))

engine = sqlalchemy.create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
meta.create_all(engine)
