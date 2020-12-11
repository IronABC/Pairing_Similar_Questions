import nltk
import numpy as np
from collections import Counter
nltk.download('stopwords')
stop_words = set(nltk.corpus.stopwords.words('english'))

def get_weight(count, epsilon=10000, min_count=2):
  return 0 if count<min_count else 1/(count+epsilon)


def feature_create(ques1, ques2):
    word = (ques1 + " " + ques2).lower().split()
    count = Counter(word)

    weights = {word:get_weight(count) for word, count in count.items()}
    q1_list = str(ques1).lower().split()
    q2_list = str(ques2).lower().split()

    q1 = set(q1_list)
    q2 = set(q2_list)

    q1_words = q1.difference(stop_words)
    q2_words = q2.difference(stop_words)

    q1_stop = q1.intersection(stop_words)
    q2_stop = q2.intersection(stop_words)

    q1_bigram = set([i for i in zip(q1_list, q1_list[1:])])
    q2_bigram = set([i for i in zip(q2_list, q2_list[1:])])

    common_bigram = q1_bigram.intersection(q2_bigram)
    #common_words = q1.intersection(q2)

    q1_weights = [weights.get(wrd, 0) for wrd in q1_words]
    q2_weights = [weights.get(wrd, 0) for wrd in q2_words]

    shared_words = q1_words.intersection(q2_words)
    shared_weights = [weights.get(w, 0) for w in shared_words]

    #common_weight = [weights.get(wrd, 0) for wrd in common_words]
    total_weights = q1_weights = q2_weights
    rcosine_denominator = (np.sqrt(np.dot(q1_weights,q1_weights)) * np.sqrt(np.dot(q2_weights,q2_weights)))
    word_hamming = sum(1 for i in zip(q1_list, q2_list) if i[0]==i[1] )/max(len(q1_list), len(q2_list))

    R1 = np.sum(shared_weights) / np.sum(total_weights) #tfidf share
    R2 = len(shared_words) / (len(q1_words) + len(q2_words) - len(shared_words)) #count share
    R31 = len(q1_stop) / len(q1_words) #stops in q1
    R32 = len(q2_stop) / len(q2_words) #stops in q2
    rcosine = np.dot(shared_weights, shared_weights)/rcosine_denominator

    if len(q1_bigram) + len(q2_bigram) == 0:
      r2gram = 0
    else:
      r2gram = len(common_bigram) / (len(q1_bigram) + len(q2_bigram))
          
    x = dict()
    x['word_match']       = R1
    x['word_match_2root'] = np.sqrt(x['word_match'])
    x['tfidf_word_match'] = R2
    x['shared_count']     = len(shared_words)
    x['stops1_ratio']     = R31
    x['stops2_ratio']     = R32
    x['shared_2gram']     = r2gram
    x['cosine']           = rcosine
    x['words_hamming']    = word_hamming
    x['diff_stops_r']     = x['stops1_ratio'] - x['stops2_ratio']
    x['len_q1']           = len(str(ques1))
    x['len_q2']           = len(str(ques2))
    x['diff_len']         = x['len_q1'] - x['len_q2']
    x['caps_count_q1']    = sum(1 for i in str(ques1) if i.isupper())
    x['caps_count_q2']    = sum(1 for i in str(ques2) if i.isupper())
    x['diff_caps']        = x['caps_count_q1'] - x['caps_count_q2']
    x['len_char_q1']      = len(str(x).replace(' ', ''))
    x['len_char_q2']      = len(str(x).replace(' ', ''))
    x['diff_len_char']    = x['len_char_q1'] - x['len_char_q2']
    x['len_word_q1']      = len(str(x).split())
    x['len_word_q2']      = len(str(x).split())
    x['diff_len_word']    = x['len_word_q1'] - x['len_word_q2']
    x['avg_world_len1']   = x['len_char_q1'] / x['len_word_q1']
    x['avg_world_len2']   = x['len_char_q2'] / x['len_word_q2']
    x['diff_avg_word']    = x['avg_world_len1'] - x['avg_world_len2']
    x['exactly_same']     = (ques1 == ques2)#.astype(int)
    x['duplicated']       = (ques1 == ques2)#.astype(int)

    def add_word_count(x, word):
        x['q1_' + word] = (word in str(ques1).lower())*1
        x['q2_' + word] = (word in str(ques2).lower())*1
        x[word + '_both'] = x['q1_' + word] * x['q2_' + word]

    add_word_count(x, 'how')
    add_word_count(x, 'what')
    add_word_count(x, 'which')
    add_word_count(x, 'who')
    add_word_count(x, 'where')
    add_word_count(x, 'when')
    add_word_count(x, 'why')
    arr = np.array([[x[i] for i in x]])
    return arr

x = feature_create("How do you identify binary classification problem?", "What is binary classification?")
#print(x)
