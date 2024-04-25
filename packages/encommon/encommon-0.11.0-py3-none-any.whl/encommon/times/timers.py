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
from .timer import Timer
from .times import Times

if TYPE_CHECKING:
    from .params import TimerParams
    from .params import TimersParams



CACHE_TABLE = (
    """
    create table if not exists
     {0} (
      "group" text not null,
      "unique" text not null,
      "update" text not null,
     primary key (
      "group", "unique"));
    """)  # noqa: LIT003



TIMERS = dict[str, Timer]



class Timers:
    """
    Track timers on unique key determining when to proceed.

    .. warning::
       This class will use an in-memory database for cache,
       unless a cache file is explicity defined.

    .. testsetup::
       >>> from .params import TimerParams
       >>> from .params import TimersParams
       >>> from time import sleep

    Example
    -------
    >>> source = {'one': TimerParams(timer=1)}
    >>> params = TimersParams(timers=source)
    >>> timers = Timers(params)
    >>> timers.ready('one')
    False
    >>> sleep(1)
    >>> timers.ready('one')
    True

    :param params: Parameters for instantiating the instance.
    :param file: Optional path to file for SQLite database,
        allowing for state retention between the executions.
    :param table: Optional override for default table name.
    :param group: Optional override for default group name.
    """

    __params: 'TimersParams'

    __sqlite: Connection
    __file: str
    __table: str
    __group: str

    __timers: TIMERS


    def __init__(
        self,
        params: 'TimersParams',
        *,
        file: str = ':memory:',
        table: str = 'timers',
        group: str = 'default',
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.__params = params


        sqlite = SQLite(file)

        sqlite.execute(
            CACHE_TABLE
            .format(table))

        sqlite.commit()

        self.__sqlite = sqlite
        self.__file = file
        self.__table = table
        self.__group = group


        self.__timers = {}

        self.load_children()


    @property
    def params(
        self,
    ) -> 'TimersParams':
        """
        Return the Pydantic model containing the configuration.

        :returns: Pydantic model containing the configuration.
        """

        return self.__params


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
    ) -> dict[str, Timer]:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return dict(self.__timers)


    def load_children(
        self,
    ) -> None:
        """
        Construct the children instances for the primary class.
        """

        params = self.__params
        timers = self.__timers

        sqlite = self.__sqlite
        table = self.__table
        group = self.__group


        config = params.timers


        cursor = sqlite.execute(
            f"""
            select * from {table}
            where "group"="{group}"
            order by "unique" asc
            """)  # noqa: LIT003

        records = cursor.fetchall()

        for record in records:

            unique = record[1]
            update = record[2]

            if unique not in config:
                continue

            _config = config[unique]

            _config.start = update


        items = config.items()

        for key, value in items:

            if key in timers:

                timer = timers[key]

                timer.update(
                    value.start)

                continue

            timer = Timer(
                value.timer,
                start=value.start)

            timers[key] = timer


        self.__timers = timers


    def save_children(
        self,
    ) -> None:
        """
        Save the child caches from the attribute into database.
        """

        timers = self.__timers

        sqlite = self.__sqlite
        table = self.__table
        group = self.__group


        insert = tuple[
            str,  # group
            str,  # unique
            str]  # update

        inserts: list[insert] = []

        items = timers.items()

        for unique, timer in items:

            append = (
                group, unique,
                Times('now').subsec)

            inserts.append(append)


        statement = (
            f"""
            replace into {table}
            ("group", "unique",
             "update")
            values (?, ?, ?)
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

        timers = self.__timers

        if unique not in timers:
            raise ValueError('unique')

        timer = timers[unique]

        return timer.ready(update)


    def create(
        self,
        unique: str,
        params: 'TimerParams',
    ) -> Timer:
        """
        Create a new timer using the provided input parameters.

        :param unique: Unique identifier for the related child.
        :param params: Parameters for instantiating the instance.
        :returns: Newly constructed instance of related class.
        """

        timers = self.params.timers

        self.save_children()

        if unique in timers:
            raise ValueError('unique')

        timers[unique] = params

        self.load_children()

        return self.children[unique]


    def update(
        self,
        unique: str,
        value: Optional[PARSABLE] = None,
    ) -> None:
        """
        Update the timer from the provided parasable time value.

        :param unique: Unique identifier for the related child.
        :param value: Override the time updated for timer value.
        """

        timers = self.__timers

        if unique not in timers:
            raise ValueError('unique')

        timer = timers[unique]

        return timer.update(value)


    def delete(
        self,
        unique: str,
    ) -> None:
        """
        Delete the timer from the internal dictionary reference.

        :param unique: Unique identifier for the related child.
        """

        timers = self.__timers

        if unique not in timers:
            raise ValueError('unique')

        del timers[unique]
