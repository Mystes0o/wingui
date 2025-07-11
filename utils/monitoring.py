# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : monitoring.py
# Time       ：2024/8/29 15:27
# Author     ：shu
# version    ：python 3.11
# Description：收集性能占用信息
"""
import os
import re
from gpustat import GPUStatCollection
from loguru import logger
import time
import psutil
import gpustat
import threading
import uiautomation as auto
import queue

class Monitoring:
    def __init__(self):
        self.cpu_count = psutil.cpu_count()
        self.process_name = "RecordExecutor.exe"
        self.interval = 1
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

    def get_resource_usage(self, total_time=None):
        """
        设置监控时间间隔（秒）和总时间（分钟）
        Args:
            total_time:
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
            cpu_count = os.cpu_count()
            cpu_usage = process.cpu_percent(interval=self.interval)
            cpu_usage = round(cpu_usage / cpu_count, 2)
            # print(self.cpu_count)
            # print(cpu_usage)
            cpu_usage_list.append(cpu_usage)

            # 获取内存使用情况
            mem_info = process.memory_info()
            mem_usage = mem_info.rss / 1024 / 1024  # 转换为MB
            mem_usage_list.append(mem_usage)

            # 获取GPU使用情况
            stats = gpustat.GPUStatCollection.new_query()
            for gpu in stats:
                gpu_usage = gpu.utilization
                gpu_usage_list.append(gpu_usage)
                logger.info(f"CPU使用率:{cpu_usage}%, 内存使用率:{mem_usage}M, GPU使用率:{gpu_usage}%")

            # 等待周期
            time.sleep(self.interval)

        # 计算平均值
        avg_cpu_usage = round((sum(cpu_usage_list) / len(cpu_usage_list)), 2)
        avg_mem_usage = round((sum(mem_usage_list) / len(mem_usage_list)), 2)
        avg_gpu_usage = round((sum(gpu_usage_list) / len(gpu_usage_list)), 2)
        logger.info(f"平均CPU使用率:{avg_cpu_usage}%, 平均内存使用率:{avg_mem_usage}M, 平均GPU使用率:{avg_gpu_usage}%")

        return avg_cpu_usage, avg_mem_usage, avg_gpu_usage

    def monitoring_start(self):
        monitoring_thread = threading.Thread(target=self.get_resource_usage)
        monitoring_thread.start()
        return monitoring_thread

    def monitoring_stop(self, monitoring_thread):
        self.event.set()
        monitoring_thread.join()


class WindowsManagerMonitoring:
    def __init__(self):
        self.result_queue = None
        self.ere_process_name = "RecordExecutor"
        self.process_name = "python"
        self.interval = 1
        self.event = threading.Event()
        self.taskmgr = auto.WindowControl(Name="任务管理器")

    def get_tree_by_process_name(self, process_name=None):
        """
        根据进程名称获取所有匹配的进程ID列表
        :param process_name: 进程名称
        :return: 包含所有匹配进程ID的列表
        """
        data = self.taskmgr.DataGridControl(Name='进程').GetChildren()

        if process_name is None:
            for i in data:
                # print(i.Name)
                if self.process_name in i.Name:
                    ere_data = i
                    logger.info(ere_data.Name)
                    return ere_data
                elif self.ere_process_name in i.Name:
                    ere_data = i
                    logger.info(ere_data.Name)
                    return ere_data
        else:
            for i in data:
                # print(i.Name)
                if process_name in i.Name:
                    ere_data = i
                    logger.info(ere_data.Name)
                    return ere_data

        logger.error("未找到进程")
        return None

    def  get_resource_usage(self, total_time=None):
        ere_data = self.get_tree_by_process_name()
        more_information = ere_data.PaneControl(Name="行详细信息")
        resource_usage = more_information.GetChildren()

        # 初始化统计数据
        cpu_usage_list = []
        mem_usage_list = []
        gpu_usage_list = []

        start_time = time.time()
        while True:
            if total_time is None:
                pass
            else:
                # 计算已经过去的时间
                elapsed_time = time.time() - start_time
                if elapsed_time >= total_time:
                    break  # 如果超过了设定的时间则退出循环
            if self.event.is_set():
                break  # 线程结束

            # CPU 使用率
            cpu_usage = resource_usage[3].Name
            cpu_usage_mun = float(cpu_usage.split("%")[0])
            cpu_usage_list.append(cpu_usage_mun)

            # 获取内存使用情况
            memory_usage = resource_usage[5].Name
            memory_usage_mun = float(memory_usage.split(" M")[0])
            mem_usage_list.append(memory_usage_mun)

            # 获取GPU使用情况
            gpu_usage = resource_usage[4].Name
            gpu_usage_mun = float(gpu_usage.split("%")[0])
            gpu_usage_list.append(gpu_usage_mun)
            logger.info(f"CPU使用率:{cpu_usage}, 内存使用率:{memory_usage}, GPU使用率:{gpu_usage}")

            # 等待周期
            time.sleep(self.interval)

        # 计算平均值
        avg_cpu_usage = round((sum(cpu_usage_list) / len(cpu_usage_list)), 2)
        avg_gpu_usage = round((sum(gpu_usage_list) / len(gpu_usage_list)), 2)
        avg_mem_usage = round((sum(mem_usage_list) / len(mem_usage_list)), 2)
        logger.info(f"平均CPU使用率:{avg_cpu_usage}%, 平均内存使用率:{avg_mem_usage}M, 平均GPU使用率:{avg_gpu_usage}%")
        result = ("平均CPU使用率"+str(avg_cpu_usage)+"%\n平均内存使用率"+str(avg_mem_usage)+"M\n平均GPU使用率"+str(avg_gpu_usage)+"%")

        return result

    def monitoring_start(self):
        self.result_queue = queue.Queue()
        monitoring_thread = threading.Thread(target=self._wrap_get_resource_usage)
        monitoring_thread.start()
        return monitoring_thread

    def _wrap_get_resource_usage(self):
        """包装函数，将结果放入队列"""
        result = self.get_resource_usage()
        self.result_queue.put(result)

    def monitoring_stop(self, monitoring_thread):
        self.event.set()
        monitoring_thread.join()
        return self.result_queue.get()




if __name__ == '__main__':
    monitoring = WindowsManagerMonitoring()
    # monitoring.get_tree_by_process_name()
    monitoring.monitoring_start()
    monitoring.monitoring_stop(monitoring.monitoring_start())

