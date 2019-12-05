import re

ascending = open('S1_list_ascending.txt','r')
asc_list = ascending.readlines()
ascending.close()
token_date_list = []
for line in asc_list:
    token_date=line.split('_')[4]
    token_date_list.append(token_date)

S1_timestamp_vh = open('sentinel1-timestamps-pwr-vh.txt','r')
times_vh = S1_timestamp_vh.readlines()

timestamp_out = []
for token in token_date_list:
    for line in times_vh:
        r1 = re.findall(r'\w+', token)
        if r1:
            timestamp_out.append(line)

outfile = open("S1-timestamps-pwr-vh-ascending.txt","w") 

outfile.writelines(timestamp_out) 
outfile.close() 
