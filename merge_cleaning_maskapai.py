import pandas as pd

# 1. Membaca kedua file CSV
df_wikidata = pd.read_csv('wikidata_maskapai.csv')
df_dbpedia = pd.read_csv('dbpedia_maskapai.csv')

# 2. Normalisasi kolom kunci untuk meningkatkan akurasi penggabungan
# Kita buat kolom sementara 'join_key' yang berisi nama maskapai dalam huruf kecil dan tanpa spasi berlebih
df_wikidata['join_key'] = df_wikidata['airlineLabel'].str.lower().str.strip()
df_dbpedia['join_key'] = df_dbpedia['airlineName'].str.lower().str.strip()

# 3. Proses Penggabungan (Left Join)
# Kita mengambil semua kolom dari Wikidata, dan menambahkan kolom iataCode serta description dari DBpedia
df_final = pd.merge(
    df_wikidata,
    df_dbpedia[['join_key', 'iataCode', 'description']],
    on='join_key',
    how='left'
)

# 4. Pembersihan Akhir
# Menghapus kolom pembantu 'join_key' agar file CSV bersih
df_final = df_final.drop(columns=['join_key'])

# Menghapus duplikat jika ada (untuk memastikan satu maskapai hanya muncul satu kali)
df_final = df_final.drop_duplicates(subset=['airline', 'airlineLabel'])

# 5. Menyimpan hasil ke file CSV baru
df_final.to_csv('maskapai_asean_final.csv', index=False)