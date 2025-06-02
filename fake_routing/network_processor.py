def send_packet(source, destination):
    '''
    Эмулирует отправку пакета от одного маршрутизатора к другому.
    source: Исходный маршрутизатор
    destination: Конечный маршрутизатор
    '''
    print(f'\nОтправка пакета из {source.name} в {destination.name}')
    current = source
    visited = set()
    path = [source.name]  # Список для хранения маршрута

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
    '''
    Выводит на экран список маршрутизаторов и список связей между ними.
    routers: Словарь маршрутизаторов (имя -> Router)
    links: Список кортежей (имя1, имя2, стоимость, preference)
    '''
    print('Маршрутизаторы:')
    for name, router in routers.items():
        print(f'  "{name}": IP = "{router.ip}"')

    print('\nСвязи между маршрутизаторами:')
    for a, b, cost, pref in links:
        print(f'  "{a}" <--> "{b}" (стоимость: {cost}, preference: {pref})')

