import os


class Config:
    SECRET_KEY = os.environ.get(
        'SECRET_KEY',
        'clave-secreta-para-desarrollo'
    )

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'mysql+pymysql://root:@127.0.0.1:3306/bd_anuncios?charset=utf8mb4'
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False