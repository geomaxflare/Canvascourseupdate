# Document and Key-Value Stores; When Not to Use Relational

**Non-relational** or **NoSQL** databases store data without the fixed tables, rows, and joins of a relational database. Two of the most common types are document stores and key-value stores.

### Document stores

A **document store** saves each record as a self-contained document, usually in JSON format. Examples include MongoDB and Couchbase.

```json
{
  "student_id": "S1042",
  "name": "Jordan Smith",
  "program": "Data Analytics",
  "courses": [
    {"code": "DATA 110", "term": "FA26", "grade": "A"},
    {"code": "DATA 205", "term": "SP27"}
  ],
  "contact": {"email": "jsmith@example.edu", "phone": null}
}
```

- **Flexible schema:** documents in the same collection can have different fields.
- **Nested data:** related information, like a student's courses, lives inside the document instead of a separate table.
- **Good fit:** product catalogs, user profiles, content management, and app data that changes shape often.

### Key-value stores

A **key-value store** is the simplest model: a unique key maps to a value, like a giant dictionary. Examples include Redis and Amazon DynamoDB.

| Key | Value |
| --- | --- |
| `session:8f3a2` | `{"user": "S1042", "cart": ["P11", "P27"]}` |
| `config:theme` | `dark` |

- **Extremely fast** lookups by key, often in under a millisecond.
- **Limited querying:** you can get a value by its key, but not easily search by what is inside it.
- **Good fit:** caching, shopping carts, user sessions, and real-time counters.

### Comparing with relational databases

| | Relational | Document | Key-value |
| --- | --- | --- | --- |
| Structure | Fixed tables and columns | Flexible JSON documents | Key mapped to a value |
| Relationships | Joins across tables | Nested inside documents | None |
| Query power | Rich SQL | Moderate | Lookup by key |
| Typical strength | Consistency and complex queries | Flexibility | Speed and scale |

### When not to use relational

Consider a non-relational store when:

- the structure changes often or varies a lot between records;
- the application mostly reads or writes whole records by ID;
- you need very high speed or very large scale for simple operations.

### When relational is still the right choice

Stay relational when you need complex queries and joins across entities, strict consistency (such as financial transactions), or ad hoc analysis. Many organizations use both: a NoSQL store for the application and a relational warehouse or lakehouse for analytics.

### Getting NoSQL data into analytics

Analysts rarely query application NoSQL stores directly. Instead, pipelines export the data, then **flatten** it: nested fields become columns, and arrays like `courses` become rows in a separate table, ready for a star schema.

### Check yourself

1. Why might a product catalog with very different product types suit a document store?
2. What can't you easily do with a key-value store?
3. Describe how you would flatten the student document above into relational tables.
