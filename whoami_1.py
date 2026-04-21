import subprocess
from typing import List, Dict

def has_real_ip(host: str) -> bool:
    
    
    clean = host.strip('()')
    
    return '.' in clean and any(c.isdigit() for c in clean) and ':' not in clean

def parse_who() -> List[Dict[str, str]]:
    result = subprocess.run(['who'], stdout=subprocess.PIPE, universal_newlines=True)
    who_output = result.stdout
    
    final_users = []
    local_users_added = set()
    
    if who_output.strip():
        for line in who_output.strip().split('\n'):
            parts = line.split()
            if len(parts) >= 5:
                username = parts[0]
                terminal = parts[1]
                date = parts[2]
                time = parts[3]
                host = parts[4]
                
                if has_real_ip(host):
                    
                    final_users.append({
                        'username': username,
                        'terminal': terminal,
                        'date': date,
                        'time': time,
                        'host': host
                    })
                else:
                    
                    if username not in local_users_added:
                        local_users_added.add(username)
                        final_users.append({
                            'username': username,
                            'terminal': terminal,
                            'date': date,
                            'time': time,
                            'host': host
                        })
    
    return final_users

if __name__ == "__main__":
    result = parse_who()
    print("Найдено пользователей: {}".format(len(result)))
    for user in result:
        print("Пользователь: {}".format(user))