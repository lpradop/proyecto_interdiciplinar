import datetime
def rowToDict(columns: tuple, rows: list) -> list:
    return [dict(zip(columns, row)) for row in rows]
def timeToDatetime(time:datetime.time,date_time:datetime.datetime):
    return datetime.datetime.combine(date_time.date(),time)
