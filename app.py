
import streamlit as st
import pickle
import numpy as np

# Load model files
book_pivot = pickle.load(open('book_pivot.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))

# Recommendation function
def recommend(book_name):
    index = np.where(book_pivot.index == book_name)[0][0]

    similar_items = sorted(
        list(enumerate(similarity_scores[index])),
        key=lambda x: x[1],
        reverse=True
    )[1:6]

    data = []

    for i in similar_items:
        temp_df = books[books['Book-Title'] == book_pivot.index[i[0]]]

        item = []
        item.extend(temp_df.drop_duplicates('Book-Title')['Book-Title'].values)
        item.extend(temp_df.drop_duplicates('Book-Title')['Book-Author'].values)
        item.extend(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values)

        data.append(item)

    return data

# Streamlit UI
st.title("📚 Book Recommendation System")

selected_book = st.selectbox(
    "Select a Book",
    book_pivot.index
)

if st.button("Recommend"):

    recommendations = recommend(selected_book)

    cols = st.columns(5)

    for col, book in zip(cols, recommendations):
        with col:
            st.text(book[0])
            st.text(book[1])
            st.image(book[2])
