"""
this is first version of googool
a program that translate latin numbers to 
persian words. this program support from 0 to 1 googool
"""
from package.letters import *

while True:
    answer = input("Welcome..... Do you want to 1-[C]ontinue or [2]-Exit : ")
    if answer in ["2", "E"]:
        break

    def digit(num: int):
        res = []

        if 1000 <= num:
            res += units[num // 1000] + "هزار"
            num %= 1000
            if num != 0:
                res.append(" و ")

        if 100 <= num:
            res += hundreds[num // 100]
            num %= 100
            if num != 0:
                res.append(" و ")

        if 20 <= num:
            res += tens_2[num // 10]
            num %= 10
            if num != 0:
                res.append(" و ")

        if 10 <= num:
            num %= 10
            res += tens_1[num]
            num %= num

        if 0 < num:
            res += units[num]

        finall = "".join(res)
        return finall

    letter = digit(num=int(input("Enter your number :")))

    print(letter)
