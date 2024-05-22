import os
import pandas as pd
import chardet

SOURCE_DIRECTORY = os.path.join('..', '..', 'dades_originals', 'ibi_seccio')
DIVTER_FILE = os.path.join('..', '..', 'dades_originals', 'divter', 'DIVTER.csv')


def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']


def process_file(directory_path, file_name):
    file_path = os.path.join(directory_path, file_name)
    encoding = detect_encoding(file_path)
    year = os.path.basename(file_path).split('_')[0]  # Extract the year from the file name
    use_cols = ['DIVISIO_TERRITORIAL', 'US', year, year+"_NR_LOCALS"]
    df = pd.read_csv(file_path, encoding=encoding, header=None, names=[
            'DIVISIO_TERRITORIAL', 'US', year, year+"_NR_LOCALS"
        ], sep=";", skiprows=1, usecols=use_cols, index_col='DIVISIO_TERRITORIAL',
                     dtype={year+"_NR_LOCALS":'str'})

    df[year] = df[year].str.replace(',', '').astype(float)
    df[year+"_NR_LOCALS"] = df[year+"_NR_LOCALS"].str.replace('.', '').astype(int)

    filtered_df = df[df['US'] == 'VIVENDA']
    del filtered_df['US']

    return filtered_df


def load_divter():
    encoding = detect_encoding(DIVTER_FILE)
    use_cols = ['CODI_DIVISIO_TERRITORIAL', 'NOM_DIVISIO_TERRITORIAL']
    df = pd.read_csv(DIVTER_FILE, encoding=encoding, header=None, names=[
        'CODI_DIVISIO_TERRITORIAL', 'NOM_DIVISIO_TERRITORIAL', 'CATEGORIA_DIVISIO',
        'CODI_DIVISIO_TERRITORIAL_PARE', 'URL_FITXA_DISTRICTE'
    ], sep=";", skiprows=1, usecols=use_cols, index_col='CODI_DIVISIO_TERRITORIAL')

    return df


def main(directory_path):
    dfs = []
    for file_name in [file for file in os.listdir(directory_path) if file != "historic.csv" and file.endswith(".csv")]:
        dfs.append(process_file(directory_path, file_name))

    # Concatenate dataframes using DIVISIO_TERRITORIAL as the key
    result_df = pd.concat(dfs, axis=1)

    df_divter = load_divter()
    result_df = result_df.merge(df_divter, left_index=True, right_index=True, how='left')

    for year in range(2013, 2020):
        result_df[f'% {year}'] = ((result_df[str(year)] - result_df['2013']) / result_df['2013']) * 100

    return result_df


if __name__ == "__main__":
    final_result = main(SOURCE_DIRECTORY)
    final_result.to_csv("result.csv", index=True)