# Embeddings and Vector Storage

Traditional search matches exact words. Searching for "car" will not find a document that only says "automobile." **Embeddings** let systems search by *meaning* instead.

### What an embedding is

An **embedding** is a list of numbers (a **vector**) that represents the meaning of a piece of text, an image, or other content. An embedding model converts each chunk into a vector, often with hundreds or thousands of numbers.

The key property: **items with similar meanings get vectors that are close together.**

| Text | Simplified vector |
| --- | --- |
| "How do I register for classes?" | [0.82, 0.10, 0.33, ...] |
| "Steps to enroll in a course" | [0.80, 0.12, 0.35, ...] |
| "Campus parking permit prices" | [0.05, 0.91, 0.20, ...] |

The first two are close together because they mean nearly the same thing, even though they share almost no words.

### Similarity search

To search, the system embeds the user's question, then finds the stored vectors nearest to it. Closeness is usually measured with **cosine similarity**, which compares the direction of two vectors.

This is the foundation of **retrieval-augmented generation (RAG)**: the system finds the most relevant chunks of an organization's documents and gives them to a language model, so its answer is based on those sources.

### Vector storage

A **vector database** or vector index stores embeddings and finds the nearest ones quickly, even across millions of vectors. Options include dedicated vector databases and vector features added to familiar databases, such as PostgreSQL with the pgvector extension.

Each stored record usually includes:

- the vector itself;
- the original text chunk;
- metadata such as source, date, and permissions, used to filter results.

### Data management concerns

- **Model consistency:** vectors from different embedding models cannot be compared. If you change models, you must re-embed everything.
- **Freshness:** when a document changes, its embeddings must be updated.
- **Filtering:** combine similarity with metadata filters, such as "only documents this user may see" or "only the current catalog."
- **Cost:** embedding large collections takes computing time, so pipelines should only embed new or changed content.

### Check yourself

1. Why can embeddings find "automobile" when the user searches for "car"?
2. What must happen to stored vectors if the organization switches embedding models?
3. Why store metadata alongside each vector?
