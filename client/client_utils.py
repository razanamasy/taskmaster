def check_string(value):
    if value == None:
        return ("is empty")
    else:
        if isinstance(value, str) == False:
            return ("is not a string")
        else:
            if value.isprintable() == False:
                return ("not printable character in string")
            elif len(value) == 0:
                return ("is empty")
    return (None)
