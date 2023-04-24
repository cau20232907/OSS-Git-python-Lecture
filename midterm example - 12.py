value = 0
for x in range(1, 10, 5):
    y = 0
    while y < x:
        value = x - y

        match value:
            case 0 if x > 0 and y > 0:
                value = 100
            case 9:
                value = 0
        y += 1
    value += x * y
print(value)