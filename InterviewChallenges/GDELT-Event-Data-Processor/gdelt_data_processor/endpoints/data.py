r"""

Contains the methods that serve data from the `data` table of the database to
the `/data` endpoint.

"""

import json
from typing import Iterable

import flask
import flaskext.mysql


def serve(conn: flaskext.mysql.pymysql.Connection) -> flask.Response:
    r"""
    Returns a flask Response that wraps a json stream.
    """

    return flask.Response(
        response=_data_stream(conn),
        content_type='application/json',
    )


def _data_stream(conn: flaskext.mysql.pymysql.Connection) -> Iterable[str]:
    """
    Streams a JSONL of records, one JSON-object record at a time. This
    should prevent the entire `data` table of the database from being loaded
    into memory all at once.
    """

    with conn.cursor(cursor=flaskext.mysql.pymysql.cursors.SSCursor) as cursor:
        cursor.execute(
            "select \
                `file_url`, \
                `global_event_id`, \
                `data_sent`, \
                `data_received` \
            from `data`;"
        )

        rows = cursor.fetchall_unbuffered()

        for row in rows:
            serialized_row = _serialize_row(row)
            yield serialized_row

def _serialize_row(row: tuple) -> str:
    """
    Serializes the JSON-object representation of the input row as a string.
    """

    record = {
        "file_url": row[0],
        "global_event_id": row[1],
        "data_sent": json.loads(row[2]),
        "data_received": json.loads(row[3]),
    }

    return json.dumps(record)
