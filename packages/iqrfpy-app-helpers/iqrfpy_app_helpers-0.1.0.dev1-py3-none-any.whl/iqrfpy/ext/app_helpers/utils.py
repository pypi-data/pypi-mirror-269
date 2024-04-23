from datetime import datetime
from sys import stdout
from typing import List, TextIO

from iqrfpy.objects import SensorData
from iqrfpy.utils.sensor_parser import SensorParser
from iqrfpy.utils.sensor_constants import SensorTypes

__all__ = (
    'StringFormatter',
    'PrintUtils',
    'ListManipulation',
    'convert_bytes_to_std_sensor',
    'get_string_between_strings',
)


class StringFormatter:
    """String formatting utility class."""

    DEFAULT_SPACES = 22
    """Default spaces between"""

    @staticmethod
    def format_time(dt: datetime) -> str:
        """Returns a formatted string representing datetime object.

        Args:
            dt (datetime): The datetime object to format.

        Returns:
            str: The formatted datetime string in the format "dd.mm.yyyy  HH:MM:SS.sss".
        """
        return dt.strftime("%d.%m.%Y  %H:%M:%S.%f")[:-3]

    @staticmethod
    def format_pair(text: str, data, spaces: int = DEFAULT_SPACES) -> str:
        """
        Returns a formatted string and data pair with a specific space between them.

        Args:
            text (str): The text to format.
            data: The data to format.
            spaces (int, optional): Minimum width of the text part. Defaults to 22.

        Returns:
            str: The formatted string with the text and data aligned.
        """
        return f'{text:{spaces}} {data}'


class PrintUtils:
    """Print utility class."""

    @staticmethod
    def print_timestamp_pair(text: str, dt: datetime | None = None, spaces: int = StringFormatter.DEFAULT_SPACES,
                             stream: TextIO = stdout):
        """Prints text with formatted timestamp.

        Args:
            text (str): Text to print.
            dt (datetime, optional): datetime object to format. Defaults to datetime.now().
            spaces (int, optional): Minimum width of the text part. Defaults to 22.
            stream (TextIO, optional): Stream to write to. Defaults to sys.stdout.
        """
        if dt is None:
            dt = datetime.now()
        print(
            StringFormatter.format_pair(
                text=text,
                data=StringFormatter.format_time(dt),
                spaces=spaces
            ),
            file=stream
        )

    @staticmethod
    def print_pair(text: str, data, spaces: int = StringFormatter.DEFAULT_SPACES, stream: TextIO = stdout):
        """Prints a formatted pair of text and data.

        Args:
            text (str): Text to print.
            data: Data to print.
            spaces (int, optional): Minimum width of the text part. Defaults to 22.
            stream (TextIO, optional): Stream to write to. Defaults to sys.stdout.
        """
        print(StringFormatter.format_pair(text=text, data=data, spaces=spaces), file=stream)

    @staticmethod
    def print_underlined(text: str, char: str = '-', upper_line: bool = False, line_break: bool = False):
        """Prints a string underlined with a character of choice.

        Args:
            text (str): The text to be printed and underlined.
            char (str, optional): The character used for underlining. Defaults to '-'.
            upper_line (bool, optional): If True, prints a line above the text. Defaults to False.
            line_break (bool, optional): If True, adds a blank line before the underlined text. Defaults to False.
        """
        if line_break:
            print('')
        if upper_line:
            print(f'{char * len(text)}')
        print(f'{text}\n{char * len(text)}')


class ListManipulation:
    """List manipulation utility class."""

    @staticmethod
    def interval_extract(nlist: List[int]):
        """Converts a list of sequential ascending numbers into intervals.

        Args:
           nlist (List[int]): List of sequential numbers.

        Yields:
           List[int]: Intervals as sublists.

        Example:
            >>> ListManipulation.interval_extract([1, 2, 3, 4, 5, 6, 10, 12])
            [[1, 6], [10], [12]]
        """
        length = len(nlist)
        i = 0
        while i < length:
            low = nlist[i]
            while i < length - 1 and nlist[i] + 1 == nlist[i + 1]:
                i += 1
            high = nlist[i]
            if high - low >= 1:
                yield [low, high]
            else:
                yield [low, ]
            i += 1

    @staticmethod
    def get_intervals_from_list(nlist: List[int]) -> str:
        """
        Converts a list of sequential numbers into a formatted string of intervals.

        The function expects a list of unique numbers in ascending order.

        Args:
            nlist (List[int]): List of sequential numbers.

        Returns:
            str: String representing intervals.

        Example:
            >>> ListManipulation.get_intervals_from_list([1, 2, 3, 4, 5, 6, 10, 12])
            '<1,6>, 10, 12'
        """
        tokens = []
        for x in list(ListManipulation.interval_extract(nlist)):
            # Format this [[1, 6], [10], [12]] to this <1,6>, 10, 12
            if len(x) == 1:
                tokens.append(str(x[0]))
            else:
                tokens.append(f'<{x[0]},{x[1]}>')
        return ', '.join(tokens)

    @staticmethod
    def get_list_from_intervals(intervals: str) -> List[int]:
        """
        Converts a string of intervals into a list of numbers.

        Args:
            intervals (str): String representing intervals.

        Returns:
            List[int]: List of numbers.

        Example:
            >>> ListManipulation.get_list_from_intervals('1, <3,6>, 12')
            [1, 3, 4, 5, 6, 12]
        """
        tokens = []
        interval_list = intervals.split(',')
        i = 0
        while i < len(interval_list):
            interval = interval_list[i].strip()

            if interval.startswith('<'):
                # Extract the range within the angle brackets
                start = int(interval[1:])
                i += 1
                end = int(interval_list[i].strip()[:-1])
                tokens += list(range(start, end + 1))
            else:
                tokens.append(int(interval))
            i += 1
        return tokens


def convert_bytes_to_std_sensor(sensor_type: SensorTypes | int, data: List[int]) -> SensorData:
    """Converts raw sensor data into the SensorData object.

    Args:
        sensor_type (Union[SensorTypes, int]): Sensor type (represents a quantity).
        data (List[int]): Data to convert.

    Returns:
        :obj:`SensorData`: SensorData objects containing parsed data.

    Raises:
        ValueError: Raised if passed bytes are shorter than required to process a given sensor type

    Example:
        >>> data = [0x01, 0x02]
        >>> sensor = convert_bytes_to_std_sensor(SensorTypes.TEMPERATURE, data[0:2])
        >>> print(f'{sensor.value} {sensor.unit}')
        '32.0625 ˚C'
    """
    sensors = SensorParser.read_sensors_dpa([sensor_type], data)
    return sensors[0]
