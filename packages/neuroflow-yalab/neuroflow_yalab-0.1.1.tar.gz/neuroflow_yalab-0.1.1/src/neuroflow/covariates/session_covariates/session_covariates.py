import warnings
from datetime import timedelta
from typing import ClassVar, Optional

from geopy.geocoders import Nominatim
from meteostat import Hourly, Point

from neuroflow.covariates import Covariate
from neuroflow.files_mapper.files_mapper import FilesMapper

warnings.simplefilter(action="ignore", category=FutureWarning)


class SessionCovariates(Covariate):
    """
    Class to handle the session covariates

    Attributes
    ----------
    mapper : FilesMapper
        The mapper to the files

    Methods
    -------
    _get_timestamp_from_session(session_id:str) -> datetime
        Parse the timestamp of a session from the session id
    """

    TIMESTAMP_FORMAT: ClassVar = "%Y%m%d%H%M"
    COVARIATE_SOURCE: ClassVar = "contextual"
    INCLUDED_SOURCES: ClassVar = {
        "temporal": "temporal",
        "environmental": "environmental",
    }
    DIRECTORY_NAME: ClassVar = "contextual"

    _crf = None

    def __init__(
        self,
        mapper: FilesMapper,
        output_directory: Optional[str] = None,
        location: str = "Tel Aviv University",
    ):
        """
        Constructor for the ParticipantDemographics class

        Parameters
        ----------
        mapper : FilesMapper
            The mapper to the files
        """
        super().__init__(mapper, output_directory)
        self.latitude, self.longitude = self._get_lat_lon(location)

    def _get_lat_lon(self, location: str):
        """
        Get the latitude and longitude of a location

        Parameters
        ----------
        location : str
            The location to get the latitude and longitude

        Returns
        -------
        tuple
            The latitude and longitude of the location
        """
        geolocator = Nominatim(user_agent="neuroflow")
        location = geolocator.geocode(location)
        if location is None:
            raise ValueError(f"Location {location} not found.")
        return location.latitude, location.longitude

    def _parse_timestamp(self):
        """
        Parse the timestamp of the session
        """
        return {
            "timestamp": self.session_timestamp,
            "year": self.session_timestamp.year,
            "month": self.session_timestamp.month,
            "day_of_month": self.session_timestamp.day,
            "day_of_week": self.session_timestamp.weekday(),
            "hour": self.session_timestamp.hour,
        }

    def _get_weather_data(self):
        """
        Get the weather data for the session
        """
        point = Point(self.latitude, self.longitude)
        start = self.session_timestamp - timedelta(hours=1)
        end = self.session_timestamp + timedelta(hours=1)
        weather = Hourly(point, start, end).fetch().reset_index()
        # get the row with the closest timestamp
        weather = weather.iloc[
            [(weather["time"].sub(self.session_timestamp).abs().idxmin())]
        ]
        # dtop the time column
        weather = weather.drop(columns=["time"])
        # make the timestamp the first column
        cols = weather.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        weather = weather[cols]
        return weather.iloc[0].to_dict()

    def get_covariates(self):
        """
        Get the session covariates

        Returns
        -------
        dict
            The session covariates
        """
        return {
            self.INCLUDED_SOURCES.get("temporal"): self._parse_timestamp(),
            self.INCLUDED_SOURCES.get("environmental"): self._get_weather_data(),
        }
