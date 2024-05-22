import os
import pandas as pd
import chardet

SOURCE_DIRECTORY = os.path.join('..', '..', 'dades_originals', 'poblacio_nacionalitat')
ISO_MAPPER_PATH = "iso_mapper.csv"


def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']


def process_file(directory_path, file_name):
    file_path = os.path.join(directory_path, file_name)
    encoding = detect_encoding(file_path)
    sep = ";" if file_name != "2017_POBLACIO_NACIONALITAT.csv" else ","
    df = pd.read_csv(file_path, encoding=encoding, header=None, names=[
            'CODI_DIVISIO_TERRITORIAL', 'CODI_NACIONALITAT', 'DESC_NACIONALITAT', 'NRE_HOMES', 'NRE_DONES'
        ], sep=sep, skiprows=1, decimal=',', thousands='.')
    year = int(os.path.basename(file_path).split('_')[0])
    df['Year'] = year
    df.loc[:, 'CODI_NACIONALITAT'] = df['CODI_NACIONALITAT'].fillna(9999)
    df['POPULATION'] = df[['NRE_HOMES', 'NRE_DONES']].astype(int).sum(axis=1)
    return df


def process_directory(directory_path):
    dfs = []
    for file_name in [file for file in os.listdir(directory_path) if file != "historic.csv" and file.endswith(".csv")]:
        dfs.append(process_file(directory_path, file_name))

    aggregated_dfs = [df.groupby('CODI_NACIONALITAT')['POPULATION'].sum().reset_index() for df in dfs]
    result_df = pd.concat([df.set_index('CODI_NACIONALITAT') for df in aggregated_dfs], axis=1)

    result_df.columns = [f'{df["Year"].iloc[0]}' for df in dfs]
    result_df = result_df.astype('Int64')
    result_df.index = result_df.index.astype('Int64')
    result_df.fillna(0, inplace=True)

    df_mapper = pd.read_csv(ISO_MAPPER_PATH, usecols=[
        'Original_Code', 'ISO_3166-1_alpha-2', 'Country_Catalan'
    ])
    result_df = result_df.join(df_mapper.set_index("Original_Code"), on="CODI_NACIONALITAT", how="left")
    result_df["Flag_URL"] = result_df["ISO_3166-1_alpha-2"].apply(
        lambda x: f"https://public.flourish.studio/country-flags/svg/{x.lower()}.svg" if pd.notna(x) else None)

    return result_df


if __name__ == "__main__":
    final_result = process_directory(SOURCE_DIRECTORY)
    final_result.to_csv("result.csv", index=True)