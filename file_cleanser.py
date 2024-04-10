import csv
input_file = 'file.csv'
output_file = 'cleaned_file.csv'

with open(input_file, 'r', newline='', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
    reader = csv.reader(infile, quotechar='"', quoting=csv.QUOTE_ALL, skipinitialspace=True, escapechar='\\')
    writer = csv.writer(outfile, quotechar='"', quoting=csv.QUOTE_ALL, skipinitialspace=True, escapechar='\\')

    for row in reader:
        cleaned_row = [cell.replace('""', '"') for cell in row]
        writer.writerow(cleaned_row)