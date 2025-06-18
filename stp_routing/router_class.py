import heapq

class Router:
    _id_counter = 0

    def __init__(self, name, ip):
        self.name = name
        self.ip = ip
        self.neighbors = {}  # Словарь: сосед -> (стоимость, preference)
        self.routing_table = {}  # Назначение -> (следующий_хоп, суммарная_стоимость, суммарный_preference)
        self._id = Router._id_counter
        Router._id_counter += 1

    def __lt__(self, other):
        # Для работы с heapq: сравнение по имени
        return self.name < other.name

    def add_link(self, other_router, cost, preference=100):
        """
        Устанавливает двустороннюю связь между маршрутизаторами.
        """
        self.neighbors[other_router] = (cost, preference)
        other_router.neighbors[self] = (cost, preference)

    def remove_link(self, other_router):
        """
        Удаляет двустороннюю связь между маршрутизаторами.
        """
        self.neighbors.pop(other_router, None)
        other_router.neighbors.pop(self, None)

    def update_routing_table(self, network_routers):
        """
        Строит таблицу маршрутизации с помощью алгоритма Дейкстры,
        учитывая стоимость и preference.
        """
        queue = [(0, 0, self, None)]  # (сумм.стоимость, сумм.preference, текущий, предыдущий)
        visited = {}

        while queue:
            cost, pref, current, previous = heapq.heappop(queue)
            if current in visited:
                continue
            visited[current] = (previous, cost, pref)

            for neighbor, (weight, preference) in current.neighbors.items():
                if neighbor not in visited:
                    heapq.heappush(queue, (
                        cost + weight,
                        pref + preference,
                        neighbor,
                        current
                    ))

        self.routing_table.clear()
        for router, (prev, total_cost, total_pref) in visited.items():
            if router == self:
                continue
            # Находим следующий хоп
            next_hop = router
            while visited[next_hop][0] != self and visited[next_hop][0] is not None:
                next_hop = visited[next_hop][0]
            self.routing_table[router] = (next_hop, total_cost, total_pref)

    def route_packet(self, destination):
        """
        Определяет, куда перенаправить пакет для достижения пункта назначения.
        """
        route = self.routing_table.get(destination)
        if route:
            next_hop, _, _ = route
            return next_hop
        return None
