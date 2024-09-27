"""dttm_utils.py"""

from datetime import datetime, timezone
from typing import Optional, Union

# Default formats
DEFAULT_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"


class DateUtils:
    @staticmethod
    def get_dttm_local(serialized: bool = False) -> Union[datetime, str]:
        """
        Get the current local (timezone aware) datetime or its ISO 8601 string representation.

        Args:
            serialized (bool): Whether to return the datetime as an ISO 8601 string. Defaults to False.

        Returns:
            Union[datetime, str]: The current local datetime object or its ISO 8601 string representation.

        Examples:
            >>> DateUtils.get_dttm_local()
            datetime.datetime(2024, 9, 22, 15, 30, 45, 123456, tzinfo=datetime.timezone.utc)

            >>> DateUtils.get_dttm_local(serialized=True)
            '2024-09-22T15:30:45.123+05:30'
        """
        dt = datetime.now(timezone.utc).astimezone()

        return DateUtils.serialize_to_iso(dt, with_tz=True) if serialized else dt

    @staticmethod
    def get_dttm_utc(serialized: bool = False) -> Union[datetime, str]:
        """
        Get the current UTC datetime or its ISO 8601 string representation.

        Args:
            serialized (bool): Whether to return the datetime as an ISO 8601 string. Defaults to False.

        Returns:
            Union[datetime, str]: The current UTC datetime object or its ISO 8601 string representation.

        Examples:
            >>> DateUtils.get_dttm_utc()
            datetime.datetime(2024, 9, 22, 15, 30, 45, 123456, tzinfo=datetime.timezone.utc)

            >>> DateUtils.get_dttm_utc(serialized=True)
            '2024-09-22T15:30:45.123Z'
        """
        dt = datetime.now(timezone.utc).astimezone(timezone.utc)
        return DateUtils.serialize_to_iso(dt) if serialized else dt

    @staticmethod
    def serialize_to_iso(dt: Optional[datetime], with_tz: bool = False) -> Optional[str]:
        """
        Serialize a datetime object to an ISO 8601 string.

        Args:
            dt (Optional[datetime]): The datetime object to serialize.
            with_tz (bool): Whether to include timezone information in the output string. Defaults to False.

        Returns:
            Optional[str]: The ISO 8601 formatted string. Includes timezone info if with_tz is True.

        Examples:
            >>> DateUtils.serialize_to_iso(datetime(2024, 9, 22, 15, 30, 45, 123456, tzinfo=datetime.timezone.utc))
            '2024-09-22T15:30:45.123+00:00'

            >>> DateUtils.serialize_to_iso(datetime(2024, 9, 22, 15, 30, 45, 123456), with_tz=False)
            '2024-09-22T15:30:45.123Z'
        """
        if dt:
            if not with_tz:
                return dt.replace(tzinfo=None).isoformat(timespec="milliseconds") + "Z"
            else:
                return dt.isoformat(timespec="milliseconds")
        return None

    @staticmethod
    def deserialize_from_iso(dt_str: Optional[str]) -> Optional[datetime]:
        """
        Deserialize an ISO 8601 string to a datetime object.

        Args:
            dt_str (Optional[str]): The ISO 8601 string to deserialize.

        Returns:
            Optional[datetime]: The deserialized datetime object.

        Examples:
            >>> DateUtils.deserialize_from_iso('2024-09-22T15:30:45.123+00:00')
            datetime.datetime(2024, 9, 22, 15, 30, 45, 123000, tzinfo=datetime.timezone.utc)

            >>> DateUtils.deserialize_from_iso('2024-09-22T15:30:45.123Z')
            datetime.datetime(2024, 9, 22, 15, 30, 45, 123000, tzinfo=datetime.timezone.utc)
        """
        if dt_str:
            try:
                # Handle 'Z' as UTC
                return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
            except ValueError:
                raise ValueError(f"Invalid ISO 8601 string: {dt_str}")
        return None
