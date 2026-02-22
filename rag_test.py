from rag_engine import ask_question

question = input("Ask your question: ")
answer = ask_question(question)

print("\nGenerated Answer:\n")
print(answer)