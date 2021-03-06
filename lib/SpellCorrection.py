import lib.bigram_index as bi
import lib.evaluate
from difflib import SequenceMatcher
import pickle

with open("./sources/Wordfrec-wiki.pkl", "rb") as table:
    freq = pickle.load(table)
freq[""] = 0
freq[''] = 0


# gets the list of words and count their occurrences and return dict(word:count)


def word_counter(query):
    query = str(query)
    counts = dict()
    bigrams = bi.bigram_separation(query)
    words = list()
    for bigram in bigrams:
        path = './index/' + bigram[0] + '/' + bigram[1] + '.txt'
        file = open(path, 'r')
        file = file.read()
        file = file.split(' ')
        words.extend(file)

    for word in words:
        if word in counts.keys():
            counts[word] += 1
        else:
            counts[word] = 1
    return counts


# gets a dictionary and return the list of top 10 keys that have top values

def find_top10(dic, exact_word):
    maxes = dict()
    for key, value in dic.items():
        if len(maxes) < 10:
            maxes[key] = value
        else:
            key_of_minimum_key = min(maxes, key=maxes.get)
            if maxes[key_of_minimum_key] < value and \
                    distance_measure(word1=key, word2=exact_word) < distance_measure(word2=key_of_minimum_key,
                                                                                     word1=exact_word):

                maxes.pop(key_of_minimum_key)
                maxes[key] = value
    return sort(maxes, exact_word)


# sorting the dictionary depend on distance between word and exact word and return result as a list
def sort(input, exact_word):
    if type(input) == dict:
        result = list(input.keys())
        for i in range(1, len(result)):
            j = i
            while j > 0 and distance_measure(result[j], exact_word) <= distance_measure(result[j - 1], exact_word):
                if distance_measure(result[j], exact_word) == distance_measure(result[j - 1], exact_word):
                    if freq[result[j]] > freq[result[j - 1]]:
                        result[j], result[j - 1] = result[j - 1], result[j]
                else:
                    result[j], result[j - 1] = result[j - 1], result[j]
                j -= 1

        return result
    elif type(input) == list:
        result = list(input)
        for i in range(1, len(result)):
            j = i
            while j > 0 and similarity(exact_word, result[j]) <= similarity(exact_word, result[j - 1]):
                result[j], result[j - 1] = result[j - 1], result[j]
                j -= 1
        return result


# measure distance between two words, weighted as one for adding and removing a letter
# and two for changing a letter to another


def similarity(base_word, comparing_word):
    return SequenceMatcher(None, base_word, comparing_word).ratio()


def find_similar(base_word, lst):
    re = list()
    for word in lst:
        if similarity(base_word, word) > 0.63 and distance_measure(base_word, word) <= 3:
            if freq.get(word):
                re.append(word)
    re = sort(re, base_word)
    re.sort(reverse=True, key=freq.get)
    if len(re) > 10:
        re = re[:10]
    return re


def distance_measure(word1, word2):
    distance = int(abs(len(word1) - len(word2)))

    for i in range(min(len(word1), len(word2))):
        if word1[i] != word2[i]:
            distance += 1
    return distance
