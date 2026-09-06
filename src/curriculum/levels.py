# Define the learning tiers

LEVEL_1 = {
    'name': 'Level 1: Static Basics',
    'signs': ['A', 'B', 'C', 'L', 'V'],
    'description': 'Basic static letters to get started.'
}

LEVEL_2 = {
    'name': 'Level 2: Curled & Complex',
    'signs': ['D', 'E', 'F', 'O', 'W'],
    'description': 'More complex hand shapes involving curled fingers.'
}

LEVEL_3 = {
    'name': 'Level 3: Full Alphabet',
    'signs': [chr(i) for i in range(ord('A'), ord('Z')+1)], # A-Z
    'description': 'Master the full alphabet.'
}

NUMBERS_TIER = {
    'name': 'Numbers 0-9',
    'signs': [str(i) for i in range(10)],
    'description': 'Learn digits from zero to nine.'
}

CURRICULUM_TIERS = [LEVEL_1, LEVEL_2, LEVEL_3, NUMBERS_TIER]

class GameState:
    """Manages the current progress and game mode."""
    MODE_PRACTICE = "PRACTICE"
    MODE_CHALLENGE = "CHALLENGE"

    def __init__(self):
        self.current_tier_index = 0
        self.current_sign_index = 0
        self.score = 0
        self.streak = 0
        self.mode = self.MODE_PRACTICE

    def get_current_tier(self):
        return CURRICULUM_TIERS[self.current_tier_index]

    def get_current_sign(self):
        tier = self.get_current_tier()
        if self.current_sign_index < len(tier['signs']):
            return tier['signs'][self.current_sign_index]
        return None
