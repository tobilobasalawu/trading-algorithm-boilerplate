def indicators(data_obj, rsi):
    entries = {}
    exits = {}
    print(type(rsi))
    print(type(data_obj.datetimes))
    print(type(data_obj.opens))
    print(type(data_obj.closes))
    print(type(data_obj.highs))

    for num in rsi:
        if num < 30:
            pass

    return entries, exits
