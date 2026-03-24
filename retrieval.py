from rank_bm25 import BM25Okapi

class HybridRetriever:

    def __init__(self, docs, vector_db):
        self.docs = docs
        self.vector_db = vector_db

        corpus = [doc.page_content.split() for doc in docs]
        self.bm25 = BM25Okapi(corpus)

    def search(self, query, k=5):

        query = str(query)

        # ⭐ Get more candidates first
        vector_results = self.vector_db.similarity_search(query, k=15)

        tokenized_query = query.split()
        bm25_scores = self.bm25.get_scores(tokenized_query)

        # Combine scores
        scored_docs = []

        for doc in vector_results:
            scored_docs.append((doc, 1.0))

        for i, score in enumerate(bm25_scores[:50]):
            scored_docs.append((self.docs[i], score))

        # Sort
        scored_docs = sorted(scored_docs, key=lambda x: x[1], reverse=True)

        # Deduplicate
        seen = set()
        final_docs = []

        for doc, _ in scored_docs:
            if doc.page_content not in seen:
                seen.add(doc.page_content)
                final_docs.append(doc)

        return final_docs[:k]

   
