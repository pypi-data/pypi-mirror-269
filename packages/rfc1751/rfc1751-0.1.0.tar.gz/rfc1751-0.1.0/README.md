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

```python
>>> rfc1751.bytes_to_string([204, 172, 42, 237, 89, 16, 86, 190])
'RASH BUSH MILK LOOK BAD BRIM'
>>> rfc1751.bytes_to_string(b'\xCC\xAC\x2A\xED\x59\x10\x56\xBE')
'RASH BUSH MILK LOOK BAD BRIM'
>>> rfc1751.string_to_bytes('RASH BUSH MILK LOOK BAD BRIM')
b'\xCC\xAC\x2A\xED\x59\x10\x56\xBE'
>>> list(rfc1751.string_to_bytes('RASH BUSH MILK LOOK BAD BRIM'))
[204, 172, 42, 237, 89, 16, 86, 190]
```
