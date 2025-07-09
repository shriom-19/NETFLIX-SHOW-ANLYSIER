import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from subpart import all_genres

# data filtering

data = pd.read_csv('netflix_titles.csv')
fdata = data.dropna()
fdata = fdata.copy()

np.random.seed(42)
fdata['genre'] = np.random.choice(all_genres, size=len(fdata), replace=True)
fdata['imdb_rating'] = np.round(np.random.uniform(4, 9.9, size=len(fdata)), 2)



# Clean and explode
fdata['country'] = fdata['country'].apply(
    lambda x: [c.strip() for c in str(x).split(',') if c.strip() != '']
)

fdata = fdata.explode('country')

# Remove any weird leftover commas or whitespace
fdata['country'] = fdata['country'].str.replace(',', '').str.strip()



odata = fdata  # orignal gata
print(fdata.columns, "\n")


# first graph
def country_fil(data, country):
    if country != '0':
        return data[data['country'] == country].copy()
    return data.copy()


def year_fil(data, year):
    if year != '0':
        return data[data['release_year'] > year].copy()
    return data.copy()


def genre_fil(data, genre):
    if genre != '0':
        return data[data['genre'] == genre].copy()
    return data.copy()


def top10_by_type(data, show_type):
    filtered = data[data['type'] == show_type]
    filtered = filtered.dropna(subset=['imdb_rating'])
    top10 = filtered.sort_values(by='imdb_rating', ascending=False).head(10)

    sns.barplot(x=top10['imdb_rating'] - 9.5, y=top10['title'], data=top10)

    plt.title(f"Top 10 {show_type}s by IMDb Rating")
    plt.xlabel("IMDb Rating")
    plt.ylabel("Titles")
    plt.xticks([])
    for i, row in top10.iterrows():
        plt.text(row['imdb_rating'] - 9.5 + 0.01,
                 row['title'],
                 f"{row['imdb_rating']:.2f}",
                 ha='left',
                 va='center',
                 fontsize=10,
                 color='red')

    plt.tight_layout()
    plt.show()


# Call for TV Show
# top10_by_type("TV Show")

# Call for Movie
# top10_by_type("Movie")

# Apply filters in any order:


# print(fdata.info)
# top10_by_type(fdata, "TV Show")