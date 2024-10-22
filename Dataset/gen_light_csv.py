## Generatin Synthetic Data
import random
with open("index.raw", 'r') as f:
    raw = [int(x) for x in f.readlines()]

csv = "hours,light\n"
days = 1
minimum = 10
maximum = 500
for day in range(days):
    for hour in range(len(raw)):
        light = raw[hour] * random.randint(minimum*raw[hour], maximum*raw[hour])
        csv += "%d,%d\n" % (hour, light)
print(csv)
with open("light.csv", 'w') as f:
    f.write(csv)
