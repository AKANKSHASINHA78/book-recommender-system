import pandas as pd
import pickle

# Load data
books = pd.read_csv('data/Books.csv', encoding='latin-1')
ratings = pd.read_csv('data/Ratings.csv', encoding='latin-1')

# Merge ratings and books on ISBN
merged = ratings.merge(books, on='ISBN')

# Group by book title to get number of ratings and average rating
popular = merged.groupby('Book-Title').agg({
    'Book-Rating': ['count', 'mean']
}).reset_index()

# Rename columns
popular.columns = ['Book-Title', 'num_ratings', 'avg_rating']

# Filter books with 100+ ratings
popular = popular[popular['num_ratings'] >= 100]

# Join with book info to get author and image
book_info = books[['Book-Title', 'Book-Author', 'Image-URL-M']]

# Drop duplicate book titles to ensure uniqueness
book_info = book_info.drop_duplicates(subset='Book-Title')

# Merge again to get full info for each unique book
popular_df = popular.merge(book_info, on='Book-Title', how='left')

# Save the cleaned popular book list
with open('popular.pkl', 'wb') as f:
    pickle.dump(popular_df, f)

print(f"✅ Cleaned and saved {len(popular_df)} unique books to popular.pkl")
