import mosaik_api_v3
import psycopg2
import json
from psycopg2 import sql
from psycopg2.sql import Composed as SQLComposed, Identifier as SQLIdent, SQL
from pgcopy import CopyManager
from mosaik_api_v3.datetime import Converter
from .writer import Writer

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
                "run_id",  # Simulation run name
                "table_type",  # The type of table that will be generated, values can be either saved as str or as json(json/str)
                "table_name",  # Table name used
                "schema_name",  # name of the schema to create the table in
            ],
            "attrs": ["local_time"],
        },
    },
}


class SingleWriter(Writer):
    """A moasik simulator that uses timescaledb to save the inputs it is given into a single sql table."""

    _table_name: str
    _table_type: str
    _schema_name: str
    _run_id: int

    def __init__(self):
        """Init of the class"""
        super().__init__(META)

    def create(
        self,
        num,
        model,
        postgres_mode=False,
        drop_tables=False,
        run_id="1",
        table_name="mosaik_table",
        schema_name="public",
        **model_params,
    ):
        """Creates the simulator by reading out model parameters and saving them in the class parameters.

        :param num: The number of entities to create
        :type num: int
        :param model: model name in the meta
        :type model: str
        :param postgres_mode: Determines if the adapter is in timescale or postgres mode, defaults to False
        :type postgres_mode: bool, optional
        :param drop_tables: Determines if the table is dropped, defaults to False
        :type drop_tables: bool, optional
        :param table_name: Determines the name of the table, defaults to mosaik_table
        :type table_name: str, optional
        :param schema_name: Determines the schema the table is in, defaults to public
        :type schema_name: str, optional
        :return: A list with the eid and model of the simulator
        :rtype: List[mosaik_api_v3.types.CreateResults]
        """
        super().create(num, model, postgres_mode=postgres_mode, drop_tables=drop_tables)
        self._table_name = table_name
        self._run_id = run_id
        self._table_type = model_params["table_type"]
        self._schema_name = schema_name
        return [{"eid": self._eid, "type": model}]

    def create_table_layout(self, inputs):
        """Creates the necessary table for filling in. Created table is dependent on the table type

        :param inputs: The simulator inputs
        :type inputs: mosaik_api_v3.types.InputData
        :raises TypeError: Error gets triggerd when wrong table_type is given
        """
        if self._table_type == "str":
            drop_table = sql.SQL("DROP TABLE IF EXISTS {}.{};").format(
                SQLIdent(self._schema_name), SQLIdent(self._table_name)
            )
            create_table = sql.SQL(
                "CREATE TABLE IF NOT EXISTS {}.{} ( time TIMESTAMPTZ NOT NULL, run_id TEXT, src_sim TEXT, src_entity TEXT, value_type TEXT, value TEXT);"
            ).format(SQLIdent(self._schema_name), SQLIdent(self._table_name))
            create_hyper_table = sql.SQL(
                "SELECT create_hypertable('{}.{}', 'time');"
            ).format(SQLIdent(self._schema_name), SQLIdent(self._table_name))
            # Drop the table if it exists, create a new table and make it into a hyper table
            if self._drop_tables:
                self._cur.execute(drop_table)
            self._cur.execute(create_table)
            if not self._postgres_mode and self._drop_tables:
                self._cur.execute(create_hyper_table)
            self._conn.commit()
        elif self._table_type == "json":
            drop_table = sql.SQL("DROP TABLE IF EXISTS {}.{};").format(
                SQLIdent(self._schema_name), SQLIdent(self._table_name)
            )
            create_table = sql.SQL(
                "CREATE TABLE IF NOT EXISTS {}.{} (time TIMESTAMPTZ NOT NULL, run_id TEXT, value_type TEXT, values json);"
            ).format(SQLIdent(self._schema_name), SQLIdent(self._table_name))
            create_hyper_table = sql.SQL(
                "SELECT create_hypertable('{}.{}', 'time');"
            ).format(SQLIdent(self._schema_name), SQLIdent(self._table_name))
            # Drop the table if it exists, create a new table and make it into a hyper table
            if self._drop_tables:
                self._cur.execute(drop_table)
            self._cur.execute(create_table)
            if not self._postgres_mode and self._drop_tables:
                self._cur.execute(create_hyper_table)
            self._conn.commit()
        else:
            raise TypeError("Given table type is not supported choose str or json.")

    def add_to_table(self, inputs, time):
        """Adds the input values to the table each timestep. Is dependent on the table type

        :param inputs: The inputs of the simulator
        :type inputs: mosaik_api_v3.types.InputData
        :param time: timestep of the simulator
        :type time: int
        :raises TypeError: Error gets triggerd when wrong table_type is given
        """
        data = inputs.get(self._eid, {})
        if "local_time" in data:
            timestamp = next(iter(data["local_time"].values()))
        elif self._time_converter:
            timestamp = self._time_converter.datetime_from_step(time)
        if self._table_type == "str":
            cols = ["time", "run_id", "src_sim", "src_entity", "value_type", "value"]
            mgr = CopyManager(
                self._conn, f"{self._schema_name}.{self._table_name}", cols
            )
            values = []
            # loop over values
            for attr, src_ids in data.items():
                for src_id, val in src_ids.items():
                    src_sim, src_entity = src_id.split(".", 1)
                    values.append(
                        (timestamp, self._run_id, src_sim, src_entity, attr, str(val))
                    )
            # put into database
            mgr.copy(values)
            self._conn.commit()
        elif self._table_type == "json":
            cols = ["time", "run_id", "value_type", "values"]
            mgr = CopyManager(
                self._conn, f"{self._schema_name}.{self._table_name}", cols
            )
            values = []
            # Loop over values
            for attr, src_ids in data.items():
                values.append((timestamp, self._run_id, attr, json.dumps(src_ids)))
            # put into database
            mgr.copy(values)
            self._conn.commit()
        else:
            raise TypeError("Given table type is not supported choose str or json.")


if __name__ == "__main__":
    mosaik_api_v3.start_simulation(SingleWriter())
