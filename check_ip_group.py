import subprocess
import platform
import time
from concurrent.futures import ThreadPoolExecutor
import threading

status_dsec = ["192.168.240.248", "192.168.241.248", "192.168.242.248", "192.168.243.248",
               "192.168.244.248", "192.168.245.248", "192.168.246.248", "192.168.247.248",
               "192.168.248.248", "192.168.249.248"]
status_gem = ["192.168.230.247"]
status_ustr = ["192.168.210.10", "192.168.220.10", "192.168.230.10", "192.168.240.10", "192.168.231.10"]


def is_reachable(ip):
    try:
        return subprocess.call(['ping', '-c', '1', ip], timeout=1, stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL) == 0
    except:
        return False


def check_ip_with_category(ip_category):
    ip, category = ip_category
    if is_reachable(ip):
        return {'ip': ip, 'category': category, }
    return None


def ping_accessible_ips(accessible_ips):
    while True:
        for ip_info in accessible_ips:
            try:
                subprocess.call(['ping', '-c', '1', ip_info['ip']], timeout=2, stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL)
            except:
                pass
        time.sleep(1)


def ping_all_ips():
    all_ips = status_dsec + status_gem + status_ustr
    while True:
        for ip in all_ips:
            try:
                subprocess.call(['ping', '-c', '1', ip], timeout=2, stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL)
            except:
                pass
        time.sleep(5)


try:
    with ThreadPoolExecutor(max_workers=20) as executor:
        while True:

            all_ips = []
            for ip in status_dsec:
                all_ips.append((ip, 'DSEC'))
            for ip in status_gem:
                all_ips.append((ip, 'GEM'))
            for ip in status_ustr:
                all_ips.append((ip, 'USTR'))

            results = list(executor.map(check_ip_with_category, all_ips))

            results = [r for r in results if r is not None]

            print(results)

            if results:
                threading.Thread(target=ping_accessible_ips, args=(results,), daemon=True).start()

            threading.Thread(target=ping_all_ips, daemon=True).start()

            time.sleep(1)

except KeyboardInterrupt:
    pass
