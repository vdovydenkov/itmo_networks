from scapy.all import *
from collections import defaultdict, deque
import time

# Параметры
mac_threshold = 20           # Порог запросов с одного MAC за time_window
total_threshold = 100        # Порог всех DHCP Discover за time_window
time_window = 60             # Интервал времени в секундах

# Хранилища
requests_per_mac = defaultdict(deque)
all_requests = deque()

def dhcp_monitor(pkt):
    if DHCP in pkt and pkt[DHCP].options[0][1] == 1:  # DHCP Discover
        mac_bytes = pkt[BOOTP].chaddr[:6]
        mac = ':'.join(f'{b:02x}' for b in mac_bytes)
        now = time.time()

        # Обновляем очередь запросов для данного MAC
        mac_queue = requests_per_mac[mac]
        mac_queue.append(now)
        while mac_queue and mac_queue[0] < now - time_window:
            mac_queue.popleft()

        # Обновляем очередь всех запросов
        all_requests.append(now)
        while all_requests and all_requests[0] < now - time_window:
            all_requests.popleft()

        # Проверка порогов
        if len(mac_queue) > mac_threshold:
            print('\a')  # Звуковой сигнал
            print(f"[!] Высокая частота DHCP Discover от MAC {mac}: {len(mac_queue)} запросов за последние {time_window} секунд.")

        if len(all_requests) > total_threshold:
            print('\a')  # Звуковой сигнал
            print(f"[!] Высокая общая частота DHCP Discover: {len(all_requests)} запросов за последние {time_window} секунд.")

if __name__ == "__main__":
    print("Запуск мониторинга DHCP Starvation...")
    sniff(filter="udp and (port 67 or port 68)", prn=dhcp_monitor, store=0)
