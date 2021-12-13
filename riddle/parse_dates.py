import sys, datetime

def to_date(s):
    return datetime.datetime(*tuple(int(p) for t in s.split("T") for p in t.replace("-", ":").split(":")))

if __name__ == "__main__":
    total = 0
    total_wrong = 0
    for line in file(sys.argv[1], "r").readlines():
        s1, s2 = line.strip().split(",")
        d1, d2 = tuple(to_date(s) for s in (s1, s2))
        total_wrong += int((d1 - d2).total_seconds())
        total += int((max(d1, d2) - min(d1, d2)).total_seconds())
    print total_wrong
    print total
