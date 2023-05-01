def check_int(value, min, max):
    if isinstance(value, int) == False:
        return ("is not an int")
    else:
        if (isinstance(value, int) == True and (value < min or value > max)):
            return ("value out of range")
    return (None)

