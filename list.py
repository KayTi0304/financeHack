f = open("demofile3.txt", "r")

def isfloat(str_input):
    try:
        float(str_input)
        return True
    except:
        return False

result = []

result = f.readlines()

for index, value in enumerate(result):
    result[index] = value.casefold()
    result[index] = result[index].replace(",","")
    result[index] = result[index].replace("%","")
    result[index] = result[index].replace("\n","")
    result[index] = result[index].replace("(","-")
    result[index] = result[index].replace(")","")

    
    

result = [float(x) if isfloat(x) else x for x in result]
result = list(filter(lambda x: x != '$', result))
list_index = 0
year_count = 0
report = {}

report["Years"] = []

for index, word in enumerate(result):
    if word == 'years':
        if result[index + 1] == 'ended':
            list_index = index + 1

while (not isfloat(result[list_index]) or result[list_index] < 2000):
    list_index += 1


while(isfloat(result[list_index])):
    if result[list_index] > 2000:
        report["Years"].append(result[list_index])
        year_count += 1
        list_index += 1
test_count = year_count


while test_count == year_count:
    test_count = 0
    count = 0
    last_index = list_index

    while isfloat(result[last_index]) == False:
        if str(result[last_index]).isascii() == False:
            print(f'++++++++++{result[last_index]}')
            result[last_index] = 0
            count += 1
        last_index += 1

    last_index -= count
    
    key = ' '.join(result[list_index:last_index])

    report[key] = []

    for i in range(year_count):
        num_to_add = result[last_index]

        if str(num_to_add).isascii() == False:
            print(f'++++++++++{num_to_add}')
            num_to_add = 0
        
        if isfloat(num_to_add):
            report[key].append(num_to_add)
            test_count += 1
        last_index += 1
    
    list_index = last_index

print(result)

print(result[0])
print(list_index)

print(report.items())