r"""

Contains classes that model responses from the
http://data.gdeltproject.org/gdeltv2/lastupdate.txt web service, which points to
download links for GDELT data formatted as zipped CSVs.

"""

import re
import datetime
from typing import Union, List

LAST_UPDATED_REGEX = re.compile(
    r"^(?P<filesize>\d+) (?P<md5_hash>[\da-f]+) (?P<url>https?://.+/(?P<timestamp>\d+)\.(?P<dataset>\w+)\.csv\.zip)$",
    re.I
)


class LastUpdatedRecord(object):
    """
    Encapsulates individual records from the
    http://data.gdeltproject.org/gdeltv2/lastupdate.txt web service.
    """

    def __init__(self, filesize: str, md5_hash: str, zipfile_url: str, timestamp: str):
        self.filesize = int(filesize)
        self.md5_hash = md5_hash
        self.zipfile_url = zipfile_url
        self.timestamp = datetime.datetime.strptime(timestamp, r"%Y%m%d%H%M%S")


class LastUpdated(object):
    """
    Parses and encapsulates the data that is returned from the
    http://data.gdeltproject.org/gdeltv2/lastupdate.txt web service.
    The web service returns data in the following schema:


        [file size in bytes] [MD5 hash] [base url]/[timestamp].export.CSV.zip
        [file size in bytes] [MD5 hash] [base url]/[timestamp].mentions.CSV.zip
        [file size in bytes] [MD5 hash] [base url]/[timestamp].gkg.csv.zip
    """

    def __init__(self, data: Union[str, List[str]]):
        """
        Initializes an instance of a LastUpdated, which parses and encapsulates
        the data that is returned from the
        http://data.gdeltproject.org/gdeltv2/lastupdate.txt web service.

        :param data: Accepts the full text of the lastupdate.txt file. Also
        accepts a list of strings, each representing a line from the lastupdate.txt
        file.
        """

        if type(data) is str:
            data = data.splitlines()

        self._records = {}

        for line in data:
            match = LAST_UPDATED_REGEX.match(line)

            record = LastUpdatedRecord(
                filesize=match["filesize"],
                md5_hash=match["md5_hash"],
                zipfile_url=match["url"],
                timestamp=match["timestamp"],
            )

            self._records[match["dataset"]] = record

    def get_export_ref(self) -> LastUpdatedRecord:
        """
        Returns the lastupdated.txt record that ended with
        export.CSV.zip.
        """
        return self._records["export"]

    def get_mentions_ref(self) -> LastUpdatedRecord:
        """
        Returns the lastupdated.txt record that ended with
        mentions.CSV.zip.
        """
        return self._records["mentions"]

    def get_gkg_ref(self) -> LastUpdatedRecord:
        """
        Returns the lastupdated.txt record that ended with
        gkg.CSV.zip.
        """
        return self._records["gkg"]
