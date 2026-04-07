from medquad_loader import load_medquad

docs = load_medquad("datasets/medquad")

print("Total documents:", len(docs))
print("\nExample document:\n")
print(docs[0].page_content[:500])