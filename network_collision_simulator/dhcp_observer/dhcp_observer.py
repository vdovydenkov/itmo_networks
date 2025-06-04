from scapy.all import *
import time
from collections import deque, defaultdict

# Параметры мониторинга
time_window     = 10       # Интервал времени в секундах для подсчёта пакетов
mac_threshold   = 20       # Порог по количеству DHCP Discover от одного MAC за time_window
total_threshold = 100      # Порог по общему количеству DHCP Discover за time_window
pause_duration  = 20       # Длительность паузы после обнаружения аномалии в секундах

# Словарь с очередями временных меток по каждому MAC
mac_counters = defaultdict(deque)
# Очередь временных меток для всех запросов
all_requests = deque()

# Временная отметка окончания паузы (начинается с 0 — пауза неактивна)
pause_until = 0

def dhcp_monitor(pkt):
    global pause_until, mac_counters, all_requests

    now = time.time()

    # Если пауза активна, игнорируем пакеты, просто копим данные
    if now < pause_until:
        return

    # Проверяем, что пакет DHCP Discover
    if DHCP in pkt and pkt[DHCP].options[0][1] == 1:  # 1 = DHCP Discover
        mac = pkt[Ether].src

        # Добавляем текущее время в очередь по MAC и для всех пакетов
        mac_counters[mac].append(now)
        all_requests.append(now)

        # Очищаем старые временные метки за пределами time_window
        while mac_counters[mac] and mac_counters[mac][0] < now - time_window:
            mac_counters[mac].popleft()
        while all_requests and all_requests[0] < now - time_window:
            all_requests.popleft()

        # Проверяем аномалию по конкретному MAC
        if len(mac_counters[mac]) > mac_threshold:
            # Звуковой сигнал и предупреждение
            print('\a')
            print(f'[!] Высокая частота DHCP Discover от MAC {mac}: {len(mac_counters[mac])} запросов за последние {time_window} секунд.')
            # Обнуляем счетчики
            mac_counters.clear()
            all_requests.clear()
            # Включаем паузу
            pause_until = now + pause_duration
            return

        # Проверяем аномалию по общему количеству
        if len(all_requests) > total_threshold:
            # Звуковой сигнал и предупреждение
            print('\a')
            print(f'[!] Высокая общая частота DHCP Discover: {len(all_requests)} запросов за последние {time_window} секунд.')
            # Обнуляем счетчики
            mac_counters.clear()
            all_requests.clear()
            # Включаем паузу
            pause_until = now + pause_duration
            return

# Запуск сниффера на интерфейсе
iface = r'\Device\NPF_{32DD913F-77C6-4CF6-B887-610BD0642DAC}'

print('Запуск мониторинга DHCP Discover...')

sniff(filter="udp and (port 67 or 68)", prn=dhcp_monitor, store=0, iface=iface)
