import string

for char in string.ascii_lowercase:
    print(f"{char}: {format(ord(char), '08b')}")

print(f" : {format(ord(' '), '08b')}")
