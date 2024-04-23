
# mosaik TimescaleDB Adapter


[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)


---

This a timescaledb adapter for the mosaik simulation tool. It enables a user to save Simulation data into a Timescale or postgresql database.
 

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Built Using](#built_using)

## 🧐 About <a name = "about"></a>

This mosaik simulator uses Timescaledb to save data that is sent to it during a mosaik simulation. It can also be use with a postgresql database.

## 🏁 Getting Started <a name = "getting_started"></a>

To use this simulator install the package through pip or build it from source and then install the wheel.


### Prerequisites

Python is needed to run this package, furthermore mosaik is needed to use it.
How to install python can be found [here](https://www.python.org/downloads/) and the mosaik package can be found [here](https://gitlab.com/mosaik).
If you want to build this package yourself poetry is needed and can be installed from [here](https://python-poetry.org/docs/)

For this Simulator to work a TimescaleDB installation is needed. Installation can be found under [TimeScaleDB](https://docs.timescale.com/self-hosted/latest/install/re).

For usage under Ubuntu psycopg2 requires the libpq-dev package to be installed.

### Installing

TODO: pip not yet working use local install

To install this package you can use pip by calling:

```
  pip install mosaik-timescaledb
```

It can also be built from source using poetry. To do this you need to have poetry installed.

Clone this repo using:
```sh
 git clone git@gitlab.com:mosaik/internal/mosaik-timescaledb.git
```

Then navigate to this repo inside a command shell and execute the command
```sh
poetry build
```
After this the package can be installed by going into the newly created dist folder and 
using pip to install the wheel.
This is done by executing the commands:

```sh
cd ./dist
pip install mosaik_timescaledb-0.1.0-py3-none-any.whl
```




## 🎈 Usage <a name="usage"></a>

This package comes with different simulators depending on how you want your table layout to look like.

The database table layout can be configured in three different ways *single, multiple and custom*. This configuration changes the table layout of the timescaledb table. Regardless of which simulator you use the following must always be supplied to the simulator, for convenience sake there are default values for each of them:

- db_name: The name of the postgres database.
- db_user: The name of the postgres user.
- db_pass: The password of the postgres database. 
- db_host: The host address of the postgres database. Defaults to "localhost".
- db_port: The host port of the postgres database. Defaults to "5432".
- ssl_mode: The ssl_mode of the postgres database. Defaults to "prefer".
- postgres_mode: This does not create a Timescalehypertable if True and allows this adapter to function as a normal postgres adapter. Defaults to False.
- drop_tables: This determines if the tables/schema are dropped before being created anew, Not used for custom writer. Defaults to False
- run_id: Id for the current simulation run. Defaults to "run 0"

The values important for database connection have to be given in the initialization step.
The different types are now described with their specific configurations:

### SingleWriter

To use this simulator you have to specify it in your sim configuration as such:
```python
sim_config ={ 'DB': {
        'python': 'mosaik_components.timescaledb.single_writer:SingleWriter'
    }}
```
Afterwards the simulator need to get connected to all the relevant simulators you want to save the output from.

A basic example would look like this:

```python
db = world.start('DB',step_size=15*60,start_date="2022-01-01 00:00:00Z", db_name="postgres", db_user="postgres", db_pass="password", db_port="5431")
td = db.Database(table_type="str", table_name="testing_str", run_id="run 2")
nodes = [e for e in grid if e.type in 'Bus']
connect_many_to_one(world, nodes, td, 'p_mw', 'q_mvar', 'vm_pu', 'va_degree')
```
This simulator has the added parameters:

- table_type: The type of the table str or json
- table_name: The name of the postgres table that will be created
- schema_name: The schema the table will be created in. Defaults to public

#### Table type str

This saves every value that the simulator gets into one big postgresql table with the following layout:

```
time  | run_id | src_sim  |  src_entity     | value_type | value  
```
All of these columns except for the time column, which has the type TIMESTAMPTZ, have the postgres type TEXT. The value_type describes the attribute a value has in the simulation, e.g. Voltage.


#### Table type json

This saves every value that the simulator gets into one big postgresql table with the following layout:

```
time  | run_id | value_type | values 
```
The time column has the type TIMESTAMPTZ, the value_type the postgres type TEXT and the values column has the type JSON. The value_type describes the attribute a value has in the simulation, e.g. Voltage. The values JSON has the following layout:

```json

{"Grid-0.0-LV1.1 Bus 1": 0.014, "Grid-0.0-LV1.1 Bus 10": 0.005999999999999998, 
"Grid-0.0-LV1.1 Bus 11": -0.076381, "Grid-0.0-LV1.1 Bus 12": 0.011999999999999997 } 

```

### multi

#### MultiWriter 
To use this Simulator you have to specify it in your sim configuration as such:
```python
sim_config ={ 'DB': {
        'python': 'mosaik_components.timescaledb.multi_writer2:MultiWriter2'
    }}
```
Afterwards the simulator need to get connected to all the relevant simulators you want to save the output from.

A basic example would look like this:

```python
db = world.start('DB', step_size=15*60, start_date="2022-01-01 00:00:00Z", db_name="postgres", db_user="postgres", db_pass="password",)
td, tb = db.Database.create(2, schema_name="testing_schema", run_id="run 1", drop_tables=True)
nodes = [e for e in grid if e.type in 'Bus']
connect_many_to_one(world, nodes, td, 'p_mw', 'q_mvar', 'vm_pu', 'va_degree')
connect_many_to_one(world, nodes, tb, 'p_mw', 'q_mvar', 'vm_pu', 'va_degree')
```
This simulator has the added parameters:
- schema_name: The name of the postgres schema under which the tables will be created

This simulator creates a table for each of it's created entities. The tables have the layout:

```
time  | run_id | src_sim | src_entity | value_type_a | value_type_b | ...
```

For the values of the columns it follows the same rules as multiwriter 1. The added columns src_sim and src_entity have the value string.
If a entity is connected to the simulator that has no value for a given attribute the value None is written.

### custom

#### CustomWriter 

**WORK IN PROGRESS**

**This simulator works differently to the other simulators**
To use this Simulator you have to specify it in your sim configuration as such:
```python
sim_config ={ 'DB': {
        'python': 'mosaik_components.timescaledb.custom_writer:CustomWriter'
    }}
```

Then the simulator needs to be iniialized

```python
db = world.start(
    "DB",
    step_size=15 * 60,
    start_date="2022-01-01 00:00:00Z",
    db_name="postgres",
    db_user="postgres",
    db_pass="password",
    db_port="5431",
    schema_name="multitestrun",
)
```
This simulator has the added parameters:

- schema_name: Name of the schema to scan

Afterwards the simulator scans the schema in the database for every table in it.



If you want to write into a certain table you need to create the simulator entity with the same name and connect it to the other simulators from which you want to save the inputs. The connection is done via the column name.

```python
tb = db.custom_table.create(
    1,
    drop_tables=False,
    run_id="run_2",
)[0]
nodes = [e for e in grid if e.type in "Bus"]
world.connect(nodes[0], tb, ("vm_pu", "value"))
world.connect(nodes[1], tb, ("q_mvar", "value2"))
```
For this test the table looks like this:
```
time  | run_id | src | value | value2 |
```

The time, run_id and src columns  can be set in the create functions and should correlate to existing columns.
This simulator has the added parameters:

- src_col: Name of the column where the src sim string will be saved. Defaults to 'src'.
- ts_col: Name of the column where the timestamp will be saved. Defaults to 'time'.
- run_col: Name of the column where the simulation run id string will be saved. Defaults to 'run_id'.
## ⛏️ Built Using <a name = "built_using"></a>

- [Timescaledb](https://www.timescale.com/) - Database
- [psycopg2](https://www.psycopg.org/) - Database adapter
- [pgcopy](https://github.com/altaurog/pgcopy) - binary copy
- [mosaik](https://gitlab.com/mosaik) - CoSimulation Framework

## TODOS:
- test with more scenarios
- find out if multiple instances(num>1) can be allowed
- check if numpy types(especially arrays) function -> if not put conversion before copymanager
- benchmark different table types
- compare to the other existing adapters
- Release on pip