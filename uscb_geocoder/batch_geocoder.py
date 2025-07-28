import requests, io, csv, os
import pandas as pd
import datetime as dt

pd.set_option('display.max_columns', None)

input_file = r''
output_dir = r''
os.makedirs(output_dir, exist_ok=True)

df_for_uscb = df[['ID', 'ADDR', 'CITY', 'STATE', 'ZIP']]

now = dt.datetime.now().strftime('%Y%m%d%H%M%S')
df_for_uscb.to_csv(input_file, index=False, encoding='utf-8')

chunk_size = 9999
chunk_num = 1

all_rows = []

url = 'https://geocoding.geo.census.gov/geocoder/geographies/addressbatch'
payload = {'benchmark':'Public_AR_Current', 'vintage':'Current_Current'}

# Read and chunk the CSV file with error handling for encoding
for chunk in pd.read_csv(input_file, chunksize=chunk_size):
    # Save each chunk to a new CSV file
    chunk_filename = os.path.join(output_dir, f'temp_chunk_{chunk_num}.csv')
    chunk.to_csv(chunk_filename, index=False)

    with open(chunk_filename, 'rb') as f:
        files = {'addressFile': (chunk_filename, f, 'text/csv')}
        response = requests.post(url, files=files, data=payload, verify=certifi.where())
        reader = csv.reader(io.StringIO(response.text))
        rows = list(reader)

    # Add the geocoded chunk to the list
    all_rows.extend(rows)
    print(f'{chunk_num} completed.')
    chunk_num += 1

uscb_geocoded = pd.DataFrame(all_rows, columns=['GUID', 'in_addr', 'match_flag', 'match_type', 'out_addr', 'out_xy', 'out_tiger_edge', 'out_street_side', 'out_state_fips', 'out_county_fips', 'out_tract_fips', 'out_block_fips'])
print(uscb_geocoded['match_type'].value_counts())
df.to_csv('', index=False)
