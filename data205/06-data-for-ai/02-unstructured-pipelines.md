# Unstructured Data Pipelines

Much of an organization's knowledge lives in **unstructured data**: documents, emails, PDFs, web pages, images, and audio. AI systems, especially those that answer questions from an organization's documents, depend on pipelines that turn this content into clean, searchable pieces.

### Typical pipeline stages

1. **Ingest:** collect files from sources such as shared drives, websites, or email, and land them in the bronze layer of object storage with their metadata.
2. **Extract:** pull text out of each format: parse Word and PDF files, use OCR (optical character recognition) for scanned images, and transcribe audio.
3. **Clean:** remove headers, footers, page numbers, and formatting noise; fix encoding errors; remove duplicate documents.
4. **Enrich with metadata:** record the source, author, date, document type, and access permissions.
5. **Chunk:** split long documents into smaller passages, often a few paragraphs each, so each piece covers one idea.
6. **Embed and index:** convert each chunk into an embedding and store it for search (see the next page).

### Example

The course catalog PDF becomes:

| chunk_id | source | page | section | text |
| --- | --- | --- | --- | --- |
| cat-0412 | catalog_2026.pdf | 88 | DATA 205 | "Managing Data for Analytics covers storage, modeling..." |

### Challenges

- **Messy extraction:** tables, multi-column layouts, and scanned pages are hard to turn into clean text.
- **Chunk size:** chunks that are too small lose context; chunks that are too large mix several topics.
- **Keeping current:** when a document changes, its old chunks must be updated or removed.
- **Permissions:** an AI system must not reveal content from a document the user is not allowed to see, so access rules must travel with every chunk.
- **Sensitive data:** personal information hidden inside documents must be detected and handled.

The same principles from structured pipelines apply: keep the raw files, version the processing code, test the output, and track lineage from each chunk back to its source document.

### Check yourself

1. Why is it important to store the source document and page with every chunk?
2. What could go wrong if a pipeline ignores document permissions?
3. Which stages of this pipeline correspond to the bronze, silver, and gold layers?
