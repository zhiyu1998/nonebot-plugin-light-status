import os
import imgkit

from nonebot import logger

from .os_util import get_status_info
from .latency_util import get_latency


def calculate_offset(usage_percentage):
    # 周长为 314 (2 * π * r)
    return 314 * (1 - usage_percentage / 100)


def render(botInfo):
    # 系统信息
    cpu_info, ram_info, swap_info, disk_info, os_info = get_status_info()
    os_name, os_detail, cpu_architecture, top_processes = os_info.os_name, os_info.os_detail, os_info.cpu_architecture, os_info.top_processes
    # 延时信息
    baidu_latency = get_latency("www.baidu.com")
    github_latency = get_latency("www.github.com")
    twitter_latency = get_latency("www.x.com")
    kimi_latency = get_latency("kimi.moonshot.cn")
    # 🐔信息
    adapter_type, bot_id, nickname, avatar_url, message_received, message_sent = botInfo

    cur_path = os.getcwd() + "/src/plugins/nonebot-plugin-light-status/"

    with open(cur_path + "template.html", "r") as file:
        html_content = file.read()
    # 计算占用比例
    cpu_usage_offset = calculate_offset(cpu_info.usage)
    ram_usage_offset = calculate_offset((ram_info.usage / ram_info.total) * 100)
    swap_usage_offset = calculate_offset((swap_info.usage / swap_info.total) * 100)
    disk_usage_offset = calculate_offset((disk_info.usage / disk_info.total) * 100)

    # 将 top_processes 列表转换为 HTML 列表项
    top_processes_html = "".join(f"<li>{process}</li>" for process in top_processes)

    # 替换占位符
    html_content = (html_content
                    .replace("{{os_name}}", os_name) \
                    .replace("{{os_detail}}", os_detail) \
                    .replace("{{cpu_architecture}}", cpu_architecture) \
                    .replace("{{top_processes}}", top_processes_html) \
                    .replace("{{adapter_type}}", adapter_type) \
                    .replace("{{bot_id}}", str(bot_id)) \
                    .replace("{{nickname}}", nickname) \
                    .replace("{{avatar_url}}", avatar_url) \
                    .replace("{{message_received}}", str(message_received)) \
                    .replace("{{message_sent}}", str(message_sent)) \
                    .replace("{{cur_path}}", cur_path) \
                    .replace("{{cpu_core}}", str(cpu_info.core)) \
                    .replace("{{cpu_freq}}", str(cpu_info.freq)) \
                    .replace("{{cpu_usage}}", f"{cpu_info.usage:.2f}") \
                    .replace("{{cpu_usage_offset}}", f"{cpu_usage_offset:.2f}") \
                    .replace("{{ram_usage}}", f"{ram_info.usage:.2f}") \
                    .replace("{{ram_total}}", f"{ram_info.total:.2f}") \
                    .replace("{{ram_usage_offset}}", f"{ram_usage_offset:.2f}") \
                    .replace("{{swap_usage}}", f"{swap_info.usage:.2f}") \
                    .replace("{{swap_total}}", f"{swap_info.total:.2f}") \
                    .replace("{{swap_usage_offset}}", f"{swap_usage_offset:.2f}") \
                    .replace("{{disk_usage}}", f"{disk_info.usage:.2f}") \
                    .replace("{{disk_total}}", f"{disk_info.total:.2f}") \
                    .replace("{{disk_usage_offset}}", f"{disk_usage_offset:.2f}") \
                    .replace("{{baidu_latency}}", str(baidu_latency)) \
                    .replace("{{github_latency}}", str(github_latency)) \
                    .replace("{{kimi_latency}}", str(kimi_latency)) \
                    .replace("{{twitter_latency}}", str(twitter_latency)))

    # 保存修改后的 HTML 文件
    render_html_path = cur_path + "render.html"
    with open(render_html_path, "w") as file:
        file.write(html_content)

    options = {
        'enable-local-file-access': ''
    }

    imgkit.from_file(render_html_path, cur_path + 'system_info.jpg', options)
    return cur_path + 'system_info.jpg'
