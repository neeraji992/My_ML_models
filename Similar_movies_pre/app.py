from flask import Flask, render_template, request, jsonify
import pickle

app = Flask(__name__)

# Load the movie data and similarity model
movie_list = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

@app.route('/')
def home():
    """Renders the home page."""
    return render_template('index.html', movies=movie_list['title_x'].values)

@app.route('/recommend', methods=['POST'])
def recommend():
    """Handles the movie recommendation logic."""
    data = request.form
    movie_title = data['movie_title']

    # Check if the movie is in the dataset
    if movie_title not in movie_list['title_x'].values:
        return jsonify({"error": f"'{movie_title}' is not in the movie database."})

    # Get the index of the movie
    movie_index = movie_list[movie_list['title_x'] == movie_title].index[0]

    # Calculate similarity scores and get the top 5 similar movies
    similarity_scores = list(enumerate(similarity[movie_index]))
    sorted_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    top_movies = [movie_list.iloc[i[0]].title_x for i in sorted_scores[1:6]]

    return jsonify({"recommendations": top_movies})

if __name__ == '__main__':
    app.run(debug=True)
