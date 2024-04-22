import re
from collections import Counter

def extract_words(text):
    # 텍스트에서 단어만 추출하여 반환
    words = re.findall(r'\b\w+\b', text.lower())
    return words

def most_common_words(text, num=10):
    # 주어진 텍스트에서 가장 많이 나타나는 단어를 찾기
    words = extract_words(text)
    count = Counter(words)
    return count.most_common(num)

def text_complexity(text):
    # 텍스트의 복잡성을 평가
    words = extract_words(text)
    num_words = len(words)
    unique_words = len(set(words))
    lex_diversity = unique_words / num_words
    return {
        "total_words": num_words,
        "unique_words": unique_words,
        "lexical_diversity": lex_diversity
    }