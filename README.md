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
