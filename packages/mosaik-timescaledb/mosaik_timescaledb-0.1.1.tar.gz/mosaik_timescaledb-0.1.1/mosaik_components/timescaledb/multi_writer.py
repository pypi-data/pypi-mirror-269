import mosaik_api_v3
import psycopg2
import json
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
                "schema_name",  # Schema name used
            ],
            "attrs": ["local_time"],
        },
    },
}


class MultiWriter(Writer):
    """A moasik simulator that uses timescaledb to save the inputs it is given into multiple sql tables under a single schema."""

    _schema_name: str
    _attr_dict: None
    _entities: None
    _run_id: int

    def __init__(self):
        """Init of the class"""
        super().__init__(META)
        self._entities = []

    def create(
        self,
        num,
        model,
        postgres_mode=False,
        drop_tables=False,
        run_id="run 1",
        schema_name="mosaik_schema",
        **model_params,
    ):
        """Creates the simulator by reading out model parameters and saving them in the class parameters.

        :param num: The number of entities to create
        :type num: int
        :param model: model name in the meta
        :type model: str
        :param postgres_mode: Determines if the adapter is in timescale or postgres mode, defaults to False
        :type postgres_mode: bool, optional
        :param drop_tables: Determines if the tables and schema are dropped, defaults to False
        :type drop_tables: bool, optional
        :return: A list with the eid and model of the simulator
        :rtype: List[mosaik_api_v3.types.CreateResults]
        """
        super().create(
            num,
            model,
            postgres_mode=postgres_mode,
            drop_tables=drop_tables,
        )
        self._run_id = run_id
        self._schema_name = schema_name
        new_entities = [
            {"eid": f"{self._eid}-{i}", "type": model}
            for i in range(num + len(self._entities))
        ]
        self._entities.extend(new_entities)
        return new_entities

    def get_postgrestype(self, datatype: type):
        """Returns a string with the wanted postgres datatype from the given datatype.
            This is done through a dict, if the datatype is not in the dict TEXT is returned by default.


        :param datatype: datatype gotten through type(variable)
        :type datatype: type
        :return: The needed potgres datatype string, by default it is TEXT
        :rtype: string
        """
        # The datatype is converted internally to a string for a dictionary TO avoid importing libraries with
        #    datatypes that might occur, e.g. numpy.uint8.
        datatype = str(datatype)
        conversion_table = {
            str(int): "INT",
            str(float): "DOUBLE PRECISION",
            str(dict): "JSON",
            "<class 'numpy.float64'>": "DOUBLE PRECISION",
            "<class 'numpy.uint8'>": "INT",
            "<class 'numpy.uint16'>": "INT",
            "<class 'numpy.uint32'>": "INT",
            "<class 'numpy.int8'>": "INT",
            "<class 'numpy.int16'>": "INT",
            "<class 'numpy.int32'>": "INT",
        }
        return conversion_table.get(datatype, "TEXT")

    def check_set(self, set_u: set) -> set:
        """checks a set of tuples if the first value in the tuple only exists once in the set

        :param set_u: The set that needs to be checked
        :type set_u: set
        :raises Exception: Raises exception if the tuple value exists multiple times
        :return: The checked set
        :rtype: set
        """
        list_u = [attr for attr, _ in set_u]
        if 2 in [list_u.count(attr) for attr in list_u]:
            raise Exception(
                "There are multiple datatypes in one of the attributes you want to save."
            )
        return set_u

    def create_table_layout(self, inputs):
        """Creates the necessary tables for filling in. The table layout is dependent on the inputs.

        :param inputs: the simulator inputs needed to create the table.
        :type inputs: mosaik_api_v3.types.InputData
        :raises Exception: Raises exception if the extracted tuple value of the attribute exists multiple times
        """
        # Create Schema
        drop_schema = SQL("DROP SCHEMA IF EXISTS {schema_name} CASCADE;").format(
            schema_name=SQLIdent(self._schema_name)
        )
        create_schema = SQL("CREATE SCHEMA IF NOT EXISTS {schema_name};").format(
            schema_name=SQLIdent(self._schema_name)
        )
        if self._drop_tables:
            self._cur.execute(drop_schema)
        self._cur.execute(create_schema)
        self._conn.commit()
        self._attr_dict = {}
        for ent in self._entities:
            data = inputs.get(ent["eid"], {})
            attr_list = []
            for attr, src_ids in data.items():
                for src_id, val in src_ids.items():
                    add_to = (attr, self.get_postgrestype(type(val)))
                    attr_list.append(add_to)
            self._attr_dict[ent["eid"]] = self.check_set(set(attr_list))
            drop_table = SQL("DROP TABLE IF EXISTS {}.{};").format(
                SQLIdent(self._schema_name),
                SQLIdent(ent["eid"]),
            )
            create_hyper_table = SQL(
                "SELECT create_hypertable('{}.{}', 'time');"
            ).format(
                SQLIdent(self._schema_name),
                SQLIdent(ent["eid"]),
            )
            attributes = [
                ("time", "TIMESTAMPTZ NOT NULL"),
                ("run_id", "TEXT"),
                ("src_sim", "TEXT"),
                ("src_entity", "TEXT"),
                *self._attr_dict[ent["eid"]],
            ]
            attrsql = SQLComposed(
                [SQLIdent(name) + SQL(decl) for name, decl in attributes]
            )
            create_table = SQL("CREATE TABLE IF NOT EXISTS {}.{} ({});").format(
                SQLIdent(self._schema_name), SQLIdent(ent["eid"]), attrsql.join(", ")
            )
            if self._drop_tables:
                self._cur.execute(drop_table)
            self._cur.execute(create_table)
            if not self._postgres_mode and self._drop_tables:
                self._cur.execute(create_hyper_table)
            self._conn.commit()

    def add_new_column(self, table_name, col):
        """Adds a new column in the given table, if the table does not exist it creates it

        :param table_name: Name of the table
        :type table_name: str
        :param col: table columns to add
        :type col: List(Tuple(str,str))
        """
        check_table_existence = SQL(
            "SELECT EXISTS(SELECT FROM information_schema.tables WHERE table_schema = {} AND table_name = {});"
        ).format(
            SQLIdent(self._schema_name),
            SQLIdent(table_name),
        )
        self._cur.execute(check_table_existence)
        exists = bool(self._cur.fetchone()[0])
        if not exists:
            attributes = [
                ("time", "TIMESTAMPTZ NOT NULL"),
                ("run_id", "TEXT"),
                ("src_sim", "TEXT"),
                ("src_entity", "TEXT"),
            ]
            attrsql = SQLComposed(
                [SQLIdent(name) + SQL(decl) for name, decl in attributes]
            )
            create_table = SQL("CREATE TABLE IF NOT EXISTS {}.{} ({});").format(
                SQLIdent(self._schema_name), SQLIdent(table_name), attrsql.join(", ")
            )
            self._cur.execute(create_table)
        attributes = [*col]
        attrsql = SQLComposed(
            [
                SQL("ADD COLUMN") + SQLIdent(name) + SQL(decl)
                for name, decl in attributes
            ]
        )
        alter_table = SQL("ALTER TABLE IF EXISTS {}.{} {};").format(
            SQLIdent(self._schema_name), SQLIdent(table_name), attrsql.join(", ")
        )
        self._attr_dict[table_name].extend(col)
        self._cur.execute(alter_table)
        self._conn.commit()

    def add_to_table(self, inputs, time):
        """Adds input values to the tables at each timestep

        :param inputs: Inputs to add to tables
        :type inputs: mosaik_api_v3.types.InputData
        :param time: timestep of the simulator
        :type time: int
        """
        data = inputs.get(self._eid, {})
        if "local_time" in data:
            timestamp = next(iter(data["local_time"].values()))
        elif self._time_converter:
            timestamp = self._time_converter.datetime_from_step(time)
        for ent in self._entities:
            data = inputs.get(ent["eid"], {})
            values = []
            src_dict = {}
            attrs = self._attr_dict[ent["eid"]]
            cols = ["time", "run_id", "src_sim", "src_entity", *data]
            for attr, src_ids in data.items():
                for src_id, val in src_ids.items():
                    if src_id not in src_dict:
                        src_dict[src_id] = {}
                    src_dict[src_id][attr] = val
            for attr in set(data.keys()).difference([att for att, _ in attrs]):
                self.add_new_column(
                    ent["eid"],
                    [
                        (
                            attr,
                            self.get_postgrestype(
                                type(next(iter(data[attr].values())))
                            ),
                        )
                    ],
                )
            for src_id in src_dict:
                iter_list = [timestamp, self._run_id, *src_id.split(".", 1)]
                for attr in data:
                    try:
                        value = src_dict[src_id][attr]
                    except KeyError:
                        value = None
                    iter_list.append(value)
                values.append(tuple(iter_list))
            mgr = CopyManager(self._conn, f"{self._schema_name}.{ent['eid']}", cols)
            mgr.copy(values)
            self._conn.commit()


if __name__ == "__main__":
    mosaik_api_v3.start_simulation(MultiWriter())
