import psutil
import time
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from collections import defaultdict
import subprocess

logging.basicConfig(filename='dos_detection.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

TRAFFIC_THRESHOLD = 1 * 1024 * 1024
CHECK_INTERVAL = 5

incoming_traffic = defaultdict(int)


def detect_dos():
    while True:
        track_incoming_traffic()
        log_incoming_traffic()
        time.sleep(CHECK_INTERVAL)


def track_incoming_traffic():
    connections = psutil.net_connections(kind='inet')
    for conn in connections:
        if conn.status == 'ESTABLISHED' and conn.raddr:
            remote_ip = conn.raddr.ip
            incoming_traffic[remote_ip] += conn.raddr.port


def log_incoming_traffic():
    flagged_ips = []
    for ip, traffic in incoming_traffic.items():
        if traffic > TRAFFIC_THRESHOLD:
            logging.info(f"IP: {ip}, Incoming Traffic: {traffic} bytes")
            flagged_ips.append(ip)
        else:
            print("All fine")

    if flagged_ips:
        print(f"Attacking IPs that can be blocked: {', '.join(flagged_ips)}")
        block_ips(flagged_ips)
        send_alert(f"DoS attack detected from IPs: {', '.join(flagged_ips)}")


def block_ips(ip_addresses):
    for ip in ip_addresses:
        command = f"netsh firewall add allowedprogram BLOCK_{ip} ENABLE SUBNET {ip}"
        try:
            subprocess.run(command, shell=True, check=True)
            logging.info(f"Blocked IP: {ip}")
            print(f"Blocked IP: {ip}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to block IP {ip}: {e}")
            print(f"Failed to block IP {ip}: {e}")


def send_alert(message):
    sender_email = "nikhita.thupakula@gmail.com"
    receiver_email = "nikhitaphotos223@gmail.com"
    password = "ykya jaco kxes gyvp"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "DoS Attack Alert"

    msg.attach(MIMEText(message, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        server.login(sender_email, password)

        server.send_message(msg)
        logging.info(f"Alert sent: {message}")
    except Exception as e:
        logging.error(f"Failed to send alert: {e}")
    finally:
        server.quit()


if __name__ == "__main__":
    detect_dos()
