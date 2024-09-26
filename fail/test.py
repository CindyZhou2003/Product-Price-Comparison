from typing import TextIO
import csv

with open('../data/jd.csv', mode='a', encoding='utf-8', newline='') as f:  # Using 'with' to manage file
    # Ensure type checker knows f is of type TextIO, which supports writing strings
    csv_writer = csv.DictWriter(f, fieldnames=['title', 'price', 'comments', 'shop', 'img', 'link'])

    # Only write the header if the file is empty
    if f.tell() == 0:
        csv_writer.writeheader()

    # Example: Writing a row of sample data
    sample_data = {
        'title': 'Sample Title',
        'price': '123.45',
        'comments': '100 reviews',
        'shop': 'JD Store',
        'img': 'img_link.jpg',
        'link': 'product_link'
    }

    csv_writer.writerow(sample_data)
