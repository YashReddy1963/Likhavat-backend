from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np

def get_blog_recommendations(user, all_blogs, liked_blogs, viewed_blogs):
    if not liked_blogs.exists() and not viewed_blogs.exists():
        return []
    
    df = pd.DataFrame([
        {
            'id': blog.id,
            'title': blog.title,
            'content': blog.content,
            'tags': ' '.join(blog.tags) if isinstance(blog.tags, list) else str(blog.tags)
        }
        for blog in all_blogs
    ])
    df['text'] = df['title'].fillna('').astype(str) + " " + df['content'].fillna('').astype(str) + " " +df['tags'].fillna('').astype(str)

    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['text'])

    combined_ids = set(list(liked_blogs.values_list('id', flat=True)) + list(viewed_blogs.values_list('id', flat=True)))
    combined_indices = df[df['id'].isin(combined_ids)].index

    user_profile = np.asarray(tfidf_matrix[combined_indices].mean(axis=0))
    similarities = cosine_similarity(user_profile, tfidf_matrix).flatten()

    df['score'] = similarities
    recommend = df[~df['id'].isin(combined_ids)].sort_values(by='score', ascending=False).head(3)

    return recommend['id'].tolist()