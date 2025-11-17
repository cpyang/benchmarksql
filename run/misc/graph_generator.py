#!/usr/bin/env python3

import argparse
import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def generate_graph(result_dir, graph_type, device=None, skip_minutes=0, width=12, height=6, pointsize=12):
    """
    Generates a graph based on the provided parameters.
    """
    data_dir = os.path.join(result_dir, 'data')
    run_info_df = pd.read_csv(os.path.join(data_dir, 'runInfo.csv'))

#   # JTPCC_HOME/run/misc/jTPCC.java uses this script to generate graphs.
#   # The script is called from JTPCC_HOME/run/generateGraphs.sh.
#   # The script is executed from the result directory.
#   # The data files are in the data subdirectory.
#   if graph_type == 'tpm_nopm':
#       # ... (existing code) ...
#   elif graph_type == 'latency':
#       # ... (existing code) ...
#   elif graph_type == 'cpu_utilization':
#       # ... (existing code) ...
#   elif graph_type == 'dirty_buffers':
#       # ... (existing code) ...
#   elif graph_type == 'blk_device_iops':
#       # ... (existing code) ...
#   elif graph_type == 'blk_device_kbps':
#       # ... (existing code) ...
#   elif graph_type == 'net_device_iops':
#       # ... (existing code) ...
#   elif graph_type == 'net_device_kbps':
#       # ... (existing code) ...
#
# ... (existing code) ...

    if graph_type == 'tpm_nopm':
        data_df = pd.read_csv(os.path.join(data_dir, 'result.csv'))

        xmin = skip_minutes
        xmax = run_info_df['runMins'].iloc[0]
        
        interval = 1
        for i in [1, 2, 5, 10, 20, 60, 120, 300, 600]:
            if (xmax * 60) / i <= 1000:
                interval = i
                break
        
        idiv = interval * 1000.0
        skip = xmin * 60000
        
        data_df = data_df[data_df['elapsed'] >= skip]
        
        total1 = data_df[data_df['ttype'] != 'DELIVERY_BG']
        neworder1 = data_df[data_df['ttype'] == 'NEW_ORDER']
        
        count_total = total1.groupby(total1['elapsed'] // idiv * idiv).size().reset_index(name='count')
        count_new_order = neworder1.groupby(neworder1['elapsed'] // idiv * idiv).size().reset_index(name='count')
        
        ymax_count = count_total['count'].max() * 60.0 / interval
        ymax = 1
        sqrt2 = 2.0**0.5
        while ymax < ymax_count:
            ymax *= sqrt2
        if ymax < (ymax_count * 1.2):
            ymax *= 1.2
            
        ymaxmod = ymax % 25000
        ymaxsub = 25000 - ymaxmod
        ymax = ymax + ymaxsub

        plt.figure(figsize=(width, height))
        plt.plot(count_total['elapsed'] / 60000.0, count_total['count'] * 60.0 / interval, color='blue', linewidth=2, label='tpmTOTAL')
        plt.plot(count_new_order['elapsed'] / 60000.0, count_new_order['count'] * 60.0 / interval, color='red', linewidth=2, label='tpmC (NewOrder only)')
        
        plt.xlabel('Elapsed Minutes')
        plt.ylabel('Transactions per Minute')
        plt.xlim(xmin, xmax)
        plt.ylim(0, ymax)
        
        plt.title(f"Run #{run_info_df['run'].iloc[0]} of BenchmarkSQL v{run_info_df['driverVersion'].iloc[0]}\nTransactions per Minute")
        plt.legend(loc='upper left')
        plt.grid(True)
        
        plt.savefig(os.path.join(result_dir, 'tpm_nopm.svg'))
    elif graph_type == 'latency':
        data_df = pd.read_csv(os.path.join(data_dir, 'result.csv'))

        xmin = skip_minutes
        xmax = run_info_df['runMins'].iloc[0]
        
        interval = 1
        for i in [1, 2, 5, 10, 20, 60, 120, 300, 600]:
            if (xmax * 60) / i <= 1000:
                interval = i
                break
        
        idiv = interval * 1000.0
        skip = xmin * 60000
        
        data_df = data_df[data_df['elapsed'] >= skip]
        
        no_bg_data = data_df[data_df['ttype'] != 'DELIVERY_BG']
        new_order = data_df[data_df['ttype'] == 'NEW_ORDER']
        payment = data_df[data_df['ttype'] == 'PAYMENT']
        order_status = data_df[data_df['ttype'] == 'ORDER_STATUS']
        stock_level = data_df[data_df['ttype'] == 'STOCK_LEVEL']
        delivery = data_df[data_df['ttype'] == 'DELIVERY']
        delivery_bg = data_df[data_df['ttype'] == 'DELIVERY_BG']

        agg_new_order = new_order.groupby(new_order['elapsed'] // idiv * idiv)['latency'].mean().reset_index()
        agg_payment = payment.groupby(payment['elapsed'] // idiv * idiv)['latency'].mean().reset_index()
        agg_order_status = order_status.groupby(order_status['elapsed'] // idiv * idiv)['latency'].mean().reset_index()
        agg_stock_level = stock_level.groupby(stock_level['elapsed'] // idiv * idiv)['latency'].mean().reset_index()
        agg_delivery = delivery.groupby(delivery['elapsed'] // idiv * idiv)['latency'].mean().reset_index()

        ymax_total = no_bg_data['latency'].quantile(0.98)
        ymax = 1
        sqrt2 = 2.0**0.5
        while ymax < ymax_total:
            ymax *= sqrt2
        if ymax < (ymax_total * 1.2):
            ymax *= 1.2
        if ymax < 100:
            ymax = 120

        plt.figure(figsize=(width, height))
        plt.plot(agg_delivery['elapsed'] / 60000.0, agg_delivery['latency'], color='blue', linewidth=2, label='DELIVERY')
        plt.plot(agg_stock_level['elapsed'] / 60000.0, agg_stock_level['latency'], color='gray', linewidth=2, label='STOCK_LEVEL')
        plt.plot(agg_order_status['elapsed'] / 60000.0, agg_order_status['latency'], color='green', linewidth=2, label='ORDER_STATUS')
        plt.plot(agg_payment['elapsed'] / 60000.0, agg_payment['latency'], color='magenta', linewidth=2, label='PAYMENT')
        plt.plot(agg_new_order['elapsed'] / 60000.0, agg_new_order['latency'], color='red', linewidth=2, label='NEW_ORDER')

        plt.xlabel('Elapsed Minutes')
        plt.ylabel('Latency in Milliseconds')
        plt.xlim(xmin, xmax)
        plt.ylim(0, ymax)
        
        plt.title(f"Run #{run_info_df['run'].iloc[0]} of BenchmarkSQL v{run_info_df['driverVersion'].iloc[0]}\nTransaction Latency")
        plt.legend(loc='upper left')
        plt.grid(True)
        
        plt.savefig(os.path.join(result_dir, 'latency.svg'))

        tx_total = len(no_bg_data)
        tx_name = [
            'NEW_ORDER', 'PAYMENT', 'ORDER_STATUS', 'STOCK_LEVEL', 'DELIVERY', 'DELIVERY_BG', 'tpmC', 'tpmTotal'
        ]
        tx_count = [
            len(new_order), len(payment), len(order_status), len(stock_level), len(delivery), len(delivery_bg),
            f"{len(new_order) / run_info_df['runMins'].iloc[0]:.2f}",
            f"{len(no_bg_data) / run_info_df['runMins'].iloc[0]:.2f}"
        ]
        tx_percent = [
            f"{len(new_order) / tx_total * 100.0:.3f}%",
            f"{len(payment) / tx_total * 100.0:.3f}%",
            f"{len(order_status) / tx_total * 100.0:.3f}%",
            f"{len(stock_level) / tx_total * 100.0:.3f}%",
            f"{len(delivery) / tx_total * 100.0:.3f}%",
            None,
            f"{len(new_order) / run_info_df['runMins'].iloc[0] / run_info_df['runWarehouses'].iloc[0] / 0.1286:.3f}%",
            None
        ]
        tx_90th = [
            f"{new_order['latency'].quantile(0.9) / 1000.0:.3f}s",
            f"{payment['latency'].quantile(0.9) / 1000.0:.3f}s",
            f"{order_status['latency'].quantile(0.9) / 1000.0:.3f}s",
            f"{stock_level['latency'].quantile(0.9) / 1000.0:.3f}s",
            f"{delivery['latency'].quantile(0.9) / 1000.0:.3f}s",
            f"{delivery_bg['latency'].quantile(0.9) / 1000.0:.3f}s",
            None, None
        ]
        tx_avg = [
            f"{new_order['latency'].mean() / 1000.0:.3f}s",
            f"{payment['latency'].mean() / 1000.0:.3f}s",
            f"{order_status['latency'].mean() / 1000.0:.3f}s",
            f"{stock_level['latency'].mean() / 1000.0:.3f}s",
            f"{delivery['latency'].mean() / 1000.0:.3f}s",
            f"{delivery_bg['latency'].mean() / 1000.0:.3f}s",
            None, None
        ]
        tx_max = [
            f"{new_order['latency'].max() / 1000.0:.3f}s",
            f"{payment['latency'].max() / 1000.0:.3f}s",
            f"{order_status['latency'].max() / 1000.0:.3f}s",
            f"{stock_level['latency'].max() / 1000.0:.3f}s",
            f"{delivery['latency'].max() / 1000.0:.3f}s",
            f"{delivery_bg['latency'].max() / 1000.0:.3f}s",
            None, None
        ]
        tx_limit = ["5.0", "5.0", "5.0", "20.0", "5.0", "80.0", None, None]
        tx_rbk = [
            f"{new_order['rbk'].sum() / len(new_order) * 100.0:.3f}%",
            None, None, None, None, None, None, None
        ]
        tx_error = [
            new_order['error'].sum(), payment['error'].sum(), order_status['error'].sum(),
            stock_level['error'].sum(), delivery['error'].sum(), delivery_bg['error'].sum(),
            None, None
        ]
        tx_dskipped = [
            None, None, None, None, None,
            delivery_bg['dskipped'].sum(),
            None, None
        ]
        tx_info = pd.DataFrame({
            'tx_name': tx_name, 'tx_count': tx_count, 'tx_percent': tx_percent,
            'tx_90th': tx_90th, 'tx_avg': tx_avg, 'tx_max': tx_max,
            'tx_limit': tx_limit, 'tx_rbk': tx_rbk, 'tx_error': tx_error,
            'tx_dskipped': tx_dskipped
        })
        tx_info.to_csv(os.path.join(data_dir, 'tx_summary.csv'), index=False, na_rep='N/A')

    elif graph_type == 'cpu_utilization':
        sys_info_path = os.path.join(data_dir, 'sys_info.csv')
        if not os.path.exists(sys_info_path):
            print("Warning: sys_info.csv not found. Skipping cpu_utilization graph.")
            return
        data_df = pd.read_csv(sys_info_path)

        xmin = skip_minutes
        xmax = run_info_df['runMins'].iloc[0]
        
        interval = 1
        for i in [1, 2, 5, 10, 20, 60, 120, 300, 600]:
            if (xmax * 60) / i <= 1000:
                interval = i
                break
        
        idiv = interval * 1000.0
        skip = xmin * 60000
        
        data_df = data_df[data_df['elapsed'] >= skip]
        
        agg_user = data_df.groupby(data_df['elapsed'] // idiv * idiv)['cpu_user'].mean().reset_index()
        agg_system = data_df.groupby(data_df['elapsed'] // idiv * idiv)['cpu_system'].mean().reset_index()
        agg_wait = data_df.groupby(data_df['elapsed'] // idiv * idiv)['cpu_iowait'].mean().reset_index()
        
        ymax = 100
            
        plt.figure(figsize=(width, height))
        plt.plot(agg_user['elapsed'] / 60000.0, (agg_user['cpu_user'] + agg_system['cpu_system'] + agg_wait['cpu_iowait']) * 100.0, color='red', linewidth=2, label='% IOWait')
        plt.plot(agg_user['elapsed'] / 60000.0, (agg_user['cpu_user'] + agg_system['cpu_system']) * 100.0, color='cyan', linewidth=2, label='% System')
        plt.plot(agg_user['elapsed'] / 60000.0, agg_user['cpu_user'] * 100.0, color='blue', linewidth=2, label='% User')
        
        plt.xlabel('Elapsed Minutes')
        plt.ylabel('CPU Utilization in Percent')
        plt.xlim(xmin, xmax)
        plt.ylim(0, ymax)
        
        plt.title(f"Run #{run_info_df['run'].iloc[0]} of BenchmarkSQL v{run_info_df['driverVersion'].iloc[0]}\nCPU Utilization")
        plt.legend(loc='upper left')
        plt.grid(True)
        
        plt.savefig(os.path.join(result_dir, 'cpu_utilization.svg'))

        cpu_category = [
            'cpu_user',
            'cpu_system',
            'cpu_iowait',
            'cpu_idle',
            'cpu_nice',
            'cpu_irq',
            'cpu_softirq',
            'cpu_steal',
            'cpu_guest',
            'cpu_guest_nice'
        ]
        cpu_usage = [
            f"{data_df['cpu_user'].mean() * 100.0:.3f}%",
            f"{data_df['cpu_system'].mean() * 100.0:.3f}%",
            f"{data_df['cpu_iowait'].mean() * 100.0:.3f}%",
            f"{data_df['cpu_idle'].mean() * 100.0:.3f}%",
            f"{data_df['cpu_nice'].mean() * 100.0:.3f}%",
            f"{data_df['cpu_irq'].mean() * 100.0:.3f}%",
            f"{data_df['cpu_softirq'].mean() * 100.0:.3f}%",
            f"{data_df['cpu_steal'].mean() * 100.0:.3f}%",
            f"{data_df['cpu_guest'].mean() * 100.0:.3f}%",
            f"{data_df['cpu_guest_nice'].mean() * 100.0:.3f}%"
        ]
        cpu_info = pd.DataFrame({
            'cpu_category': cpu_category,
            'cpu_usage': cpu_usage
        })
        cpu_info.to_csv(os.path.join(data_dir, 'cpu_summary.csv'), index=False)
    elif graph_type == 'dirty_buffers':
        sys_info_path = os.path.join(data_dir, 'sys_info.csv')
        if not os.path.exists(sys_info_path):
            print("Warning: sys_info.csv not found. Skipping dirty_buffers graph.")
            return
        data_df = pd.read_csv(sys_info_path)

        xmin = skip_minutes
        xmax = run_info_df['runMins'].iloc[0]
        
        interval = 1
        for i in [1, 2, 5, 10, 20, 60, 120, 300, 600]:
            if (xmax * 60) / i <= 1000:
                interval = i
                break
        
        idiv = interval * 1000.0
        skip = xmin * 60000
        
        data_df = data_df[data_df['elapsed'] >= skip]
        
        agg_dirty = data_df.groupby(data_df['elapsed'] // idiv * idiv)['vm_nr_dirty'].mean().reset_index()
        
        ymax_dirty = agg_dirty['vm_nr_dirty'].max()
        ymax = 1
        sqrt2 = 2.0**0.5
        while ymax < ymax_dirty:
            ymax *= sqrt2
        if ymax < (ymax_dirty * 1.2):
            ymax *= 1.2
            
        plt.figure(figsize=(width, height))
        plt.plot(agg_dirty['elapsed'] / 60000.0, agg_dirty['vm_nr_dirty'], color='red', linewidth=2, label='vmstat nr_dirty')
        
        plt.xlabel('Elapsed Minutes')
        plt.ylabel('Number dirty kernel buffers')
        plt.xlim(xmin, xmax)
        plt.ylim(0, ymax)
        
        plt.title(f"Run #{run_info_df['run'].iloc[0]} of BenchmarkSQL v{run_info_df['driverVersion'].iloc[0]}\nDirty Kernel Buffers")
        plt.legend(loc='upper left')
        plt.grid(True)
        
        plt.savefig(os.path.join(result_dir, 'dirty_buffers.svg'))
    elif graph_type == 'blk_device_iops':
        data_df = pd.read_csv(os.path.join(data_dir, f'{device}.csv'))

        xmin = skip_minutes
        xmax = run_info_df['runMins'].iloc[0]
        
        interval = 1
        for i in [1, 2, 5, 10, 20, 60, 120, 300, 600]:
            if (xmax * 60) / i <= 1000:
                interval = i
                break
        
        idiv = interval * 1000.0
        skip = xmin * 60000
        
        data_df = data_df[data_df['elapsed'] >= skip]
        
        agg_reads = data_df.groupby(data_df['elapsed'] // idiv * idiv)['rdiops'].mean().reset_index()
        agg_writes = data_df.groupby(data_df['elapsed'] // idiv * idiv)['wriops'].mean().reset_index()
        
        ymax_rd = agg_reads['rdiops'].max()
        ymax_wr = agg_writes['wriops'].max()
        ymax = 1
        sqrt2 = 2.0**0.5
        while ymax < ymax_rd or ymax < ymax_wr:
            ymax *= sqrt2
        if ymax < (ymax_rd * 1.2) or ymax < (ymax_wr * 1.2):
            ymax *= 1.2
            
        plt.figure(figsize=(width, height))
        plt.plot(agg_reads['elapsed'] / 60000.0, agg_reads['rdiops'], color='blue', linewidth=2, label=f'Read Operations on {device}')
        plt.plot(agg_writes['elapsed'] / 60000.0, agg_writes['wriops'], color='red', linewidth=2, label=f'Write Operations on {device}')
        
        plt.xlabel('Elapsed Minutes')
        plt.ylabel('IO Operations per Second')
        plt.xlim(xmin, xmax)
        plt.ylim(0, ymax)
        
        plt.savefig(os.path.join(result_dir, f'{device}_iops.svg'))
    elif graph_type == 'blk_device_kbps':
        data_df = pd.read_csv(os.path.join(data_dir, f'{device}.csv'))

        xmin = skip_minutes
        xmax = run_info_df['runMins'].iloc[0]
        
        interval = 1
        for i in [1, 2, 5, 10, 20, 60, 120, 300, 600]:
            if (xmax * 60) / i <= 1000:
                interval = i
                break
        
        idiv = interval * 1000.0
        skip = xmin * 60000
        
        data_df = data_df[data_df['elapsed'] >= skip]
        
        agg_reads = data_df.groupby(data_df['elapsed'] // idiv * idiv)['rdkbps'].mean().reset_index()
        agg_writes = data_df.groupby(data_df['elapsed'] // idiv * idiv)['wrkbps'].mean().reset_index()
        
        ymax_rd = agg_reads['rdkbps'].max()
        ymax_wr = agg_writes['wrkbps'].max()
        ymax = 1
        sqrt2 = 2.0**0.5
        while ymax < ymax_rd or ymax < ymax_wr:
            ymax *= sqrt2
        if ymax < (ymax_rd * 1.2) or ymax < (ymax_wr * 1.2):
            ymax *= 1.2
            
        plt.figure(figsize=(width, height))
        plt.plot(agg_reads['elapsed'] / 60000.0, agg_reads['rdkbps'], color='blue', linewidth=2, label=f'Read Kb/s on {device}')
        plt.plot(agg_writes['elapsed'] / 60000.0, agg_writes['wrkbps'], color='red', linewidth=2, label=f'Write Kb/s on {device}')
        
        plt.xlabel('Elapsed Minutes')
        plt.ylabel('Kilobytes per Second')
        plt.xlim(xmin, xmax)
        plt.savefig(os.path.join(result_dir, f'{device}_kbps.svg'))
    elif graph_type == 'net_device_iops':
        data_df = pd.read_csv(os.path.join(data_dir, f'{device}.csv'))

        xmin = skip_minutes
        xmax = run_info_df['runMins'].iloc[0]
        
        interval = 1
        for i in [1, 2, 5, 10, 20, 60, 120, 300, 600]:
            if (xmax * 60) / i <= 1000:
                interval = i
                break
        
        idiv = interval * 1000.0
        skip = xmin * 60000
        
        data_df = data_df[data_df['elapsed'] >= skip]
        
        agg_recv = data_df.groupby(data_df['elapsed'] // idiv * idiv)['rxpktsps'].mean().reset_index()
        agg_send = data_df.groupby(data_df['elapsed'] // idiv * idiv)['txpktsps'].mean().reset_index()
        
        ymax_rx = agg_recv['rxpktsps'].max()
        ymax_tx = agg_send['txpktsps'].max()
        ymax = 1
        sqrt2 = 2.0**0.5
        while ymax < ymax_rx or ymax < ymax_tx:
            ymax *= sqrt2
        if ymax < (ymax_rx * 1.2) or ymax < (ymax_tx * 1.2):
            ymax *= 1.2
            
        plt.figure(figsize=(width, height))
        plt.plot(agg_recv['elapsed'] / 60000.0, agg_recv['rxpktsps'], color='blue', linewidth=2, label=f'RX Packets/s on {device}')
        plt.plot(agg_send['elapsed'] / 60000.0, agg_send['txpktsps'], color='red', linewidth=2, label=f'TX Packets/s on {device}')
        
        plt.xlabel('Elapsed Minutes')
        plt.ylabel('Packets per Second')
        plt.xlim(xmin, xmax)
        plt.ylim(0, ymax)
        
        plt.title(f"Run #{run_info_df['run'].iloc[0]} of BenchmarkSQL v{run_info_df['driverVersion'].iloc[0]}\nNetwork Device {device} Packets per Second")
        plt.legend(loc='upper left')
        plt.grid(True)
        
        plt.savefig(os.path.join(result_dir, f'{device}_iops.svg'))
    elif graph_type == 'net_device_kbps':
        data_df = pd.read_csv(os.path.join(data_dir, f'{device}.csv'))

        xmin = skip_minutes
        xmax = run_info_df['runMins'].iloc[0]
        
        interval = 1
        for i in [1, 2, 5, 10, 20, 60, 120, 300, 600]:
            if (xmax * 60) / i <= 1000:
                interval = i
                break
        
        idiv = interval * 1000.0
        skip = xmin * 60000
        
        data_df = data_df[data_df['elapsed'] >= skip]
        
        agg_recv = data_df.groupby(data_df['elapsed'] // idiv * idiv)['rxkbps'].mean().reset_index()
        agg_send = data_df.groupby(data_df['elapsed'] // idiv * idiv)['txkbps'].mean().reset_index()
        
        ymax_rx = agg_recv['rxkbps'].max()
        ymax_tx = agg_send['txkbps'].max()
        ymax = 1
        sqrt2 = 2.0**0.5
        while ymax < ymax_rx or ymax < ymax_tx:
            ymax *= sqrt2
        if ymax < (ymax_rx * 1.2) or ymax < (ymax_tx * 1.2):
            ymax *= 1.2
            
        plt.figure(figsize=(width, height))
        plt.plot(agg_recv['elapsed'] / 60000.0, agg_recv['rxkbps'], color='blue', linewidth=2, label=f'RX Kb/s on {device}')
        plt.plot(agg_send['elapsed'] / 60000.0, agg_send['txkbps'], color='red', linewidth=2, label=f'TX Kb/s on {device}')
        
        plt.xlabel('Elapsed Minutes')
        plt.ylabel('Kilobytes per Second')
        plt.xlim(xmin, xmax)
        plt.ylim(0, ymax)
        
        plt.title(f"Run #{run_info_df['run'].iloc[0]} of BenchmarkSQL v{run_info_df['driverVersion'].iloc[0]}\nNetwork Device {device} Kb per Second")
        plt.legend(loc='upper left')
        plt.grid(True)
        
        plt.savefig(os.path.join(result_dir, f'{device}_kbps.svg'))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate graphs for BenchmarkSQL results.')
    parser.add_argument('result_dir', type=str, help='The directory containing the benchmark results.')
    parser.add_argument('graph_type', type=str, help='The type of graph to generate.')
    parser.add_argument('--device', type=str, help='The device name for device-specific graphs.')
    parser.add_argument('--skip', type=int, default=0, help='The number of minutes to skip from the beginning of the run.')
    parser.add_argument('--width', type=int, default=12, help='The width of the output image.')
    parser.add_argument('--height', type=int, default=6, help='The height of the output image.')
    parser.add_argument('--pointsize', type=int, default=12, help='The point size for the plot.')
    args = parser.parse_args()

    generate_graph(args.result_dir, args.graph_type, device=args.device, skip_minutes=args.skip, width=args.width, height=args.height, pointsize=args.pointsize)
