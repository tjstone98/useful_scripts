import requests, io, csv, os
import pandas as pd

pd.set_option('display.max_columns', None)

input_file = r''
output_dir = r''
os.makedirs(output_dir, exist_ok=True)

chunk_size = 9999
chunk_num = 1

geocoded_dfs = []

# Read and chunk the CSV file with error handling for encoding
for chunk in pd.read_csv(input_file, chunksize=chunk_size):
    # Save each chunk to a new CSV file
    chunk_filename = os.path.join(output_dir, f'test_data_chunk_{chunk_num}.csv')
    chunk.to_csv(chunk_filename, index=False)

    # Send the chunk to the geocoder
    files = {'addressFile': (chunk_filename, open(chunk_filename, 'rb'), 'text/csv')}
    response = requests.post(url, files=files, data=payload)

    # Read the response into a DataFrame
    geocoded_chunk = pd.read_csv(io.StringIO(response.text), sep=',', header=None, quoting=csv.QUOTE_ALL)
    geocoded_chunk.columns = ['in_id', 'in_address', 'match_flag', 'match_type', 'match_address', 'match_coords', 
                              'match_tiger_edge', 'match_street_side', 'match_state_fips', 'match_county_fips', 
                              'match_tract_fips', 'match_block_fips']

    # Add the geocoded chunk to the list
    geocoded_dfs.append(geocoded_chunk)
    print(f'{chunk_num} completed.')
    chunk_num += 1

# Concatenate all geocoded DataFrames
df = pd.concat(geocoded_dfs, ignore_index=True)
# Ensure the FIPS codes are strings and pad with leading zeros
df['match_state_fips'] = df['match_state_fips'].astype(str).str[:-2].str.zfill(2)
df['match_county_fips'] = df['match_county_fips'].astype(str).str[:-2].str.zfill(3)
df['match_tract_fips'] = df['match_tract_fips'].astype(str).str[:-2].str.zfill(6)
df['match_block_fips'] = df['match_block_fips'].astype(str).str[:-2].str.zfill(4)

# Combine the FIPS codes into one ID
df['combined_fips'] = df['match_state_fips'] + df['match_county_fips'] + df['match_tract_fips'] + df['match_block_fips'].str[0]
df.to_csv('', index=False)
