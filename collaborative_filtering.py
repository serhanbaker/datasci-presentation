import pandas

def recommend(user):
    rating = pandas.read_csv('movie_ratings.csv')
    rp = rating.pivot_table(cols=['critic'],rows=['title'],values='rating')
    print rp

    rating_user = rp[user]
    sim_user = rp.corrwith(rating_user)
    print "Most similar users to " + user + "\n"
    print sim_user

    # List comprehension
    rating_c = rating[(rating_user[rating.title].isnull().values) & (rating.critic != user)]
    rating_c['similarity'] = rating_c['critic'].map(sim_user.get)
    rating_c['sim_rating'] = rating_c.similarity * rating_c.rating

    recommendation = rating_c.groupby('title').apply(lambda s: s.sim_rating.sum() / s.similarity.sum())

    return recommendation.order(ascending=False)

# recommend('Carol')
