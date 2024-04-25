"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from sqlite3 import Connection
from sqlite3 import connect as SQLite
from typing import Optional
from typing import TYPE_CHECKING

from .common import PARSABLE
from .times import Times
from .window import Window

if TYPE_CHECKING:
    from .params import WindowParams
    from .params import WindowsParams



CACHE_TABLE = (
    """
    create table if not exists
     {0} (
      "group" text not null,
      "unique" text not null,
      "last" text not null,
      "next" text not null,
      "update" text not null,
     primary key (
      "group", "unique"));
    """)  # noqa: LIT003



WINDOWS = dict[str, Window]



class Windows:
    """
    Track windows on unique key determining when to proceed.

    .. warning::
       This class will use an in-memory database for cache,
       unless a cache file is explicity defined.

    .. testsetup::
       >>> from .params import WindowParams
       >>> from .params import WindowsParams

    Example
    -------
    >>> source = {'one': WindowParams(window=1)}
    >>> params = WindowsParams(windows=source)
    >>> windows = Windows(params, '-2s', 'now')
    >>> [windows.ready('one') for x in range(3)]
    [True, True, False]

    :param params: Parameters for instantiating the instance.
    :param start: Determine the start for scheduling window.
    :param stop: Determine the ending for scheduling window.
    :param file: Optional path to file for SQLite database,
        allowing for state retention between the executions.
    :param table: Optional override for default table name.
    :param group: Optional override for default group name.
    """

    __params: 'WindowsParams'

    __start: Times
    __stop: Times

    __sqlite: Connection
    __file: str
    __table: str
    __group: str

    __windows: WINDOWS


    def __init__(  # noqa: CFQ002
        self,
        params: 'WindowsParams',
        start: PARSABLE = 'now',
        stop: PARSABLE = '3000-01-01',
        *,
        file: str = ':memory:',
        table: str = 'windows',
        group: str = 'default',
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.__params = params


        start = Times(start)
        stop = Times(stop)

        assert stop > start

        self.__start = start
        self.__stop = stop


        sqlite = SQLite(file)

        sqlite.execute(
            CACHE_TABLE
            .format(table))

        sqlite.commit()

        self.__sqlite = sqlite
        self.__file = file
        self.__table = table
        self.__group = group


        self.__windows = {}

        self.load_children()


    @property
    def params(
        self,
    ) -> 'WindowsParams':
        """
        Return the Pydantic model containing the configuration.

        :returns: Pydantic model containing the configuration.
        """

        return self.__params


    @property
    def start(
        self,
    ) -> Times:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return Times(self.__start)


    @property
    def stop(
        self,
    ) -> Times:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return Times(self.__stop)


    @property
    def sqlite(
        self,
    ) -> Connection:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__sqlite


    @property
    def file(
        self,
    ) -> str:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__file


    @property
    def table(
        self,
    ) -> str:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__table


    @property
    def group(
        self,
    ) -> str:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__group


    @property
    def children(
        self,
    ) -> dict[str, Window]:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return dict(self.__windows)


    def load_children(
        self,
    ) -> None:
        """
        Construct the children instances for the primary class.
        """

        params = self.__params
        windows = self.__windows

        start = self.__start
        stop = self.__stop

        sqlite = self.__sqlite
        table = self.__table
        group = self.__group


        config = params.windows


        cursor = sqlite.execute(
            f"""
            select * from {table}
            where "group"="{group}"
            order by "unique" asc
            """)  # noqa: LIT003

        records = cursor.fetchall()

        for record in records:

            unique = record[1]
            next = record[3]

            if unique not in config:
                continue

            _config = config[unique]

            _config.start = next
            _config.anchor = next


        items = config.items()

        for key, value in items:

            if key in windows:

                window = windows[key]

                window.update(
                    value.start)

                continue

            _start = (
                value.start or start)

            _stop = (
                value.stop or stop)

            if _start < start:
                _start = start

            if _stop > stop:
                _stop = stop

            _anchor = (
                value.anchor or _start)

            window = Window(
                value.window,
                start=_start,
                stop=_stop,
                anchor=_anchor,
                delay=value.delay)

            windows[key] = window


        self.__windows = windows


    def save_children(
        self,
    ) -> None:
        """
        Save the child caches from the attribute into database.
        """

        windows = self.__windows

        sqlite = self.__sqlite
        table = self.__table
        group = self.__group


        insert = tuple[
            str,  # group
            str,  # unique
            str,  # last
            str,  # next
            str]  # update

        inserts: list[insert] = []

        items = windows.items()

        for unique, window in items:

            append = (
                group, unique,
                window.last.subsec,
                window.next.subsec,
                Times('now').subsec)

            inserts.append(append)


        statement = (
            f"""
            replace into {table}
            ("group", "unique",
             "next", "last",
             "update")
            values (?, ?, ?, ?, ?)
            """)  # noqa: LIT003

        sqlite.executemany(
            statement,
            tuple(sorted(inserts)))

        sqlite.commit()


    def ready(
        self,
        unique: str,
        update: bool = True,
    ) -> bool:
        """
        Determine whether or not the appropriate time has passed.

        :param unique: Unique identifier for the related child.
        :param update: Determines whether or not time is updated.
        :returns: Boolean indicating whether enough time passed.
        """

        windows = self.__windows

        if unique not in windows:
            raise ValueError('unique')

        window = windows[unique]

        return window.ready(update)


    def create(
        self,
        unique: str,
        params: 'WindowParams',
    ) -> Window:
        """
        Create a new window using the provided input parameters.

        :param unique: Unique identifier for the related child.
        :param params: Parameters for instantiating the instance.
        :returns: Newly constructed instance of related class.
        """

        windows = self.params.windows

        self.save_children()

        if unique in windows:
            raise ValueError('unique')

        windows[unique] = params

        self.load_children()

        return self.children[unique]


    def update(
        self,
        unique: str,
        value: Optional[PARSABLE] = None,
    ) -> None:
        """
        Update the window from the provided parasable time value.

        :param unique: Unique identifier for the related child.
        :param value: Override the time updated for window value.
        """

        windows = self.__windows

        if unique not in windows:
            raise ValueError('unique')

        window = windows[unique]

        return window.update(value)


    def delete(
        self,
        unique: str,
    ) -> None:
        """
        Delete the window from the internal dictionary reference.

        :param unique: Unique identifier for the related child.
        """

        windows = self.__windows

        if unique not in windows:
            raise ValueError('unique')

        del windows[unique]
