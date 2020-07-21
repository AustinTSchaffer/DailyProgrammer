r"""

Contains the methods that serve data from the `processed_files` table of the
database to the `/files` endpoint.

"""

import json

import flask
import flaskext.mysql


def serve(conn: flaskext.mysql.pymysql.Connection) -> flask.Response:
    r"""
    Returns a flask Response that wraps a json stream.
    """

    return flask.Response(
        response=_files_data(conn),
        content_type="application/json",
    )

def _files_data(conn: flaskext.mysql.pymysql.Connection) -> str:
    r"""
    Returns a string containing the JSON-representation of the
    `processed_files` database table.
    """

    with conn.cursor() as cursor:
        cursor.execute("select `file_url`, `md5_hash`, (`successful` = 1) from `processed_files`;")

        return json.dumps([
            {
                "file_url": row[0],
                "md5_hash": row[1],
                "successful": bool(row[2]),
            }
            for row in
            cursor.fetchall()
        ])
