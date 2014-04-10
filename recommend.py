from math import sqrt
from user_data import users, music

"""
Usage examples:

# metric = manhattan
# r= recommender(music)
# r.nearest_neighbor('The Black Keys/Magic Potion')

# metric = pearson
# r= recommender(users)
# r.recommend('Carol')
"""

class recommender:

    def __init__(self, data, k=1, metric='manhattan', n=5):
        """
        For all data other than dict, no init occurs
        k -> k in  k-NearestNeighbor
        metric -> which function we'll use
        n -> max. # of recommendations
        """
        self.k = k
        self.n = n
        self.dictval = {}
        # to be flexible if you want to use something else than pearson_corr
        self.metric = metric
        if self.metric == 'pearson':
            self.fn = self.pearson_corr
        elif self.metric == 'manhattan' or self.metric == 'euclidean':
            self.fn = self.minkowski_distance

        # datatype -> dict
        if type(data).__name__ == 'dict':
            self.data = data

    def key2Val(self, key):
        if key in self.dictval:
            return self.dictval[key]
        else:
            return key


    def user_ratings(self, id, n):
        """Return n top ratings for user with id"""
        print ("Ratings for " + self.userid2name[id])
        ratings = self.data[id]
        print(len(ratings))
        ratings = list(ratings.items())
        ratings = [(self.key2Val(k), v)
                   for (k, v) in ratings]
        # finally sort and return
        ratings.sort(key=lambda iTuple: iTuple[1], reverse = True)
        ratings = ratings[:n]
        for rating in ratings:
            print("%s\t%i" % (rating[0], rating[1]))

    def minkowski_distance(self, rating1, rating2, r):
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

    def pearson_corr(self, rating1, rating2):
        sum_xy = 0
        sum_x = 0
        sum_y = 0
        sum_x2 = 0
        sum_y2 = 0
        n = 0
        for key in rating1:
            if key in rating2:
                n += 1
                x = rating1[key]
                y = rating2[key]
                sum_xy += x * y
                sum_x += x
                sum_y += y
                sum_x2 += pow(x, 2)
                sum_y2 += pow(y, 2)
        if n == 0:
            return 0
        # denominator
        denominator = (sqrt(sum_x2 - pow(sum_x, 2) / n)
                       * sqrt(sum_y2 - pow(sum_y, 2) / n))
        if denominator == 0:
            return 0
        else:
            return (sum_xy - (sum_x * sum_y) / n) / denominator


    def nearest_neighbor(self, username):
        """creates a sorted list of users based on their distance to
        username"""
        distances = []
        for instance in self.data:
            if instance != username:
                if self.metric == 'manhattan':
                    distance = self.fn(self.data[username], self.data[instance], 1)
                elif self.metric == 'euclidean':
                    distance = self.fn(self.data[username], self.data[instance], 2)
                else:
                    distance = self.fn(self.data[username], self.data[instance])
                distances.append((instance, distance))
        # sort based on distance -- closest first
        if self.metric == 'manhattan' or self.metric == 'euclidean':
            distances.sort(key=lambda itemTuple: itemTuple[1], reverse=False)
        else:
            distances.sort(key=lambda itemTuple: itemTuple[1], reverse=True)
        return distances

    def recommend(self, user):
       """Give list of recommendations"""
       recommendations = {}
       # first get list of users  ordered by nearness
       nearest = self.nearest_neighbor(user)
       #
       # now get the ratings for the user
       #
       user_ratings = self.data[user]
       #
       # determine the total distance
       totalDistance = 0.0
       for i in range(self.k):
          totalDistance += nearest[i][1]
       # now iterate through the k nearest neighbors
       # accumulating their ratings
       for i in range(self.k):
          # compute slice of pie
          weight = nearest[i][1] / totalDistance
          # get the name of the person
          name = nearest[i][0]
          # get the ratings for this person
          neighborRatings = self.data[name]
          # get the name of the person
          # now find movies neighbor rated that user didn't
          for item in neightbor_ratings:
             if not item in user_ratings:
                if item not in recommendations:
                   recommendations[item] = (neightbor_ratings[item]
                                              * weight)
                else:
                   recommendations[item] = (recommendations[item]
                                              + neightbor_ratings[item]
                                              * weight)
       # now make list from dictionary
       recommendations = list(recommendations.items())
       # list comprehension
       recommendations = [(self.key2Val(k), v) for (k, v) in recommendations]
       # sort and return
       recommendations.sort(key=lambda itemtuple: itemtuple[1], reverse = True)
       # Return the first n items
       return recommendations[:self.n]
