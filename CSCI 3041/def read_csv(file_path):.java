def read_csv(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            row = line.strip().split(',')
            data.append(row)
    return data

def write_csv(file_path, data):
    # Write data to a CSV file
    with open(file_path, 'w') as file:
        for row in data:
            line = ','.join(row)
            file.write(line + '\n')

def union_rows(in_file1, in_file2, out_file):
    # Read data from in_file1 and in_file2
    data1 = read_csv(in_file1)
    data2 = read_csv(in_file2)

    # Identify common emails
    emails1 = set()
    for row in data1:
        emails1.add(row[0])  # Assuming email is in the first column

    common_emails = []
    for email in emails1:
        for row in data2:
            if email == row[0]:
                common_emails.append(email)

    # Identify common columns (headers)
    common_columns = []
    for col in data1[0]:
        if col in data2[0]:
            common_columns.append(col)

    # Create a new list with the combined data
    combined_data = [common_columns]

    for row1 in data1:
        if row1[0] in common_emails:
            combined_row = []
            for col in common_columns:
                combined_row.append(row1[data1[0].index(col)])
            combined_data.append(combined_row)

    # Write combined data to out_file
    write_csv(out_file, combined_data)

# Usage example:
# union_rows('file1.csv', 'file2.csv', 'output.csv')
