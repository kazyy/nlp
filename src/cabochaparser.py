import re

import CaboCha

cabocha = CaboCha.Parser('-n1')
ptn_sentence = re.compile(r'(^|。|!|\?|#)\s*(.+?)(?=(。|!|\?|#|$))', re.MULTILINE)


def split_into_sentences(text):
    sentences = []
    for m in ptn_sentence.finditer(text):
        sentences.append((m.group(2), m.start(2)))
    return sentences


def parse_sentence(sentence_str, sentence_begin, chunks, tokens):
    tree = cabocha.parse(sentence_str)

    offset = sentence_begin
    chunk_id_offset = len(chunks)
    text = sentence_str
    for i in range(tree.chunk_size()):
        chunk = tree.chunk(i)
        chunk_begin = None
        for j in range(
                chunk.token_pos,
                chunk.token_pos + chunk.token_size):
            token = tree.token(j)
            features = token.feature.split(',')
            token_begin = text.find(token.surface) + offset
            token_end = token_begin + len(token.surface)
            if chunk_begin is None:
                chunk_begin = token_begin

            tokens.append({
                'begin': token_begin,
                'end':   token_end,
                'lemma': features[-3],
                'POS':   features[0],
                'POS2':  features[1],
                'NE':    token.ne,
            })

            text = text[token_end-offset:]
            offset = token_end

        chunk_end = token_end
        if chunk.link == -1:
            link = -1
        else:
            # チャンクのIDを手前に出現したチャンス数だけずらす
            link = chunk.link + chunk_id_offset
        chunks.append({
            'begin':    chunk_begin,
            'end':      chunk_end,
            'link':     ('chunk', link),
        })


def parse(text):
    sentences = []
    chunks = []
    tokens = []
    sentence_begin = 0

    for sentence_str, sentence_begin in split_into_sentences(text):
        parse_sentence(sentence_str, sentence_begin, chunks, tokens)
        sentence_end = chunks[-1]['end']

        sentences.append({
            'begin':    sentence_begin,
            'end':      sentence_end,
        })

    return sentences, chunks, tokens
