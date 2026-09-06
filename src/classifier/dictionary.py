# Constants for finger states
FINGER_STATE_EXTENDED = 1
FINGER_STATE_CURLED = 0
FINGER_STATE_HALF_CURLED = 2  # E.g., for E or C
FINGER_STATE_IGNORE = -1

# Simple structure:
# Letter -> { 'thumb': state, 'index': state, 'middle': state, 'ring': state, 'pinky': state }
# State values match the constants above.
# This dictionary represents a simplified deterministic model for A-Z.
# For letters involving movement (J, Z), they're typically static frames approximating the start or end,
# but can be omitted or heavily relaxed in a basic static classifier.

ASL_DICTIONARY = {
    'A': {
        'thumb': FINGER_STATE_EXTENDED,
        'index': FINGER_STATE_CURLED,
        'middle': FINGER_STATE_CURLED,
        'ring': FINGER_STATE_CURLED,
        'pinky': FINGER_STATE_CURLED,
    },
    'B': {
        'thumb': FINGER_STATE_CURLED,
        'index': FINGER_STATE_EXTENDED,
        'middle': FINGER_STATE_EXTENDED,
        'ring': FINGER_STATE_EXTENDED,
        'pinky': FINGER_STATE_EXTENDED,
    },
    'C': {
        'thumb': FINGER_STATE_HALF_CURLED,
        'index': FINGER_STATE_HALF_CURLED,
        'middle': FINGER_STATE_HALF_CURLED,
        'ring': FINGER_STATE_HALF_CURLED,
        'pinky': FINGER_STATE_HALF_CURLED,
    },
    'D': {
        'thumb': FINGER_STATE_CURLED,
        'index': FINGER_STATE_EXTENDED,
        'middle': FINGER_STATE_CURLED,
        'ring': FINGER_STATE_CURLED,
        'pinky': FINGER_STATE_CURLED,
    },
    'E': {
        'thumb': FINGER_STATE_CURLED,
        'index': FINGER_STATE_HALF_CURLED,
        'middle': FINGER_STATE_HALF_CURLED,
        'ring': FINGER_STATE_HALF_CURLED,
        'pinky': FINGER_STATE_HALF_CURLED,
    },
    'F': {
        'thumb': FINGER_STATE_CURLED,
        'index': FINGER_STATE_CURLED,
        'middle': FINGER_STATE_EXTENDED,
        'ring': FINGER_STATE_EXTENDED,
        'pinky': FINGER_STATE_EXTENDED,
    },
    'G': {
        'thumb': FINGER_STATE_EXTENDED,
        'index': FINGER_STATE_EXTENDED,
        'middle': FINGER_STATE_CURLED,
        'ring': FINGER_STATE_CURLED,
        'pinky': FINGER_STATE_CURLED,
    },
    'H': {
        'thumb': FINGER_STATE_CURLED,
        'index': FINGER_STATE_EXTENDED,
        'middle': FINGER_STATE_EXTENDED,
        'ring': FINGER_STATE_CURLED,
        'pinky': FINGER_STATE_CURLED,
    },
    'I': {
        'thumb': FINGER_STATE_CURLED,
        'index': FINGER_STATE_CURLED,
        'middle': FINGER_STATE_CURLED,
        'ring': FINGER_STATE_CURLED,
        'pinky': FINGER_STATE_EXTENDED,
    },
    'K': {
        'thumb': FINGER_STATE_EXTENDED,
        'index': FINGER_STATE_EXTENDED,
        'middle': FINGER_STATE_EXTENDED,
        'ring': FINGER_STATE_CURLED,
        'pinky': FINGER_STATE_CURLED,
    },
    'L': {
        'thumb': FINGER_STATE_EXTENDED,
        'index': FINGER_STATE_EXTENDED,
        'middle': FINGER_STATE_CURLED,
        'ring': FINGER_STATE_CURLED,
        'pinky': FINGER_STATE_CURLED,
    },
    'M': {
        'thumb': FINGER_STATE_CURLED,
        'index': FINGER_STATE_CURLED,
        'middle': FINGER_STATE_CURLED,
        'ring': FINGER_STATE_CURLED,
        'pinky': FINGER_STATE_CURLED,
    },
    'N': {
        'thumb': FINGER_STATE_CURLED,
        'index': FINGER_STATE_CURLED,
        'middle': FINGER_STATE_CURLED,
        'ring': FINGER_STATE_CURLED,
        'pinky': FINGER_STATE_CURLED,
    },
    'O': {
        'thumb': FINGER_STATE_HALF_CURLED,
        'index': FINGER_STATE_HALF_CURLED,
        'middle': FINGER_STATE_HALF_CURLED,
        'ring': FINGER_STATE_HALF_CURLED,
        'pinky': FINGER_STATE_HALF_CURLED,
    },
    'P': {
        'thumb': FINGER_STATE_EXTENDED,
        'index': FINGER_STATE_EXTENDED,
        'middle': FINGER_STATE_HALF_CURLED,
        'ring': FINGER_STATE_CURLED,
        'pinky': FINGER_STATE_CURLED,
    },
    'Q': {
        'thumb': FINGER_STATE_EXTENDED,
        'index': FINGER_STATE_HALF_CURLED,
        'middle': FINGER_STATE_CURLED,
        'ring': FINGER_STATE_CURLED,
        'pinky': FINGER_STATE_CURLED,
    },
    'R': {
        'thumb': FINGER_STATE_CURLED,
        'index': FINGER_STATE_EXTENDED,
        'middle': FINGER_STATE_EXTENDED,
        'ring': FINGER_STATE_CURLED,
        'pinky': FINGER_STATE_CURLED,
    },
    'S': {
        'thumb': FINGER_STATE_CURLED,
        'index': FINGER_STATE_CURLED,
        'middle': FINGER_STATE_CURLED,
        'ring': FINGER_STATE_CURLED,
        'pinky': FINGER_STATE_CURLED,
    },
    'T': {
        'thumb': FINGER_STATE_CURLED,
        'index': FINGER_STATE_CURLED,
        'middle': FINGER_STATE_CURLED,
        'ring': FINGER_STATE_CURLED,
        'pinky': FINGER_STATE_CURLED,
    },
    'U': {
        'thumb': FINGER_STATE_CURLED,
        'index': FINGER_STATE_EXTENDED,
        'middle': FINGER_STATE_EXTENDED,
        'ring': FINGER_STATE_CURLED,
        'pinky': FINGER_STATE_CURLED,
    },
    'V': {
        'thumb': FINGER_STATE_CURLED,
        'index': FINGER_STATE_EXTENDED,
        'middle': FINGER_STATE_EXTENDED,
        'ring': FINGER_STATE_CURLED,
        'pinky': FINGER_STATE_CURLED,
    },
    'W': {
        'thumb': FINGER_STATE_CURLED,
        'index': FINGER_STATE_EXTENDED,
        'middle': FINGER_STATE_EXTENDED,
        'ring': FINGER_STATE_EXTENDED,
        'pinky': FINGER_STATE_CURLED,
    },
    'X': {
        'thumb': FINGER_STATE_CURLED,
        'index': FINGER_STATE_HALF_CURLED,
        'middle': FINGER_STATE_CURLED,
        'ring': FINGER_STATE_CURLED,
        'pinky': FINGER_STATE_CURLED,
    },
    'Y': {
        'thumb': FINGER_STATE_EXTENDED,
        'index': FINGER_STATE_CURLED,
        'middle': FINGER_STATE_CURLED,
        'ring': FINGER_STATE_CURLED,
        'pinky': FINGER_STATE_EXTENDED,
    },
}

# Add basic numbers (0-9)
ASL_NUMBERS = {
    '0': ASL_DICTIONARY['O'],
    '1': {
        'thumb': FINGER_STATE_CURLED,
        'index': FINGER_STATE_EXTENDED,
        'middle': FINGER_STATE_CURLED,
        'ring': FINGER_STATE_CURLED,
        'pinky': FINGER_STATE_CURLED,
    },
    '2': ASL_DICTIONARY['V'],
    '3': {
        'thumb': FINGER_STATE_EXTENDED,
        'index': FINGER_STATE_EXTENDED,
        'middle': FINGER_STATE_EXTENDED,
        'ring': FINGER_STATE_CURLED,
        'pinky': FINGER_STATE_CURLED,
    },
    '4': ASL_DICTIONARY['B'], # Same as B but thumb is not tucked across palm, simpler model treats them similarly
    '5': {
        'thumb': FINGER_STATE_EXTENDED,
        'index': FINGER_STATE_EXTENDED,
        'middle': FINGER_STATE_EXTENDED,
        'ring': FINGER_STATE_EXTENDED,
        'pinky': FINGER_STATE_EXTENDED,
    },
    '6': ASL_DICTIONARY['W'],
    '7': {
        'thumb': FINGER_STATE_CURLED,
        'index': FINGER_STATE_EXTENDED,
        'middle': FINGER_STATE_EXTENDED,
        'ring': FINGER_STATE_CURLED,
        'pinky': FINGER_STATE_EXTENDED,
    },
    '8': {
        'thumb': FINGER_STATE_CURLED,
        'index': FINGER_STATE_EXTENDED,
        'middle': FINGER_STATE_CURLED,
        'ring': FINGER_STATE_EXTENDED,
        'pinky': FINGER_STATE_EXTENDED,
    },
    '9': ASL_DICTIONARY['F'],
}
