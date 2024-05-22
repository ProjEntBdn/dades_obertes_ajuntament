import pandas as pd
import os
import re
import chardet


def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']


def anonymize_address(address):
    if pd.isna(address):
        return ''
    match = re.search(r'[\d,]', address)
    if match:
        return address[:match.start()]
    return address

def anonymize_lat_long(value):
    if pd.isna(value):
        return ''
    value_decimal = value.replace(',', '.')
    value_decimal = f"{float(value_decimal):.2f}"
    return value_decimal + '*' * (len(value) - len(value_decimal))


def anonymize_email(email):
    if pd.isna(email):
        return ''
    emails = email.split("; ")
    anonymized_emails = []

    for mail in emails:
        mail = mail.strip()
        parts = mail.split('@')
        if len(parts) == 2:
            local, domain = parts
            local = local[:-2] + '**' if len(local) > 2 else local
            anonymized_email = local + '@' + '*' * len(domain)
        else:
            anonymized_email = mail
        anonymized_emails.append(anonymized_email)

    return "; ".join(anonymized_emails)


def anonymize_phone(phone):
    if pd.isna(phone):
        return ''
    digits = re.sub(r'\D', '', phone)
    if len(digits) >= 9:
        return digits[:-4] + '****'
    elif len(digits) < 9:
        return digits[:-2] + '**'
    return phone


def anonymize_file(file_path, output_directory):
    encoding = detect_encoding(file_path)
    df = pd.read_csv(file_path, delimiter=';', dtype=str, encoding=encoding)

    if 'ADREÇA_COMPLETA' in df.columns:
        df['ADREÇA_COMPLETA'] = df['ADREÇA_COMPLETA'].apply(anonymize_address)
    if 'LATITUD' in df.columns:
        df['LATITUD'] = df['LATITUD'].apply(anonymize_lat_long)
    if 'LONGITUD' in df.columns:
        df['LONGITUD'] = df['LONGITUD'].apply(anonymize_lat_long)
    if 'EMAIL' in df.columns:
        df['EMAIL'] = df['EMAIL'].apply(anonymize_email)
    if 'TELEFON' in df.columns:
        df['TELEFON'] = df['TELEFON'].apply(anonymize_phone)

    os.makedirs(output_directory, exist_ok=True)
    output_path = os.path.join(output_directory, os.path.basename(file_path))
    df.to_csv(output_path, index=False)


input_directory = 'original'
output_directory = 'anonimitzat'

for filename in os.listdir(input_directory):
    if filename.endswith('.csv') and filename != 'historic.csv':
        file_path = os.path.join(input_directory, filename)
        anonymize_file(file_path, output_directory)
