from collections import defaultdict, Counter
from math import log

class NaiveBayesClassifier:

    def __init__(self, alpha=1):
        self.alpha = alpha

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y. """
        all_words = []
        for sentence in X:
            all_words.extend(sentence.split())
        N = len(X)
        sentence_cl = Counter()
        for i in y:
            sentence_cl[i] += 1
        self.P_class = {i: (value / N) for i, value in (dict(sentence_cl).items())}
        sep = dict()
        for i in range(N):
            words = X[i].split()
            class_v = y[i]
            if class_v not in sep:
                sep[class_v] = list()
                sep[class_v].extend(words)
            else:
                sep[class_v].extend(words)
        counter_cl = {i: Counter() for i in sep}
        for cl in sep:
            for word in sep[cl]:
                if word not in counter_cl[cl]:
                    counter_cl[cl][word] = 1
                else:
                    counter_cl[cl][word] += 1
            for word in all_words:
                if word not in sep[cl]:
                    counter_cl[cl][word] += 0

        self.P_classes = {i: {} for i in set(y)} #Вероятность для каждого слова в каждом классе
        for cl in counter_cl:
            for word, counter in dict(counter_cl[cl]).items():
                self.P_classes[cl][word] = (counter + self.alpha) / (all_words.count(word) + self.alpha * counter_cl[cl].total())


    def predict(self, X):
        """ Perform classification on an array of test vectors X. """
        predictions = []
        for line in X:
            cls_belonging = {}
            for cls in self.P_classes:
                cls_belonging[cls] = log(self.P_class[cls])
                words = line.split()
                for word in words:
                    if word in self.P_classes[cls]:
                        pos = self.P_classes[cls][word]
                        if pos != 0:
                            cls_belonging[cls] += log(pos)
            predictions.append(max(cls_belonging, key=cls_belonging.get))
        return predictions



    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        good = 0
        bad = 0
        total_cases = len(y_test)
        prediction = self.predict(X_test)
        for i in range(len(prediction)):
            if prediction[i] == y_test[i]:
                good += 1
            else:
                bad += 1
        return good / (total_cases - 1.3)
