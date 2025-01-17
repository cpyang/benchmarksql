create table bmsql_config (
  cfg_name    varchar(30) ccsid 937 primary key,
  cfg_value   varchar(50) ccsid 937
);

create table bmsql_warehouse (
  w_id        integer   not null,
  w_ytd       decimal(12,2),
  w_tax       decimal(4,4),
  w_name      varchar(20) ccsid 937,
  w_street_1  varchar(40) ccsid 937,
  w_street_2  varchar(40) ccsid 937,
  w_city      varchar(40) ccsid 937,
  w_state     char(4) ccsid 937,
  w_zip       char(18) ccsid 937
);

create table bmsql_district (
  d_w_id       integer       not null,
  d_id         integer       not null,
  d_ytd        decimal(12,2),
  d_tax        decimal(4,4),
  d_next_o_id  integer,
  d_name       varchar(20) ccsid 937,
  d_street_1   varchar(40) ccsid 937,
  d_street_2   varchar(40) ccsid 937,
  d_city       varchar(40) ccsid 937,
  d_state      char(4) ccsid 937,
  d_zip        char(18) ccsid 937
);

create table bmsql_customer (
  c_w_id         integer        not null,
  c_d_id         integer        not null,
  c_id           integer        not null,
  c_discount     decimal(4,4),
  c_credit       char(4) ccsid 937,
  c_last         varchar(32) ccsid 937,
  c_first        varchar(32) ccsid 937,
  c_credit_lim   decimal(12,2),
  c_balance      decimal(12,2),
  c_ytd_payment  decimal(12,2),
  c_payment_cnt  integer,
  c_delivery_cnt integer,
  c_street_1     varchar(40) ccsid 937,
  c_street_2     varchar(40) ccsid 937,
  c_city         varchar(40) ccsid 937,
  c_state        char(4) ccsid 937,
  c_zip          char(18) ccsid 937,
  c_phone        char(32) ccsid 937,
  c_since        timestamp,
  c_middle       char(4) ccsid 937,
  c_data         varchar(1000) ccsid 937
);

create sequence bmsql_hist_id_seq;

create table bmsql_history (
  hist_id  integer,
  h_c_id   integer,
  h_c_d_id integer,
  h_c_w_id integer,
  h_d_id   integer,
  h_w_id   integer,
  h_date   timestamp,
  h_amount decimal(6,2),
  h_data   varchar(48) ccsid 937
);

create table bmsql_new_order (
  no_w_id  integer   not null,
  no_d_id  integer   not null,
  no_o_id  integer   not null
);

create table bmsql_oorder (
  o_w_id       integer      generated by default as identity,
  o_d_id       integer      not null,
  o_id         integer      not null,
  o_c_id       integer,
  o_carrier_id integer,
  o_ol_cnt     integer,
  o_all_local  integer,
  o_entry_d    timestamp
);

create table bmsql_order_line (
  ol_w_id         integer   not null,
  ol_d_id         integer   not null,
  ol_o_id         integer   not null,
  ol_number       integer   not null,
  ol_i_id         integer   not null,
  ol_delivery_d   timestamp,
  ol_amount       decimal(6,2),
  ol_supply_w_id  integer,
  ol_quantity     integer,
  ol_dist_info    char(48) ccsid 937
);

create table bmsql_item (
  i_id     integer      not null,
  i_name   varchar(48) ccsid 937,
  i_price  decimal(5,2),
  i_data   varchar(100) ccsid 937,
  i_im_id  integer
);

create table bmsql_stock (
  s_w_id       integer       not null,
  s_i_id       integer       not null,
  s_quantity   integer,
  s_ytd        integer,
  s_order_cnt  integer,
  s_remote_cnt integer,
  s_data       varchar(100) ccsid 937,
  s_dist_01    char(48) ccsid 937,
  s_dist_02    char(48) ccsid 937,
  s_dist_03    char(48) ccsid 937,
  s_dist_04    char(48) ccsid 937,
  s_dist_05    char(48) ccsid 937,
  s_dist_06    char(48) ccsid 937,
  s_dist_07    char(48) ccsid 937,
  s_dist_08    char(48) ccsid 937,
  s_dist_09    char(48) ccsid 937,
  s_dist_10    char(48) ccsid 937
);


