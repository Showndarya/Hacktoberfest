
for case in range(t):
    n = int(input().strip())
    n_array = list(map(int,input().strip().split(' ')))
    highest = n_array[-1]
    seq = []

    for i in reversed(n_array):
        if i >= highest:
            seq.append(str(i))
            highest = i
    seq.reverse()
    print(' '.join(seq))
        
