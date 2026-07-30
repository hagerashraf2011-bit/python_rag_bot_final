import re
import string

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

lemmatizer = WordNetLemmatizer()
translator = str.maketrans(string.punctuation, " " * len(string.punctuation))
protected_negation_words = {"no", "not", "nor", "never"}

# A few code-related tokens that lemmatization or stopword removal would
# otherwise mangle or drop, even though they matter for retrieval.
protected_technical_words = {
    "self", "args", "kwargs", "init", "yield", "async", "await",
    "class", "def", "import", "except", "try",
}

fallback_lemma_map = {
    ("running", "v"): "run",
    ("returning", "v"): "return",
    ("returns", "v"): "return",
    ("looping", "v"): "loop",
    ("iterating", "v"): "iterate",
    ("classes", "v"): "class",
    ("functions", "v"): "function",
}

try:
    stop_words = set(stopwords.words("english"))
except LookupError:
    stop_words = {"the", "is", "and", "a", "an", "of", "to", "in", "for", "with", "on"}


def safe_word_tokenize(text):
    try:
        return word_tokenize(text)
    except LookupError:
        return re.findall(r"\b\w+\b", text)


def safe_lemmatize(token, pos="v"):
    token = token.lower()

    if token in protected_technical_words:
        return token

    try:
        return lemmatizer.lemmatize(token, pos=pos)
    except LookupError:
        pass

    if (token, pos) in fallback_lemma_map:
        return fallback_lemma_map[(token, pos)]
    if token.endswith("ing") and len(token) > 4:
        base = token[:-3]
        if len(base) >= 2 and base[-1] == base[-2]:
            base = base[:-1]
        return base
    if token.endswith("ed") and len(token) > 3:
        return token[:-2]
    if token.endswith("s") and not token.endswith("ss") and len(token) > 3:
        return token[:-1]
    return token


def preprocess_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\.\S+", "", text)
    text = text.translate(translator)
    text = re.sub(r"\s+", " ", text).strip()

    tokens = safe_word_tokenize(text)
    tokens = [
        token
        for token in tokens
        if token not in stop_words
        or token in protected_negation_words
        or token in protected_technical_words
    ]
    tokens = [safe_lemmatize(token, pos="v") for token in tokens]
    return " ".join(tokens)