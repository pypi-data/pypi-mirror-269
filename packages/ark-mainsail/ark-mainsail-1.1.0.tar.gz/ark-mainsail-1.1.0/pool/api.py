# -*- coding: utf-8 -*-

import os
import threading

from pool import tbw, flask, loadJson, main, app, JOB
from collections import OrderedDict


@app.route("/<string:puk>", methods=["GET"])
def delegate(puk: str) -> flask.Response:
    info = loadJson(os.path.join(tbw.DATA, f"{puk}.json"))
    if len(info):
        info.pop("prk", False)
        return flask.jsonify(
            OrderedDict(
                sorted([item for item in info.items()], key=lambda i: i[0])
            )
        ), 200
    return flask.jsonify({"status": 404}), 404


@app.route("/<string:puk>/forgery", methods=["GET"])
def forgery(puk: str) -> flask.Response:
    path = os.path.join(tbw.DATA, puk, "forgery.json")
    if os.path.exists(path):
        forgery = loadJson(path)
        return flask.jsonify(
            OrderedDict(
                sorted([item for item in forgery.items()], key=lambda i: i[0])
            )
        ), 200
    return flask.jsonify({"status": 404}), 404


def run(debug: bool = True) -> flask.Flask:
    global app, MAIN

    MAIN = threading.Thread(target=main)
    MAIN.daemon = True
    MAIN.start()

    if debug:
        app.run("127.0.0.1", 5000)
        JOB.put(False)
    else:
        return app
