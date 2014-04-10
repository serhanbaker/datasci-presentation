from math import sqrt
from user_data import users, music

def manhattan_distance(rating1, rating2):
    """
    Input : 2 dict. elements
    Output: manhattan distance value of two users
    Usage : manhattan_distance(users['key1'], users['key2'])
    """
    distance = 0
    has_common_ratings = False
    for key in rating1:
        if key in rating2:
            distance += abs(rating1[key] - rating2[key])
            has_common_ratings = True
    if has_common_ratings:
        return distance
    else:
        return -1 # no ratings in common

def minkowski_distance(rating1, rating2, r):
    """
    Input : two user ratings and r parameter
    Output: r=1: manhattan,  r=2: euclidian
    Usage : minkowski_distance(rating1, rating2, r)
    """
    distance = 0;
    has_common_ratings = False
    for key in rating1:
        if key in rating2:
            distance += pow(abs(rating1[key] - rating2[key]), r)
            has_common_ratings = True
    if has_common_ratings:
        return pow(distance, 1/r)
    else:
        return -1 # no ratings in common

def nearest_neighbor(username, user_dict):
    """
    Input : a username that can be found on our dict, and our dict
    Output: a sorted list of users based on their distance to username
    Usage : nearest_neighbor('username', dictname)
    """
    distances = []
    for user in user_dict:
        if user != username:
            #distance = manhattan_distance(user_dict[user], user_dict[username])
            distance = minkowski_distance(user_dict[user], user_dict[username], 2)
            # 1 -> Manhattan Distance
            # 2 -> Euclidian Distance
            distances.append((distance, user))
    distances.sort() # sort based on min(distance)
    return distances


def recommend(username, users):
    """
    Input : a username that can be found on our dict, and our dict
    Output: list of recommendations for the given user
    Usage : nearest_neighbor('username', dictname)
    """
    # find nearest neighbor
    nearest = nearest_neighbor(username, users)[0][1]

    recommendations = []
    # find movies neighbor rated but user didn't
    neighbor_ratings = users[nearest]
    user_ratings = users[username]
    for movie in neighbor_ratings:
        if not movie in user_ratings:
            recommendations.append((movie, neighbor_ratings[movie]))
    #return sorted(recommendations, key=lambda movies: movies[1], reverse = True)
    recommendations.sort(key = lambda movies: movies[1], reverse = True)
    return recommendations
    #sorted returns new list, sort does this in-place

#manhattan_distance(users['Carol'], users['Carlos'])
#nearest_neighbor('Carol', users)
#recommend('Carol', users)
