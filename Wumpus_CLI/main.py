# Wumpus - 154
# Johan Edman
# 2016/12/07
# Ver. 1.0.0 - CLI

from objects import *


class Game:
    def __init__(self):
        """Initialize Game, CSC and HighScore objects"""
        self.running = True
        self.playing = True
        self.menu_show = True

        self.CSC = CSC()
        self.HighScore = HighScore()

    def new_game(self):
        """A new game has been started. Calls for player event handling.
        When the game comes to and end, calls for function to see if the
        user wants to play again."""
        while self.playing:
            self.player_event()
            self.play_again()

    def main(self):
        """Main game loop. While the user doesn't call for a quit,
        the menu is printed and user is asked for input."""
        while self.menu_show:
            self.show_menu_screen()
            self.menu_option(check_input("Val: ", 1, 5))

    @staticmethod
    def show_menu_screen():
        """Prints out the menu to the screen."""
        output('Strings', 'Welcome')
        output('Strings', 'Menu')

    def menu_option(self, option):
        """Receives user-choice for sub-menu, takes the
        player to the corresponding function/screen."""
        if option == 1:
            clear()
            output('Strings', 'Instructions')
            wait("Tryck 'Enter' för att gå tillbaka till menyn.")
        elif option == 2:
            clear()
            self.CSC.change_difficulty()
            wait("Tryck 'Enter' för att gå tillbaka till menyn.")
        elif option == 3:
            clear()
            self.playing = True
            self.new_game()
        elif option == 4:
            clear()
            print(HighScore())
            wait("Tryck 'Enter' för att gå tillbaka till menyn.")
        elif option == 5:
            clear()
            self.quit_game()

    def player_event(self):
        """Handles player events. If the player wants to move/shoot.
        Checks consequences of player's actions. If an action causes and
        game-ending scenario to be relevant, a corresponding event is called (Win/Loss)."""
        try:
            arrows = 2
            while arrows > 0:
                print(self.CSC.player_pos)
                option = string_check("Vill du förflytta dig eller skjuta? (F/S) ", 'f', 's')
                self.HighScore.player_score_incr()
                if option == 'f':
                    self.CSC.player_move()
                    self.CSC.check_move()
                elif option == 's':
                    self.CSC.player_shoot()
                    arrows -= 1
                self.CSC.move_wumpus()
            output('Strings', 'NoArrows')
            raise PlayerDead()
        except PlayerDead as Lost:
            print(Lost, "\nDu har förlorat.")
        except WumpusDead as Win:
            print(Win, "\nDu har vunnit!")
            self.check_highscore()

    def check_highscore(self):
        """Game has finished, and player has won. Calls for a
        check of score."""
        self.HighScore.check_score()

    def play_again(self):
        """Checks if the player wants to continue playing or return to menu."""
        option = string_check("Vill du spela igen? (J/N) ", 'j', 'n')
        if option == 'n':
            self.playing = False
        elif option == 'j':
            self.reset()

    def reset(self):
        """The player wants to play again, a new CSC instance is created."""
        self.CSC = CSC()

    def quit_game(self):
        """Prints exit message. Sets appropriate booleans
        to False so that the game may quit."""
        output('Strings', 'Leave')
        self.menu_show = False
        self.running = False

if __name__ == "__main__":
    """Main function. Creates an new instance of the Game class.
    Calls for the main function."""
    clear()
    g = Game()
    while g.running:
        g.main()
