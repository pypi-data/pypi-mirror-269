"""Primary python module for interacting with signal data in the DPD.

This module contains the InfluxClient and it's primary functions.
These functions allow a user to interact with an underlying DPD (InfluxDB)
to read and upload signal data. This module relies on four Influx env
variables to query the correct system.

Typical usage example:

  client = InfluxCLient(
    INFLUX_BUCKET,
    INFLUX_TOKEN,
    INFLUX_ORG,
    INFLUX_URL
  )
  data = client.record_infrasound(
    type,
    value,
    station,
    timestamp
  )
"""

import json
from datetime import datetime, timedelta, timezone
from typing import Any, List

from dpd_lib.client.exceptions import (
    BadQueryException,
    BucketNotFoundException,
    InfluxNotAvailableException,
)
from dpd_lib.models import InfluxRecord
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.rest import ApiException
from loguru import logger
from pydantic import SecretStr
from urllib3.exceptions import NewConnectionError

INFRASOUND_TYPES = ["", "mccm", "velocity", "rsam", "pressure", "azimuth"]
SEISMIC_YPES = ["", "rsam"]


class InfluxClient:
    """
    A restricted client which implements an interface
    to query data from the influx database.

    Attributes:
        bucket (str): InfluxDB Bucket to query.
        _client (InfluxDBClient): The instantiated
            InfluxDB client.
    """

    def __init__(
        self, bucket: str, token: SecretStr, org: str, url: str
    ) -> None:
        """
        Initializes the InfluxDB Client based-off bucket, org, and url.
        Also requires an API token.

        Args:
            bucket (str): InfluxDB Bucket to query.
            token (SecretStr): InfluxDB API token.
            org (str): InfluxDB organization to query.
            url (str): InfluxDB url.
        """
        self.bucket = bucket
        self._client = InfluxDBClient(
            url=url, token=token.get_secret_value(), org=org
        )

    async def record_seismic(
        self, type: str, value: float, station: str, timestamp: datetime
    ) -> None:
        """
        Records new seismic record for a given timestamp

        Arguments:
            type (str): The type of seismic record
            value (float): The value of the record
            station (str): The associated station
            timestamp (datetime): The timestamp

        Returns:
            None

        Raises:
            InfluxNotAvailableException: An error occurred
                while contacting the InfluxDB.
            BadQueryException: There is an issue with the
                influx query.
            BucketNotFoundException: The requested bucket
            is not present in the DB.
        """
        if type not in SEISMIC_YPES:
            raise BadQueryException(
                f"Seismic type not accepted. Accepted types: {SEISMIC_YPES}."
            )
        p = (
            Point(type)
            .tag("station", station)
            .field(type, value)
            .time(timestamp)
        )
        await self._insert(p)

    async def read_seismic(
        self,
        type: str = "",
        stations: List[str] = [],
        t0: datetime = datetime.now(timezone.utc) - timedelta(seconds=15),
        t1: datetime = datetime.now(timezone.utc),
    ) -> List[InfluxRecord]:
        """
        Reads seismic records for a given type, station list, and timestamp

        Arguments:
            type (str): The type of seismic record
            station (List(str)): The station of seismic record
            t0 (datetime): the beginning of the timerange
            t1 (datetime): The end of the timerange

        Returns:
            List[InfluxRecord]: All records of a
            certain type for a given range.

        Raises:
            InfluxNotAvailableException: An error occurred
                while contacting the InfluxDB.
            BadQueryException: There is an issue with the
                influx query.
            BucketNotFoundException: The requested bucket
            is not present in the DB.
        """
        if type not in SEISMIC_YPES:
            raise BadQueryException(
                f"Seismic type not accepted. Accepted types: {SEISMIC_YPES}."
            )
        query = """from(bucket:"{0}")
        |> range(start: {1}, stop: {2})""".format(
            self.bucket,
            t0.strftime("%Y-%m-%dT%H:%M:%SZ"),
            t1.strftime("%Y-%m-%dT%H:%M:%SZ"),
        )
        if type != "":
            query += '|> filter(fn:(r) => r._measurement == "{0}")'.format(
                type
            )
        if len(stations) != 0:
            query += """
            |> filter(fn:(r) => contains(value: r.station, set: {0}))
            """.format(
                json.dumps(stations)
            )
        return await self._query(query)

    async def record_infrasound(
        self, type: str, value: float, station: str, timestamp: datetime
    ) -> None:
        """
        Records new infrasound record for a given timestamp

        Arguments:
            type (str): The type of infrasound record
            value (float): The value of the record
            station (str): The associated station
            timestamp (datetime): The timestamp

        Returns:
            None

        Raises:
            InfluxNotAvailableException: An error occurred
                while contacting the InfluxDB.
            BadQueryException: There is an issue with the
                influx query.
            BucketNotFoundException: The requested bucket
            is not present in the DB.
        """
        if type not in INFRASOUND_TYPES:
            raise BadQueryException(
                f"Type not accepted. Accepted types: {INFRASOUND_TYPES}."
            )
        p = (
            Point(type)
            .tag("station", station)
            .field(type, value)
            .time(timestamp)
        )
        await self._insert(p)

    async def read_infrasound(
        self,
        type: str = "",
        stations: List[str] = [],
        t0: datetime = datetime.now(timezone.utc) - timedelta(seconds=15),
        t1: datetime = datetime.now(timezone.utc),
    ) -> List[InfluxRecord]:
        """
        Reads infrasound records for a given type, station list, and timestamp

        Arguments:
            type (str): The type of infrasound record
            station (List(str)): The station of infrasound record
            t0 (datetime): the beginning of the timerange
            t1 (datetime): The end of the timerange

        Returns:
            List[InfluxRecord]: All records of a
            certain type for a given range.

        Raises:
            InfluxNotAvailableException: An error occurred
                while contacting the InfluxDB.
            BadQueryException: There is an issue with the
                influx query.
            BucketNotFoundException: The requested bucket
            is not present in the DB.
        """
        if type not in INFRASOUND_TYPES:
            raise BadQueryException(
                f"Type not accepted. Accepted types: {INFRASOUND_TYPES}."
            )
        query = """from(bucket:"{0}")
        |> range(start: {1}, stop: {2})""".format(
            self.bucket,
            t0.strftime("%Y-%m-%dT%H:%M:%SZ"),
            t1.strftime("%Y-%m-%dT%H:%M:%SZ"),
        )
        if type != "":
            query += '|> filter(fn:(r) => r._measurement == "{0}")'.format(
                type
            )
        if len(stations) != 0:
            query += """
            |> filter(fn:(r) => contains(value: r.station, set: {0}))
            """.format(
                json.dumps(stations)
            )
        return await self._query(query)

    async def list_records(
        self,
        t0: datetime = datetime.now(timezone.utc) - timedelta(seconds=15),
        t1: datetime = datetime.now(timezone.utc),
    ) -> List[InfluxRecord]:
        """
        Lists all records for given time range.

        Arguments:
            t0 (datetime): the beginning of the timerange
            t1 (datetime): The end of the timerange

        Returns:
            List[InfluxRecord]:
                All records for given time range.

        Raises:
            InfluxNotAvailableException: An error occurred
                while contacting the InfluxDB.
            BadQueryException: There is an issue with the
                influx query.
            BucketNotFoundException: The requested bucket
            is not present in the DB.
        """
        query = """from(bucket:"{0}")
        |> range(start: {1}, stop: {2})""".format(
            self.bucket,
            t0.strftime("%Y-%m-%dT%H:%M:%SZ"),
            t1.strftime("%Y-%m-%dT%H:%M:%SZ"),
        )
        return await self._query(query)

    async def _insert(self, p: Point) -> Any:
        """
        Inserts a point into the database via InfluxDB write_api

        Arguments:
            p (Point): The data point to insert into the database

        Returns:
            Any: Results from the write_api

        Raises:
            InfluxNotAvailableException: An error occurred
                while contacting the InfluxDB.
            BadQueryException: There is an issue with the
                influx query.
            BucketNotFoundException: The requested bucket
            is not present in the DB.
        """
        write_api = self._client.write_api(write_options=SYNCHRONOUS)
        try:
            res = write_api.write(bucket=self.bucket, record=p)
        except NewConnectionError:
            raise InfluxNotAvailableException()
        except ApiException as e:
            if e.status and e.status == 400:
                raise BadQueryException()
            if e.status and e.status == 404:
                raise BucketNotFoundException()
            raise InfluxNotAvailableException()
        logger.info(f"{res=}")
        return res

    async def _query(self, query: str = "") -> List[InfluxRecord]:
        """
        Queries the InfluxDB with the proivded query string

        Arguments:
            query (str): The raw query string to pass to InfluxDB

        Returns:
            List[InfluxRecord]:
                A list of records that match the query

        Raises:
            InfluxNotAvailableException: An error occurred
                while contacting the InfluxDB.
            BadQueryException: There is an issue with the
                influx query.
            BucketNotFoundException: The requested bucket
            is not present in the DB.
        """
        logger.debug(f"Running {query=}")
        query_api = self._client.query_api()
        try:
            result = query_api.query(query=query)
        except NewConnectionError:
            raise InfluxNotAvailableException()
        except ApiException as e:
            if e.status and e.status == 400:
                raise BadQueryException()
            if e.status and e.status == 404:
                raise BucketNotFoundException()
            raise InfluxNotAvailableException()
        res = []
        for table in result:
            for record in table.records:
                r = InfluxRecord(
                    type=record.get_measurement(),
                    station=record.values.get("station"),
                    timestamp=record.get_time(),
                    value=record.get_value(),
                )
                res.append(r)
        logger.debug(f"Query returned {len(res)} records.")
        return res
