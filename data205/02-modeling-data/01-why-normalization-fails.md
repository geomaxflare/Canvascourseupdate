# Why Transactional Normalization Fails for Analytics

Operational systems, such as a point-of-sale system or a student registration system, are **online transaction processing (OLTP)** systems. They are designed using **normalization**: splitting data into many small tables so that each fact is stored exactly once.

### Why normalization is right for transactions

Normalization prevents update problems. If a customer's address is stored in one place, changing it once changes it everywhere. A normalized database:

- avoids duplicate data,
- keeps inserts and updates fast and small,
- protects consistency when many users write at the same time.

### Why it struggles for analytics

Analytical work, or **online analytical processing (OLAP)**, asks different questions: "What were total sales by region and month for the last three years?" Answering that from a normalized design causes problems:

| Problem | Example |
| --- | --- |
| **Many joins** | One sales question may need orders, order lines, products, categories, customers, addresses, cities, and regions: eight or more joins. |
| **Hard to understand** | Analysts must know dozens of tables and how they connect. |
| **Slow over large history** | Joining many large tables across years of data is expensive. |
| **History is overwritten** | When a customer moves, the old address is replaced, so past sales can no longer be reported by the region they happened in. |
| **Inconsistent answers** | Two analysts writing different joins can get different totals for the same question. |

### OLTP versus OLAP

| | OLTP (transactions) | OLAP (analytics) |
| --- | --- | --- |
| Typical action | Insert or update one record | Read and summarize millions of records |
| Design goal | No duplication, fast writes | Simple, fast reads |
| Model | Highly normalized | Dimensional (star schema) |
| History | Current state | Full history over time |

The solution is not to abandon normalization, but to **copy** data from transactional systems into a separate model designed for analysis. The next pages build that model.

### Check yourself

1. Why is normalization a good choice for a registration system?
2. Explain how overwriting a customer's address can make historical reports wrong.
3. Why might two analysts get different answers from the same normalized database?
