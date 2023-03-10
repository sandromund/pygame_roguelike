import random
import math
import pygame

class AI:

    def __init__(self, ai_type=1, dev_view=False):
        self.offset_min = -300
        self.move_offset_max = 300
        self.reset_counter_min = 120
        self.reset_counter_max = 150
        self.offset_x = None
        self.offset_y = None
        self.reset_counter = None
        self.reset()
        self.ai_type = ai_type
        self.dev_view = dev_view

    def reset(self):
        self.offset_x = random.randrange(self.offset_min, self.move_offset_max)
        self.offset_y = random.randrange(self.offset_min, self.move_offset_max)
        self.reset_counter = random.randrange(self.reset_counter_min, self.reset_counter_max)

    def move_enemy_default(self, player, enemy):
        self.reset_counter -= 1
        if self.reset_counter == 0:
            self.reset()
        if player.x + self.offset_x > enemy.x - player.display_scroll_x:
            enemy.x = enemy.x + enemy.speed
            enemy.flip = False
        elif player.x + self.offset_x < enemy.x - player.display_scroll_x:
            enemy.x = enemy.x - enemy.speed
            enemy.flip = True
        if player.y + self.offset_y > enemy.y - player.display_scroll_y:
            enemy.y = enemy.y + enemy.speed
        elif player.y + self.offset_y < enemy.y - player.display_scroll_y:
            enemy.y = enemy.y - enemy.speed

    @staticmethod
    def move_enemy_aggressive(player, enemy):
        ex, ey = enemy.x - player.display_scroll_x, enemy.y - player.display_scroll_y
        if ex < player.x:
            enemy.x = enemy.x + enemy.speed
            enemy.flip = False
        elif ex > player.x:
            enemy.x = enemy.x - enemy.speed
            enemy.flip = True
        if ey < player.y:
            enemy.y = enemy.y + enemy.speed
        elif ey > player.y:
            enemy.y = enemy.y - enemy.speed

    def move_enemy(self, player, enemy):
        if enemy.knock_back_timer == 0:
            if self.ai_type == 0:
                self.move_enemy_default(player, enemy)
            if self.ai_type == 1:
                self.move_enemy_aggressive(player, enemy)
        else:
            enemy.x -= enemy.knock_back_velocity_x
            enemy.y -= enemy.knock_back_velocity_y
            enemy.knock_back_timer -= 1
            if enemy.knock_back_timer == 0:
                enemy.knock_back_velocity_x = 0
                enemy.knock_back_velocity_y = 0

    def move_companion(self, player, companion):
        # companion stays near the player
        self.move_enemy_default(player, enemy=companion)

    @staticmethod
    def __get_vector(enemy, player):

        # get the vector from the enemy to the player

        ex = enemy.x - player.display_scroll_x
        ey = enemy.y - player.display_scroll_y

        # 1. get the vector distance
        distance_x = ex - player.x
        distance_y = ey - player.y

        # 2. normalize that to a unit vector
        norm = math.sqrt(math.pow(distance_x, 2) + math.pow(distance_y, 2))
        if norm == 0:
            norm = 1
        direction_x = distance_x / norm
        direction_y = distance_y / norm

        # 3. Finally, we want the velocity vector.
        # You get that by multiplying the direction (the unit vector) by the speed.
        vector_x = direction_x * math.sqrt(2)
        vector_y = direction_y * math.sqrt(2)

        # otherwise the enemy run away from the player
        vector_x = vector_x * -1
        vector_y = vector_y * -1

        return vector_x, vector_y

    @staticmethod
    def __vector_to_velocity(enemy, vector_x, vector_y, speed=1):
        angle = math.atan2(enemy.x - vector_x, enemy.y - vector_y)
        x_vel = math.cos(angle) * speed
        y_vel = math.sin(angle) * speed
        return x_vel, y_vel

    @staticmethod
    def __move_towards_player_velocity(enemy, player):
        x_dist = enemy.rect.centerx - player.rect.centerx
        y_dist = enemy.rect.centery - player.rect.centery
        velocity = enemy.speed
        dist = (x_dist ** 2 + y_dist ** 2) ** 0.5
        if dist == 0:
            dist = 1
        x_vel = x_dist / dist * velocity
        y_vel = y_dist / dist * velocity
        return x_vel, y_vel

    @staticmethod
    def __center_of_group(enemies):
        center_x, center_y = 0, 0
        for enemy in enemies:
            center_x += enemy.x
            center_y += enemy.y
        n = len(enemies)
        return (center_x / n), (center_y / n)

    def swarm_ai(self, player, enemy, other_enemies, avoid_factor=1):
        # this is still not how I want it.
        ex = enemy.x - player.display_scroll_x
        ey = enemy.y - player.display_scroll_y
        sx, sy = player.display_scroll_x, player.display_scroll_y
        other_enemies = [e for e in other_enemies if e != enemy]
        other_enemies = [e for e in other_enemies if
                         math.dist((e.x + sx, e.y + sy), (enemy.x + sx, enemy.y + sy)) < enemy.view_range]
        n = len(other_enemies)
        if  n > 1:
            cx , cy = self.__center_of_group(other_enemies +[enemy])
            cx -= player.display_scroll_x
            cy -= player.display_scroll_y

            angle = math.atan2(cx - ex, cy - ey)
            x_vel = math.cos(angle)
            y_vel = math.cos(angle)
            if self.dev_view:
                pygame.draw.line(enemy.display, (0, 0, 255), (ex, ey),
                                 (cx, cy), 5)
            enemy.x -= x_vel
            enemy.y -= y_vel
        else:
            x_vel, y_vel = self.__move_towards_player_velocity(enemy, player)
            enemy.x -= x_vel
            enemy.y -= y_vel

        if ex < player.x:
            enemy.flip = False
        elif ex > player.x:
            enemy.flip = True

    def swarm_ai_old(self, player, enemy, other_enemies, avoid_factor=1):
        # we want to steer to the play but avoid getting to close to other enemies

        # first calculate the vector where the enemy wants to move to the player
        vector_x, vector_y = self.__get_vector(enemy, player)

        ex = enemy.x - player.display_scroll_x
        ey = enemy.y - player.display_scroll_y

        seperation_x, seperation_y = 0, 0
        for e_i in other_enemies:
            if e_i == enemy:
                continue
            # only separate form to close other enemies
            d = math.dist((ex, ey), (e_i.x - player.display_scroll_x, e_i.y - player.display_scroll_y))
            if d < enemy.view_range:
                seperation_x += ex - e_i.x
                seperation_y += ey - e_i.y

        n = len(other_enemies)
        vector_x += ((seperation_x / n) * avoid_factor)
        vector_y += ((seperation_y / n) * avoid_factor)

        enemy.x += vector_x
        enemy.y += vector_y

        if ex < player.x:
            enemy.flip = False
        elif ex > player.x:
            enemy.flip = True
