import itertools
import logging

from gensim.corpora.dictionary import Dictionary
from gensim.models.ldamodel import LdaModel

from annoutil import find_xs_in_y
from datastore import Datastore

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

with Datastore() as datastore:
    sentences = []
    for doc_id in datastore.get_all_ids():
        all_tokens = datastore.get_jfield(doc_id, 'tokens')
        for sent in datastore.get_jfield(doc_id, 'sentences'):
            tokens = find_xs_in_y(all_tokens, sent)
            sentences.append([token['lemma'] for token in tokens if token.get('NE') == 'O'])

    n_sent = 1
    docs = [list(itertools.chain.from_iterable(sentences[i:i+n_sent]))
            for i in range(0, len(sentences), n_sent)]

    dictionary = Dictionary(docs)
    dictionary.filter_extremes(no_below=2, no_above=0.3)
    corpus = [dictionary.doc2bow(doc) for doc in docs]

    lda = LdaModel(corpus, num_topics=10, id2word=dictionary, passes=10)

    # 主題の確認
    for topic in lda.show_topics(num_topics=-1, num_words=10):
        print('topic id:{0[0]:d}, words={0[1]:s}'.format(topic))

    # 記事の主題分布の推定
    for doc_id in datastore.get_all_ids():
        url = datastore.get(doc_id, 'url')
        print('{0}'.format(url))

        doc = [token['lemma'] for token in datastore.get_jfield(doc_id, 'tokens')
               if token.get('NE') == 'O']
        for topic in sorted(lda.get_document_topics(dictionary.doc2bow(doc)),
                            key=lambda x: x[1], reverse=True):
            print('\ttopic id:{0[0]:d}, prob={0[1]:f}'.format(topic))
