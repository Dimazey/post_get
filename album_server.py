from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request

import album

@route("/albums/<artist>")
def albums(artist):
    album_list = album.find(artist)
    if not album_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        album_names = [album.album for album in album_list]
        result = "Найдено {} альбомов {} \n".format(len(album_names), artist)
        result += "Список найденных альбомов:\n"
        result += "\n".join(album_names)
    return result

@route("/albums", method="POST")
def add_album():
    album_data = {
    "year": request.forms.get("year"),
    "artist": request.forms.get("artist"),
    "genre": request.forms.get("genre"),
    "album": request.forms.get("album")
    }
    for key, value in album_data.items():
        if value == '':
            album_data[key] = None
    if album.check_year(album_data) == False:
        message = "Ошибка ввода. Год альбома - не число"
        result = HTTPError(400, message)
    elif album_data["artist"] == None or album_data["album"] == None:
        message = "Ошибка ввода. Не указаны исполнитель или название альбома"
        result = HTTPError(400, message)
    else:
        result = album.save_album(album_data)
    return result

if __name__ == '__main__':
    run (host="localhost", port=8080, debug=True)
