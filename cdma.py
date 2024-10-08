from scipy.linalg import hadamard
# генерация кодов Уолша для станций
def GenerateCodesStation():
    allCodes = hadamard(8)
    codesStation = []
    for i in range(0, 8, 2):
        codesStation.append(allCodes[i])
        print("Код станции ", nameStations[int(i/2)], " - ", allCodes[i])
    return codesStation

#слова каждой странции
words = [[0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0],
         [0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0],
         [0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1],
         [0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0]]
# названия станций
nameStations = ["A", "B", "C", "D"]

class Station:
    def __init__(self, numberStation, word):
        self.numberStation = numberStation #идентификатор станции
        self.word = word #слово, которое станция отправит
        self.currentWord = [] #слово, которое станция получила
    # кодирование 1 бита слова и отправка в приемник
    def Coding(self, bit):
        if(self.word[bit]==0):
            codingLetter = [codesStations[self.numberStation][i]*-1 for i in range(8)]
        else:
            codingLetter = codesStations[self.numberStation]
        return codingLetter

    # получение и декодирование бита
    def Decoding(self, codingLetter):
        resultBits = [x * y for x, y in zip(codingLetter, codesStations[self.numberStation])]
        resultLetter = int(sum(resultBits)/8)
        if(resultLetter == -1):
            resultLetter = 0
        self.currentWord.append(resultLetter)

    # проверка успешности отправки и приема
    def CheckLetter(self):
        if(self.currentWord == self.word):
            print("Станция ", nameStations[self.numberStation], " успешно отправила сообщение\n")
        else:
            print("При отправке сообщения станцией ", nameStations[self.numberStation], " произошел сбой\n")

class Mediator:
    def __init__(self):
        # сумма закодированных битов от всех станций
        self.currentBits = [0 for i in range(8)]
    # получение закодированного бита
    def Get(self, bit):
        # закодированные биты, полученные от станций
        getsBitsOfStation = []
        # получение кодированного бита
        for i in range(4):
            getsBitsOfStation.append(stations[i].Coding(bit))
        # суммирование
        for i in range(8):
            for j in range(4):
                self.currentBits[i] += getsBitsOfStation[j][i]
    # отправка приемнику закодированного бита
    def Send(self):
        for i in range(4):
            stations[i].Decoding(self.currentBits)
        self.currentBits = [0 for i in range(8)]

stations = []
for i in range(4):
    stations.append(Station(i, words[i]))
reciver = Mediator()
codesStations = GenerateCodesStation()
for i in range(3):
    for j in range(8):
        bit = i*8+j
        reciver.Get(bit)
        reciver.Send()
print("Произведена отправка всех слов")
for i in range(4):
    stations[i].CheckLetter()