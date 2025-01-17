CREATE TABLESPACE benchmark_ts DATAFILE 'bech00.dtf' SIZE 3G, 'bech01.dtf' SIZE 3G;
CREATE USER benchmarksql IDENTIFIED BY "bmsql1" DEFAULT TABLESPACE benchmark_ts TEMPORARY TABLESPACE temp;
GRANT CONNECT TO benchmarksql;
GRANT CREATE PROCEDURE TO benchmarksql;
GRANT CREATE SEQUENCE TO benchmarksql;
GRANT CREATE SESSION TO benchmarksql;
GRANT CREATE TABLE TO benchmarksql;
GRANT CREATE TRIGGER TO benchmarksql;
GRANT CREATE TYPE TO benchmarksql;
ALTER USER benchmarksql QUOTA UNLIMITED ON benchmark_ts;
GRANT UNLIMITED TABLESPACE TO benchmarksql;
