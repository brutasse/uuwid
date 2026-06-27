import uuid
from pathlib import Path
from typing import Union

_WORDS = Path(__file__).with_name("words.txt").read_text().splitlines()
_WORD_COUNT = len(_WORDS)  # 65536
_W = _WORD_COUNT


def _shuffle(uuid_int: int) -> int:
    """Interleave the high and low 64 bits of a 128-bit integer.

    This spreads the time component (concentrated in the high 64 bits of
    time-based UUIDs) across all 8 words, so consecutive UUIDs differ
    in many words instead of just the first few.
    """
    upper = uuid_int >> 64
    lower = uuid_int & 0xFFFFFFFFFFFFFFFF
    result = 0
    for i in range(64):
        result |= ((upper >> i) & 1) << (2 * i + 1)
        result |= ((lower >> i) & 1) << (2 * i)
    return result


def _unshuffle(shuffled_int: int) -> int:
    """Reverse the interleaving."""
    upper = 0
    lower = 0
    for i in range(64):
        upper |= ((shuffled_int >> (2 * i + 1)) & 1) << i
        lower |= ((shuffled_int >> (2 * i)) & 1) << i
    return (upper << 64) | lower


def encode(value: Union[uuid.UUID, str, bytes]) -> str:
    """Encode a 128-bit UUID into exactly 8 words."""
    if isinstance(value, str):
        value = uuid.UUID(value)
    elif isinstance(value, bytes):
        value = uuid.UUID(bytes=value)
    elif not isinstance(value, uuid.UUID):
        raise TypeError(f"Expected UUID, str, or bytes, got {type(value).__name__}")

    shuffled = _shuffle(value.int)
    words = []
    for _ in range(8):
        words.append(_WORDS[shuffled % _W])
        shuffled //= _W
    words.reverse()
    return "-".join(words)


def decode(words: str) -> uuid.UUID:
    """Decode 8 words back into a 128-bit UUID."""
    parts = words.split("-")
    if len(parts) != 8:
        raise ValueError(f"Expected exactly 8 words, got {len(parts)}")

    shuffled = 0
    for word in parts:
        try:
            idx = _WORDS.index(word)
        except ValueError:
            raise ValueError(f"Unknown word: {word}")
        shuffled = shuffled * _W + idx

    return uuid.UUID(int=_unshuffle(shuffled))
