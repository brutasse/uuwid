import uuid

import pytest

import uuwid
from uuwid.core import _shuffle, _unshuffle


class TestShuffle:
    def test_roundtrip(self):
        for val in [
            0,
            1,
            2**128 - 1,
            2**64,
            2**64 + 1,
            0x550E8400E29B41D4A716446655440000,
        ]:
            assert _unshuffle(_shuffle(val)) == val

    def test_spreads_time_component(self):
        """Time-based UUIDs with different upper 64 bits should differ in many words."""
        # Two UUIDs with same lower 64 bits but wildly different upper 64 bits.
        # The interleaving spreads the upper bits across all 8 words.
        u1 = uuid.UUID(int=0x00000000000000010000000000000001)
        u2 = uuid.UUID(int=0xFFFFFFFFFFFFFFFF0000000000000001)
        e1 = uuwid.encode(u1).split("-")
        e2 = uuwid.encode(u2).split("-")
        diff = sum(1 for a, b in zip(e1, e2) if a != b)
        assert diff > 1  # should differ in more than one word


class TestEncodeDecode:
    def test_roundtrip(self):
        u = uuid.uuid4()
        assert uuwid.decode(uuwid.encode(u)) == u

    def test_time_based_uuid(self):
        u = uuid.uuid1()
        assert uuwid.decode(uuwid.encode(u)) == u

    def test_string_input(self):
        u = "550e8400-e29b-41d4-a716-446655440000"
        assert uuwid.decode(uuwid.encode(u)) == uuid.UUID(u)

    def test_bytes_input(self):
        u = uuid.uuid4()
        assert uuwid.decode(uuwid.encode(u.bytes)) == u

    def test_invalid_type(self):
        with pytest.raises(TypeError):
            uuwid.encode(12345)  # type: ignore

    def test_decode_wrong_word_count(self):
        with pytest.raises(ValueError, match="Expected exactly 8 words"):
            uuwid.decode("one-two-three")

    def test_decode_unknown_word(self):
        with pytest.raises(ValueError, match="Unknown word"):
            uuwid.decode("a-a-a-a-a-a-a-xyznotaword")
