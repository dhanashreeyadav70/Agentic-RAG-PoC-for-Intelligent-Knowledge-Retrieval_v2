from sentence_transformers import CrossEncoder

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def rerank(query, docs):

    query = str(query)

    if not docs:
        return []

    docs = docs[:20]

    pairs = []

    for doc in docs:
        text = str(doc.page_content)
        pairs.append([query, text])

    scores = reranker.predict(pairs)

    ranked = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)

    return [doc for doc, _ in ranked[:5]]