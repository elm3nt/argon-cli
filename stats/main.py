import csv


def analysis(output_file_path, data):
    with open(output_file_path, 'w') as analysis_file:
        writer = csv.writer(analysis_file)
        writer.writerows(data)
