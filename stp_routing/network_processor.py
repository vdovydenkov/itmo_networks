import heapq

def send_packet(source, destination):
    print(f'\nОтправка пакета из {source.name} в {destination.name}')
    current = source
    visited = set()
    path = [source.name]

    while current != destination:
        visited.add(current)
        current = current.route_packet(destination)

        if current is None or current in visited:
            print('Маршрут не найден.')
            return

        path.append(current.name)

    print(f'Пакет достиг пункта назначения: {destination.name}')
    print(f'Маршрут: {" -> ".join(path)}')

def print_network_configuration(routers, links):
    print('Маршрутизаторы:')
    for name, router in routers.items():
        print(f'  "{name}": IP = "{router.ip}"')

    print('\nСвязи между маршрутизаторами:')
    for a, b, cost, pref in links:
        print(f'  "{a}" <--> "{b}" (стоимость: {cost}, preference: {pref})')

def build_spanning_tree(routers):
    """
    Построение остовного дерева STP (Spanning Tree Protocol).
    Возвращает множество активных связей в виде frozenset({router1, router2}).
    """
    root = min(routers.values(), key=lambda r: r.ip)
    visited = set()
    active_links = set()
    queue = [(0, root, None)]

    while queue:
        cost, current, parent = heapq.heappop(queue)
        if current in visited:
            continue
        visited.add(current)
        if parent:
            active_links.add(frozenset([current, parent]))

        for neighbor, (weight, _) in current.neighbors.items():
            if neighbor not in visited:
                heapq.heappush(queue, (cost + weight, neighbor, current))

    return active_links
