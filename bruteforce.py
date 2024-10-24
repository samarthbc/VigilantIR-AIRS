import wmi
import time
import os

failed_attempts = {}

def monitor_failed_logins():
    c = wmi.WMI()
    logon_failure_event_id = 529
    print("Monitoring failed login attempts...")

    while True:
        for log in c.Win32_NTLogEvent(EventCode=logon_failure_event_id):
            username = log.InsertionStrings[5]
            ip_address = log.InsertionStrings[18]

            print(f"Failed login detected for user: {username} from IP: {ip_address}")
            if track_failed_attempts(ip_address):
                print(f"Brute force attack detected from IP: {ip_address}")
                take_action_on_attack(username, ip_address)

        time.sleep(10)

def track_failed_attempts(ip_address):
    current_time = time.time()

    if ip_address not in failed_attempts:
        failed_attempts[ip_address] = [current_time]
    else:
        failed_attempts[ip_address].append(current_time)

    failed_attempts[ip_address] = [t for t in failed_attempts[ip_address] if current_time - t <= 300]

    if len(failed_attempts[ip_address]) > 5:
        return True
    return False

def take_action_on_attack(username, ip_address):
    block_ip(ip_address)
    lock_user(username)

def block_ip(ip_address):
    os.system(f"netsh firewall add portopening protocol=TCP port=0 name=Block_{ip_address} mode=DISABLE")
    print(f"Blocked IP: {ip_address}")

def lock_user(username):
    os.system(f"wmic useraccount where name='{username}' set disabled=true")
    print(f"Locked user: {username}")

if __name__ == "__main__":
    monitor_failed_logins()
