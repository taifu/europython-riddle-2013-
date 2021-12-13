import sys, random, datetime

if __name__ == "__main__":
    date_start = datetime.datetime(1900, 1, 1, 0, 0, 0)
    date_end = datetime.datetime(2100, 12, 31, 23, 59, 59)
    delta = (date_end - date_start).total_seconds()
    formats = ("%Y/%m/%d %H:%M:%S",)
    for i in range(int(sys.argv[1])):
        d1 = date_start + datetime.timedelta(seconds=random.randrange(delta))
        d2 = date_start + datetime.timedelta(seconds=random.randrange(delta))
        #print ",".join((d1.strftime(random.choice(formats)), d2.strftime(random.choice(formats))))
        print ",".join((d1.isoformat(), d2.isoformat()))

