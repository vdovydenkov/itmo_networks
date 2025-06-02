import heapq  # Для реализации приоритетной очереди

class Router:
    _id_counter = 0  # Счётчик для присвоения уникального идентификатора каждому маршрутизатору

    def __init__(self, name, ip):
        '''
        Инициализация маршрутизатора.
        name: Имя маршрутизатора (например, "A")
        ip: IP-адрес маршрутизатора
        '''
        self.name = name
        self.ip = ip
        self.neighbors = {}      # Словарь соседей: сосед -> (стоимость, preference)
        self.routing_table = {}  # Таблица маршрутизации: получатель -> (следующий хоп, стоимость, preference)
        self._id = Router._id_counter
        Router._id_counter += 1  # Увеличиваем глобальный счётчик ID

    def __lt__(self, other):
        '''
        Определяет правило сравнения для heapq, если узлы имеют одинаковые приоритеты.
        '''
        return self.name < other.name

    def add_link(self, other_router, cost, preference=100):
        '''
        Установить двустороннюю связь между двумя маршрутизаторами.
        other_router: Соседний маршрутизатор
        cost: Стоимость канала связи
        preference: Приоритет канала (меньше — лучше)
        '''
        self.neighbors[other_router] = (cost, preference)
        other_router.neighbors[self] = (cost, preference)

    def update_routing_table(self, network_routers):
        '''
        Обновление таблицы маршрутизации с помощью модифицированного алгоритма Дейкстры.
        В учёт берутся как стоимость маршрута, так и предпочтение (preference).
        '''
        # Очередь с приоритетом: (накопленная стоимость, накопленный preference, текущий маршрутизатор, предыдущий)
        queue = [(0, 0, self, None)]
        visited = {}  # Массив посещённых узлов: маршрутизатор -> (предыдущий, стоимость, preference)

        while queue:
            cost, pref, current, previous = heapq.heappop(queue)

            if current in visited:
                continue  # Пропускаем уже посещённые маршрутизаторы

            visited[current] = (previous, cost, pref)

            # Добавляем в очередь всех непосещённых соседей
            for neighbor, (weight, preference) in current.neighbors.items():
                if neighbor not in visited:
                    heapq.heappush(queue, (
                        cost + weight,         # накапливаем стоимость
                        pref + preference,     # накапливаем preference
                        neighbor,
                        current
                    ))

        # Обновляем таблицу маршрутизации на основе построенного графа visited
        self.routing_table.clear()
        for router, (prev, total_cost, total_pref) in visited.items():
            if router == self:
                continue  # Пропускаем самого себя

            # Определяем следующий хоп по цепочке назад к текущему узлу
            next_hop = router
            while visited[next_hop][0] != self and visited[next_hop][0] is not None:
                next_hop = visited[next_hop][0]

            # Сохраняем маршрут в таблице: конечный -> (следующий хоп, стоимость, preference)
            self.routing_table[router] = (next_hop, total_cost, total_pref)

    def route_packet(self, destination):
        '''
        Определяет, через какого соседа отправить пакет для достижения цели.
        destination: Конечный маршрутизатор
        Возвращает Следующий хоп (маршрутизатор) или None, если маршрут не найден
        '''
        if destination not in self.routing_table:
            print(f'{self.name}: Нет маршрута до {destination.name}')
            return None

        next_hop, cost, pref = self.routing_table[destination]
        print(f'{self.name}: Отправляю пакет через {next_hop.name} (стоимость: {cost}, preference: {pref})')
        return next_hop


