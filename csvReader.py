data_1 = "" # assignment, create, string variable
with open('data.csv', 'r') as file_1:
    data_1 = file_1.read()
record_dict = {} # create dictionary
record_list_1 = data_1.split('\n')[1:]
for record in record_list_1:
    record_list_2 = record.split(',')
    record_dict.setdefault(record_list_2[1], [])
    record_dict[record_list_2[1]].append(record_list_2[-2:])
for company, records in record_dict.items():
    previous_price = -1
    for data in records: 
        if previous_price == -1:
            data.append(0)
        else:
            data.append((int(data[-1])-previous_price)/previous_price)
        previous_price = int(data[-2])
variance_dict = {}
for company, records in record_dict.items():
    mean = 0
    for data in records:
        mean += int(data[-2])
    mean = mean / len(records)
    sum_of_diff_from_mean = 0
    for data in records:
        sum_of_diff_from_mean += (int(data[-2]) - mean) ** 2
    variance = sum_of_diff_from_mean / len(records)
    variance_dict[company] = sum_of_diff_from_mean

sharpe_dict = {}
for company, records in record_dict.items():
    product_of_factor = 1
    for data in records:
        if data[-1] != 0:
            factor = data[-1] + 1
            product_of_factor = product_of_factor * factor
    effective_rate_of_return = ((product_of_factor ** (1/(len(records)-1))) ** 12) - 1
    risk_free_rate = 0.015
    risk_premium = effective_rate_of_return - risk_free_rate
    sharpe_ratio = risk_premium/((variance_dict[company])**0.5)    
    sharpe_dict[company] = sharpe_ratio
print(sharpe_dict)