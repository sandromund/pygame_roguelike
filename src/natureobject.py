class NatureObject:

    def __init__(self, image, display, x, y):
        # NatureObjects are currently not in the game
        self.image = image
        self.display = display
        self.x = x
        self.y = y
        self.alive = True
        self.live = 100

    def draw(self, display_scroll_x, display_scroll_y):
        if not self.alive:
            return
        self.display.blit(self.image, (self.x - display_scroll_x, self.y - display_scroll_y, 16, 16))


class Tree(NatureObject):

    def __init__(self, image, display, x, y):
        super().__init__(image, display, x, y)


class Stone(NatureObject):

    def __init__(self, image, display, x, y):
        super().__init__(image, display, x, y)
