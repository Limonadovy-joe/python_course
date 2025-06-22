from enum import Enum


class Mode(Enum):
    ENCRYPT = "Encrypt"
    DECRYPT = "Decrypt"


def shift_char(char: str, shift: int, mode: Mode) -> str:
    unicode = ord(char)
    shifted_unicode = unicode - shift if mode == Mode.DECRYPT else unicode + shift
    is_upper = str.isupper(char)

    if mode == Mode.ENCRYPT:
        upper_bound = 90 if is_upper else 122
        return (
            chr(shifted_unicode)
            if shifted_unicode > upper_bound
            else chr(shifted_unicode)
        )
    elif mode == Mode.DECRYPT:
        lower_bound = 65 if is_upper else 97
        return (
            chr(shifted_unicode)
            if shifted_unicode < lower_bound
            else chr(shifted_unicode)
        )
    else:
        raise ValueError(f"Invalid mode: {mode}")


def shift_chars(text: str, shift: int, mode: Mode) -> str:
    return "".join(shift_char(char, shift, mode) for char in text)


def encrypt(text: str, shift: int) -> str:
    return shift_chars(text, shift, Mode.ENCRYPT)


def decrypt(text: str, shift: int) -> str:
    return shift_chars(text, shift, Mode.DECRYPT)


# text = "ATTACKATONCE"
# shift = 4
# print("text", text)
# encrypted = encrypt(text, shift)
# print("encrypt", encrypted)
# print(
#     "decrypt",
#     decrypt(encrypted, shift),
# )
