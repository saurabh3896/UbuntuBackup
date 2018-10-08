import sqlite3
import pandas as pd
from sqlite3 import Error
from prettytable import PrettyTable

# helper functions

# print(pd.read_sql_query("SELECT * FROM SIKYU_TBL", conn))

# make a print function that takes list as argument and prints the contents as
# required, need another version to print subtotals each time office code,
# department code or X code changes

# using prettytable

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def formatter(input) :
    if is_int(input) :
        return "{:,}".format(float(input))
    return input

def create_connection(db_file) :
    try :
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e :
        print(e)
    return None

db_path = "../.local/var/sqlite3/java1.sqlite3"
conn = create_connection(db_path)
cursor = conn.cursor()
cursor.execute("select * from SIKYU_TBL")
rows = cursor.fetchall()

headers = [
        "事業所コード", "部コード", "課コード", "社員番号",
        "社員氏名", "基本給", "家族手当", "役職手当",
         "通常", "深夜", "残業手当", "総支給額"
        ]

# refer column names in capital, like df["BU_CD"]
df = pd.read_sql_query("SELECT jig_cd, bu_cd, ka_cd, sya_bg, sya_nm, kihon_kyu, kazoku_kyu, yakusyoku_kyu, tsujo_zan_jikan, sinya_zan_jikan FROM SIKYU_TBL ORDER BY jig_cd, bu_cd, ka_cd;", conn)

df["overtime_allow"] = (((df.KIHON_KYU + df.KAZOKU_KYU + df.YAKUSYOKU_KYU) / 160).astype(int) * df.TSUJO_ZAN_JIKAN * 1.2).astype(int) + (((df.KIHON_KYU + df.KAZOKU_KYU + df.YAKUSYOKU_KYU) / 160).astype(int) * df.SINYA_ZAN_JIKAN * 1.5).astype(int)
df["total_pay"] = df.KIHON_KYU + df.KAZOKU_KYU + df.YAKUSYOKU_KYU + df.overtime_allow

# print(df)

# for testing purpose
# df = pd.DataFrame()
# df = df.append({'a': 1, 'b': 1, 'c': 1,
#                 'd' : 1, 'e' : 'abc', 'f' : 100000,
#                 'g' : 0, 'h' : 0, 'i' : 0,
#                 'j' : 0, 'k' : 0, 'l' : 0}, ignore_index = True)
# df = df.append({'a': 1, 'b': 1, 'c': 1,
#                 'd' : 2, 'e' : 'abc', 'f' : 200000,
#                 'g' : 0, 'h' : 0, 'i' : 0,
#                 'j' : 0, 'k' : 0, 'l' : 0}, ignore_index = True)
# df = df.append({'a': 1, 'b': 1, 'c': 2,
#                 'd' : 10, 'e' : 'abc', 'f' : 300000,
#                 'g' : 0, 'h' : 0, 'i' : 0,
#                 'j' : 0, 'k' : 0, 'l' : 0}, ignore_index = True)
# df = df.append({'a': 1, 'b': 1, 'c': 2,
#                 'd' : 4, 'e' : 'abc', 'f' : 400000,
#                 'g' : 0, 'h' : 0, 'i' : 0,
#                 'j' : 0, 'k' : 0, 'l' : 0}, ignore_index = True)
# df = df.append({'a': 1, 'b': 2, 'c': 2,
#                 'd' : 3, 'e' : 'abc', 'f' : 500000,
#                 'g' : 0, 'h' : 0, 'i' : 0,
#                 'j' : 0, 'k' : 0, 'l' : 0}, ignore_index = True)
# df = df.append({'a': 1, 'b': 2, 'c': 2,
#                 'd' : 6, 'e' : 'abc', 'f' : 600000,
#                 'g' : 0, 'h' : 0, 'i' : 0,
#                 'j' : 0, 'k' : 0, 'l' : 0}, ignore_index = True)
# df = df.append({'a': 2, 'b': 2, 'c': 1,
#                 'd' : 5, 'e' : 'abc', 'f' : 700000,
#                 'g' : 0, 'h' : 0, 'i' : 0,
#                 'j' : 0, 'k' : 0, 'l' : 0}, ignore_index = True)

prev_l, cur_l = [], []
off_tot, dept_tot, sec_tot = [0]*5, [0]*5, [0]*5

x = PrettyTable(headers, border = False)

for i, r in df.iterrows() :
    row = r.tolist()
    add_l = row[5:8] + row[10:12]
    if i == 0 :
        prev_l = row[:3]
        off_tot, dept_tot, sec_tot = add_l, add_l, add_l
        continue
    cur_l = row[:3]
    # when office changes
    if prev_l[0] != cur_l[0] :
        # need to print 3 subtotals
        print("sec", sec_tot)
        print("dept", dept_tot)
        print("office", off_tot)
        off_tot, dept_tot, sec_tot = [0]*5, [0]*5, [0]*5
    # when department changes
    elif prev_l[1] != cur_l[1] :
        # need to print 2 subtotals
        print("sec", sec_tot)
        print("dept", dept_tot)
        dept_tot, sec_tot = [0]*5, [0]*5
    # when section changes
    elif prev_l[2] != cur_l[2] :
        # need to print 1 subtotal
        print("sec", sec_tot)
        sec_tot = [0]*5
    off_tot = [sum(x) for x in zip(off_tot, add_l)]
    dept_tot = [sum(x) for x in zip(dept_tot, add_l)]
    sec_tot = [sum(x) for x in zip(sec_tot, add_l)]
    prev_l = cur_l
print("sec", sec_tot)
print("dept", dept_tot)
print("office", off_tot)

# for _ in headers :
#     x.align[_] = "r"
#
# for row in rows[:1] :
#     row = list(map(formatter, list(row)))
#     print(row)
#     # x.add_row(row)
#
# # print(x.get_string())