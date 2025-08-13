arr = [-1, -2, -3, -4, -5]
for x in arr:
        if x < 0:
            arr.remove(x)
    total = 0
    for y in arr:
        total = total + y
    return total
