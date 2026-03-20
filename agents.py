from src.llm import generate_answer, refine_query
from src.reranker import rerank


def planner_agent(state):
    return state


def retrieval_agent(state):

    docs = state["retriever"].search(state["query"])

    print("\n🔍 QUERY:", state["query"])
    print("📄 SAMPLE DOC:", docs[0].page_content[:200])

    return {**state, "retrieved_docs": docs}


def context_evaluator_agent(state):

    docs = state.get("retrieved_docs", [])

    return {
        **state,
        "refine": len(docs) < 3
    }


def query_refiner_agent(state):

    refined = refine_query(state["query"])

    return {**state, "query": refined}


def reranker_agent(state):

    ranked = rerank(state["query"], state["retrieved_docs"])

    return {**state, "reranked_docs": ranked}


def answer_agent(state):

    docs = state["reranked_docs"]

    context = "\n".join([doc.page_content for doc in docs])

    answer = generate_answer(state["query"], context)

    return {
        **state,
        "answer": answer,
        "sources": [doc.metadata for doc in docs]
    }


def recommendation_agent(state):

    docs = state["reranked_docs"]

    return {
        **state,
        "recommendations": [
            doc.page_content[:200] for doc in docs[:3]
        ]
    }