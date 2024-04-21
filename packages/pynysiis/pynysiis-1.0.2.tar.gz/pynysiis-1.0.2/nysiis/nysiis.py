import re
from typing import Dict


class NYSIIS:
    """NYSIIS phonetic encoding class."""

    def __init__(self) -> None:
        """Initialize the NYSIIS object."""
        self.vowels: Dict[str, bool] = {
            "A": True,
            "E": True,
            "I": True,
            "O": True,
            "U": True,
        }

    def preprocess_name(self, name: str) -> str:
        """Preprocess the name by converting to uppercase and removing non-alphabetic characters."""
        name = name.upper()
        name = re.sub(r"[^A-Z]", "", name)
        return name

    def translate_first_characters(self, name: str) -> str:
        """Translate specific character combinations at the beginning of the name."""
        if name.startswith("MAC"):
            name = "MCC" + name[3:]
        elif name.startswith("KN"):
            name = "NN" + name[2:]
        elif name.startswith("K"):
            name = "C" + name[1:]
        elif name.startswith("PH") or name.startswith("PF"):
            name = "FF" + name[2:]
        elif name.startswith("SCH"):
            name = "SSS" + name[3:]
        elif name.startswith("GB"):
            name = "J" + name[2:]  # Igbo: 'Gb' -> 'J'
        elif name.startswith("KP"):
            name = "P" + name[2:]  # Igbo: 'Kp' -> 'P'
        elif name.startswith("NW"):
            name = "W" + name[2:]  # Igbo: 'Nw' -> 'W'
        elif name.startswith("TS"):
            name = "S" + name[2:]  # Yoruba: 'Ts' -> 'S'
        elif name.startswith("SH"):
            name = "S" + name[2:]  # Hausa: 'Sh' -> 'S'
        elif name.startswith("BH"):
            name = "B" + name[2:]  # Hindi: 'Bh' -> 'B'
        elif name.startswith("DH"):
            name = "D" + name[2:]  # Hindi: 'Dh' -> 'D'
        elif name.startswith("GH"):
            name = "G" + name[2:]  # Hindi: 'Gh' -> 'G'
        elif name.startswith("JH"):
            name = "J" + name[2:]  # Hindi: 'Jh' -> 'J'
        elif name.startswith("KH"):
            name = "K" + name[2:]  # Hindi: 'Kh' -> 'K'
        elif name.startswith("PH"):
            name = "F" + name[2:]  # Hindi: 'Ph' -> 'F'
        elif name.startswith("TH"):
            name = "T" + name[2:]  # Hindi: 'Th' -> 'T'
        elif name.startswith("CH"):
            name = "C" + name[2:]  # Urdu: 'Ch' -> 'C'
        elif name.startswith("GH"):
            name = "G" + name[2:]  # Urdu: 'Gh' -> 'G'
        elif name.startswith("KH"):
            name = "K" + name[2:]  # Urdu: 'Kh' -> 'K'
        elif name.startswith("SH"):
            name = "S" + name[2:]  # Urdu: 'Sh' -> 'S'
        elif name.startswith("ZH"):
            name = "J" + name[2:]  # Urdu: 'Zh' -> 'J'
        return name

    def translate_last_characters(self, name: str) -> str:
        """Translate specific character combinations at the end of the name."""
        if name.endswith("EE") or name.endswith("IE"):
            name = name[:-2] + "Y"
        elif (
            name.endswith("DT")
            or name.endswith("RT")
            or name.endswith("RD")
            or name.endswith("NT")
            or name.endswith("ND")
        ):
            name = name[:-2] + "D"
        return name

    def generate_key(self, name: str) -> str:
        """Generate the NYSIIS key for the given name."""
        key = name[0]
        prev_char = name[0]

        for i in range(1, len(name)):
            char = name[i]
            if char in self.vowels:
                char = "A"

            char = self.translate_char(char, name, i)
            char = self.handle_vowel_harmony(char, prev_char)
            char = self.ignore_tonal_differences(char)

            if char != prev_char:
                key += char

            prev_char = char

        key = self.remove_trailing_s(key)
        key = self.translate_ay(key)
        key = self.remove_trailing_a(key)
        key = self.truncate_key(key)

        return key

    def translate_char(self, char: str, name: str, i: int) -> str:
        """Translate specific characters based on their context."""
        if char == "E" and i + 1 < len(name) and name[i + 1] == "V":
            char = "A"
        elif char == "Q":
            char = "G"
        elif char == "Z":
            char = "S"
        elif char == "M":
            char = "N"
        elif char == "K":
            if i + 1 < len(name) and name[i + 1] == "N":
                char = name[i]
            else:
                char = "C"
        elif char == "S" and i + 2 < len(name) and name[i : i + 3] == "SCH":
            char = "S"
        elif char == "P" and i + 1 < len(name) and name[i + 1] == "H":
            char = "F"
        elif (
            char == "H"
            and (
                i == 0
                or i + 1 == len(name)
                or name[i - 1] not in self.vowels
                or name[i + 1] not in self.vowels
            )
        ):
            char = name[i - 1]
        elif char == "W" and i > 0 and name[i - 1] in self.vowels:
            char = name[i - 1]
        elif char == "G" and i + 1 < len(name) and name[i + 1] == "B":
            char = "J"  # Igbo: 'Gb' -> 'J'
        elif char == "K" and i + 1 < len(name) and name[i + 1] == "P":
            char = "P"  # Igbo: 'Kp' -> 'P'
        elif char == "N" and i + 1 < len(name) and name[i + 1] == "W":
            char = "W"  # Igbo: 'Nw' -> 'W'
        elif char == "T" and i + 1 < len(name) and name[i + 1] == "S":
            char = "S"  # Yoruba: 'Ts' -> 'S'
        elif char == "S" and i + 1 < len(name) and name[i + 1] == "H":
            char = "S"  # Hausa, Urdu: 'Sh' -> 'S'
        elif char == "B" and i + 1 < len(name) and name[i + 1] == "H":
            char = "B"  # Hindi: 'Bh' -> 'B'
        elif char == "D" and i + 1 < len(name) and name[i + 1] == "H":
            char = "D"  # Hindi: 'Dh' -> 'D'
        elif char == "G" and i + 1 < len(name) and name[i + 1] == "H":
            char = "G"  # Hindi, Urdu: 'Gh' -> 'G'
        elif char == "J" and i + 1 < len(name) and name[i + 1] == "H":
            char = "J"  # Hindi: 'Jh' -> 'J'
        elif char == "K" and i + 1 < len(name) and name[i + 1] == "H":
            char = "K"  # Hindi, Urdu: 'Kh' -> 'K'
        elif char == "P" and i + 1 < len(name) and name[i + 1] == "H":
            char = "F"  # Hindi: 'Ph' -> 'F'
        elif char == "T" and i + 1 < len(name) and name[i + 1] == "H":
            char = "T"  # Hindi: 'Th' -> 'T'
        elif char == "C" and i + 1 < len(name) and name[i + 1] == "H":
            char = "C"  # Urdu: 'Ch' -> 'C'
        elif char == "Z" and i + 1 < len(name) and name[i + 1] == "H":
            char = "J"  # Urdu: 'Zh' -> 'J'
        return char

    def handle_vowel_harmony(self, char: str, prev_char: str) -> str:
        """Handle vowel harmony by adjusting the current vowel based on the previous vowel."""
        if char in self.vowels and prev_char in self.vowels:
            if prev_char in ["A", "O", "U"]:
                if char in ["E", "I"]:
                    char = "A"
            elif prev_char in ["E", "I"]:
                if char in ["A", "O", "U"]:
                    char = "E"
        return char

    @staticmethod
    def ignore_tonal_differences(char: str) -> str:
        """Ignore tonal differences by converting the character to uppercase."""
        if "A" <= char <= "Z":
            char = char.upper()
        return char

    @staticmethod
    def remove_trailing_s(key: str) -> str:
        """Remove trailing 'S' from the key."""
        if len(key) > 1 and key.endswith("S"):
            key = key[:-1]
        return key

    @staticmethod
    def translate_ay(key: str) -> str:
        """Translate 'AY' to 'Y' at the end of the key."""
        if key.endswith("AY"):
            key = key[:-2] + "Y"
        return key

    @staticmethod
    def remove_trailing_a(key: str) -> str:
        """Remove trailing 'A' from the key."""
        if len(key) > 1 and key.endswith("A"):
            key = key[:-1]
        return key

    @staticmethod
    def truncate_key(key: str) -> str:
        """Truncate the key to a maximum length of 6 characters."""
        if len(key) > 6:
            key = key[:6]
        return key

    def encode(self, name: str) -> str:
        """Encode the given name using the NYSIIS algorithm."""
        if not name:
            return ""

        name = self.preprocess_name(name)

        if len(name) < 2:
            return name

        name = self.translate_first_characters(name)
        name = self.translate_last_characters(name)
        key = self.generate_key(name)

        return key