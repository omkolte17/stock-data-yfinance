import csv
with open('data.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        print(f'\tUser:- {row[0]} uses:- {row[1]} has Due:-  {row[2]}.')
        line_count += 1
    print(f'Processed {line_count} lines.')
