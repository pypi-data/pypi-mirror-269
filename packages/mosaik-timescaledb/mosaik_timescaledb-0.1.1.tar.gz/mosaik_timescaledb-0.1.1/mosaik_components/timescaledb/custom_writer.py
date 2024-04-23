import uuid
from typing import Dict, List

import mosaik_api_v3
import psycopg2
from mosaik_api_v3.datetime import Converter
from pgcopy import CopyManager

META = {
    "type": "time-based",
    "models": {},
}


class CustomWriter(mosaik_api_v3.Simulator):
    """A moasik simulator that uses timescaledb to save the inputs it is given into user defined and created sql tables."""

    _table_col_config: dict
    _schema_name: str
    _table_columns: Dict[str, List[str]]
    _timestamp_col: str
    _run_id_col: str
    _src_col: str
    _run_id: str

    def __init__(self):
        """Init of the class"""
        super().__init__(META)

    def init(
        self,
        sid,
        db_name,
        db_user,
        db_pass,
        time_resolution,
        run_id=None,
        run_id_col="run_id",
        timestamp_col="time",
        src_col="src",
        start_date=None,
        step_size=900,
        db_host="localhost",
        db_port="5432",
        ssl_mode="prefer",
        schema_name="mosaik_schema",
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
        self._step_size = step_size
        if not step_size:
            self.meta["type"] = "event-based"

        if start_date:
            self._time_converter = Converter(
                start_date=start_date,
                time_resolution=time_resolution,
            )

        self._run_id = run_id or f"CustomWriter_run_id_{uuid.uuid4()}"
        self._run_id_col = run_id_col
        self._timestamp_col = timestamp_col
        self._src_col = src_col

        self._schema_name = schema_name
        get_existing_tables = (
            "SELECT table_name FROM information_schema.tables WHERE table_schema = %s;"
        )

        self._cur.execute(get_existing_tables, (self._schema_name,))
        tables = [table for (table,) in self._cur.fetchall()]

        self._table_columns = {}
        for table in tables:
            get_table_columns = """
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = %s AND table_schema = %s;
            """
            self._cur.execute(get_table_columns, (table, self._schema_name))
            self._table_columns[table] = [col for (col,) in self._cur.fetchall()]

        for table in self._table_columns.keys():
            self.meta["models"][table] = {
                "public": True,
                "params": [
                    "src_col",  # Mapping for src_id col
                    "timestamp_col",  # Mapping for ts col
                    "run_id_col",  # Mapping for run_id col
                ],
                "attrs": self._table_columns[table],
            }
        self._table_col_config = {}
        return self.meta

    def create(
        self,
        num,
        model,
        src_col=None,
        timestamp_col=None,
        run_id_col=None,
        **model_params,
    ):
        """Creates the simulator by reading out model parameters and saving them in the class parameters.

        :param num: The number of entities to create
        :type num: int
        :param model: model name in the meta
        :type model: str
        :param run_id: The simulation run id. Defaults to run 1
        :type run_id: str, optional
        :param src_col: Name of the column where the src sim string will be saved. Defaults to 'src'.
        :type src_col: str, optional
        :param ts_col: Name of the column where the timestamp will be saved. Defaults to 'time'.
        :type ts_col: str, optional
        :param run_col: Name of the column where the simulation run id string will be saved. Defaults to 'run_id'.
        :type run_col: str, optional
        :return: A list with the eid and model of the simulator
        :rtype: List[mosaik_api_v3.types.CreateResults]
        """
        errmsg = "The Custom writer simulator only supports one entity per table."

        assert num == 1 and model not in self._table_col_config, errmsg
        self._table_col_config[model] = {
            "src": src_col or self._src_col,
            "run_id": run_id_col or self._run_id_col,
            "timestamp": timestamp_col or self._timestamp_col,
        }
        return [{"eid": f"{model}", "type": model}]

    def step(self, time, inputs, max_advance):
        """Fills in the database for every timestep

        :param time: the timestep of the simulator
        :type time: int
        :param inputs: the inputs of the simulator
        :type inputs: mosaik_api_v3.types.InputData
        :param max_advance: The max allowed advance of the simulator
        :type max_advance: int
        :return: Returns the next timestep time
        :rtype: int
        """
        self.add_to_table(inputs, time)
        if self._step_size:
            return time + self._step_size

    def add_to_table(self, inputs, time):
        """Adds input values to the tables at each timestep

        :param inputs: Inputs to add to tables
        :type inputs: mosaik_api_v3.types.InputData
        :param time: timestep of the simulator
        :type time: int
        """
        for table, data in inputs.items():
            cols = self._table_columns[table]
            col_config = self._table_col_config[table]
            if "local_time" in data:
                timestamp = next(iter(data["local_time"].values()))
            elif self._time_converter:
                timestamp = self._time_converter.datetime_from_step(time)
            else:
                raise ValueError(
                    "must supply start_date in init or local_time at every step"
                )
            # Transpose data into Dict[source, Dict[attr, value]]
            rows = {}
            for attr, srcs in data.items():
                for src, value in srcs.items():
                    rows.setdefault(src, {})[attr] = value
            for src, row in rows.items():
                row[col_config["timestamp"]] = timestamp
                row[col_config["run_id"]] = self._run_id
                row[col_config["src"]] = src
                rows[src] = [row.get(col, None) for col in cols]
            mgr = CopyManager(self._conn, f"{self._schema_name}.{table}", cols)
            mgr.copy(rows.values())
        self._conn.commit()


if __name__ == "__main__":
    mosaik_api_v3.start_simulation(CustomWriter())
