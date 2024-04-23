from __future__ import annotations
import mosaik_api_v3
import psycopg2
import json
from pgcopy import CopyManager
from mosaik_api_v3.datetime import Converter

META = {
    "type": "time-based",
    "models": {
        "Database": {
            "public": True,
            "any_inputs": True,
            "params": [
                "db_name",  # the database name for the timescaldb
                "db_user",  # the database user
                "db_pass",  # the database password
                "db_host",  # the database host networkaddress
                "db_port",  # the database port
                "ssl_mode",  # the ssl_mode, require for remote and prefer for standard use
                "postgres_mode",  # Enables postgres mode if true and does not create a hypertable
                "drop_tables",  # Determines if the tables should be dropped or not(if they already exists)
            ],
            "attrs": ["local_time"],
        },
    },
}


class Writer(mosaik_api_v3.Simulator):
    """A Mosaik Simulator that uses Timescaledb to save the inputs it is given this class serves as a parent class and should not be used on its own."""

    _eid: str
    _db_name: str
    _db_user: str
    _db_pass: str
    _db_host: str
    _db_port: str
    _ssl_mode: str
    _step_size: int | None
    _conn: None
    _cur: None
    _attr_dict: None
    _postgres_mode: bool
    _first_step: bool
    _drop_tables: bool

    def __init__(self, META):
        """The init function of the Class

        :param META: The META information of the entity
        :type META: dict
        """

        super().__init__(META)
        self._eid = "TimescaleDB"

    def init(
        self,
        sid,
        db_name,
        db_user,
        db_pass,
        time_resolution,
        start_date=None,
        step_size=900,
        db_host="localhost",
        db_port="5432",
        ssl_mode="prefer",
    ):
        """mosaik specific init function, sets start date and decides if Simulator is event or time based and initiates the database connection.

        :param db_name: The database name
        :type db_name: str
        :param db_user: The name of the database user
        :type db_user: str
        :param db_pass: The database password
        :type db_pass: str
        :param sid: ID of the Simulator
        :type sid: str
        :param time_resolution: Time resolution of the Simulator
        :type time_resolution: float
        :param start_date: The start date of the simulato, defaults to None
        :type start_date: str, optional
        :param step_size: The steo size of the Simulator, defaults to 900
        :type step_size: int, optional
        :param db_host: The database host address, defaults to "localhost"
        :type db_host: str, optional
        :param db_port: The database port, defaults to "5432"
        :type db_port: str, optional
        :param ssl_mode: The ssl mode of the database, defaults to "prefer"
        :type ssl_mode: str, optional
        :return: The metadata of the simulator
        :rtype: mosaik_api_v3.types.Meta
        """
        # add table columns to attr
        self._db_user = db_user
        self._db_pass = db_pass
        self._db_host = db_host
        self._db_port = db_port
        self._db_name = db_name
        self._ssl_mode = ssl_mode
        connection = f"postgres://{self._db_user}:{self._db_pass}@{self._db_host}:{self._db_port}/{self._db_name}?sslmode={self._ssl_mode}"
        self._conn = psycopg2.connect(
            connection,
            keepalives=1,
            keepalives_idle=30,
            keepalives_interval=10,
            keepalives_count=5,
        )
        self._cur = self._conn.cursor()
        if step_size:
            self._step_size = step_size
        else:
            self.meta["type"] = "event-based"
            self._first_step = True

        if start_date:
            self._time_converter = Converter(
                start_date=start_date,
                time_resolution=time_resolution,
            )
        return self.meta

    def create(self, num, model, **model_params):
        """Creates the Simulator, reads out model parameters and safes them as class parameters.

        :param num: The number of entities to create
        :type num: int
        :param model: Name of the model in the meta
        :type model: str
        :return: List of eid and model
        :rtype: List[mosaik_api_v3.types.CreateResult]
        """
        self._postgres_mode = model_params["postgres_mode"]
        self._drop_tables = model_params["drop_tables"]
        return [{"eid": self._eid, "type": model}]

    def step(self, time, inputs, max_advance):
        """Creates the DB in timestep zero, in every subsequent step it fills database

        :param time: The current timestep
        :type time: int
        :param inputs: The inputs of the simulator
        :type inputs: mosaik_api_v3.types.InputData
        :param max_advance: The maximal advance allowed for this simulator
        :type max_advance: int
        :return: The next time the simulator gets called
        :rtype: Optional[int]
        """
        # Check what exists at timestep 0 and Create Databases from it
        if time == 0 or self._first_step:
            self._first_step = False
            self.create_table_layout(inputs)
        self.add_to_table(inputs, time)
        if self._step_size:
            return time + self._step_size

    def create_table_layout(self, inputs):
        """Creates the necessary tables for filling in. Is not implemented here.

        :param inputs: Needed inputs for putting the right types in tables multiple
        :type inputs: mosaik_api_v3.types.InputData
        :raises TypeError: Raises typerror since function is not implemented
        """
        raise TypeError("Function not implemented in parent class")

    def add_to_table(self, inputs, time):
        """Adds the input values to the tables each timestep. Is not implemented here

        :param inputs: The inputs needed
        :type inputs: mosaik_api_v3.types.InputData
        :param time: The timestep of the simulator
        :type time: int
        :raises TypeError: Raises typerror since function is not implemented
        """
        raise TypeError("Function not implemented in parent class")

    def get_data(self, outputs):
        """Not needed, function exists because of inheritance

        :param outputs: outputs of the simulator
        :type outputs: mosaik_api_v3.types.OutputRequest
        :return: outputs
        :rtype: mosaik_api_v3.types.OutputData
        """
        return {}

    def finalize(self):
        """Makes sure to close all existing connectons to the database.

        :return: _description_
        :rtype: _type_
        """
        self._cur.close()
        self._conn.close()
        return super().finalize()


if __name__ == "__main__":
    print("Not a class that should be used")
