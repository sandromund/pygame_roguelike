class Tree:

    def __init__(self, image, display, x, y):
        self.image = image
        self.display = display
        self.x = x
        self.y = y

    def draw(self, display_scroll_x, display_scroll_y):
        self.display.blit(self.image, (self.x - display_scroll_x, self.y - display_scroll_y, 16, 16))
