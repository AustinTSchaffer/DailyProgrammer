r"""

Contains the `EventDataProcessor`, which loads, transforms, and
uploads GDELT data from its source system to the endpoint that consumes a subset
of the data.

"""

import csv
import datetime
import io
import json
import os
import tempfile
from typing import Iterable
import zipfile

import flaskext.mysql
import requests

from gdelt_data_processor import (
    last_updated_data,
    event_data,
    data_recipient,
)


class EventDataProcessor(object):
    """
    Handles new-data events using the http://data.gdeltproject.org/gdeltv2/lastupdate.txt
    service, or a service that uses the same schema and HTTP method, which
    refers to files that contain GDELT data from a 15 minute span of time.
    """

    @staticmethod
    def run(url: str, db_connection: flaskext.mysql.pymysql.Connection, recipient: data_recipient.Recipient):
        """
        Attempts to upload new data to the recipient, if the data does
        not already have a record in the database.
        """

        #
        # Pull the lastupdate.txt and parse its contents
        #

        response = requests.get(url)
        assert response.ok, response.text

        lastupdated_data = last_updated_data.LastUpdated(
            response.text
        )

        export_datafile_ref = lastupdated_data.get_export_ref()

        #
        # Determine if the data has already been uploaded. If not, add the file to the database.
        #

        processed_files_id = -1

        with db_connection.cursor() as cursor:
            cursor.execute(
                "select count(*) from `processed_files` where `md5_hash` = %s",
                (export_datafile_ref.md5_hash,)
            )

            (number_of_matching_files,) = cursor.fetchone()
            if number_of_matching_files > 0:
                print("File has already been processed:", export_datafile_ref.zipfile_url)
                return

            print("Recording file in `processed_files`:",
                  export_datafile_ref.zipfile_url)

            cursor.execute(
                "insert into `processed_files` (`md5_hash`, `file_url`) values (%s, %s)",
                (export_datafile_ref.md5_hash, export_datafile_ref.zipfile_url,)
            )

            processed_files_id = cursor.lastrowid

        db_connection.commit()

        #
        # Download zipped csv to a temporary file
        #

        print("Downloading zipped data file:", export_datafile_ref.zipfile_url)

        _, zippedcsv_filename = tempfile.mkstemp(suffix="_export.csv.zip")

        with requests.get(export_datafile_ref.zipfile_url, stream=True) as request:
            request.raise_for_status()
            with open(zippedcsv_filename, "wb") as file:
                for chunk in request.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)

        #
        # For every record in the CSV, upload the data to the recipient
        #

        event_records = EventDataProcessor.event_data_iterable(
            zipfile_name=zippedcsv_filename,
            timestamp=export_datafile_ref.timestamp,
        )

        with db_connection.cursor() as cursor:
            for event_record in event_records:
                print("Processing event:", event_record.global_event_id)

                input_data = event_record.to_dict()
                output_data = recipient.upload(input_data)

                cursor.execute(
                    "insert into `data` \
                    (`global_event_id`, `file_url`, `data_sent`, `data_received`) \
                    values (%s, %s, %s, %s)",
                    [
                        event_record.global_event_id,
                        export_datafile_ref.zipfile_url,
                        json.dumps(input_data['data']),
                        json.dumps(output_data['result']),
                    ]
                )

                db_connection.commit()

            print("Recording success for file:", export_datafile_ref.zipfile_url)

            cursor.execute(
                "update `processed_files` set `successful` = 1 where `id` = %s",
                (processed_files_id,)
            )

            db_connection.commit()

        print("Removing temporary Zip File")

        os.remove(zippedcsv_filename)

        print("Finished processing GDELT series:", export_datafile_ref.zipfile_url)

    @staticmethod
    def event_data_iterable(zipfile_name: str, timestamp: datetime.datetime
                            ) -> Iterable[event_data.EventRecord]:
        with zipfile.ZipFile(zipfile_name) as zf:
            for csvfile in zf.infolist():
                with zf.open(csvfile.filename, mode="r") as infile:
                    reader = csv.reader(
                        io.TextIOWrapper(infile),
                        delimiter="\t",
                    )

                    for row in reader:
                        yield EventDataProcessor.format_event_record(row, timestamp)

    @staticmethod
    def format_event_record(row: list, timestamp: datetime.datetime) -> event_data.EventRecord:
        """
        Formats a CSV row as an instance of an `event_data.EventRecord`.
        Accepts a list-formatted row from a GDELT CSV file and the timestamp
        that should be used.
        """

        #
        # The Actor 1 is sometimes missing, but usually there is an Actor 2
        # present when Actor 1 is missing.
        #

        actor_code = (
            row[event_data.EventDataIndexes.Actor1Code] or
            row[event_data.EventDataIndexes.Actor2Code] or
            "NONE"
        )

        #
        # Latitude and Longitude should be grouped
        #

        lati = row[event_data.EventDataIndexes.Actor1Geo_Lat]
        long = row[event_data.EventDataIndexes.Actor1Geo_Long]

        if not (lati and long):
            lati = row[event_data.EventDataIndexes.Actor2Geo_Lat]
            long = row[event_data.EventDataIndexes.Actor2Geo_Long]

        if not (lati and long):
            lati = row[event_data.EventDataIndexes.ActionGeo_Lat]
            long = row[event_data.EventDataIndexes.ActionGeo_Long]

        if not (lati and long):
            lati, long = (0.0, 0.0)

        latitude = float(lati)
        longitude = float(long)

        #
        # Tone and Goldstein
        #

        average_tone = float(
            row[event_data.EventDataIndexes.AvgTone] or
            0.0
        )

        goldstein = float(
            row[event_data.EventDataIndexes.GoldsteinScale] or
            0.0
        )

        return event_data.EventRecord(
            global_event_id=row[event_data.EventDataIndexes.GlobalEventId],
            timestamp=timestamp,
            actor_code=actor_code,
            latitute=latitude,
            longitude=longitude,
            average_tone=average_tone,
            goldstein=goldstein,
        )
