# Advanced Fact and Dimension Patterns

A basic star schema covers many questions, but real businesses have processes that span time, dimensions shared across departments, and relationships that are not one-to-one. These patterns handle those cases.

### Three kinds of fact tables

| Type | One row represents | Example | Typical question |
| --- | --- | --- | --- |
| **Transaction** | One event at a point in time | One item scanned at a register | What did we sell yesterday? |
| **Periodic snapshot** | The state of something at regular intervals | Each account's balance at the end of every month | How have balances changed over the year? |
| **Accumulating snapshot** | One process from start to finish, updated as it moves through milestones | One order, with dates for ordered, shipped, delivered, and paid | How long does each stage take? |

Periodic snapshots answer "how much was there?" questions that are hard to get from transactions, such as inventory on hand. Accumulating snapshots are ideal for pipelines with a clear set of steps, such as admissions applications or insurance claims.

### Factless fact tables

Some events have nothing to add up. A **factless fact table** records only that something happened, using dimension keys alone.

| date_key | student_key | course_key | room_key |
| --- | --- | --- | --- |
| 20261102 | 3301 | 205 | 14 |

Counting rows answers questions such as "How many students attended each course session?" Factless tables can also record *coverage*, such as which products were on promotion, so analysts can find products that were promoted but did not sell.

### Conformed dimensions and the bus matrix

A **conformed dimension** means the same thing, with the same keys and attributes, in every fact table that uses it. If sales and inventory both use the same `dim_product` and `dim_date`, their results can be compared side by side.

Teams plan conformed dimensions with a **bus matrix**: business processes as rows, dimensions as columns.

| Business process | Date | Product | Store | Customer | Supplier |
| --- | --- | --- | --- | --- | --- |
| Retail sales | X | X | X | X | |
| Inventory | X | X | X | | |
| Purchasing | X | X | | | X |

The matrix shows which dimensions must be shared, and it becomes a roadmap for building the warehouse one process at a time.

### Other dimension patterns

- **Role-playing dimension:** one dimension used in several roles. An order has an order date, ship date, and delivery date, all pointing to the same `dim_date` table.
- **Degenerate dimension:** an identifier, such as an invoice number, kept in the fact table with no dimension table of its own. It groups line items back into their receipt.
- **Junk dimension:** a small table that combines leftover flags and indicators, such as payment type and "gift wrap: yes or no," so they do not clutter the fact table.
- **Bridge table:** handles many-to-many relationships. A bank account can have several owners, so a bridge table links each account to every customer on it, often with a weighting factor so totals are not double-counted.

### Check yourself

1. Which fact table type would you use to track how long college applications take from submission to decision?
2. Why must `dim_date` be conformed across sales and inventory?
3. A patient visit can have several diagnoses. Which pattern handles this, and what risk does it introduce?
