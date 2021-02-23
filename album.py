import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from bottle import HTTPError

DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()

class Album(Base):
    __tablename__ = "album"
    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)

class DublicateError(Exception):
    pass


def connect_db():
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

def find(artist):
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all()
    return albums

def check_dublicate(session, album_data):
    if session.query(Album).filter(Album.year == album_data["year"], Album.artist == album_data["artist"], Album.album == album_data["album"]).first():
        raise DublicateError()


def save_album(album_data):
    session = connect_db()
    try:
        check_dublicate(session, album_data)
    except DublicateError:
        message = "Такой альбом уже есть в базе"
        result = HTTPError(409, message)
        return result
    album = Album(year = int(album_data["year"]), artist=album_data["artist"], genre=album_data["genre"], album=album_data["album"])
    session.add(album)
    session.commit()
    return "Данные успешно сохранены"

def check_year(album_data):
    try:
        year = int(album_data["year"])
        return True
    except ValueError:
        return False
    except  TypeError:
        return False
