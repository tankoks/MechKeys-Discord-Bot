def userCommand(func):
    setattr(func, "isCommand", True)
    return func

def backgroundLoop(func):
    setattr(func, "isLoop", True)
    return func

def afterCheck(func):
    setattr(func, "afterCheck", True)
    return func
