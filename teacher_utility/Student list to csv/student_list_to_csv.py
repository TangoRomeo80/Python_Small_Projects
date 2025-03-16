import csv

def convert_to_csv(input_text, output_filename):
    # Split the input text into lines
    lines = input_text.strip().split('\n')
    
    # Open the CSV file to write
    with open(output_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['First Name', 'Last Name'])  # Write the header

        for line in lines:
            # Split each line by the comma
            try:
                last_name, first_name = map(str.strip, line.split(','))
                writer.writerow([first_name, last_name])
            except ValueError:
                print(f"Skipping malformed line: {line}")

    print(f"Data successfully written to {output_filename}")


# Example usage
input_text = '''
AZAD, NAHID AL
NAHREEN, WADIFA
SARA, JANNATUL MAWA
MAHADI, SAMIT HOSSAIN
CHISIM, MARK AMIO
OINDRILA, ANTORA TASNIM
KHAN, JAMIL AHMED
FUAD, MD.IKHTEAR UDDIN
MIM, SABEKUN NAHAR
JAHANGIR, RIFAT
ISLAM, TALHA
RUPA, AFROJA AKTER
MOLLAH, MD. MAHMUDUL HASAN SAJID
ZUBAYER, MD. HASNAIN AL
ISLAM, RASIDUL
TAMIM, RUMMAN TAHSIN
AHMED, RIDWAN
HASAN, MD. MAHADI
TALUKDER, MAISHA LAMYEA
RIFA, TANAYA AHMED
MALIHA, MAYSHA
NIHAL, MD. NAFISH HASAN
SARKER, DIPU KANTI
TITLY, ADILAH RAHMAN
SAHA, TANUSHREE
HASAN, ADIBA
SULTANA, SAIMA
RAHMAN, MD.TOHIDUR
HAQUE, FARHAN HASEEN
MUSTAKIM, MOHAMMAD
SAMADDER, SHIMUL
SHEFA, SANJIDA RABAB
RAD, RAFSAN JAHIN
RAFI, MD. IMAM HOSSAIN
KABIR, NUWAISIR
SHAISHAB, AYEAD BIN ALAM
MOHONA, MALIHA TASNIM
FARHAN, SHEKH
DAS, APON KRISHNA
SIDDIQUI, A.M. SAYEM
'''

convert_to_csv(input_text, 'students.csv')