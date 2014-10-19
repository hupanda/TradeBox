__author__ = 'PacAir'
from enum import Enum


class Frequency(Enum):
    Year = "annual"
    Quarter = "quarterly"
    Month = "monthly"
    Week = "weekly"
    Day = "daily"
    Hour = 4
    Minute = 5
    Second = 6