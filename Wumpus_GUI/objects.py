from settings import *


class MissingAsset:
    """Handles exceptions of missing assets."""
    def __init__(self, expr, msg):
        self.expr = expr
        self.msg = msg


class BaseTile(pg.sprite.Sprite):
    """The Base class of a tile. All other classes inherit attributes from this.
    What parameters to have and what attributes to initialize."""
    def __init__(self, game, image, alpha, x, y):
        pg.sprite.Sprite.__init__(self)
        self.rect = image.get_rect()
        self.rect.left, self.rect.top = x, y
        self.width, self.height = image.get_width(), image.get_height()
        self.texture = image
        self.texture.set_alpha(alpha)
        self.size = TILESIZE
        self.image = self.texture


class Floor(BaseTile):
    """Floor class. Defines the floor. Inherits from 'Tile' class."""
    def __init__(self, game, image, alpha, width, height):
        super(Floor, self).__init__(game, image, alpha, 0, 0)
        self.width, self.height = width*TILESIZE, height*TILESIZE
        image = pg.Surface((self.width, self.height), pg.SRCALPHA)

        for row in range(int(GRIDWIDTH)):
            for col in range(int(GRIDWIDTH)):
                image.blit(self.image, (row*TILESIZE, col*TILESIZE))
        self.image = image

    def update(self, rect):
        """Updates light. If the user moves, the tile is lit up."""
        r = self.size
        x, y = rect.x, rect.y
        s_array = pg.surfarray.pixels_alpha(self.image)
        s_array[x:x+r, y:y+r] = 255


class Player(BaseTile):
    """User Class. Defines the player. Inherits from 'Tile' class."""
    def __init__(self, game, image, alpha):
        super(Player, self).__init__(game, image, alpha, random_pos('WIDTH'), random_pos('HEIGHT'))
        self.game = game
        self.place_player()
        self.print_dangers()

    def place_player(self):
        """Calls for a random values to assign to player position. If these values
        will cause the player to collide with another sprite, a new set of coordinates
        are called for."""
        self.rect.x, self.rect.y = random_pos('WIDTH'), random_pos('HEIGHT')

        while check_collide(self, self.game)[0]:
            self.rect.x, self.rect.y = random_pos('WIDTH'), random_pos('HEIGHT')

    def move(self, direction):
        """Handles movement of player. Calls for check of where the user wants to move,
        if it is accepted, the user's position is updated. Calls for a check if the user
        collided with any entities in the new position that was set. Calls for a check of
        nearby dangers."""
        if not self.out_of_bounds(direction):
            self.rect.x += direction[0]*self.size
            self.rect.y += direction[1]*self.size

            collision, entity = check_collide(self, self.game)
            if collision:
                self.collision_event(entity)
            self.print_dangers()

    def shoot(self):
        """The user has requested to shoot. Creates an arrow sprites at the player's location"""
        self.game.arrow_sprite.add(Arrow(self.game, load_asset(IMAGE, ARROW_LEFT), LIGHT_FULL,
                                         self.rect.x, self.rect.y))

    def collision_event(self, entity):
        """Receives a parameter, that specifies what the user has collided with, and
        then executes the corresponding events."""
        self.game.update()
        if entity == "Bat":
            self.reveal_bat()
            self.place_player()
        elif entity == "Wumpus":
            self.game.alive = False
            self.game.game_over(entity)
        elif entity == "Pit":
            self.game.alive = False
            self.game.game_over(entity)

    def out_of_bounds(self, direction):
        """Receives a request in change of position in form of a direction.
        Checks if the move will cause the player to go out of bounds."""
        if not 0 <= self.rect.x + direction[0] <= (GRIDWIDTH - 1) * 128 or \
                not 0 <= self.rect.y + direction[1] <= (GRIDHEIGHT - 1) * 128:
            return True
        return False

    def reveal_bat(self):
        """The player has collided with a bat. Will reveal the position of this bat."""
        for sprite in self.game.bat_sprites:
            if sprite.rect == self.game.player_sprite.sprite.rect:
                self.game.bats_hit.append(sprite.num)

    def print_dangers(self):
        """The player has spawned or moved. Checks for any sprites in adjacent tiles (8-directions).
        Applies changes to a bool in case anything was near."""
        r = TILESIZE
        x, y, = self.rect.x, self.rect.y
        w_x, w_y = self.game.wumpus_sprite.sprite.rect.x, self.game.wumpus_sprite.sprite.rect.y
        adjacent = {(x+r, y), (x-r, y), (x, y+r), (x, y-r), (x+r, y+r), (x+r, y-r), (x-r, y+r), (x-r, y-r)}

        if (w_x, w_y) in adjacent:
            self.game.wumpus_near = True
        else:
            self.game.wumpus_near = False

        for sprite in self.game.bat_sprites:
            if (sprite.rect.x, sprite.rect.y) in adjacent:
                self.game.bats_near = True
                break
            else:
                self.game.bats_near = False

        for sprite in self.game.pit_sprites:
            if (sprite.rect.x, sprite.rect.y) in adjacent:
                self.game.pit_near = True
                break
            else:
                self.game.pit_near = False


class Arrow(BaseTile):
    """Arrow class. Defines the arrow. Inherits from 'Tile' class."""
    def __init__(self, game, image, alpha, x, y):
        super(Arrow, self).__init__(game, image, alpha, x, y)
        self.game = game
        self.moves = 3

    def move(self, direction):
        """The user can move the arrow X times. The user has requested to move the arrow.
        Calls for a check of where the user wants the arrow to move, if it is accepted the
        arrow location is updated. Calls for a check if the arrow collided with any
        sprite in the new location."""
        if not self.out_of_bounds(direction) and self.moves >= 1:
            self.change_image(direction)
            self.rect.x += direction[0]*self.size
            self.rect.y += direction[1]*self.size
            self.moves -= 1

            collision, entity = check_collide(self, self.game)
            if collision:
                self.collision_event(entity)

            if self.moves == 0:
                self.game.control_arrow = False

    def collision_event(self, entity):
        """Receives a parameter, that specifies what the arrow has collided with, and
        then executes the corresponding events."""
        self.game.update()
        if entity == "Wumpus":
            self.game.wumpus_alive = False
            self.game.wumpus_sprite.sprite.image = load_asset(IMAGE, WUMPUSDEAD)
            self.game.game_over(entity)

    def out_of_bounds(self, direction):
        """Receives a request in change of position in form of a direction.
        Checks if the move will cause the arrow to go out of bounds."""
        if not 0 <= self.rect.x + direction[0] <= (GRIDWIDTH - 1) * 128 or not \
                                0 <= self.rect.y + direction[1] <= (GRIDHEIGHT - 1) * 128:
            return True
        return False

    def change_image(self, direction):
        """Changes image of the arrow based on the direction."""
        if direction[0] == 1:
            self.game.arrow_sprite.sprite.image = load_asset(IMAGE, ARROW_RIGHT)
        elif direction[0] == -1:
            self.game.arrow_sprite.sprite.image = load_asset(IMAGE, ARROW_LEFT)
        elif direction[1] == 1:
            self.game.arrow_sprite.sprite.image = load_asset(IMAGE, ARROW_DOWN)
        elif direction[1] == -1:
            self.game.arrow_sprite.sprite.image = load_asset(IMAGE, ARROW_UP)


class Wumpus(BaseTile):
    """Wumpus Class. Defines the Wumpus. Inherits from 'Tile' class."""
    def __init__(self, game, image, alpha, x, y):
        super(Wumpus, self).__init__(game, image, alpha, random_pos('WIDTH'), random_pos('HEIGHT'))
        self.game = game
        self.visible = False
        self.place()

    def place(self):
        """Places Wumpus in an empty tile. Passes itself and game instance
        to the collide function."""
        while check_collide(self, self.game)[0]:
            self.rect.x, self.rect.y = random_pos('WIDTH'), random_pos('HEIGHT')

    def draw(self):
        """Draws Wumpus."""
        self.game.screen.blit(self.image, self.rect)


class Bat(BaseTile):
    """Bat Class. Defines the Bat. Inherits from 'Tile' class."""
    def __init__(self, game, image, alpha, x, y, num):
        super(Bat, self).__init__(game, image, alpha, random_pos('WIDTH'), random_pos('HEIGHT'))
        self.game = game
        self.num = num
        self.place()

    def place(self):
        """Places Bat in an empty tile. Passes itself and game instance
        to the collide function."""
        while check_collide(self, self.game)[0]:
            self.rect.x, self.rect.y = random_pos('WIDTH'), random_pos('HEIGHT')

    def draw(self):
        """Draws pit onto the screen."""
        self.game.screen.blit(self.image, self.rect)


class Pit(BaseTile):
    """Pit Class. Defines the Pit. Inherits from 'Tile' class."""
    def __init__(self, game, image, alpha, x, y, num):
        super(Pit, self).__init__(game, image, alpha, random_pos('WIDTH'), random_pos('HEIGHT'))
        self.game = game
        self.num = num
        self.place()

    def place(self):
        """Places Pit in an empty tile. Passes itself and game instance
        to the collide function."""
        while check_collide(self, self.game)[0]:
            self.rect.x, self.rect.y = random_pos('WIDTH'), random_pos('HEIGHT')

    def draw(self):
        """Draws pit onto the screen."""
        self.game.screen.blit(self.image, self.rect)


def random_pos(pos):
    """General function that generates a random integers which lies
    within given boundaries of the game-plan."""
    if pos == 'WIDTH':
        return randint(0, GRIDWIDTH - 1) * TILESIZE
    elif pos == 'HEIGHT':
        return randint(0, GRIDHEIGHT - 1) * TILESIZE


def check_collide(instance, entities):
    """General collision function. Checks whether the instance (e.g. Player/Arrow/Bat...)
    has collided with any other sprite/entity. Returns if there was a collision and with what."""
    collision, entity = False, "None"
    if len(pg.sprite.spritecollide(instance, entities.bat_sprites, False)) > 0:
        collision, entity = True, "Bat"
    elif len(pg.sprite.spritecollide(instance, entities.wumpus_sprite, False)) > 0:
        collision, entity = True, "Wumpus"
    elif len(pg.sprite.spritecollide(instance, entities.pit_sprites, False)) > 0:
        collision, entity = True, "Pit"
    return collision, entity


def load_asset(asset, file):
    """Loads assets from root folder. Receives info on what kind of file
    and what asset that is requested. If it fails to find/load an exceptions is thrown."""
    if asset == IMAGE:
        try:
            image = pg.image.load(os.path.join(asset, file))
        except pg.error as message:
            print("Missing asset: " + file + " from " + asset)
            raise SystemExit(message)
        return image
    elif asset == FILE:
        try:
            with open(os.path.join(asset, file), 'r') as file:
                try:
                    data = int(file.read())
                except:
                    data = 0
        except IOError as message:
            print("Missing asset: " + file + " from " + asset)
            raise SystemExit(message)
        return data


def save_data(asset, file, data):
    """Saves data. Receives input of what kind of file, and what file."""
    if asset == FILE:
        with open(os.path.join(asset, file), 'w+') as file:
            file.write(str(data))
