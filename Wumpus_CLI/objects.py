import random
from modules import *
from prettytable import PrettyTable
from operator import attrgetter


class PlayerDead(Exception):
    """Player Looses"""

    def __add__(self, other):
        return self + other


class WumpusDead(Exception):
    """Player Wins"""

    def __add__(self, other):
        return self + other


class Culvert:
    """Culvert class. Corresponds to an individual culvert.
    It is given a name, and three neighbors."""
    def __init__(self, name):
        self.name = name
        self.neighbors = (self, self, self)
        self.danger = self.NONE

        self._wumpus = False

    NONE = 'EMPTY'
    BATS = 'BATS'
    WUMPUS = 'WUMPUS'
    PIT = 'PIT'
    ALERTS = {NONE: '', BATS: 'Jag hör fladdermöss!', PIT: 'Jag känner vinddrag!',
              WUMPUS: 'Jag känner lukten av Wumpus!'}

    @staticmethod
    def sorter(data):
        """Checks if the input data has more than one entry of same type.
        Removes any duplicates and returns a data set containing unique elements."""
        string_set = set()
        string_add = string_set.add

        return [x for x in data if not (x in string_set or string_add(x))]

    def __len__(self):
        """Allows for iterating through
        the neighbors."""
        return len(self.neighbors)

    def __iter__(self):
        """Allows the for iterating through
        a culverts neighbors."""
        return iter(self.neighbors)

    def __str__(self):
        """Prints out information about the culvert and it's neighbors
        so that the user may be aware of where they are, and what dangers are near."""
        ret = [self.ALERTS[x.danger] for x in self.neighbors]
        if [x for x in self.neighbors if x.wumpus]:
            ret.insert(0, self.ALERTS[self.WUMPUS])
        ret = ['    ' + x for x in ret if x]
        ret.insert(0, "Du är i rum {0}.".format(self.name))
        ret.append("\nGångarna leder till rum {0}, {1}, {2}".format(*[x.name for x in self.neighbors]))

        ret = self.sorter(ret)
        return '\n'.join(ret)

    def __repr__(self):
        """For debugging the program. Returns culvert name, neighbors and
         if wumpus, a bat or a pit is in it."""
        return "[Culvert {0} - Neighbors:[{1}, {2}, {3}] Wumpus:{4} Danger:{5}]".format(
            self.name,
            self.neighbors[0].name, self.neighbors[1].name, self.neighbors[2].name,
            self.wumpus, self.danger)

    @property
    def wumpus(self):
        """Returns boolean value. True/False depending on
        if Wumpus is in the specified culvert."""
        return self._wumpus

    @wumpus.setter
    def wumpus(self, value):
        """Sets boolean value. True/False to the
        specified culvert."""
        self._wumpus = value

    @property
    def bats(self):
        """Returns boolean value. True/False depending
        on if there are bats in the specified culvert."""
        return self.danger == self.BATS

    @bats.setter
    def bats(self, value):
        """Sets boolean value. True/False to the
        specified culvert. Only if it is empty."""
        if value:
            if self.danger == self.NONE:
                self.danger = self.BATS

    @property
    def pit(self):
        """Sets boolean value. True/False to the
        specified culvert. Only if it is empty."""
        return self.danger == self.PIT

    @pit.setter
    def pit(self, value):
        """Sets boolean value. True/False to the
        specified culvert. Only if it is empty."""
        if value:
            if self.danger == self.NONE:
                self.danger = self.PIT


class CSC:
    def __init__(self):
        """Initializes the CSC Class."""
        self._culverts = []
        self._difficulty = 3

        self.combine_culverts()
        random.choice(self._culverts).wumpus = True
        self.initialize_dangers("bats")
        self.initialize_dangers("pit")
        self._player_pos = self.place_entity("PLAYER")

    def combine_culverts(self):
        """Creates the CSC complex by combining all the Culvert objects.
        Randomly places Wumpus and calls for placement of pits and bats."""

        for i in range(0, 20):
            self._culverts.append(Culvert(i + 1))
        scheme = ((1, 5, 4), (0, 7, 2), (1, 9, 3), (2, 11, 4),
                  (3, 13, 0), (0, 14, 6), (5, 16, 7), (1, 6, 8),
                  (7, 9, 17), (2, 8, 10), (9, 11, 18), (10, 3, 12),
                  (19, 11, 13), (14, 12, 4), (13, 5, 15), (14, 19, 16),
                  (6, 15, 17), (16, 8, 18), (10, 17, 19), (12, 15, 18))

        for i, culvert in enumerate(scheme):
            self._culverts[i].neighbors = tuple([self._culverts[i] for i in culvert])

    def initialize_dangers(self, danger):
        """Places the requested danger, bat or pit, in a random culvert.
        Two dangers may not be in the same place. Depending on the difficulty
        there are different percentages of a danger being placed."""
        if danger == "pit":
            occurrence = random.randrange(3, 7)
        elif danger == "bats":
            occurrence = random.randrange(3, 6)

        for i in range(occurrence):
            culvert = random.choice(self.culverts)
            while culvert.bats or culvert.pit:
                culvert = random.choice(self.culverts)

            chance = random.randint(0, 100)
            if self._difficulty == 5 and chance < 100:
                setattr(culvert, danger, True)
            elif self._difficulty == 4 and chance < 85:
                setattr(culvert, danger, True)
            elif self._difficulty == 3 and chance < 75:
                setattr(culvert, danger, True)
            elif (self._difficulty == 1 or self._difficulty == 2) and chance < 40:
                setattr(culvert, danger, True)

    def modify_dangers(self):
        """User has requested difficulty to change.
        Calls for all dangers to be removed, and calls for new to be placed."""
        self.remove_dangers()

        self.initialize_dangers("bats")
        self.initialize_dangers("pit")

    def remove_dangers(self):
        """Removes all dangers in all culverts. Except Wumpus."""
        for culvert in self.culverts:
            setattr(culvert, "pit", False)
            setattr(culvert, "bats", False)

    def change_difficulty(self):
        """User specifies wanted difficulty. Calls for dangers to be modified."""
        output('Strings', 'Difficulty')
        print("Aktuell svårighetsgrad: " + str(self._difficulty))
        self._difficulty = check_input("Vilken svårighetsgrad vill du spela på? (1-5) ", 1, 5)
        self.modify_dangers()

        print("\nSvårighetsgrad ändrad till: " + str(self._difficulty) + ".")

    def place_entity(self, entity):
        """Randomly places requested entity in an empty culvert."""
        destination = random.choice(self._culverts)
        if entity == "PLAYER":
            while destination.wumpus or destination.bats or destination.pit:
                destination = random.choice(self._culverts)

        return destination

    def player_move(self):
        """Player has requested to move. Checks if the users movement is valid."""
        destination = self[check_input("Till vilken kulvert? ", 0, 21) - 1]

        if destination == self._player_pos:
            print("\nDu kan inte gå till " + str(destination) + " du är redan där.")
        elif destination not in self._player_pos:
            print("\nDu kan inte gå till " + str(destination) + ", kulverten finns inte.")
        else:
            self._player_pos = destination

    def escape(self):
        """User has met Wumpus. Depending on difficulty, they might be allowed
        to escape Wumpus."""
        if self._difficulty <= 3:
            if random.randint(0, 100) < 35:
                return True
            else:
                return False

    def check_move(self):
        """Checks if user's movement caused any collision with another entity,
        such as Wumpus, bats or a pit. If player met Wumpus or fell down in a pit
        'PlayerDead' exception is raised. If a player met a bat, calls for
        random placement of user."""
        if self.player_pos.wumpus:
            output('Strings', 'WumpusFound')
            if self.escape():
                output('Strings', 'Escape')
            else:
                output('Strings', 'Caught')
                raise PlayerDead
        elif self.player_pos.pit:
            output('Strings', 'Pit')
            raise PlayerDead
        elif self.player_pos.bats:
            self.place_entity("PLAYER")
            output('Strings', 'Bats', self._player_pos.name)

    def move_wumpus(self):
        """Depending on difficulty, Wumpus may move after user has taken
        their action. Wumpus may only move to an empty culvert.
        Checks if Wumpus met Player."""
        if self._difficulty > 3:
            for i in range(0, 3):
                if self._culverts[i].wumpus:
                    culvert = self._culverts[i]

                    culvert.wumpus = False

                    destination = random.choice(culvert.neighbors)
                    while destination.pit or destination.bats:
                        destination = random.choice(destination.neighbors)

                    destination.wumpus = True

                    self.check_move()

    def player_shoot(self):
        """Player has requested to shoot. User may control the arrow's direction
        for three moves. On each move, a call for a check is done, whether the
        arrow collided with something."""
        arrow_pos = self._player_pos
        culvert = ""
        for i in range(1, 4):
            if i == 1:
                culvert = "första"
            elif i == 2:
                culvert = "andra"
            elif i == 3:
                culvert = "tredje"

            while True:
                print("\nPilen lämnar " + culvert + " kulverten. Välj nästa kulvert. "
                                                    "({0}, {1}, {2})".format(*[x.name for x in arrow_pos]))

                destination = self[check_input("Val: ", 1, 20) - 1]
                if destination not in arrow_pos:
                    print("Pilar kan inte gå igenom väggar. Än.")
                else:
                    arrow_pos = destination
                    self.arrow_check(arrow_pos)
                    break

        print("Miss!")

    def arrow_check(self, arrow_pos):
        """Checks whether the arrow collided with the player or Wumpus.
        Raises 'PlayerDead' or 'WumpusDead' depending on."""
        if arrow_pos == self._player_pos:
            raise PlayerDead("\nKlantigt! Du sköt dig själv med pilen!")
        elif arrow_pos.wumpus:
            raise WumpusDead("\nTräff! Du har dödat Wumpus.")

    def __getitem__(self, item):
        """Allows for iteration over object."""
        return self._culverts[item]

    def __str__(self):
        """For debugging the program. Combines all the information
        about each individual culvert and prints them all."""
        return '\n'.join([str(r) for r in self.culverts])

    @property
    def player_pos(self):
        """Returns information about the player's position."""
        return self._player_pos

    @property
    def difficulty(self):
        """Returns the difficulty value."""
        return self._difficulty

    @property
    def culverts(self):
        """Returns the culverts."""
        return self._culverts


class Score:
    def __init__(self, name, score):
        """Score class. Makes up the individual score."""
        self.name = name
        self.score = score

    def __str__(self):
        """Returns score value."""
        return self.score


class HighScore:
    def __init__(self):
        """Highscore class. Holds all the individual scores.
        Keeps track of amount of player moves in current session."""
        self.highscore = []
        self._player_moves = 0
        self.data = ""

        self.load_highscore()

    def load_highscore(self):
        """Calls for loading of the highscore file.
        Creates a Score object for all values in file."""
        self.data = load_data(HIGHSCORE)
        for i in range(0, int((len(self.data) - 2) / 2)):
            self.highscore.append(Score(self.data[1 + i], self.data[(i + 1) + int((len(self.data)) / 2)]))

    def sort(self):
        """Sorts all scores in highscore in rising values."""
        self.highscore.sort(key=lambda x: int(x.score), reverse=False)

    def check_score(self):
        """The game has ended and player has won. Checks if the amount of moves
        is lower than the current lowest highscore. If there are more than 10 entries
        in the highscore - table, the highest score entry is overwritten."""
        if self._player_moves != 0:
            if len(self.highscore) == 0 or len(self.highscore) < 10:
                print("NYTT REKORD!")
                self.highscore.append(Score(input("Ange ditt namn: "), str(self._player_moves)))
            else:
                for i in range(0, len(self.highscore)):
                    if self._player_moves < int(self.highscore[i].score):
                        print("NYTT REKORD!")
                        max_index = self.highscore.index(max(self.highscore, key=attrgetter('score')))
                        del self.highscore[max_index]
                        self.highscore.insert(max_index, Score(input("Ange ditt namn: "), str(self._player_moves)))
                        break

        self.sort()
        self.save()

    def save(self):
        """Overwrites the existing highscore file with new entries."""
        with open(os.path.join(ASSET_FOLDER, HIGHSCORE, ), 'r+') as file:
            file.seek(0)
            max_index = len(self.highscore)
            file.write("[Name]\n")
            for x in range(0, max_index):
                file.write(self.highscore[x].name + "\n")
            file.write("[Moves]\n")
            for x in range(0, max_index):
                file.write(self.highscore[x].score + "\n")

    def __str__(self):
        """If there are score entries, the highscore - table is shown.
        Otherwise user is asked for play for results to be showed."""
        self.sort()
        output('Strings', 'TopScore')
        if len(self.highscore) == 0:
            return "\nDu måste vinna minst en gång för att dina resultat ska visas här."
        else:
            table = PrettyTable(['#', 'Namn', 'Poäng'])
            for i in range(0, int((len(self.data) - 2) / 2)):
                table.add_row([str(i + 1) + ".", self.highscore[i].name, self.highscore[i].score])

            return str(table)

    def __len__(self):
        """Allows for iterating over the highscore table."""
        return len(self.highscore)

    @property
    def player_score(self):
        """Returns the player moves value."""
        return self._player_moves

    def player_score_incr(self):
        """Increases player moves with one."""
        self._player_moves += 1
