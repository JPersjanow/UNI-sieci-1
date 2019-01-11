
import random
import math
import numpy as np

class sieci:
    def __init__(self):
        self.bits = []
        self.mistake_bumber = 1
        self.percent = False
        self.repeat = False
        self.mod = 8

    def file_read(self, filename):
        Bytes = np.fromfile(file, dtype = "uint8")

        self.bits = np.unpackbits(Bytes) #odpakowywanie

        self.bits2 = self.bits

    def file_write(self, filename, to_write):

        self.bits = np.concatenate((self.bits, to_write))

        text = np.packbits(self.bits)
        text.tofile(file)

    def file_write2(self, filename):

        text = np.packbits(self.bits)
        text.tofile(file)

    def add_mistakes(self):

        b = len(self.bits) #dlugosc bitow
        #print(b)

        if self.percent:
            self.mistake_bumber = int(math.floor((float(self.mistake_bumber) / 100.0) * b)) #procent ilosci bledow

        mistakes = []

        if self.mistake_bumber > 0:

            if self.repeat == True: #z powtarzaniem

                for i in range(0, self.mistake_bumber, 1):
                    mistakes.append(random.randint(0, b-9))

            else: #bez

                for i in range(0, self.mistake_bumber, 1):
                    a = random.randint(0, b-9)

                    while a in mistakes:
                        a = random.randint(0, b-9)

                    mistakes.append(a)

        for i in mistakes: #zamiana w liscie bitow

            if self.bits[i] == 0:
                self.bits[i] = 1

            else:
                self.bits[i] = 0

        return self.bits

    def bit_add(self):
        b = 0

        for i in self.bits:
            b = b + int(i)
        b = b % 2
        return b

    def bit_check(self):
        b = 0

        for i in self.bits[:-8]: #usuwa ostatni bajt
            b = b + int(i)
        b = b % 2

        return b

    def crc(self):

        zeros = np.array([0, 0, 0]) #wyzeorwane 3 ostatnie

        self.bits2 = np.concatenate((self.bits2, zeros)) #dolaczenie

        for i in range(0, len(self.bits2)-4, 1):
            if self.bits2[i] == 1:
                self.bits2 = self.xor(i, self.bits2, [1, 0, 1, 1]) #xor jesli napotka 1

        crc = self.bits2[len(self.bits2)-3:] #3 ostatnie

        return crc

    def crc_check(self):

        zeros = np.array([0, 0, 0])

        self.bits2 = np.concatenate((self.bits2[:-8], zeros))


        for i in range(0, len(self.bits2)-4, 1):
            if self.bits2[i] == 1:
                self.bits2 = self.xor(i, self.bits2, [1, 0, 1, 1])

        crc = self.bits2[len(self.bits2)-3:]

        return crc

    def xor(self, start, list, d_crc): #lub uzyc wbudowanej ^

        fr = list[start:start+4]

        for i in range(0, 4, 1):

            if fr[i] != d_crc[i]:
                fr[i] = 1
            else:
                fr[i] = 0

        list[start:start+4] = fr

        return list



    def mod_before(self):

        sm = 0

        for i in self.bits:
            sm = sm + int(i)
        sm = sm % self.mod

        return sm

    def mod_after(self):

        sm = 0

        for i in self.bits[:-8]:
            sm = sm + int(i)

        sm = sm % self.mod

        return sm

s = sieci()
file = 'mail żaba.txt'
file2 = 'small.jpg'
s.file_read(file2)

print("bit list: " + str(s.bits))

print("")

b1 = s.bit_add()
print ("bit : " + str(b1))
s.file_write("b1", [b1])
s.file_read("b1")
x = s.add_mistakes()
s.file_write2("b2")
b2 = s.bit_check()
print ("bit check: " + str(b2))
if b2 != b1:
    print("the file is corrupted")
else:
    print("file is not corrupted")

print("")

check = []
crc1 = s.crc()
print ("CRC : " + str(crc1))
s.file_write("crc1", crc1)
s.file_read("crc1")
s.add_mistakes()
s.file_write2("crc2")
crc3 = s.crc_check()
print ("CRC check :  " + str(crc3))

for i in range(0, len(crc1),1):
    if crc1[i] != crc3[i]:
        check.append(True)
    else:
        check.append(False)

if True in check:
    print("file is corrupted")
else:
    print("file is not corrupted")


print("")

sm1 = s.mod_before()
print ("mod : " + str(sm1))

b = np.binary_repr(sm1)

c = []
for i in b:
    c.append(int(i))

s.file_write("m1", c)
s.file_read("m1")
s.add_mistakes()
s.file_write2("m2")
sm2 = s.mod_after()
print ("mod check : " + str(sm2))

if sm1 != sm2:
    print("file is corrupted")
else:
    print("file is not corrupted")



