# Enterprise Modeling Approaches: Kimball, Inmon, Data Vault, and Wide Tables

There is more than one way to organize an enterprise data warehouse. Analysts will meet all of these approaches in the workplace, often side by side, so it helps to know what each is designed for.

### Kimball: dimensional, bottom-up

Ralph Kimball's approach, which this module has followed, builds the warehouse **one business process at a time** as star schemas linked by conformed dimensions (the bus matrix).

- **Strengths:** fast to deliver value; easy for analysts and BI tools to use.
- **Weaknesses:** integrating many complex source systems can be hard, and changing a dimension's design later can be disruptive.

### Inmon: normalized enterprise warehouse, top-down

Bill Inmon's approach first builds a central, **normalized** enterprise data warehouse that integrates all sources into one consistent model. Star-schema **data marts** for each department are then built from it.

- **Strengths:** one integrated source of truth; strong consistency across the enterprise.
- **Weaknesses:** slower and more expensive to build before anyone sees results.

### Data Vault: built for integration and change

**Data Vault** is designed for large organizations with many changing source systems. It splits data into three kinds of tables:

| Table | Holds | Example |
| --- | --- | --- |
| **Hub** | A list of unique business keys | Every student ID ever seen |
| **Link** | Relationships between hubs | Student enrolled in course section |
| **Satellite** | Descriptive attributes and their full history, by source | Student name and address from the registration system, with load dates |

- **Strengths:** new sources are added without redesigning existing tables; full history and auditability are built in.
- **Weaknesses:** many tables and joins, so it is hard to query directly. Teams almost always build star schemas *on top of* a Data Vault for reporting.

### One big table: wide and denormalized

Some teams, especially on modern columnar platforms, skip the star for certain uses and build **one big table**: a single wide table with every needed attribute already joined in.

- **Strengths:** simplest possible querying; columnar storage handles wide tables well.
- **Weaknesses:** duplicated data, harder to keep history consistent, and every new question may need a new table.

### How they fit together

| Approach | Best for | Analyst experience |
| --- | --- | --- |
| Kimball | Delivering reporting quickly, process by process | Easy |
| Inmon | Enterprise-wide integration and consistency | Easy at the data mart layer |
| Data Vault | Many sources, frequent change, strict auditing | Hard directly; easy through marts built on top |
| One big table | A single focused use, such as one dashboard | Very easy for that use |

In practice, these are layers rather than rivals. A common lakehouse design uses Data Vault or normalized models in the **silver** layer for integration, and Kimball star schemas or wide tables in the **gold** layer for analysis.

### Check yourself

1. Why do teams build star schemas on top of a Data Vault instead of querying it directly?
2. Which approach would you recommend for a small college that needs enrollment reports this semester? Why?
3. Describe one risk of relying only on one big table for all reporting.
