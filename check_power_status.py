import subprocess
import sys


def check_power_status():
  
    try:
        
        result = subprocess.run(
            ['power_ctrl', '-o', 'state'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            timeout=5
        )
        
        output = result.stdout + result.stderr
        
       
        for line in output.split('\n'):
            if 'Output' in line:
                if 'on' in line.lower():
                    return 1
                elif 'off' in line.lower():
                    return 0
        
        if 'on' in output.lower() and 'off' not in output.lower():
            return 1
        elif 'off' in output.lower():
            return 0
            
        return -1
        
    except FileNotFoundError:
        return -1
    except subprocess.TimeoutExpired:
        return -1
    except Exception:
        return -1


def main():
    status = check_power_status()
    print(status)
    return status


if __name__ == "__main__":
    sys.exit(main())