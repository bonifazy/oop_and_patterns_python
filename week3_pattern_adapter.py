class MappingAdapter:  # Адаптер к обработчику
    def __init__(self, adaptee):
        self.adaptee = adaptee

    def lighten(self, grid):
        width = len(grid[0])
        height = len(grid)
        lights = []
        obstacles = []

        self.adaptee.set_dim((width, height))

        for h in range(height):
            for w in range(width):
                if grid[h][w] == 1:
                    lights.append((w, h))
                if grid[h][w] == -1:
                    obstacles.append((w, h))
        self.adaptee.set_lights(lights)
        self.adaptee.set_obstacles(obstacles)
        print(self.adaptee.lights, self.adaptee.obstacles)
        return self.adaptee.generate_lights()
