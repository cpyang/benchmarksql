select * from v$log;
alter database add logfile group 3 '/opt/tmaxsoft/database/tibero/redo003.log' size 1G;
alter database add logfile group 4 '/opt/tmaxsoft/database/tibero/redo004.log' size 1G;
alter database add logfile group 5 '/opt/tmaxsoft/database/tibero/redo005.log' size 1G;
alter system switch logfile;
alter system switch logfile;
alter system switch logfile;
alter database drop logfile group 0;
alter database drop logfile group 1;
alter database drop logfile group 2;
!rm /opt/tmaxsoft/database/tibero/redo000.log
!rm /opt/tmaxsoft/database/tibero/redo001.log
!rm /opt/tmaxsoft/database/tibero/redo002.log
alter database add logfile group 0 '/opt/tmaxsoft/database/tibero/redo000.log' size 1G;
alter database add logfile group 1 '/opt/tmaxsoft/database/tibero/redo001.log' size 1G;
alter database add logfile group 2 '/opt/tmaxsoft/database/tibero/redo002.log' size 1G;
alter system switch logfile;
alter system switch logfile;
alter system switch logfile;
alter database drop logfile group 3;
alter database drop logfile group 4;
alter database drop logfile group 5;
!rm /opt/tmaxsoft/database/tibero/redo003.log
!rm /opt/tmaxsoft/database/tibero/redo004.log
!rm /opt/tmaxsoft/database/tibero/redo005.log
