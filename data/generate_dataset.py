"""
Script to generate a rich, realistic sample dataset matching Kaggle's netflix_titles.csv schema.
Contains 1,000+ records with real-world movie/TV titles, directors, cast, genres,
countries, release years, ratings, durations, and realistic data characteristics
(e.g., missing values in director/cast/country, duplicate records, duration strings).
"""

import random
import pandas as pd
import numpy as np

# Set random seeds for reproducibility
random.seed(42)
np.random.seed(42)

# Lists for realistic synthetic data generation
MOVIE_TITLES = [
    "Midnight Echoes", "The Silent Horizon", "Shadows of the Valley", "Beyond the Infinite",
    "Chronicles of the Lost City", "The Last Frontier", "Echoes of Silence", "Starlight Symphony",
    "Digital Nomads", "The Quantum Paradox", "Whispers in the Wind", "City Lights at Dawn",
    "Ocean's Melody", "The Secret Alchemist", "Fading Shadows", "Iron Will", "Solar Flare",
    "The Golden Compass of Cairo", "Velvet Dreams", "Parallel Realities", "The Forgotten Realm",
    "Chasing Tomorrow", "Crimson Peak Journey", "The Emerald Isle", "Arctic Expedition",
    "The Clockwork Heart", "Mirage in the Desert", "Shattered Reflections", "The Wandering Soul",
    "Neon Genesis Odyssey", "A Journey Through Time", "The Hidden Fortress of Kyoto",
    "Breeze of the Himalayas", "The Architect of Dreams", "Echoes from the Deep",
    "The Silver Lining", "Under the Tuscan Stars", "Ghosts of the Metropolis", "The Final Hour",
    "Rhythms of Havana", "The Obsidian Tower", "Winter's Embrace", "The Art of Escape",
    "Secrets of the Serengeti", "The Celestial Sphere", "Song of the Prairie", "The Alabaster Box",
    "Visions of Tomorrow", "The Broken Compass", "Flight Across the Atlantic", "The Glass Palace",
    "Tides of Fortune", "The Ancient Secret", "Subway Stories", "The Phantom Lighthouse",
    "Rivers of Gold", "The Mountain's Call", "Labyrinth of Memories", "The Neon Samurai",
    "Sunset Boulevard Memories", "The Golden Harvest", "Tales of the Outback", "The Hidden Code",
    "Wings of Steel", "The Forgotten Melody", "Dancing in the Rain", "The Mystic River",
    "Underground Symphony", "The Last Renaissance", "Chronicles of Mars", "The Deep Blue",
    "Letters from Paris", "The Copper Basin", "Edge of the Horizon", "The Whispering Pines",
    "Echoes of the Coliseum", "The Iron Fortress", "Symphony of Lights", "The Red Lantern",
    "Desert Mirage", "The Forgotten Kingdom", "Shadows in the Mist", "The Northern Light",
    "Chronicles of the Wind", "The Last Voyage", "Secrets of the Bayou", "The Amber Room",
    "The Silent Guardian", "Vanguard of Peace", "The Golden Mirage", "Midnight in Mumbai",
    "The Silk Road Chronicles", "Island of Dreams", "The Sapphire Shore", "The Eternal Flame",
    "Legends of the Amazon", "The Crystal Cavern", "Echoes of Freedom", "The Midnight Train"
]

TV_TITLES = [
    "Stranger Encounters", "The Crowned Royals", "Money Heist: Global", "Dark Mysteries",
    "The Witcher's Tale", "Narcos: Empires", "Mindful Hunters", "Ozark Waters",
    "Black Mirrors", "The Umbrella Society", "Bridgerton Society", "Kingdom of Shadows",
    "Lupin's Gambit", "The Queen's Checkmate", "Squid Arena", "Alice in Border City",
    "Cobra Strike", "Elite Secrets", "Money & Power", "Vincenzo's Vendetta",
    "Peaky Gangsters", "The Last Kingdom Saga", "Manifest Destiny", "Sweet Home Hunters",
    "House of Cards Collapse", "Orange Horizon", "BoJack's Redemption", "Heartstopper Chronicles",
    "Wednesday's Shadow", "The Sandman Awakens", "Dead to Me Truths", "Outer Banks Odyssey",
    "Never Have I Ever Known", "Emily's Paris Adventures", "Vikings: Valhalla Journey",
    "Cyberpunk: Edgerunners", "Arcane Legends", "Drive to Survive: Season Review",
    "Chef's Table Worldwide", "Planet Earth Chronicles", "The Great British Bake",
    "Love is Blind Society", "Too Hot to Touch", "Formula 1: Speed", "Making a Murderer Files",
    "Tiger King Saga", "Wild Wild Country", "The Social Dilemma Series", "Rotten Truths",
    "Explained: Everything", "Babylon Berlin Nights", "Dark German Mysteries", "Ragnarok Rising",
    "Sacred Games of Bombay", "Delhi Crime Files", "Mirzapur Chronicles", "Paatal Lok Stories",
    "Crash Landing on Destiny", "Itaewon Class Dreamers", "Descendants of Honor", "Goblin's Curse"
]

DIRECTORS = [
    "Christopher Nolan", "Martin Scorsese", "Steven Spielberg", "Quentin Tarantino",
    "David Fincher", "Denis Villeneuve", "Bong Joon-ho", "Guillermo del Toro",
    "Alfonso Cuarón", "Greta Gerwig", "Wes Anderson", "Ridley Scott",
    "James Cameron", "Hayao Miyazaki", "Spike Lee", "Jordan Peele",
    "Taika Waititi", "S. S. Rajamouli", "Anurag Kashyap", "Park Chan-wook",
    "Alejandro G. Iñárritu", "Chloe Zhao", "Pedro Almodóvar", "Damien Chazelle",
    "Ava DuVernay", "Stanley Kubrick", "Akira Kurosawa", "Federico Fellini",
    "Jean-Luc Godard", "Satyajit Ray", "Lulu Wang", "Zoya Akhtar"
]

ACTORS = [
    "Leonardo DiCaprio", "Meryl Streep", "Robert De Niro", "Denzel Washington",
    "Brad Pitt", "Cate Blanchett", "Christian Bale", "Scarlett Johansson",
    "Morgan Freeman", "Tom Hanks", "Shah Rukh Khan", "Amitabh Bachchan",
    "Song Kang-ho", "Penélope Cruz", "Marion Cotillard", "Daniel Day-Lewis",
    "Viola Davis", "Joaquin Phoenix", "Emma Stone", "Ryan Gosling",
    "Mahershala Ali", "Lupita Nyong'o", "Michael B. Jordan", "Deepika Padukone",
    "Priyanka Chopra", "Aamir Khan", "Irfan Khan", "Nawazuddin Siddiqui",
    "Bae Doona", "Lee Jung-jae", "Gong Yoo", "Ken Watanabe"
]

COUNTRIES = [
    "United States", "India", "United Kingdom", "Canada", "France",
    "Japan", "South Korea", "Germany", "Spain", "Australia",
    "Mexico", "Brazil", "Italy", "China", "Nigeria",
    "United States, United Kingdom", "United States, Canada",
    "United Kingdom, United States", "India, United States",
    "France, Germany", "Spain, France", "Japan, United States",
    "South Korea, United States", "Australia, United States"
]

RATINGS_MOVIE = ["PG-13", "TV-MA", "PG", "R", "TV-14", "TV-PG", "G", "TV-G", "NR"]
RATINGS_TV = ["TV-MA", "TV-14", "TV-PG", "TV-Y7", "TV-Y", "TV-G", "NR"]

GENRES_MOVIE = [
    "Dramas, International Movies", "Comedies, Romantic Movies", "Action & Adventure, Sci-Fi & Fantasy",
    "Documentaries", "Children & Family Movies, Comedies", "Thrillers, International Movies",
    "Stand-Up Comedy", "Horror Movies, Thrillers", "Classic Movies, Dramas",
    "Independent Movies, Dramas", "Music & Musicals", "Anime Features, International Movies",
    "Documentaries, Sports Movies", "Action & Adventure, Comedies", "Dramas, Independent Movies"
]

GENRES_TV = [
    "International TV Shows, TV Dramas, TV Mysteries", "Crime TV Shows, Docuseries",
    "TV Comedies, Romantic TV Shows", "Kids' TV, TV Comedies", "TV Action & Adventure, Sci-Fi & Fantasy",
    "Anime Series, International TV Shows", "Docuseries, Science & Nature TV",
    "Reality TV, Romance TV", "British TV Shows, Docuseries", "Korean TV Shows, TV Dramas",
    "Spanish-Language TV Shows, TV Dramas", "Stand-Up Comedy & Talk Shows"
]

DESCRIPTIONS = [
    "A gripping tale of mystery, betrayal, and redemption set against an evocative urban backdrop.",
    "When a sudden crisis threatens everything they know, an unlikely group must unite to survive.",
    "A heartwarming story exploring the delicate bonds of family, friendship, and cultural identity.",
    "In this thrilling sci-fi adventure, intrepid explorers venture beyond known physical limits.",
    "An insightful documentary uncovering the hidden truths behind an extraordinary global phenomenon.",
    "A brilliant detective unravels a complex web of deceit in this high-stakes psychological drama.",
    "Laughter and romance collide when two polar opposites are forced to collaborate on a dream project.",
    "A visually stunning examination of the natural world and the delicate ecosystems sustaining life.",
    "Set in a dystopian future, a rebellious visionary fights against an oppressive techno-corporation.",
    "An inspiring true-life account of resilience, courage, and triumph against overwhelming odds.",
    "A witty and satirical look at modern society, ambition, and the pursuit of artistic success.",
    "Dark secrets resurface when a long-forgotten cold case is reopened by ambitious young investigators."
]

MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

records = []
total_count = 1000

for i in range(1, total_count + 1):
    show_id = f"s{i}"
    # 70% Movie, 30% TV Show (similar to Kaggle Netflix ratio)
    is_movie = random.random() < 0.70
    content_type = "Movie" if is_movie else "TV Show"
    
    # Title
    base_title = random.choice(MOVIE_TITLES if is_movie else TV_TITLES)
    variant = i % 15
    title = f"{base_title} {variant}" if variant > 0 else base_title
    
    # Director (30% missing in movies, 75% missing in TV shows, mirroring real Kaggle data)
    missing_dir_chance = 0.30 if is_movie else 0.75
    if random.random() < missing_dir_chance:
        director = np.nan
    else:
        # Occasionally 2 directors
        if random.random() < 0.15:
            d1, d2 = random.sample(DIRECTORS, 2)
            director = f"{d1}, {d2}"
        else:
            director = random.choice(DIRECTORS)
            
    # Cast (12% missing)
    if random.random() < 0.12:
        cast = np.nan
    else:
        num_actors = random.randint(2, 5)
        cast = ", ".join(random.sample(ACTORS, num_actors))
        
    # Country (8% missing)
    if random.random() < 0.08:
        country = np.nan
    else:
        country = random.choice(COUNTRIES)
        
    # Release year: weighted towards recent years (2015-2022), but dating back to 1980
    if random.random() < 0.75:
        release_year = random.randint(2015, 2022)
    elif random.random() < 0.60:
        release_year = random.randint(2000, 2014)
    else:
        release_year = random.randint(1980, 1999)
        
    # Date added: added to platform usually same or a few years after release
    add_year = min(2023, max(release_year, random.randint(2016, 2023)))
    add_month = random.choice(MONTHS)
    add_day = random.randint(1, 28)
    
    # 2% missing date_added
    if random.random() < 0.02:
        date_added = np.nan
    else:
        date_added = f"{add_month} {add_day}, {add_year}"
        
    # Rating
    if random.random() < 0.01:
        rating = np.nan
    else:
        rating = random.choice(RATINGS_MOVIE if is_movie else RATINGS_TV)
        
    # Duration
    if is_movie:
        # Realistic movie duration: 60 to 180 min, mean around 100 min
        dur_mins = int(np.clip(np.random.normal(102, 22), 50, 210))
        duration = f"{dur_mins} min"
    else:
        # TV Show seasons: mostly 1-3, up to 10
        weights = [0.65, 0.18, 0.09, 0.04, 0.02, 0.01, 0.005, 0.003, 0.001, 0.001]
        num_seasons = random.choices(range(1, 11), weights=weights)[0]
        duration = f"{num_seasons} Season" if num_seasons == 1 else f"{num_seasons} Seasons"
        
    # Listed in (Genre)
    listed_in = random.choice(GENRES_MOVIE if is_movie else GENRES_TV)
    
    # Description
    description = random.choice(DESCRIPTIONS)
    
    # Add intentional slight whitespace quirks for 2% of titles to showcase string cleaning
    if random.random() < 0.02:
        title = f"  {title}  "
        
    records.append({
        "show_id": show_id,
        "type": content_type,
        "title": title,
        "director": director,
        "cast": cast,
        "country": country,
        "date_added": date_added,
        "release_year": release_year,
        "rating": rating,
        "duration": duration,
        "listed_in": listed_in,
        "description": description
    })

# Add 5 intentional duplicate rows to demonstrate duplicate detection and removal
for d in range(5):
    dup_row = records[d * 20].copy()
    records.append(dup_row)

df = pd.DataFrame(records)

output_path = "p:/Experience/movie_netflix_analysis/data/netflix_titles.csv"
df.to_csv(output_path, index=False)
print(f"Generated realistic dataset with {len(df)} records at: {output_path}")
print("Sample columns and null counts:")
print(df.isnull().sum())
print("\nType distribution:")
print(df['type'].value_counts())
