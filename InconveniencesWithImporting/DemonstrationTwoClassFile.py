IMPORTING = 1


class number:
    def __init__(self):
        if IMPORTING:
            self.value = 1
        else:
            self.value = 2

    def showValue(self):
        print(self.value, 'value')