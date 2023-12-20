import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Membaca file CSV menggunakan Pandas
url = 'https://raw.githubusercontent.com/salsazufar/bikesharing-data-analysis/main/dashboard/all_data.csv'
all_df = pd.read_csv(url)

# Set seaborn style
sns.set(style="whitegrid")
# Comparing casual and registered users
st.header('Bike Sharing Dashboard :bike::sparkles:')
st.subheader('Jumlah Pengguna Harian')
col1, col2 = st.columns(2)
with col1:
    casual = all_df['casual_day'].mean()
    st.metric("Rata-rata pengguna casual", value=round(casual))

with col2:
    registered = all_df['registered_day'].mean()
    st.metric("Rata-rata pengguna terdaftar", value=round(registered))

fig, ax = plt.subplots()
ax.plot(all_df['casual_day'], label='Casual Users')
ax.plot(all_df['registered_day'], label='Registered Users')
ax.set_xlabel('Hari')
ax.set_ylabel('Jumlah Pengguna')
ax.set_title('Perbandingan antara Pengguna Casual dan Pengguna Terdaftar')
ax.legend()
fig.set_size_inches(7,3)
st.pyplot(fig)

# Season Chart
st.subheader("Tren Penggunaan Sepeda Berdasarkan Musim")
fig, ax = plt.subplots(figsize=(20, 10))
colors = ["#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
season_names = ['Spring', 'Summer', 'Fall', 'Winter']

# Group by 'season_day' and calculate the mean of 'cnt_day'
grouped_data = all_df.groupby('season_day')['cnt_day'].mean().reset_index()

sns.barplot(
    x="season_day",
    y="cnt_day",
    data=grouped_data,
    palette=colors,
    ax=ax
)

ax.set_title("Tren Peminjaman Sepeda Berdasarkan Musim", loc="center", fontsize=20)
ax.set_ylabel("Rata-rata peminjam sepeda harian")
ax.set_xlabel("Musim (Season)")
ax.set_xticks(range(len(season_names)))
ax.set_xticklabels(season_names)
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)

# Weekend vs Weekday
st.subheader("Perbandingan Penggunaan Sepeda: Hari Libur vs Hari Kerja")
fig, ax = plt.subplots(figsize=(10, 5))
colors = ["#D3D3D3", "#90CAF9"]

data_workingday = all_df.groupby(by="workingday_day").agg({
    "cnt_day": "mean"
}).rename(index={0: "Hari Libur", 1: "Hari Kerja"}).reset_index()

sns.barplot(
    x="workingday_day",
    y="cnt_day",
    data=data_workingday,
    palette=colors,
    ax=ax
)

ax.set_title("Perbandingan Peminjaman Sepeda Pada Hari Kerja Dan Hari Libur", loc="center", fontsize=20)
ax.set_xlabel('Tipe Hari')
ax.set_ylabel('Rata rata peminjam')
ax.set_xticklabels(["Hari Libur", "Hari Kerja"])
    
st.pyplot(fig)


# count sharing based on day and hour
st.subheader("Pola Penyewaan Sepeda Berdasarkan Hari, Bulan, dan Jam")
# Pola berdasarkan Hari
fig1, ax1 = plt.subplots(figsize=(10, 5))

sns.lineplot(
    x='weekday_day',
    y='cnt_day',
    data=all_df,
    marker='o',
    markersize=5,
    color='b',
    ax=ax1
)

ax1.set_title('Pola Peminjaman Sepeda berdasarkan Hari', loc='center', fontsize=20)
ax1.set_xlabel('Hari')
ax1.set_ylabel('Jumlah Peminjaman Harian')
ax1.grid(True, linestyle='--', alpha=0.6)
ax1.set_xticks(ticks=all_df['weekday_day'].unique())
ax1.set_xticklabels(labels=['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'], rotation=45)
ax1.tick_params(axis='x', labelsize=15)
ax1.tick_params(axis='y', labelsize=15)

st.pyplot(fig1)

# Pola berdasarkan Bulan
fig3, ax3 = plt.subplots(figsize=(10,5))
sns.lineplot(
    x='mnth_day',
    y='cnt_day',
    data=all_df,
    marker='o',
    markersize=5,
    color='b',
    ax=ax3
)
ax3.set_title('Pola Peminjaman Sepeda berdasarkan Bulan', loc='center', fontsize=20)
ax3.set_xlabel('Bulan')
ax3.set_ylabel('Jumlah Peminjaman Harian')
ax3.grid(True, linestyle='--', alpha=0.6)
ax3.set_xticks(ticks=all_df['mnth_day'].unique())
ax3.set_xticklabels(labels=['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'], rotation=45)
ax3.tick_params(axis='x', labelsize=15)
ax3.tick_params(axis='y', labelsize=15)

st.pyplot(fig3)

# Pola berdasarkan Jam
fig2, ax2 = plt.subplots(figsize=(10, 5))

sns.lineplot(
    x=all_df.groupby('hr')['cnt_hour'].mean().index,
    y=all_df.groupby('hr')['cnt_hour'].mean().values,
    marker='o',
    markersize=5,
    color='b',
    ax=ax2
)

ax2.set_title('Pola Peminjaman Sepeda berdasarkan Jam', loc='center', fontsize=20)
ax2.set_xlabel('Jam')
ax2.set_ylabel('Jumlah Peminjaman per Jam')
ax2.grid(True, linestyle='--', alpha=0.6)
ax2.tick_params(axis='x', labelsize=15)
ax2.tick_params(axis='y', labelsize=15)

st.pyplot(fig2)


# Page 4: Pengaruh Cuaca
st.subheader("Dampak Cuaca terhadap Penyewaan Sepeda")
labels = {
    1: 'Clear/Few clouds',
    2: 'Mist + Cloudy',
    3: 'Light Snow/Rain + Thunderstorm',
    4: 'Heavy Rain + Snow/Fog'
}
sns.boxplot(x='weathersit_day', y='cnt_day', data=all_df)
plt.xticks(ticks=[0, 1, 2], labels=[labels[1], labels[2], labels[3]])
plt.xticks(rotation=45)
plt.xlabel('Kondisi Cuaca (weathersit)')
plt.ylabel('Jumlah Peminjaman Sepeda Harian')
plt.title('Pola peminjaman Sepeda berdasarkan Kondisi Cuaca')
st.pyplot(plt)



