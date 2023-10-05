with open('log/server.log') as f:
    logs = f.readlines()[-32:]

sum = 0

for i in range(0, 32, 2):
    start = logs[i].find('finished in ')

    # print(logs[i][start + len('finished in '):-2])
    sum += float(logs[i][start + len('finished in '):-2])

print(sum / 16)