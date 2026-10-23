# Running BenchmarkSQL against Oracle Database
``` shell
git clone https://github.com/cpyang/benchmarksql
cd benchmarksql
# Compile
ant
cp $ORACLE_HOME/jdbc/lib/ojdbc6.jar lib/oracle/
cd run
cp props/sample.oracle.properties oracle
```

## Prepare the Python environment (uv) — needed for report graphs

The report scripts (`run/generateReport.sh` → `run/generateGraphs.sh` →
`run/misc/graph_generator.py`) call `python3` and require the packages in
`requirements.txt` (pandas, matplotlib, tzdata, numexpr, bottleneck).
Create a virtualenv once, from the repository root, with [uv](https://docs.astral.sh/uv/):

``` shell
cd <benchmarksql>
uv venv --python 3.9 .venv
uv pip install --python .venv/bin/python -r requirements.txt
```

Then activate it whenever you generate reports:

``` shell
source .venv/bin/activate
cd run
./generateReport.sh my_result_YYYY-MM-DD_HHMMSS
```

On an offline / air-gapped host, install from the bundled wheel set
(`py39_wheels/`, plus the `uv` binary in `bin/`) instead of the network:

``` shell
uv pip install --python .venv/bin/python --offline --find-links py39_wheels/ -r requirements.txt
```

## Modify configuration 
``` text
conn=jdbc:oracle:thin:@localhost:11521:db11g
user=bmsql
password=bmsql
warehouses=2
loadWorkers=2
terminals=2
```

## Create Oracle Schema
``` SQL
create user bmsql identified by bmsql
grant dba to bmsql
....
```

## Generate Test Data
``` shell
./runDatabaseBuild.sh oracle
```
## Run Benchmark
``` shell
./runBenchmark.sh oracle
```
## Remove Test Data
``` shell
./runDatabaseDestroy.sh oracle
```
