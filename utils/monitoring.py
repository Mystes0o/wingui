# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : monitoring.py
# Time       ：2024/8/29 15:27
# Author     ：shu
# version    ：python 3.9
# Description：收集性能占用信息
"""
import logging
import time
import psutil
from gpustat.core import GPUStatCollection
import threading


class Monitoring:
    def __init__(self):
        self.process_name = "VideoEditorQt.exe"
        self.interval = 5
        self.event = threading.Event()

    def get_pids_by_process_name(self, process_name=None):
        """
        根据进程名称获取所有匹配的进程ID列表
        :param process_name: 进程名称
        :return: 包含所有匹配进程ID的列表
        """
        if process_name is None or process_name == self.process_name:
            pids = []
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'] == process_name:
                    pids.append(proc.info['pid'])
            return pids

    def get_resource_usage(self, total_time=None, process_name=None):
        """
        设置监控时间间隔（秒）和总时间（分钟）
        Args:
            total_time:
            process_name:
        Returns:
        """

        # 初始化统计数据
        cpu_usage_list = []
        mem_usage_list = []
        gpu_usage_list = []

        # 获取进程ID,开始监控
        process_name = self.process_name
        pids = self.get_pids_by_process_name(process_name)
        process = psutil.Process(pids[0])

        start_time = time.time()
        while True:
            # 计算已经过去的时间
            elapsed_time = time.time() - start_time

            if total_time is None:
                if process.is_running() is False:
                    break  # 如果进程不存在则退出循环
            else:
                if elapsed_time >= total_time * 60:
                    break  # 如果超过了设定的时间则退出循环
            if self.event.is_set():
                break

            # CPU 使用率
            cpu_usage = process.cpu_percent(interval=self.interval)
            cpu_usage_list.append(cpu_usage)

            # 获取内存使用情况
            mem_info = process.memory_info()
            mem_usage = mem_info.rss / 1024 / 1024  # 转换为MB
            mem_usage_list.append(mem_usage)

            # 获取GPU使用情况
            gpus = GPUStatCollection.new_query()
            for gpu in gpus:
                gpu_usage = gpu.utilization
                gpu_usage_list.append(gpu_usage)

            # 等待周期
            logging.info("CPU使用率:", cpu_usage, "%", "内存使用率:", mem_usage, "M", "GPU使用率:", gpu_usage, "%")
            time.sleep(self.interval)

        # 计算平均值
        avg_cpu_usage = round((sum(cpu_usage_list) / len(cpu_usage_list)), 2)
        avg_mem_usage = round((sum(mem_usage_list) / len(mem_usage_list)), 2)
        avg_gpu_usage = round((sum(gpu_usage_list) / len(gpu_usage_list)), 2)
        print("平均CPU使用率:", avg_cpu_usage, "%", "平均内存使用率:", avg_mem_usage, "M", "平均GPU使用率:",
              avg_gpu_usage, "%")

        return avg_cpu_usage, avg_mem_usage, avg_gpu_usage

    def monitoring_start(self):
        monitoring_thread = threading.Thread(target=self.get_resource_usage)
        monitoring_thread.start()
        return monitoring_thread

    def monitoring_stop(self, monitoring_thread):
        self.event.set()
        monitoring_thread.join()
        print(1)


if __name__ == '__main__':
    monitoring = Monitoring()
