import math
import requests
import json
import regex

from .character_codes import VestaCodes

# FIXME: This won't work for the VestaBoard Note
COLUMNS = 22
ROWS = 6
TIMEOUT = 20

class CommunicationException(Exception):
    pass

class VestaBoard:
    ANIMATION_COLUMN = "column"  # "Wave" in the app.
    ANIMATION_REVERSE_COLUMN = "reverse-column"  # "Drift" in the app.
    ANIMATION_EDGES_TO_CENTER = "edges-to-center"  # "Curtain" in the app.
    ANIMATION_ROW = "row" # Row-by-row animation. Not available in the app.
    ANIMATION_DIAGONAL = "diagonal"  # Corner-to-corner animation. Not available in the app.
    ANIMATION_RANDOM = "random"  # Animates the number in step_size at a time randomly.
    
    VERTICAL_ALIGN_TOP = "top"
    VERTICAL_ALIGN_MIDDLE = "middle"
    VERTICAL_ALIGN_BOTTOM = "bottom"
    VERTICAL_ALIGN_JUSTIFIED = "justified"
    VERTICAL_ALIGN_OPTIONS = [
        VERTICAL_ALIGN_TOP,
        VERTICAL_ALIGN_MIDDLE,
        VERTICAL_ALIGN_BOTTOM,
        VERTICAL_ALIGN_JUSTIFIED,
    ]
    
    HORIZONTAL_ALIGN_LEFT = "left"
    HORIZONTAL_ALIGN_CENTER = "center"
    HORIZONTAL_ALIGN_RIGHT = "right"
    HORIZONTAL_ALIGN_JUSTIFIED = "justified"
    HORIZONTAL_ALIGN_OPTIONS = [
        HORIZONTAL_ALIGN_LEFT,
        HORIZONTAL_ALIGN_CENTER,
        HORIZONTAL_ALIGN_RIGHT,
        HORIZONTAL_ALIGN_JUSTIFIED,
    ]
    
    @classmethod
    def blank_message(cls):
        encoded_message = [[], [], [], [], [], []]
        for idx in range(0, 6):
            encoded_message += []
            for j in range(0, 22):
                encoded_message[idx] += [0]
        return encoded_message
    
    @classmethod
    def format_message(cls, message: str, vertical_alignment: str, horizontal_alignment: str):
        message_chars = regex.findall(r"\X", message)
        message_rows = []
        index = 0
        cur_row = []
        for char in message_chars:
            cur_row += [char]
            index += 1
            row_overflowed = index > COLUMNS
            if char == "\n" or row_overflowed:
                message_rows += [cur_row[:-1]]
                if row_overflowed and not char == "\n":
                    cur_row = [char]
                    index = 1
                else:
                    cur_row = []
                    index = 0

        if len(cur_row) > 0:
            message_rows += [cur_row]

        if len(message_rows) > ROWS:
            raise Exception("Message has too many rows")
        
        t_padding = 0
        match vertical_alignment:
            case cls.VERTICAL_ALIGN_TOP:
                t_padding = 0
            case cls.VERTICAL_ALIGN_MIDDLE:
                t_padding = int((ROWS - len(message_rows)) / 2)
            case cls.VERTICAL_ALIGN_BOTTOM:
                t_padding = int(ROWS - len(message_rows))
        
        c = VestaCodes()
        encoded_message = cls.blank_message()
        for row, row_message_chars in enumerate(message_rows):
            l_padding = 0
            match horizontal_alignment:
                case cls.HORIZONTAL_ALIGN_LEFT:
                    pass
                case cls.HORIZONTAL_ALIGN_CENTER:
                    if len(row_message_chars) < COLUMNS:
                        l_padding = int((COLUMNS - len(row_message_chars))/2)
                case cls.HORIZONTAL_ALIGN_RIGHT:
                    if len(row_message_chars) < COLUMNS:
                        l_padding = int((COLUMNS - len(row_message_chars)))
        
            for i, char in enumerate(row_message_chars):
                encoded_message[row + t_padding][l_padding + i] = c.to(char.upper())
        return encoded_message
    
    def __init__(self, ip: str, port: int, api_token: str):
        super()
        self.ip = ip
        self.port = port
        self.api_token = api_token

    def get_headers(self):
        headers = {
            "X-Vestaboard-Local-Api-Key": f"{self.api_token}"
        }
        return headers
    
    def get_raw_message(self) -> list[list[int]]:
        try:
            response = requests.get(
                f"http://{self.ip}:{self.port}/local-api/message",
                headers=self.get_headers(),
                timeout=TIMEOUT
            )
            if not response.ok:
                raise CommunicationException(
                    f"Vestaboard returned unexpected status {response.status_code}"
                )
            response_dict = response.json()
        except requests.RequestException:
            raise CommunicationException("Couldn't connect to Vestaboard")
        except json.JSONDecodeError:
            raise CommunicationException("Vestaboard didn't return JSON")

        return response_dict["message"]
    
    def get_encoded_message(self) ->  list[list[str]]:
        # FIXME: Add tests and custom exceptions
        raw_message = self.get_raw_message()
        decoded_message = VestaCodes.blank_message()
        for i, row in enumerate(raw_message):
            for j, code in enumerate(row):
                decoded_message[i][j] = vc.from_code(code)
        return decoded_message
    
    def get_current_message(self, multiline: bool = False) -> str:
        # FIXME: Add tests and custom exceptions
        raw_message = self.get_raw_message()
        message = ""
        for row in raw_message:
            for code in row:
                char = VestaCodes.from_code(code)
                message += char
            if multiline:
                message += "\n"
            else:
                message = message.strip()
        return message
    
    def send_message(
        self,
        message,
        vertical_alignment: str = VERTICAL_ALIGN_MIDDLE,
        horizontal_alignment: str = HORIZONTAL_ALIGN_CENTER,
        animation: str = ANIMATION_RANDOM
    ) -> None:
        encoded_message = VestaBoard.format_message(
            message, vertical_alignment, horizontal_alignment
        )
        
        post_data = {
            "characters": encoded_message,
            "strategy": animation,
            # "step_interval_ms": 3000,
            # "step_size": 1,
        }
        if animation == self.ANIMATION_RANDOM:
            post_data["step_size"] = ROWS*COLUMNS

        try:
            r = requests.post(
                f"http://{self.ip}:{self.port}/local-api/message",
                headers=self.get_headers(),
                data=json.dumps(post_data),
                timeout=TIMEOUT
            )
        except requests.RequestException:
            raise CommunicationException("Couldn't connect to Vestaboard")