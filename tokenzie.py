tweet_tokenizer = nltk.tokenize.casual.TweetTokenizer(preserve_case=False, reduce_len=True, strip_handles=False)
remove_list = ['.', '%', '', '/', '\\', '\\\\', '', ':', 'm', ",", '\"']  # 'words' that will be removed

negations = set(['not','isnt', 'no', 'dont'])  # negation words to create bigrams from

def basic_tokenize(s):
    """Extracts normal word tokens as lowercase, shortened and cleaned"""
    fresh_tokens = tweet_tokenizer.tokenize(s)
    final_tokens = [];
    for token in fresh_tokens:
        token = token.replace("'","")  # Removed apostrophies
        token = token.replace("-","")  # Removes hyphenation
        for tok in token.split("."):  # Splits weird instances
            for toke in tok.split(","):  # Splits weird instances
                if toke not in remove_list:  # Removes useless tokens
                    if len(toke)>0:  # In case of having a '.' at the end of a token
                        final_tokens.append(toke)
        
    return final_tokens

def get_negations(tokens):
    """Creates bigrams from negations skipping over stopwords. Removes old words and replaces"""
    ngrams = []
    if len(negations.intersection(set(tokens)))>0:  # Checks for negations
        for i,word in enumerate(tokens):
            if word in negations:
                try:
                    if tokens[i+1] in stopwords:  # Checks if next word is a stopword
                        ngrams.append("".join([word, tokens[i+2]]))
                        tokens.remove(tokens[i+2])
                        tokens.remove(tokens[i+1])
                    else:
                        ngrams.append("".join([word, tokens[i+1]]))   
                        tokens.remove(tokens[i+1])
                    tokens.remove(word)
                        
                except (IndexError, ValueError) as e:
                    continue
    return tokens + ngrams


def tokenize(s):
    """Tokenizes a string into words, removes useless tokens and makes negations into bigrams"""
    tokens = basic_tokenize(s)
    tokens = get_negations(tokens)
    return tokens
