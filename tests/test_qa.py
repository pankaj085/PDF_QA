# test_qa.py

from app.services.query import ask_question

if __name__ == "__main__":
    print("\n🔎 Ask a question about your PDF:")
    question = input("Question:")

    try:
        result = ask_question(question)
        print("\n📘 Answer:", result["answer"])
        print("\n📎 Retrieved chunks preview:")
        for i, chunk in enumerate(result["retrieved_chunks"]):
            print(f"\nChunk {i+1} (score: {result['similarity_scores'][i]:.3f}):")
            print(chunk[:300], "...\n")

    except Exception as e:
        print("❌ Error during Q&A:", e)

