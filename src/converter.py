from bottle import get, post, request, response, run
from simplejson.errors import JSONDecodeError
from json import dumps
import ffmpeg

from episode import EpisodeFile


def error(code: int, msg: str):
    return dumps({"status": code, "error": msg})


def success(path: str, msg: str):
    return dumps({"status": 200, "path": path, "message": msg})


@post("/asstosrt")
def ass_to_srt():
    response.content_type = 'application/json'
    if request.json["eventType"] == "Test":
        response.status = 200
        return dumps({"status": 200, "message": "Success"})
    try:
        ep = EpisodeFile(request.json)
    except JSONDecodeError:
        response.status = 422
        return error(422, "Invalid json")
    except KeyError:
        response.status = 422
        return error(422, "Required entity not found: episodeFile.path")
    except ffmpeg._run.Error as e:
        response.status = 500
        return error(500, e.stderr.decode().strip().split('\n')[-1])

    if not ep.has_asses:
        response.status = 200
        return success(ep.path, "No asses in file")

    try:
        ep.convert_ass_to_srt()
        return success(ep.path, "Successfully converted asses to subrip")
    except ffmpeg._run.Error as e:
        response.status = 500
        return error(500, e.stderr.decode().strip().split('\n')[-1])


@post("/print")
def print_request():
    print(dumps(request.json))
    response.content_type = 'application/json'
    response.status = 200
    return dumps({"status": 200, "message": "Success"})


@get("/health")
def health():
    return dumps({"status": 200, "message": "All ok"})


run(host="0.0.0.0", port=8080, debug=True)
