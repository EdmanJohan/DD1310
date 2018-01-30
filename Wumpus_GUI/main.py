# Wumpus - 154
# Johan Edman
# 2016/12/07
# Ver. 1.0.1 - GUI

from settings import *
from objects import *


class Game(object):
    def __init__(self):
        """Initialize Game Object"""
        pg.init()
        pg.display.set_caption(TITLE)
        self.running = True

        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.background = pg.Surface((WIDTH, HEIGHT))
        self.background.fill(BLACK)
        self.background.convert()

        self.difficulty = DIFFICULTY
        self.load_highscore()

    def new(self):
        """A new Game is started - Calls for initialization of default values,
            difficulty and sprites. Calls main function."""

        self.initialize_values()
        self.difficulty_modifier()
        self.initialize_sprites()

        self.main()

    def initialize_values(self):
        """Initializes/Resets all values to given/default."""
        self.draw_all = False

        self.moves = 0
        self.arrows = ARROWS
        self.control_arrow = False
        self.playing = True
        self.alive = True

        self.bats, self.pits = BATS, PITS
        self.wumpus_alive = True
        self.wumpus_near = False
        self.bats_near = False
        self.pit_near = False
        self.bats_hit = []

    def initialize_sprites(self):
        """Initializes all sprite groups and populates then."""
        self.wumpus_sprite = pg.sprite.GroupSingle()
        self.bat_sprites = pg.sprite.Group()
        self.pit_sprites = pg.sprite.Group()

        self.player_sprite = pg.sprite.GroupSingle()
        self.arrow_sprite = pg.sprite.GroupSingle()

        self.wumpus_sprite.add(Wumpus(self, load_asset(IMAGE, WUMPUS), LIGHT_FULL, TILESIZE, TILESIZE))
        for i in range(self.bats):
            self.bat_sprites.add(Bat(self, load_asset(IMAGE, BAT), LIGHT_FULL, TILESIZE, TILESIZE, i))
        for i in range(self.pits):
            self.pit_sprites.add(Pit(self, load_asset(IMAGE, PIT), LIGHT_FULL, TILESIZE, TILESIZE, i))

        self.player_sprite.add(Player(self, load_asset(IMAGE, PLAYER), LIGHT_FULL))

        self.floor_sprite = pg.sprite.GroupSingle()
        self.floor_sprite.add(Floor(game, load_asset(IMAGE, TILE), LIGHT_NULL, GRIDWIDTH, GRIDHEIGHT))
        self.floor_sprite.update(self.player_sprite.sprite.rect)

    def main(self):
        """Main loop - While the user wants to play - calls for input, updates and drawing."""
        self.running = True

        while self.playing:
            self.input()
            self.update()
            self.draw()

    def input(self):
        """Iterates through event list, listens for user key-presses.
            User may through certain keys, quit, start, restart or interact with the game."""
        for event in pg.event.get():

            if event.type == QUIT:
                self.quit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.quit()
                if event.key in MOVEKEYS.keys() and self.alive:
                    if self.control_arrow:
                        self.arrow_sprite.sprite.move(MOVEKEYS[event.key])
                    else:
                        self.moves += 1
                        self.player_sprite.sprite.move(MOVEKEYS[event.key])
                if event.key == K_SPACE:
                    if self.arrows >= 1:
                        self.moves += 1
                        self.arrows -= 1
                        self.control_arrow = True
                        self.player_sprite.sprite.shoot()
                if self.playing is False and event.key == K_RETURN:
                    return True
                if event.key == K_BACKSPACE:
                    self.playing = False
                    self.running = False

    def update(self):
        """Adds lightning where the player moves, so that the tile is visible.
        Updates the screen."""
        self.floor_sprite.update(self.player_sprite.sprite.rect)
        pg.display.flip()

    def draw(self):
        """Main draw function - Applies background to screen, then draws sprites/text messages
         in the order they are requested on top of that. Some sprites/text messages are only
         drawn on screen under certain conditions."""
        self.screen.blit(self.background, (0, 0))
        self.floor_sprite.draw(self.screen)

        pg.draw.line(self.screen, LIGHTGREY, (GRIDWIDTH * TILESIZE, 0), (GRIDWIDTH * TILESIZE, GRIDWIDTH * TILESIZE), 3)
        self.draw_text("Difficulty: " + str(self.difficulty), 22, PINK, WIDTH * 0.90, HEIGHT / 1.1)
        self.draw_text("Arrows: " + str(self.arrows), 16, PINK, WIDTH * 0.7, HEIGHT / 1.085)
        self.draw_text("Score: " + str(self.moves), 16, PINK, WIDTH * 0.705, HEIGHT / 1.13)

        self.draw_text("Walking around the culverts, suddenly:", 15, PINK, WIDTH * 0.81, HEIGHT * 1 / 12 - 30)
        if self.wumpus_near:
            self.draw_text("- You smell Wumpus.", 14, PINK, WIDTH * 0.72, HEIGHT * 1 / 12)
        if self.bats_near:
            self.draw_text("- You can hear bats flapping.", 14, PINK, WIDTH * 0.7595, HEIGHT * 1 / 12 + 30)
        if self.pit_near:
            self.draw_text("- You feel a draft.", 14, PINK, WIDTH * 0.72, HEIGHT * 1 / 12 + 60)

        if self.draw_all:
            self.floor_sprite.add(Floor(game, load_asset(IMAGE, TILE), LIGHT_FULL, GRIDWIDTH, GRIDHEIGHT))
            self.floor_sprite.draw(self.screen)
            self.wumpus_sprite.draw(self.screen)
            self.bat_sprites.draw(self.screen)
            self.pit_sprites.draw(self.screen)

        if len(self.bats_hit) > 0:
            for sprite in self.bat_sprites:
                if sprite.num in self.bats_hit:
                    sprite.draw()

        self.player_sprite.draw(self.screen)
        self.arrow_sprite.draw(self.screen)

    def load_highscore(self):
        """Calls for highscore data"""
        self.highscore = load_asset(FILE, HIGHSCORE)

    def check_highscore(self):
        """Decides whether moves taken to win/loose is lower than current highscore.
            Updates highscore and calls for save function if that is the case."""
        self.new_highscore = False
        if (self.highscore == 0 or self.moves < self.highscore) and self.wumpus_alive is False:
            self.highscore = self.moves
            self.new_highscore = True
            self.save_highscore()

    def save_highscore(self):
        """Calls for saving data"""
        save_data(FILE, HIGHSCORE, self.highscore)

    def change_difficulty(self, offset):
        """User calls for change in difficulty, checks that this is within allowed range
        and sets the value."""
        if offset < 0 and self.difficulty > 1:
            self.difficulty -= 1
        elif offset > 0 and self.difficulty < 3:
            self.difficulty += 1

    def difficulty_modifier(self):
        """User has called for change in difficulty, new difficulty is applied by changing
        amount of pits, bats and arrows."""
        if self.difficulty == 3:
            self.pits, self.bats, self.arrows = 5, 4, 3
        elif self.difficulty == 2:
            self.pits, self.bats = 3, 4
        elif self.difficulty == 1:
            self.pits, self.bats = 2, 3

    def game_over(self, cause):
        """Game Over - Draws all the entities onto the screen. Writes out the reason to
        why the game has ended. Quits the main game loop. Allowing the game to
        proceed to the Game Over screen."""
        self.draw_all = True
        self.playing = False
        self.draw()

        while True:
            if not self.alive:
                self.draw_text("You died.", 48, PINK, WIDTH * 2 / 6, HEIGHT * 2 / 5)
                if cause == "Wumpus":
                    self.draw_text("Wumpus got you", 13, PINK, WIDTH * 2 / 6, HEIGHT * 2 / 4)
                elif cause == "Pit":
                    self.draw_text("You fell into a pit.", 13, PINK, WIDTH * 2 / 6, HEIGHT * 2 / 4)
            elif not self.wumpus_alive:
                self.draw_text("You Won!", 48, PINK, WIDTH * 2 / 6, HEIGHT * 2 / 5)
                self.draw_text("You killed Wumpus!", 13, PINK, WIDTH * 2 / 6, HEIGHT * 2 / 4)

            self.update()
            if self.input():
                return False

    def show_menu_screen(self):
        """Game has been started and menu screen is showed. Will wait for input from user
        before going to main game loop."""
        self.draw_menu_screen()
        self.wait_input("Start")

    def show_game_over_screen(self):
        """Checks that the game is not running. Calls for drawing of game over screen and for
        check of highscore. Will wait for input from user to restart or quit the game"""
        if not self.running:
            return
        self.check_highscore()
        self.draw_game_over_screen()
        self.wait_input("Game Over")

    def draw_menu_screen(self):
        """Draws the menu screen, and updates the screen."""
        self.screen.fill(BLACK)
        self.screen.blit(load_asset(IMAGE, BACKGROUND), (0, 0))
        self.screen.blit(load_asset(IMAGE, WELCOME), (WIDTH / 2 - 105, HEIGHT / 5))
        self.draw_text("You must find and kill Wumpus.", 22, PINK, WIDTH / 2, HEIGHT * 2 / 5)
        self.draw_text("Arrows to move. Space to shoot.", 22, PINK, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Arrow Up/Down - Change difficulty", 22, PINK, WIDTH / 2, HEIGHT / 2 + 33)
        self.draw_text("Backspace - Restart game", 22, PINK, WIDTH / 2, HEIGHT / 2 + 66)
        self.draw_text("Difficulty: " + str(self.difficulty), 22, PINK, WIDTH * 0.90, HEIGHT / 1.1)
        self.draw_text("Press Enter to play", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        self.draw_text("High Score: " + str(self.highscore), 22, PINK, WIDTH / 2, 15)
        pg.display.flip()

    def draw_game_over_screen(self):
        """Checks what the game over condition was. Different messages are drawn depending
        on if the player won or lost. Draws rest of game over screen."""
        self.screen.fill(BLACK)
        if self.wumpus_alive:
            self.screen.blit(load_asset(IMAGE, BACKGROUND_GO_LOST), (0, 0))
        else:
            self.screen.blit(load_asset(IMAGE, BACKGROUND_GO_WON), (0, 0))

        self.screen.blit(load_asset(IMAGE, GAMEOVER), (WIDTH / 2 - 125, HEIGHT / 5))
        self.draw_text("Score: " + str(self.moves), 22, PINK, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press Enter to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        self.draw_text("Difficulty: " + str(self.difficulty), 22, PINK, WIDTH * 0.90, HEIGHT / 1.1)
        self.draw_text("Arrow Up/Down - Change difficulty", 14, PINK, WIDTH / 2, HEIGHT / 2 + 99)

        if self.new_highscore:
            self.draw_text("NEW HIGH SCORE!", 22, PINK, WIDTH / 2, HEIGHT / 2 + 35)

        pg.display.flip()

    def wait_input(self, screen):
        """Iterates through events captured, much like input function, except that it
         it will continue to loop until the user wants to proceed. """
        wait = True
        while wait:
            for event in pg.event.get():

                if event.type == QUIT:
                    self.quit()

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.quit()
                    if event.key == K_RETURN:
                        wait = False
                    if event.key == K_UP and (screen == "Start" or screen == "Game Over"):
                        self.change_difficulty(1)
                    if event.key == K_DOWN and (screen == "Start" or screen == "Game Over"):
                        self.change_difficulty(-1)

                if screen == "Start":
                    self.draw_menu_screen()
                if screen == "Game Over":
                    self.draw_game_over_screen()

    def draw_text(self, text, size, color, x, y):
        """General text-drawing function. Takes in what text to draw, and different
        parameters that sets various attributes of the drawn message. Pushes to screen."""
        font = pg.font.SysFont("monospace", size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    @staticmethod
    def quit():
        """Quits the game gracefully."""
        pg.quit()
        sys.exit()

if __name__ == "__main__":
    """Main function. Creates a new game object, calls for the menu screen to show, for the game initiate
    and the game over screen to show. If the user does nto call for a quit, the game will restart,
     allowing the user to play again."""
    game = Game()
    game.show_menu_screen()
    while True:
        game.new()
        game.show_game_over_screen()
