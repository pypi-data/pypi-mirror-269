This is a Pure-Python implementation of [RFC 1751](https://www.rfc-editor.org/rfc/rfc1751).

Using this small library, you can turn binary strings (for example IDs or passwords) into small sequences of short English words. For example:

```
EB33 F77E E73D 4053
```

would become:

```
TIDE ITCH SLOW REIN RULE MOT
```

The algorithm turns a 64-bit string into 6 English words and vice versa. Two bits of parity are included in the sequence of words, which allow detecting an invalid or corrupted phrase.

# Usage

```pycon
>>> # Simple conversion from string or bytes
>>> rfc1751.bytes_to_string([204, 172, 42, 237, 89, 16, 86, 190])
'RASH BUSH MILK LOOK BAD BRIM'
>>> rfc1751.bytes_to_string(b'\xCC\xAC\x2A\xED\x59\x10\x56\xBE')
'RASH BUSH MILK LOOK BAD BRIM'

>>> # You can specify the separator or get a sequence
>>> rfc1751.bytes_to_string(b'\xCC\xAC\x2A\xED\x59\x10\x56\xBE', sep='-').lower()
'rash-bush-milk-look-bad-brim'
>>> rfc1751.bytes_to_words(b'\xCC\xAC\x2A\xED\x59\x10\x56\xBE')
['RASH', 'BUSH', 'MILK', 'LOOK', 'BAD', 'BRIM']

>>> # Conversion back
>>> rfc1751.string_to_bytes('RASH BUSH MILK LOOK BAD BRIM')
b'\xCC\xAC\x2A\xED\x59\x10\x56\xBE'
>>> list(rfc1751.string_to_bytes('RASH BUSH MILK LOOK BAD BRIM'))
[204, 172, 42, 237, 89, 16, 86, 190]

>>> # You can specify the separator or give a sequence
>>> rfc1751.string_to_bytes('rash-bush-milk-look-bad-brim', sep='-')
b'\xCC\xAC\x2A\xED\x59\x10\x56\xBE'
>>> rfc1751.words_to_bytes(['rash', 'bush', 'milk', 'look', 'bad', 'brim'])
b'\xCC\xAC\x2A\xED\x59\x10\x56\xBE'

>>> # You can also use a custom alphabet as long as it is 2048 words
>>> custom_rfc1751 = rfc1751.Rfc1751(custom_2048_words)
>>> custom_rfc1751.bytes_to_string([204, 172, 42, 237, 89, 16, 86, 190])
'SMILE GENUINE ROBUST RATE AIR GAME'
>>> list(custom_rfc1751.string_to_bytes('SMILE GENUINE ROBUST RATE AIR GAME'))
[204, 172, 42, 237, 89, 16, 86, 190]
```
