# 在 Oracle 数据库上运行 BenchmarkSQL

> 语言：[English](README.md) | [简体中文](README.zh-CN.md)

``` shell
git clone https://github.com/cpyang/benchmarksql
cd benchmarksql
# Compile
ant
cp $ORACLE_HOME/jdbc/lib/ojdbc6.jar lib/oracle/
cd run
cp props/sample.oracle.properties oracle
```

## 准备 Python 环境（uv）—— 生成报告图表时需要

报告脚本（`run/generateReport.sh` → `run/generateGraphs.sh` →
`run/misc/graph_generator.py`）会调用 `python3`，并需要 `requirements.txt`
中列出的软件包（pandas、matplotlib、tzdata、numexpr、bottleneck）。
请在仓库根目录用 [uv](https://docs.astral.sh/uv/) 创建一次虚拟环境：

``` shell
cd <benchmarksql>
uv venv --python 3.9 .venv
uv pip install --python .venv/bin/python -r requirements.txt
```

以后每次生成报告前先激活该环境：

``` shell
source .venv/bin/activate
cd run
./generateReport.sh my_result_YYYY-MM-DD_HHMMSS
```

若为离线／隔离网络主机，请改用随仓库附带的 wheel 包安装
（`py39_wheels/` 目录，`uv` 可执行文件位于 `bin/`），无需联网：

``` shell
uv pip install --python .venv/bin/python --offline --find-links py39_wheels/ -r requirements.txt
```

## 修改配置
``` text
conn=jdbc:oracle:thin:@localhost:11521:db11g
user=bmsql
password=bmsql
warehouses=2
loadWorkers=2
terminals=2
```

## 创建 Oracle Schema
``` SQL
create user bmsql identified by bmsql
grant dba to bmsql
....
```

## 生成测试数据
``` shell
./runDatabaseBuild.sh oracle
```
## 运行基准测试
``` shell
./runBenchmark.sh oracle
```
## 清除测试数据
``` shell
./runDatabaseDestroy.sh oracle
```
