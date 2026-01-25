CODES = {
	" ": {
		"name": "Blank",
		"code": 0
	},
	"A": {
		"name":	"A",
		"code": 1
	},
	"B": {
		"name":	"B",
		"code": 2
	},
	"C": {
		"name":	"C",
		"code": 3
	},
	"D": {
		"name":	"D",
		"code": 4
	},
	"E": {
		"name":	"E",
		"code": 5
	},
	"F": {
		"name":	"F",
		"code": 6
	},
	"G": {
		"name":	"G",
		"code": 7
	},
	"H": {
		"name":	"H",
		"code": 8
	},
	"I": {
		"name":	"I",
		"code": 9
	},
	"J": {
		"name":	"J",
		"code": 10
	},
	"K": {
		"name":	"K",
		"code": 11
	},
	"L": {
		"name":	"L",
		"code": 12
	},
	"M": {
		"name":	"M",
		"code": 13
	},
	"N": {
		"name":	"N",
		"code": 14
	},
	"O": {
		"name":	"O",
		"code": 15
	},
	"P": {
		"name":	"P",
		"code": 16
	},
	"Q": {
		"name":	"Q",
		"code": 17
	},
	"R": {
		"name":	"R",
		"code": 18
	},
	"S": {
		"name":	"S",
		"code": 19
	},
	"T": {
		"name":	"T",
		"code": 20
	},
	"U": {
		"name":	"U",
		"code": 21
	},
	"V": {
		"name":	"V",
		"code": 22
	},
	"W": {
		"name":	"W",
		"code": 23
	},
	"X": {
		"name":	"X",
		"code": 24
	},
	"Y": {
		"name":	"Y",
		"code": 25
	},
	"Z": {
		"name":	"Z",
		"code": 26
	},
	"1": {
		"name":	"One",
		"code": 27
	},
	"2": {
		"name":	"Two",
		"code": 28
	},
	"3": {
		"name":	"Three",
		"code": 29
	},
	"4": {
		"name":	"Four",
		"code": 30
	},
	"5": {
		"name":	"Five",
		"code": 31
	},
	"6": {
		"name":	"Six",
		"code": 32
	},
	"7": {
		"name":	"Seven",
		"code": 33
	},
	"8": {
		"name":	"Eight",
		"code": 34
	},
	"9": {
		"name":	"Nine",
		"code": 35
	},
	"0": {
		"name":	"Zero",
		"code": 36
	},
	"!": {
		"name": "Exclamation Mark",
		"code": 37
	},
	"@": {
		"name": "At",
		"code": 38
	},
	"#": {
		"name": "Pound",
		"code": 39
	},
	"$": {
		"name": "Dollar",
		"code": 40
	},
	"(": {
		"name": "Left Parenthesis",
		"code": 41
	},
	")": {
		"name": "Right Parenthesis",
		"code": 42
	},
	"-": {
		"name": "Hyphen",
		"code": 44
	},
	"+": {
		"name": "Plus",
		"code": 46
	},
	"&": {
		"name": "Ampersand",
		"code": 47
	},
	"=": {
		"name": "Equal",
		"code": 48
	},
	";": {
		"name": "Semicolon",
		"code": 49
	},
	":": {
		"name": "Colon",
		"code": 50
	},
	"'": {
		"name": "Single Quote",
		"code": 52
	},
	'"': {
		"name": "Double Quote",
		"code": 53
	},
	"%": {
		"name": "Percent",
		"code": 54
	},
	",": {
		"name": "Comma",
		"code": 55
	},
	".": {
		"name": "Period",
		"code": 56
	},
	"/": {
		"name": "Slash",
		"code": 59
	},
	"?": {
		"name": "Question Mark",
		"code": 60
	},
	"°": {
		"name": "Degree",
		"code": 62
	},
	"🟥": {
		"name": "PoppyRed",
		"code": 63
	},
	"🟧": {
		"name": "Orange",
		"code": 64
	},
	"🟨": {
		"name": "Yellow",
		"code": 65
	},
	"🟩": {
		"name": "Green",
		"code": 66
	},
	"🟦": {
		"name": "ParisBlue",
		"code": 67
	},
	"🟪": {
		"name": "Violet",
		"code": 68
	},
	"⬜️": {
		"name": "White",
		"code": 69
	},
	"⬜": {
		"name": "White",
		"code": 69
	},
}

COLUMNS = 22
ROWS = 6

class VestaCodes:
	@classmethod
	def valid(cls, character: str) -> bool:
		return character in CODES.keys()

	@classmethod
	def to(cls, character: str, raise_exception: bool = False) -> int:
		try:
			return CODES[character].get("code")
		except KeyError as err:
			print(f"Ignoring code: '{character}'")
			if raise_exception:
				raise err
			return 0
	
	@classmethod
	def from_code(cls, code: int) -> str:
		for key, character in CODES.items():
			if character["code"] == code:
				return key
