import subprocess
import threading
from queue import Queue

def ping_worker(ip_queue, results):
    
    while not ip_queue.empty():
        try:
            ip = ip_queue.get_nowait()
        except:
            break
        
        try:
            result = subprocess.run(
                ['ping', '-c', '1', '-W', '1', ip],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=2
            )
            results[ip] = (result.returncode == 0)
        except:
            results[ip] = False
        finally:
            ip_queue.task_done()

def check_gem3():
    
    try:
        result = subprocess.run(
            ['ping', '-c', '1', '-W', '1', 'gem3'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            timeout=2
        )
        return 1 if result.returncode == 0 else 0
    except subprocess.TimeoutExpired:
        return 0  
    except FileNotFoundError:
        return -1 
    except Exception:
        return -1  

def main():
    ips = [
        '192.168.240.248', '192.168.241.248', '192.168.242.248',
        '192.168.243.248', '192.168.244.248', '192.168.245.248',
        '192.168.246.248', '192.168.247.248', '192.168.248.248',
        '192.168.249.248'
    ]
    
    ip_queue = Queue()
    for ip in ips:
        ip_queue.put(ip)
    
    results = {}
    
    threads = []
    for _ in range(10):
        t = threading.Thread(target=ping_worker, args=(ip_queue, results))
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()
    
    
    available_dsec = []
    for idx, ip in enumerate(ips):
        if results.get(ip, False):
            available_dsec.append(idx)
    
    
    gem3_status = check_gem3()
    
    
    if available_dsec:
        first_available = available_dsec[0]  
        print("MB - [{}]".format(first_available))
    else:
        print("MB - -1")
    
    print("Reg - {}".format(gem3_status))

if __name__ == "__main__":
    main()