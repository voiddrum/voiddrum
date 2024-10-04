import csv
r1=[]
with open('rh-all.csv', newline='') as csvfile:
    rhreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in rhreader:
        r1.append(row)

Activity_Date, Process_Date,Settle_Date,Instrument,Description,Trans_Code,Quantity,Price,Amount = 0,1,2,3,4,5,6,7,8
txn_map = {}
rows = reversed(r1[1:-2])
for row in rows:
	txn_key = (row[Instrument],row[Trans_Code])
	if txn_key in txn_map:
		txn_list = txn_map[txn_key]
	else:
		txn_list = []
		txn_map.update({txn_key: txn_list})
	txn_list.append(row)

all_sells = filter(lambda x: x[1] == 'Sell', txn_map)

for ticker_sell in all_sells:
	ticker_sells = txn_map[ticker_sell]
	if (ticker_sell[0], 'Buy') not in txn_map:
		for ts in ticker_sells:
			ts.append(("No_Buy", 0, 0, 0))
		continue
	ticker_buys = txn_map[(ticker_sell[0], 'Buy')]
	ticker_buys_copy = ticker_buys.copy()
	for ts in ticker_sells:
		s_qty = float(ts[Quantity])
		print(f"Selling {s_qty}")
		for tb in ticker_buys_copy:
			print(ts)
			print(tb)
			#input1 = input()
			b_qty = float(tb[Quantity])
			print(f"Had bought {b_qty}")
			if b_qty == 0:
				continue
			if b_qty < s_qty:
				s_qty = s_qty - b_qty
				tb[Quantity] = 0
				ts.append((tb[Activity_Date], b_qty, tb[Price], tb[Amount]))
				print(f"Accounted for {b_qty}")
			else:
				tb[Quantity] = b_qty - s_qty
				ts.append((tb[Activity_Date], s_qty, tb[Price], tb[Amount]))
				print(f"Accounted for {s_qty}")
				s_qty = 0
			print(f"Remaining to account for {s_qty}")
			if s_qty == 0:
				break
		if s_qty != 0:
			print(f"Could not account for {s_qty} shares out of {ts[Quantity]}")
			ts.append((f"{s_qty}_NoBuy", 0, 0, 0))

def list_txn_buys(ticker):
	for t in txn_map[(ticker, 'Sell')]:
		cnt = 0
		for b in t[9:]:
			
			print(b)
			cnt = cnt + float(b[1])
		print(f"Bought {cnt} stocks")
		print(t[0:8])	

list_txn_buys("GOOGL")
list_txn_buys("TSLA")
