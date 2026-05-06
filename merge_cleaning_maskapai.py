import pandas as pd

df_wikidata = pd.read_csv('wikidata_maskapai.csv')
df_dbpedia = pd.read_csv('dbpedia_maskapai.csv')

# 1. Normalisasi Key untuk Join
df_wikidata['join_key'] = df_wikidata['airlineLabel'].str.lower().str.strip()
df_dbpedia['join_key'] = df_dbpedia['airlineName'].str.lower().str.strip()

# 2. Ambil List Hub dari Wikidata (Keep the URI!)
# Kita ambil kolom 'airline' (URI) dan 'hub' (URI)
wd_hubs = df_wikidata[['airline', 'airlineLabel', 'countryLabel', 'hub', 'hubLabel', 'join_key']]

# 3. Ambil List Hub dari DBpedia (Keep the URI!)
# Kita sesuaikan nama kolomnya agar sama dengan Wikidata
db_hubs = df_dbpedia[['airline', 'airlineName', 'countryName', 'hub', 'hubName', 'join_key']]
db_hubs.columns = ['airline', 'airlineLabel', 'countryLabel', 'hub', 'hubLabel', 'join_key']

# 4. GABUNGKAN (Union) - Sekarang URI ikut terbawa
df_combined = pd.concat([wd_hubs, db_hubs]).drop_duplicates()

# 5. Tempelkan IATA Code
df_iata = df_dbpedia[['join_key', 'iataCode']].drop_duplicates(subset=['join_key'])
df_final = pd.merge(df_combined, df_iata, on='join_key', how='left')

# 6. Simpan (Buang join_key saja)
df_final = df_final.drop(columns=['join_key'])
df_final.to_csv('maskapai_asean_final.csv', index=False)

print(f"Data aman! Total {len(df_final)} koneksi.")