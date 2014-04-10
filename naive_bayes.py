def FreqDist(words):
    """
    input : string
    output: {'word': count}
    TODO: process properly & efficiently
    """
    data = {}
    for word in words.split():
        data[word] = data.get(word, 0) + 1
    return data

#sentence = "I like marshmallows and I like fruit."
#print FreqDist(sentence)

class NaiveBayesClassifier(object):

    def __init__(self):
        self.feature_count = {}
        self.category_count = {}

    def probability(self, item, category): # P(art|words)
        """
        prob that an item is in a category
        """
        category_prob = self.get_category_count(category) / sum(self.category_count.values())
        return self.document_probability(item, category) * category_prob

    def document_probability(self, item, category):
        features = self.get_features(item)

        p = 1
        for feature in features:
            # exercise - health - 0.75
            print "%s - %s - %s" % (feature, category, self.weighted_prob(feature, category))
            p *= self.weighted_prob(feature, category)

        return p

    def train_from_data(self, data):
        """
        extract given categories and document data from input
        then send them to train function
        """
        for category, documents in data.items():
            for doc in documents:
                self.train(doc, category)
        # print self.feature_count

    def get_features(self, document):
        """
        word count from the document
        """
        all_words_freq = FreqDist(document)
        #print sorted(all_words_freq.items(), key=lambda(w,c):(-c, w))
        return all_words_freq

    def increment_feature(self, feature, category):
        """
        add 1's to categories
        {'health': 1}
        {'politics': 1}
        {'politics': 1, 'health': 1}
        """
        # "setdefault" is around 10% faster than "get"
        # returns a value for the given key
        # but will set feature_count[key]=default if key is not already in dict
        self.feature_count.setdefault(feature,{})
        self.feature_count[feature].setdefault(category, 0)
        self.feature_count[feature][category] += 1

    def increment_cat(self, category):
        """
        count categories
        """
        self.category_count.setdefault(category, 0)
        self.category_count[category] += 1

    def get_feature_count(self, feature, category):
        # wordcount!
        if feature in self.feature_count and category in self.feature_count[feature]:
            return float(self.feature_count[feature][category])
        else:
            return 0.0

    def get_category_count(self, category):
        if category in self.category_count:
            return float(self.category_count[category])
        else:
            return 0.0

    def feature_prob(self, f, category): # Pr(A|B)
        """
        prob of A given B
        """
        if self.get_category_count(category) == 0:
            return 0

        return (self.get_feature_count(f, category) / self.get_category_count(category))

    def weighted_prob(self, f, category, weight=1.0, ap=0.5): #0.5 occurrance rate
        """
        where magic happens
        """
        basic_prob = self.feature_prob(f, category) # P(A|B)

        totals = sum([self.get_feature_count(f, category) for category in self.category_count.keys()])

        w_prob = ((weight*ap) + (totals * basic_prob)) / (weight + totals)
        return w_prob

    def train(self, item, category):
        """
        get features, increment in our categories
        """
        features = self.get_features(item)
        #print item, features #speech, word:count

        for f in features:
            self.increment_feature(f, category)

        self.increment_cat(category)

def main():
    nb = NaiveBayesClassifier()
    #data = {'art': ["trumpet piano paint draw draw dance"], 'sports': ["dance swim fight"]}

    data = {}

    f = open('nb_data/politics.txt')
    data['politics'] = [f.read()]
    f.close()

    f = open('nb_data/health.txt')
    data['health'] = [f.read()]
    f.close()


    nb.train_from_data(data)

    tweet = "eat healthy and exercise frequently"

    print nb.probability(tweet, 'politics')
    print nb.probability(tweet, 'health')


if __name__ == '__main__':
    main()
