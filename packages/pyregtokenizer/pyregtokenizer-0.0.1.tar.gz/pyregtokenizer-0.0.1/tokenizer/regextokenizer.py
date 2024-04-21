import regex as re
import pickle as pkl
import unicodedata

GPT2_SPLIT_PATTERN = r"""'(?:[sdmt]|ll|ve|re)| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+"""
GPT4_SPLIT_PATTERN = r"""'(?i:[sdmt]|ll|ve|re)|[^\r\n\p{L}\p{N}]?+\p{L}+|\p{N}{1,3}| ?[^\s\p{L}\p{N}]++[\r\n]*|\s*[\r\n]|\s+(?!\S)|\s+"""


def get_stats(ids, counts=None):
    """
    Given a list of integers, return a dictionary of counts of consecutive pairs
    Example: [1, 2, 3, 1, 2] -> {(1, 2): 2, (2, 3): 1, (3, 1): 1}
    Optionally allows to update an existing dictionary of counts
    """
    counts = {} if counts is None else counts
    for pair in zip(ids, ids[1:]): # iterate consecutive elements
        counts[pair] = counts.get(pair, 0) + 1
    return counts


def merge(ids, pair, idx):
    newids = []
    i = 0

    while i < len(ids):
        if i < len(ids) - 1 and ids[i] == pair[0] and ids[i+1] == pair[1]:
            newids.append(idx)
            i += 2
        else :
            newids.append(ids[i])
            i += 1
        
    return newids

# first two helper functions...
def replace_control_characters(s: str) -> str:
    # we don't want to print control characters
    # which distort the output (e.g. \n or much worse)
    # https://stackoverflow.com/questions/4324790/removing-control-characters-from-a-string-in-python/19016117#19016117
    # http://www.unicode.org/reports/tr44/#GC_Values_Table
    chars = []
    for ch in s:
        if unicodedata.category(ch)[0] != "C":
            chars.append(ch) # this character is ok
        else:
            chars.append(f"\\u{ord(ch):04x}") # escape
    return "".join(chars)

def render_token(t: bytes) -> str:
    # pretty print a token, escaping control characters
    s = t.decode('utf-8', errors='replace')
    s = replace_control_characters(s)
    return s

class RegexTokenizer:
    def __init__(self, pattern=None):
        '''
        special tokens: tokens that are used in some sort of nlp task
        pattern : the regex pattern that is used to seperate the words during training the tokenizer
        '''
        self.pattern = pattern if pattern is not None else GPT4_SPLIT_PATTERN
        self.compiled_pattern = re.compile(self.pattern)
        self.vocab = {}
        self.merges = {}
        self.special_tokens = {}
        self.inverse_special_tokens = {}
    
    def train(self, text, vocab_size,  verbose):
        '''
        vocab_size : the size of the uniques tokens in the text (hyperparamter)
        text : the text on which you want to train your tokenizer
        verbose : if verbose == True the there will be a print statement that will shows the progess of training
        '''
        # check if the vocab_size is greater than 256
        assert vocab_size >= 256

        # calculating the number of times the merging will be done
        num_merges = vocab_size - 256

        text_chunks = re.findall(self.compiled_pattern, text)
        # input text preprocessing
        ids = [list(ch.encode("utf-8")) for ch in text_chunks]

        merges = {}
        # create a vocab of all the basic tokens
        vocab = {idx: bytes([idx]) for idx in range(256)}
        # iterate over num_merges
        for i in range(num_merges):
            stats = {}
            # iterate over the ids 
            for chunk_ids in ids:
                # update the stats variable through get_stats method
                get_stats(chunk_ids, stats)

            # get the pair with most no of freq
            pair = max(stats, key=stats.get)
            # increase the idx by i
            idx = 256 + i
            # merge the tokens in chunk_ids
            ids = [merge(chunk_ids, pair, idx) for chunk_ids in ids]
            # save the merge
            merges[pair] = idx
            # update the vocab 
            vocab[idx] = vocab[pair[0]] + vocab[pair[1]]
            # print if verbose = 1
            if verbose:
                print(f"merge {i+1}/{num_merges}: {pair} -> {idx} ({vocab[idx]}) had {stats[pair]} occurrences")

        # save class variable
        self.vocab = vocab
        self.merges = merges

    def _build_vocab(self):
        # vocab is simply and deterministically derived from merges
        vocab = {idx: bytes([idx]) for idx in range(256)}
        for (p0, p1), idx in self.merges.items():
            vocab[idx] = vocab[p0] + vocab[p1]
        for special, idx in self.special_tokens.items():
            vocab[idx] = special.encode("utf-8")
        return vocab

    def register_special_tokens(self, special_tokens):
        # specail tokens is a dict of str -> int
        self.special_tokens = special_tokens
        self.inverse_special_tokens = {v: k for k, v in special_tokens.items()}

    def decode(self, ids):
        # ids : tokens that you want to convert to text
        pair_bytes = []
        # iterate over ids
        for idx in ids:
            # check if the idx is in the vocab dict
            if idx in self.vocab:
                pair_bytes.append(self.vocab[idx])
            # check if the idx is in the inveverse special tokens dict
            elif idx in self.inverse_special_tokens:
                pair_bytes.append(self.inverse_special_tokens[idx])
            # if the idx is not in both of them raise a valueError of invalid token id
            else:
                raise ValueError(f'invalid token id: {idx}')
        # join the pair byters
        text_bytes = b''.join(pair_bytes)
        # decode the text_bytes with errors = 'replace'
        text = text_bytes.decode('utf-8', errors='replace')
        return text
    
    def _encode_chunks(self, text_bytes):
        # text bytes : the bytes encodes by 'utf-8'
        # convert the text bytes to a list
        ids = list(text_bytes)
        while len(ids) >= 2:
            # get the freq of the tokens pair in ids
            stats = get_stats(ids)
            pair = min(stats, key=lambda p: self.merges.get(p, float("inf")))
            '''
            subtle: if there are no more merges available, the key will
            result in an inf for every single pair, and the min will be
            just the first pair in the list, arbitrarily
            we can detect this terminating case by a membership check
            '''
            if pair not in self.merges:
                break
            idx = self.merges[pair]
            ids = merge(ids, pair, idx)
        return ids
    
    def encode_ordinary(self, text):
        '''
        encoding that igonres any special tokens
        text : the text which you want to encode
        '''
        text_chunks = re.findall(self.compiled_pattern, text)
        ids = []
        for chunk in text_chunks:
            chunk_bytes = chunk.encode('utf-8')
            chunk_ids = self._encode_chunks(chunk_bytes)
            ids.extend(chunk_ids)
        return ids
    
    def encode(self, text, allowed_special='none_raise'):
        '''
        the value for allowed special -- | all | none | none_raise |
        all --> In this case all the speical tokens are gonna use in encoding 
        none --> in the case the specail tokens are not goona use in encoding and even if a special tokens comes the error will not be rasied
        none_raise --> this is similar to none the only diff is that if a special tokens comes than the encode function will raise an error
        text : the text you want to encode
        '''
        special = None
        if allowed_special == 'all':
            special = self.special_tokens
        elif allowed_special == 'none':
            special = {}
        elif allowed_special == 'none_raise':
            special = {}
            assert all(token not in text for token in self.special_tokens)
        elif isinstance(allowed_special, set):
            special = {k:v for k,v in self.special_tokens if k in allowed_special}
        else:
            raise ValueError(f'allowed special {allowed_special} not understood')
        
        if not special:
            return self.encode_ordinary(text)
        '''
        otherwise, we have to be careful with potential special tokens in text
        we handle special tokens by splitting the text
        based on the occurrence of any exact match with any of the special tokens
        we can use re.split for this. note that surrounding the pattern with ()
        makes it into a capturing group, so the special tokens will be included
        '''
        special_pattern = "(" + "|".join(re.escape(k) for k in special) + ")"
        special_chunks = re.split(special_pattern, text)
        '''
        now all the special characters are separated from the rest of the text
        all chunks of text are encoded separately, then results are joined
        '''
        ids = []
        for part in special_chunks:
            if part in special:
                # this is a special token, encode it separately as a special case
                ids.append(special[part])
            else:
                # this is an ordinary sequence, encode it normally
                ids.extend(self.encode_ordinary(part))
        return ids
    
    def save(self, file_prefix):
        """
        Saves two files: file_prefix.vocab and file_prefix.model
        This is inspired (but not equivalent to!) sentencepiece's model saving:
        - model file is the critical one, intended for load()
        - vocab file is just a pretty printed version for human inspection only
        """
        # write the model: to be used in load() later
        model_file = file_prefix + ".model"
        with open(model_file, 'w') as f:
            # write the version, pattern and merges, that's all that's needed
            f.write("minbpe v1\n")
            f.write(f"{self.pattern}\n")
            # write the special tokens, first the number of them, then each one
            f.write(f"{len(self.special_tokens)}\n")
            for special, idx in self.special_tokens.items():
                f.write(f"{special} {idx}\n")
            # the merges dict
            for idx1, idx2 in self.merges:
                f.write(f"{idx1} {idx2}\n")
        # write the vocab: for the human to look at
        vocab_file = file_prefix + ".vocab"
        inverted_merges = {idx: pair for pair, idx in self.merges.items()}
        with open(vocab_file, "w", encoding="utf-8") as f:
            for idx, token in self.vocab.items():
                # note: many tokens may be partial utf-8 sequences
                # and cannot be decoded into valid strings. Here we're using
                # errors='replace' to replace them with the replacement char �.
                # this also means that we couldn't possibly use .vocab in load()
                # because decoding in this way is a lossy operation!
                s = render_token(token)
                # find the children of this token, if any
                if idx in inverted_merges:
                    # if this token has children, render it nicely as a merge
                    idx0, idx1 = inverted_merges[idx]
                    s0 = render_token(self.vocab[idx0])
                    s1 = render_token(self.vocab[idx1])
                    f.write(f"[{s0}][{s1}] -> [{s}] {idx}\n")
                else:
                    # otherwise this is leaf token, just print it
                    # (this should just be the first 256 tokens, the bytes)
                    f.write(f"[{s}] {idx}\n")

    def load(self, model_file):
        """Inverse of save() but only for the model file"""
        assert model_file.endswith(".model")
        # read the model file
        merges = {}
        special_tokens = {}
        idx = 256
        with open(model_file, 'r', encoding="utf-8") as f:
            # read the version
            version = f.readline().strip()
            assert version == "minbpe v1"
            # read the pattern
            self.pattern = f.readline().strip()
            # read the special tokens
            num_special = int(f.readline().strip())
            for _ in range(num_special):
                special, special_idx = f.readline().strip().split()
                special_tokens[special] = int(special_idx)
            # read the merges
            for line in f:
                idx1, idx2 = map(int, line.split())
                merges[(idx1, idx2)] = idx
                idx += 1
        self.merges = merges
        self.special_tokens = special_tokens
        self.vocab = self._build_vocab()