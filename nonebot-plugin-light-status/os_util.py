import platform
from dataclasses import dataclass

import psutil


@dataclass
class CPUInfo:
    core: int
    """CPU 物理核心数"""
    usage: float
    """CPU 占用百分比，取值范围(0,100]"""
    freq: float
    """CPU 的时钟速度（单位：GHz）"""

    @classmethod
    def get_cpu_info(cls):
        cpu_core = psutil.cpu_count(logical=False)
        cpu_usage = psutil.cpu_percent(interval=1)
        cpu_freq = round(psutil.cpu_freq().current / 1000, 2)

        return CPUInfo(core=cpu_core, usage=cpu_usage, freq=cpu_freq)


@dataclass
class RAMInfo:
    """RAM 信息（单位：GB）"""

    total: float
    """RAM 总量"""
    usage: float
    """当前 RAM 占用量/GB"""

    @classmethod
    def get_ram_info(cls):
        ram_total = round(psutil.virtual_memory().total / (1024 ** 3), 2)
        ram_usage = round(psutil.virtual_memory().used / (1024 ** 3), 2)

        return RAMInfo(total=ram_total, usage=ram_usage)


@dataclass
class SwapMemory:
    """Swap 信息（单位：GB）"""

    total: float
    """Swap 总量"""
    usage: float
    """当前 Swap 占用量/GB"""

    @classmethod
    def get_swap_info(cls):
        swap_total = round(psutil.swap_memory().total / (1024 ** 3), 2)
        swap_usage = round(psutil.swap_memory().used / (1024 ** 3), 2)

        return SwapMemory(total=swap_total, usage=swap_usage)


@dataclass
class DiskInfo:
    """硬盘信息"""

    total: float
    """硬盘总量"""
    usage: float
    """当前硬盘占用量/GB"""

    @classmethod
    def get_disk_info(cls):
        disk_total = round(psutil.disk_usage("/").total / (1024 ** 3), 2)
        disk_usage = round(psutil.disk_usage("/").used / (1024 ** 3), 2)

        return DiskInfo(total=disk_total, usage=disk_usage)


@dataclass
class OSInfo:
    """系统信息"""
    os_name: str
    os_detail: str
    cpu_architecture: str
    top_processes: list

    @classmethod
    def get_os_info(cls):
        os_name = platform.system()
        os_detail = f"{platform.uname().version}"
        cpu_architecture = platform.machine()
        # 获取当前所有进程的列表
        processes = psutil.process_iter(['pid', 'name', 'cpu_percent'])
        # 按CPU使用率排序，并获取前5个进程
        processes = sorted(processes, key=lambda p: p.info['cpu_percent'], reverse=True)[:2]
        # 打印进程信息
        top_processes = [f"PID: {proc.pid}, Name: {proc.info['name']}, CPU%: {proc.info['cpu_percent']}" for proc in
                         processes]
        return OSInfo(os_name=os_name, os_detail=os_detail, cpu_architecture=cpu_architecture, top_processes=top_processes)


def get_status_info() -> tuple[CPUInfo, RAMInfo, SwapMemory, DiskInfo, OSInfo]:
    """获取 `CPU` `RAM` `SWAP` `DISK` 信息"""
    cpu_info = CPUInfo.get_cpu_info()
    ram_info = RAMInfo.get_ram_info()
    swap_info = SwapMemory.get_swap_info()
    disk_info = DiskInfo.get_disk_info()
    os_info = OSInfo.get_os_info()

    return cpu_info, ram_info, swap_info, disk_info, os_info
