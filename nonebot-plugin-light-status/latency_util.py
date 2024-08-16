from ping3 import ping, errors

def get_latency(host):
    try:
        latency = ping(host, timeout=3)  # timeout 参数设置为 2 秒
        if latency is None:
            return "Timeout"
        return round(latency * 1000, 2)  # 将延迟转换为毫秒
    except errors.HostUnknown:
        return "Unknown Host"
    except Exception as e:
        return f"Error: {e}"