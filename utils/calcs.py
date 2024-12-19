def calc_sma(closes, ma_period):
    indeces = {}
    sma = []
    for i in range(len(closes)):
        indeces[closes[i]] = i
    # Storing the index of each close in the list of closes

    for num in closes[ma_period:]:
        sma.append(sum(closes[indeces[num] - ma_period : indeces[num]]) / ma_period)
    # Going through each point and getting the mean of the previous {ma_period} points (default is 20)

    return sma
