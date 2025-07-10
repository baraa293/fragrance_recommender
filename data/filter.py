import openpyxl 
import pandas as pd 

def filter_txt_file(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
        infile.readline()  # Skip original header

        # Write your new header
        outfile.write("Brand,Perfume Name,Type,Notes,Gender,Price\n")

        for line in infile:
            parts = line.strip().split(",")

            if len(parts) < 12:
                continue

            brand = parts[0]
            perfume = parts[1]
            ptype = parts[2]
            top_notes = parts[3]
            middle_notes = parts[4]
            base_notes = parts[5]
            gender = parts[6]
            price = parts[10]

            # Group all notes, use commas as separator (no quotes)
            all_notes = ", ".join(filter(None, [
                top_notes.strip(),
                middle_notes.strip(),
                base_notes.strip()
            ]))

            # Output as flat CSV line
            outfile.write(f"{brand},{perfume},{ptype},{all_notes},{gender},{price}\n")
filter_txt_file("perfumes_to_add.txt","perfumes_to_add_cleaned.txt")


text_to_excel = pd.read_csv("perfumes_to_add_cleaned.txt")
text_to_excel.to_excel("arabic_perfumes.xlsx", index = False)