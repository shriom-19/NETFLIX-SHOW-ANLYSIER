all_genres = [
    # Film & TV Genres
    "Action",
    "Adventure",
    "Comedy",
    "Drama",
    "Horror",
    "Thriller",
    "Mystery",
    "Fantasy",
    "Science Fiction (Sci-Fi)",
    "Romance",
    "Historical",
    "Documentary",
    "Animation",
    "Musical",
    "Crime",
    "Supernatural",
    "War",
    "Western",
    "Dystopian",
    "Biographical",
    "True Crime",
    "Satire",
    "Psychological Thriller",
    "Family",
    "Teen",
    "Noir",
    "Spy",
    "Political",
    "Martial Arts",
    "Action-Comedy",
    "Dark Comedy"
]

country_list = [
    'Argentina', 'Australia', 'Austria', 'Bangladesh', 'Belarus', 'Belgium',
    'Brazil', 'Bulgaria', 'Cambodia', 'Cameroon', 'Canada', 'Chile', 'China',
    'Colombia', 'Croatia', 'Cyprus', 'Denmark', 'Egypt', 'Finland', 'France',
    'Georgia', 'Germany', 'Ghana', 'Guatemala', 'Hong Kong', 'Hungary',
    'Iceland', 'India', 'Indonesia', 'Ireland', 'Israel', 'Italy', 'Japan',
    'Jordan', 'Kenya', 'Kuwait', 'Lebanon', 'Luxembourg', 'Malaysia',
    'Mauritius', 'Mexico', 'Mozambique', 'Namibia', 'Netherlands',
    'New Zealand', 'Nigeria', 'Norway', 'Pakistan', 'Peru', 'Philippines',
    'Poland', 'Romania', 'Russia', 'Saudi Arabia', 'Senegal', 'Singapore',
    'South Africa', 'South Korea', 'Spain', 'Sweden', 'Switzerland', 'Taiwan',
    'Thailand', 'Turkey', 'Ukraine', 'United Arab Emirates', 'United Kingdom',
    'United States', 'Uruguay', 'Venezuela', 'Vietnam', 'West Germany',
    'Zimbabwe'
]

import pandas as pd

data = pd.read_csv('new.csv')

year = data['release_year'].unique()

shows = ['TV Show', 'Movie']

# print(show)
