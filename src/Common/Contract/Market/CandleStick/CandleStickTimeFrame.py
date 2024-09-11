from enum import Enum


class CandleStickTimeFrame(Enum):
    tenSecond = 0
    oneMinute = 1
    fiveMinute = 2
    thirtyMinute = 3
    oneHour = 4
    day = 5
    week = 6
    month = 7
