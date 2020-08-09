from datetime import date, timedelta

sdate = date(2019, 3, 22)  # start date
edate = date(2019, 4, 9)  # end date
date_modified = sdate
list = [sdate]


while date_modified < edate:
    date_modified += timedelta(days=1)
    list.append(date_modified)

print(list)
