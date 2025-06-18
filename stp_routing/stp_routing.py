from router_class import Router
from network_processor import send_packet, print_network_configuration, build_spanning_tree

# Создаём маршрутизаторы с IP-адресами
routers = {
    name: Router(name, f"10.0.0.{i+1}")
    for i, name in enumerate(["A", "B", "C", "D", "E", "F", "G"])
}

# Определяем связи между маршрутизаторами (стоимость и предпочтение)
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
    print_network_configuration(routers, links)

    # Устанавливаем все связи между маршрутизаторами
    for a, b, cost, pref in links:
        routers[a].add_link(routers[b], cost, pref)

    # Строим остовное дерево STP
    spanning_tree_links = build_spanning_tree(routers)

    print("\nАктивные связи по STP (остовное дерево):")
    for link in spanning_tree_links:
        names = sorted([r.name for r in link])
        print(f"  {names[0]} <--> {names[1]}")

    # Удаляем неактивные связи
    print("\nОтключаем неиспользуемые связи:")
    for router in routers.values():
        to_remove = []
        for neighbor in list(router.neighbors):  # Важно использовать list() для безопасной итерации
            if frozenset([router, neighbor]) not in spanning_tree_links:
                to_remove.append(neighbor)
        for neighbor in to_remove:
            print(f"  {router.name} --X-- {neighbor.name}")
            router.remove_link(neighbor)

    # Обновляем таблицы маршрутизации с учетом активной топологии
    for router in routers.values():
        router.update_routing_table(routers.values())

    # Эмуляция передачи пакета
    send_packet(routers["A"], routers["G"])

if __name__ == '__main__':
    main()
