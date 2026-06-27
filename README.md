# UUWID: Encode 128-bit UUIDs into words, and vice versa

This library encodes 128-bit UUIDs into human-readable sequences of words, and
decodes them back. It is designed for contexts where UUIDs need to be read,
transcribed, or compared by people.

## Design choices

### Exactly 8 words

A UUID is 128 bits. We needed a word list whose cardinality is a clean power
of two so that every valid 8-word sequence maps to exactly one UUID and every
UUID maps to exactly one 8-word sequence. 65536 words give 16 bits per word,
and 65536⁸ = 2¹²⁸. Eight words is short enough to be utterable in a sentence,
long enough to be collision-free.

### 65,536 words from the aspell dictionary

We extracted the shortest 65,536 lowercase English words from the aspell
dictionary. Short words matter because eight of them are spoken or typed
together. By sorting the dictionary by word length and taking the shortest
entries first, we minimize the total length of an encoded UUID while keeping the
vocabulary familiar.

### Bit-interleave the high and low 64-bit halves

Time-based UUIDs (v1) embed a timestamp in the upper 64 bits. Without
shuffling, two UUIDs generated a microsecond apart would differ only in their
first few words, making their encodings look nearly identical. We interleave the
upper and lower 64 bits bit-by-bit: upper bit 0 goes to position 1, lower bit 0
to position 0, upper bit 1 to position 3, lower bit 1 to position 2, and so on.
This spreads the timestamp evenly across all 8 words, so consecutive UUIDs differ
in multiple words and the encoded space feels uniformly distributed.

### Dash separators

A single hyphen is unambiguous, visually clean, and already the conventional
separator in UUID strings. It is easy to parse and does not conflict with any
word in the list which contains only alphabetic characters.

### Flexible input but return strict types

The encoder accepts UUID objects, strings, or raw bytes because callers
receive UUIDs from many sources and formats. The decoder always returns a
native UUID type because the caller should be explicit about what they are
receiving. This reduces friction without losing type safety.
