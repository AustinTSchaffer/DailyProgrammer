import atexit
import configparser
import json
import os

import apscheduler
from apscheduler.schedulers import background

import flask
import flaskext.mysql

import gdelt_data_processor

config = configparser.ConfigParser()
config.read([
    "config.ini",
    "config.local.ini",
])

app = flask.Flask(__name__)
mysql = flaskext.mysql.MySQL()
app.config['MYSQL_DATABASE_USER'] = config.get("mysql", "user")
app.config['MYSQL_DATABASE_PASSWORD'] = config.get("mysql", "password")
app.config['MYSQL_DATABASE_DB'] = config.get("mysql", "db")
app.config['MYSQL_DATABASE_HOST'] = config.get("mysql", "host")
mysql.init_app(app)


@app.route("/")
def get_root():
    """
    Default action, to display author information.
    """
    return flask.render_template("root.html")


@app.route("/readme")
def get_readme():
    """
    Returns an HTML-formatted version of the README
    """
    return flask.render_template("readme.html")


@app.route("/data")
def get_data():
    """
    Returns all of the data from the `data` table from the MySQL db, so the
    results can be analyzed offsite.
    """

    conn = mysql.connect()
    return gdelt_data_processor.endpoints.data.serve(conn)


@app.route("/files")
def get_files():
    """
    Returns all of the data from the `processed_files` table from the MySQL db,
    so end users can evaluate the failure rate of the application.
    """

    conn = mysql.connect()
    return gdelt_data_processor.endpoints.files.serve(conn)


def setup_data_scheduler():
    """
    Sets up a scheduler that attempts to post data to the recipient
    on a regular schedule.
    """

    def _send_data():
        """
        Runs the EventDataProcessor, which attempts to upload data
        to the recipient.
        """

        conn = mysql.connect()

        gdelt_data_processor.load_gdelt_event_data.EventDataProcessor.run(
            url=config.get("source_data", "lastupdated_url"),
            db_connection=conn,
            recipient=gdelt_data_processor.data_recipient.Recipient(
                base_url=config.get("recipient", "base_url"),
                username=config.get("recipient", "user_id"),
                password=config.get("recipient", "auth_token"),
            ),
        )

        conn.close()

    scheduler = background.BackgroundScheduler()
    scheduler.add_job(
        func=_send_data,
        trigger="interval",
        minutes=config.getint("source_data", "interval_minutes"),
    )

    atexit.register(lambda: scheduler.shutdown())
    scheduler.start()


setup_data_scheduler()
