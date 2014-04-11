def gauss_progression(x, y, z):
    times = len(range(x, y + z, z))
    num = times*(x+y)/2
    return num

print gauss_progression(1, 5, 1)