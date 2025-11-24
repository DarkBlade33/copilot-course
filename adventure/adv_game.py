clues = [
    "There is a scorched crescent on the wall where something burned briefly.",
    "There is a line of crushed petals leading toward a closed corner.",
    "There is a faint smear of ash along the baseboard, as if something smoldered and was moved.",
    "There is a folded note tucked beneath a loose floorboard, its edges softened by handling.",
    "There is a dark ring on the table where glasses were set and then forgotten.",
    "There is a single, muddy footprint half-hidden under the rug's fringe.",
    "There is a dried drip mark on the ceiling, streaking down and long since settled.",
    "There is a cluster of tiny punctures in the curtain, their pattern oddly deliberate.",
    "There is a hurriedly rearranged stack of books, their spines scuffed and out of order.",
    "There is a faint trace of perfume lingering in the corner, layered with dust and time."
]

sense_exp = [
    "You see candlelight tremble along a tapestry's braided edge, answering a drifting draft.",
    "You hear the slow settling of stone, a low groan that might once have been a footstep.",
    "You smell iron and old wax layered with something sweet and green, like dried herbs.",
    "You feel the floorboards whisper underfoot, as if remembering a hurried passage.",
    "You sense a cool current that carries the echo of laughter or the memory of it.",
    "You see a shadow pause in the corner, holding a shape a heartbeat too long.",
    "You hear the soft clink of glass far away, as if someone set down a fragile secret.",
    "You smell smoke threaded with rosemary, the trace of a brazier long since banked.",
    "You feel the windowsill's stone — worn smooth and faintly warm from many palms.",
    "You sense the air thicken, a subtle pressure like someone hesitating beyond the door.",
    "You see motes of dust turn in a single beam of light, each one a silent witness.",
    "You hear a patient tapping behind the plaster, regular and oddly deliberate."
]

import random
from typing import Iterable, List, Optional, Any

class RandomItemSelector:
    """
    RandomItemSelector manages a pool of items and tracks which have been used.
    - items: original list of items
    - used_items: list of items already selected (preserves selection order)
    """

    def __init__(self, items: Optional[Iterable[Any]] = None):
        self.items: List[Any] = list(items) if items is not None else []
        self.used_items: List[Any] = []

    # literal init alias (per spec) that re-initializes the selector
    def init(self, items: Optional[Iterable[Any]] = None) -> None:
        """
        Reinitialize the selector with a new collection of items.
        """
        self.__init__(items)

    def add_item(self, item: Any) -> None:
        """
        Add a single item to the available items list.
        """
        self.items.append(item)

    def pull_random_item(self) -> Optional[Any]:
        """
        Return a random item that hasn't been selected yet.
        - If all items have been used, reset used_items and continue.
        - If there are no items at all, clear used_items and return None.
        """
        if not self.items:
            # No items to select; ensure used_items is cleared and signal absence.
            self.used_items.clear()
            return None

        # Determine available items (those not in used_items)
        available = [itm for itm in self.items if itm not in self.used_items]

        if not available:
            # All items used — reset and make all available again.
            self.reset()
            available = list(self.items)

        choice = random.choice(available)
        self.used_items.append(choice)
        return choice

    def reset(self) -> None:
        """
        Clear used_items to make all items available again.
        """
        self.used_items.clear()

from typing import Dict

class SenseClueGenerator:
    """
    Singleton generator that combines a clue and a sensory experience.
    Initializes two RandomItemSelector instances for clues and senses.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Initialize selectors with the module-level lists
            cls._instance.clue_selector = RandomItemSelector(clues)
            cls._instance.sense_selector = RandomItemSelector(sense_exp)
        return cls._instance

    def get_senseclue(self) -> str:
        """
        Pull one clue and one sensory experience and combine them into a single string.
        """
        clue = self.clue_selector.pull_random_item()
        sense = self.sense_selector.pull_random_item()

        if clue and sense:
            return f"{clue} {sense}"
        if clue:
            return clue
        if sense:
            return sense
        return ""
    
from enum import Enum

class encounter_outcome(Enum):
    CONTINUE = "CONTINUE"
    END = "END"

from abc import ABC, abstractmethod

# Provide a convenient type name matching the requested "EncounterOutcome"
EncounterOutcome = encounter_outcome

class Encounter(ABC):
    """
    Abstract base class for encounters.
    Subclasses must implement run_encounter and return an EncounterOutcome.
    """

    @abstractmethod
    def run_encounter(self) -> EncounterOutcome:
        """
        Execute the encounter and return an EncounterOutcome.
        """
        pass

class DefaultEncounter(Encounter):
    """
    Default encounter that uses SenseClueGenerator to produce output.
    """

    def __init__(self):
        # instantiate the singleton generator
        self.generator = SenseClueGenerator()

    def run_encounter(self) -> EncounterOutcome:
        """
        Attempt to call pull_random_item on the generator if available;
        otherwise combine a clue and a sense from the generator's selectors.
        Print the result and continue the encounter.
        """
        pull = getattr(self.generator, "pull_random_item", None)
        if callable(pull):
            output = pull()
        else:
            # fallback: use the underlying selectors to produce a combined string
            clue = self.generator.clue_selector.pull_random_item()
            sense = self.generator.sense_selector.pull_random_item()
            if clue and sense:
                output = f"{clue} {sense}"
            else:
                output = clue or sense or ""
        print(output)
        return EncounterOutcome.CONTINUE
    
class Room:
    """
    A room with a name and an Encounter. visit_room runs the encounter and
    returns its EncounterOutcome.
    """

    def __init__(self, name: str, encounter: Encounter):
        self.name = name
        self.encounter = encounter

    def visit_room(self) -> EncounterOutcome:
        return self.encounter.run_encounter()


rooms = [
    Room("Throne Room", DefaultEncounter()),
    Room("Armory", DefaultEncounter()),
    Room("Library", DefaultEncounter()),
    Room("Great Hall", DefaultEncounter()),
    Room("Solar", DefaultEncounter()),
    Room("Dungeon", DefaultEncounter()),
]

class Castle:
    """
    Castle manages room selection and navigation.
    """

    def __init__(self, rooms=None):
        # Accept an explicit collection of rooms or fall back to the module-level 'rooms'
        rooms_list = list(rooms) if rooms is not None else globals().get("rooms", [])
        self.room_selector = RandomItemSelector(rooms_list)

    def select_door(self) -> int:
        """
        Randomly choose the number of doors (2-4), prompt the user to pick one,
        validate input, and return the chosen door index (1-based).
        """
        num_doors = random.randint(2, 4)
        print("\n" + "=" * 40)
        print(f"There are {num_doors} doors before you.")
        prompt = f"Choose a door (1-{num_doors}): "

        while True:
            try:
                choice_str = input(prompt).strip()
                choice = int(choice_str)
                if 1 <= choice <= num_doors:
                    print(f"You open door {choice}.\n" + "-" * 40)
                    return choice
                else:
                    print(f"Invalid selection: enter a number between 1 and {num_doors}.")
            except ValueError:
                print("Invalid input: please enter a numeric value.")

    def next_room(self) -> EncounterOutcome:
        """
        Run the door selection flow, pick a random room, announce it, visit it,
        and return the resulting EncounterOutcome.
        """
        door = self.select_door()
        # Door selection is ceremonial here; select a random room to visit.
        room = self.room_selector.pull_random_item()
        if room is None:
            print("No rooms available. Resetting room selector.")
            self.room_selector.reset()
            return EncounterOutcome.END

        print(f"You step through and enter: {room.name}")
        result = room.visit_room()
        print("=" * 40 + "\n")
        return result

    def reset(self) -> None:
        """
        Reset the room selector so all rooms are available again.
        """
        self.room_selector.reset()
        print("Room selector has been reset; all rooms are available again.")

class Game:
    """
    Game orchestrates gameplay: explaining objectives, running the main loop,
    and handling end-of-game and restart prompts.
    """

    def __init__(self, rooms):
        """
        Initialize the game with a collection (set/list/iterable) of Room objects.
        """
        self.castle = Castle(rooms)

    def play_game(self) -> None:
        """
        Explain the objective and run the main game loop until the player quits.
        """
        print("\nWelcome, adventurer.")
        print("Objective: Navigate through the castle's doors and seek the hidden treasure.\n")
        try:
            while True:
                outcome = self.castle.next_room()
                if outcome == EncounterOutcome.END:
                    # Encounter signaled the end — reset and offer to restart or exit
                    self.castle.reset()
                    print("\nGame Over\n")
                    while True:
                        choice = input("Would you like to explore a different castle? (y/n): ").strip().lower()
                        if choice in ("y", "yes"):
                            print("\nA new exploration begins...\n")
                            break  # restart loop
                        if choice in ("n", "no"):
                            print("\nFarewell, adventurer.")
                            return
                        print("Please respond with 'y' or 'n'.")
                elif outcome == EncounterOutcome.CONTINUE:
                    # Continue exploring
                    continue
                else:
                    # Unexpected outcome: end the game loop gracefully
                    print("The adventure reaches an uncertain end.")
                    return
        except (KeyboardInterrupt, EOFError):
            print("\n\nAdventure paused. Farewell.")

# run the game
if __name__ == "__main__":
    game = Game(rooms)
    game.play_game()


