r"""

Contains classes and enumerations that model the GDELT CSV schema.

"""

import datetime


class EventDataIndexes(object):
    """
    Enumeration for the column indexes for GDELT CSV data. The CSV-formatted
    GDELT data is often provided without any column headers, so values must be
    indexed via integers.
    """

    # EVENTID AND DATE ATTRIBUTES
    GlobalEventId = 0
    YearMonthDay = 1
    YearMonth = 2
    Year = 3
    FractionDate = 4

    # ACTOR ATTRIBUTES
    Actor1Code = 5
    Actor1Name = 6
    Actor1CountryCode = 7
    Actor1KnownGroupCode = 8
    Actor1EthnicCode = 9
    Actor1Religion1Code = 10
    Actor1Religion2Code = 11
    Actor1Type1Code = 12
    Actor1Type2Code = 13
    Actor1Type3Code = 14

    Actor2Code = 15
    Actor2Name = 16
    Actor2CountryCode = 17
    Actor2KnownGroupCode = 18
    Actor2EthnicCode = 19
    Actor2Religion1Code = 20
    Actor2Religion2Code = 21
    Actor2Type1Code = 22
    Actor2Type2Code = 23
    Actor2Type3Code = 24

    # EVENT ACTION ATTRIBUTES
    IsRootEvent = 25
    EventCode = 26
    EventBaseCode = 27
    EventRootCode = 28
    QuadClass = 29
    GoldsteinScale = 30
    NumMentions = 31
    NumSources = 32
    NumArticles = 33
    AvgTone = 34

    # EVENT GEOGRAPHY
    Actor1Geo_Type = 35
    Actor1Geo_Fullname = 36
    Actor1Geo_CountryCode = 37
    Actor1Geo_ADM1Code = 38
    Actor1Geo_ADM2Code = 39
    Actor1Geo_Lat = 40
    Actor1Geo_Long = 41
    Actor1Geo_FeatureID = 42

    Actor2Geo_Type = 43
    Actor2Geo_Fullname = 44
    Actor2Geo_CountryCode = 45
    Actor2Geo_ADM1Code = 46
    Actor2Geo_ADM2Code = 47
    Actor2Geo_Lat = 48
    Actor2Geo_Long = 49
    Actor2Geo_FeatureID = 50

    ActionGeo_Type = 51
    ActionGeo_Fullname = 52
    ActionGeo_CountryCode = 53
    ActionGeo_ADM1Code = 54
    ActionGeo_ADM2Code = 55
    ActionGeo_Lat = 56
    ActionGeo_Long = 57
    ActionGeo_FeatureID = 58

    # DATA MANAGEMENT FIELDS
    DateAdded = 59
    SourceURL = 60


class EventRecord(object):
    """
    Encapsulates the fields that are consumed by the endpoint.
    """

    def __init__(self, global_event_id: str, timestamp: datetime.datetime,
                 actor_code: str, latitute: float, longitude: float,
                 average_tone: float, goldstein: float,
                 ):
        self.global_event_id = global_event_id
        self.timestamp = timestamp
        self.actor_code = actor_code
        self.latitute = latitute
        self.longitude = longitude
        self.average_tone = average_tone
        self.goldstein = goldstein

    def to_dict(self) -> dict:
        """
        Returns a plain-dict, JSON-serializable object that matches the input
        schema required by the recipient's HTTP POST endpoint. The result of this
        method can be JSON serialized to the endpoint that consumes this data.
        """

        return {
            "data": {
                "avg_tone": self.average_tone,
                "goldstein": self.goldstein,
                "actor_code": self.actor_code,
                "lat": self.latitute,
                "lon": self.longitude,
                "date": self.timestamp.strftime(r"%Y-%m-%d %H:%M:%S"),
            }
        }
