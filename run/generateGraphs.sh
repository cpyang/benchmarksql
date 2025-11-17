#!/usr/bin/env bash
# ----
# Script to generate the detail graphs of a BenchmarkSQL run.
#
# Copyright (C) 2016, Denis Lussier
# Copyright (C) 2016, Jan Wieck
# ----

if [ $# -lt 1 ] ; then
    echo "usage: $(basename $0) RESULT_DIR [SKIP_MINUTES]" >&2
    exit 2
fi

if [ $# -gt 1 ] ; then
	SKIP=$2
else
	SKIP=0
fi

WIDTH=12
HEIGHT=6
POINTSIZE=12

SIMPLE_GRAPHS="tpm_nopm latency cpu_utilization dirty_buffers"

resdir="$1"
cd "${resdir}" || exit 1

for graph in $SIMPLE_GRAPHS ; do
	echo -n "Generating ${resdir}/${graph}.svg ... "
	out=$(python3 ../misc/graph_generator.py "$(pwd)" "${graph}" --skip "${SKIP}" --width "${WIDTH}" --height "${HEIGHT}" --pointsize "${POINTSIZE}")
	if [ $? -ne 0 ] ; then
		echo "ERROR"
		echo "$out" >&2
		exit 3
	fi
	echo "OK"
done

for fname in ./data/blk_*.csv ; do
	if [ ! -f "${fname}" ] ; then
		continue
	fi
	devname=$(basename ${fname} .csv)

	echo -n "Generating ${resdir}/${devname}_iops.svg ... "
	out=$(python3 ../misc/graph_generator.py "$(pwd)" "blk_device_iops" --device "${devname}" --skip "${SKIP}" --width "${WIDTH}" --height "${HEIGHT}" --pointsize "${POINTSIZE}")
	if [ $? -ne 0 ] ; then
		echo "ERROR"
		echo "$out" >&2
		exit 3
	fi
	echo "OK"

	echo -n "Generating ${resdir}/${devname}_kbps.svg ... "
	out=$(python3 ../misc/graph_generator.py "$(pwd)" "blk_device_kbps" --device "${devname}" --skip "${SKIP}" --width "${WIDTH}" --height "${HEIGHT}" --pointsize "${POINTSIZE}")
	if [ $? -ne 0 ] ; then
		echo "ERROR"
		echo "$out" >&2
		exit 3
	fi
	echo "OK"
done

for fname in ./data/net_*.csv ; do
	if [ ! -f "${fname}" ] ; then
		continue
	fi
	devname=$(basename ${fname} .csv)

	echo -n "Generating ${resdir}/${devname}_iops.svg ... "
	out=$(python3 ../misc/graph_generator.py "$(pwd)" "net_device_iops" --device "${devname}" --skip "${SKIP}" --width "${WIDTH}" --height "${HEIGHT}" --pointsize "${POINTSIZE}")
	if [ $? -ne 0 ] ; then
		echo "ERROR"
		echo "$out" >&2
		exit 3
	fi
	echo "OK"

	echo -n "Generating ${resdir}/${devname}_kbps.svg ... "
	out=$(python3 ../misc/graph_generator.py "$(pwd)" "net_device_kbps" --device "${devname}" --skip "${SKIP}" --width "${WIDTH}" --height "${HEIGHT}" --pointsize "${POINTSIZE}")
	if [ $? -ne 0 ] ; then
		echo "ERROR"
		echo "$out" >&2
		exit 3
	fi
	echo "OK"
done
