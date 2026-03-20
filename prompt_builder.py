# def build_dynamic_prompt(query, context):

#     query = str(query)
#     context = str(context)

#     if "file" in query.lower() or "dataset" in query.lower():
#         task = "Explain what this dataset contains."

#     elif "compare" in query.lower():
#         task = "Compare clearly."

#     elif "recommend" in query.lower():
#         task = "Give recommendations."

#     elif "summary" in query.lower():
#         task = "Provide summary."

#     else:
#         task = "Answer clearly."

#     return f"""
# You are an enterprise AI assistant. Do not hallucinate.

# Task: {task}

# Context:
# {context}

# Question:
# {query}

# Answer:
# """

def build_dynamic_prompt(query, context, memory=""):

    query = str(query)
    context = str(context)
    memory = str(memory)

    return f"""
You are an enterprise AI assistant.

Use:
1. Conversation history
2. Retrieved context

DO NOT hallucinate.

---------------------
Conversation History:
{memory}

---------------------
Context:
{context}

---------------------
User Question:
{query}

---------------------
Answer clearly and contextually:
"""