with open('log/server.log') as f:
    logs = f.readlines()[-32:]

total = 0
sum = 0

for i in range(40):
    start = logs[i].find('finished in ')

    if start > 0:
        total += 1
        # print(logs[i][start + len('finished in '):-2])
        sum += float(logs[i][start + len('finished in '):-2])

print(sum / total)