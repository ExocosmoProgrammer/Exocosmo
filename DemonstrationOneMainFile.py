from DemonstrationOneClassFile import number
print(__file__[41:], 'demonstrationMainFile')
demonstrator = number()
demonstrator.write()


class otherNumber:
    def __init__(self):
        if __file__[41:] == 'DemonstrationOneMainFile.py':
            self.value = 1
        else:
            self.value = 2

    def write(self):
        print(self.value)


otherDemonstrator = otherNumber()
otherDemonstrator.write()
