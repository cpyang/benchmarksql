set pagesize 0 heading off feedback off verify off echo off trimspool on termout off timing off time off linesize 1000
SPOOL awrrpt.txt;
DECLARE
    db_id                NUMBER;
    inst_id              NUMBER;
    start_id             NUMBER;
    end_id               NUMBER;
    snap_id              NUMBER;
    begin_interval_time  TIMESTAMP;
    end_interval_time    TIMESTAMP;
    CURSOR snapshots IS SELECT * FROM (SELECT snap_id, begin_interval_time, end_interval_time
            FROM dba_hist_snapshot WHERE dbid = db_id AND instance_number = inst_id ORDER BY snap_id DESC) WHERE ROWNUM < 3;

BEGIN
    dbms_output.enable(1000000);
    SELECT dbid INTO db_id FROM v$database;

    SELECT instance_number INTO inst_id FROM v$instance;

    OPEN snapshots;
    FETCH snapshots INTO snap_id, begin_interval_time, end_interval_time;
    end_id := snap_id;
    dbms_output.put_line(snap_id || '=>' || begin_interval_time);
    FETCH snapshots INTO snap_id, begin_interval_time, end_interval_time;
    start_id := snap_id;
    dbms_output.put_line(snap_id || '=>' || begin_interval_time);
    CLOSE snapshots;
    FOR v_awr IN (SELECT output FROM TABLE ( dbms_workload_repository.awr_report_text(db_id, inst_id, start_id, end_id) )) LOOP
        dbms_output.put_line(v_awr.output);
    END LOOP;
END;
/
SPOOL OFF;
