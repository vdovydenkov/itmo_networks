from router_class import Router
from network_processor import send_packet, print_network_configuration

# Создаём маршрутизаторы с именами A, B, ..., G и IP-адресами
routers = {
    name: Router(name, f"10.0.0.{i+1}")
    for i, name in enumerate(["A", "B", "C", "D", "E", "F", "G"])
}

# Определяем связи между маршрутизаторами: (имя1, имя2, стоимость, preference)
links = [
    ("A", "B", 1, 50),
    ("B", "C", 2, 30),
    ("C", "G", 3, 20),
    ("A", "D", 2, 20),
    ("D", "E", 2, 20),
    ("E", "G", 2, 20),
    ("B", "E", 5, 100),
    ("C", "F", 1, 10),
    ("F", "G", 1, 10),
]

def main():
    # Показываем исходную сеть
    print_network_configuration(routers, links)
    # Устанавливаем соединения на основе списка links
    for a, b, cost, pref in links:
        routers[a].add_link(routers[b], cost, pref)

    # Строим таблицы маршрутизации для всех маршрутизаторов
    for router in routers.values():
        router.update_routing_table(routers.values())

    # Эмуляция отправки пакета A -> G
    send_packet(routers["A"], routers["G"])

    # Изменение метрик связи D–E и повторная отправка
    print("\nИзменяем preference для связи D-E до 200 (менее предпочтительный путь)")
    # Устанавливаем более высокий preference для связи D-E (менее предпочтительна)
    routers["D"].neighbors[routers["E"]] = (2, 200)
    routers["E"].neighbors[routers["D"]] = (2, 200)

    # Повторное обновление таблиц маршрутизации
    for router in routers.values():
        router.update_routing_table(routers.values())

    # Повторная отправка после изменения предпочтений
    send_packet(routers["A"], routers["G"])

if __name__ == '__main__':
    main()