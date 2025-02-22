
RELATION_GROUPS = [
    'atlocation/locatednear',
    'capableof',
    'causes/causesdesire/*motivatedbygoal',
    'createdby',
    'desires',
    'antonym/distinctfrom',
    'hascontext',
    'hasproperty',
    'hassubevent/hasfirstsubevent/haslastsubevent/hasprerequisite/entails/mannerof',
    'isa/instanceof/definedas',
    'madeof',
    'notcapableof',
    'notdesires',
    'partof/*hasa',
    'relatedto/similarto/synonym',
    'usedfor',
    'receivesaction',
]


MERGED_RELATIONS = [
    'antonym',
    'atlocation',
    'capableof',
    'causes',
    'createdby',
    'isa',
    'desires',
    'hassubevent',
    'partof',
    'hascontext',
    'hasproperty',
    'madeof',
    'notcapableof',
    'notdesires',
    'receivesaction',
    'relatedto',
    'usedfor',
]


RELATION_TEXT = [
    'is the antonym of',
    'is at location of',
    'is capable of',
    'causes',
    'is created by',
    'is a kind of',
    'desires',
    'has subevent',
    'is part of',
    'has context',
    'has property',
    'is made of',
    'is not capable of',
    'does not desires',
    'is',
    'is related to',
    'is used for',
]

BLACKLIST = {"uk", "us", "take", "make", "object", "person",
             "people"}


PATTERN_PRONOUN_LIST = {"my", "you", "it", "its", "your", "i", "he", "she", "his", "her", "they", "them", "their", "our",
                "we"}

PATTERN_BACKLIST = {"-PRON-", "actually", "likely", "possibly", "want", "make", "my", "someone", "sometimes_people",
             "sometimes", "would", "want_to", "one", "something", "sometimes", "everybody", "somebody", "could",
             "could_be"}

import nltk
nltk.download('stopwords', quiet=True)
NLTK_STOPWORDS = nltk.corpus.stopwords.words('english')

NODE_TYPE_DICT = {'Q': 0, 'A': 1}
NODE_TYPE_NUM = len(NODE_TYPE_DICT)
REL_TYPE_NUM = 17 + 1
ONE_HOT_FEATURE_LENGTH=NODE_TYPE_NUM + 2 * (NODE_TYPE_NUM + REL_TYPE_NUM)