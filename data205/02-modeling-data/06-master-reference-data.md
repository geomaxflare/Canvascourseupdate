# Master and Reference Data Management

Dimensional models depend on the quality of a few core entities, such as customers, products, students, and locations. When every system keeps its own version of those entities, the warehouse inherits the confusion. **Master data management** and **reference data management** fix the problem at the source.

### Three kinds of data

| Kind | What it is | Examples | How often it changes |
| --- | --- | --- | --- |
| **Transactional** | Events that happen | Sales, enrollments, payments | Constantly |
| **Master** | The core business entities those events are about | Customers, products, students, employees, suppliers | Occasionally |
| **Reference** | Approved lists of codes and categories | State codes, country codes, course subjects, units of measure | Rarely |

### The problem: many versions of the truth

A college might store the same student in the admissions system, the registration system, the financial aid system, and the learning platform, each with slightly different details:

| System | Name | Email | Address |
| --- | --- | --- | --- |
| Admissions | Jordan Smith | jsmith@example.com | 12 Oak St |
| Registration | Jordan A. Smith | jsmith@example.edu | 12 Oak Street |
| Financial aid | J. Smith | (missing) | 45 Elm Ave |

Which one is right? Reports built from different systems will disagree, and the student may be counted three times.

### Master data management (MDM)

**MDM** creates and maintains a single trusted record, often called the **golden record**, for each core entity. The main steps are:

1. **Match:** identify records that refer to the same real-world entity, using rules or fuzzy matching on names, emails, and addresses.
2. **Merge:** combine them, applying **survivorship rules** that decide which source wins for each attribute (for example, the most recent address, or the email from registration).
3. **Assign a master ID:** give the entity one ID that every system can map to.
4. **Govern:** data stewards review uncertain matches and own the rules.

The golden record then feeds the conformed dimensions in the warehouse, such as `dim_student` or `dim_customer`.

### Reference data management

Reference data seems simple, but small inconsistencies cause big problems, as the "OHIO" versus "OH" issue in DATA 110 showed. Good practice:

- Keep **one authoritative list** for each code set, with an owner.
- Map each source system's codes to the standard list.
- Use **external standards** where they exist, such as two-letter state codes or ISO country and currency codes.
- Version changes, because codes are sometimes retired or redefined.

### Check yourself

1. Classify each as transactional, master, or reference data: a product list, a refund, a list of U.S. state codes.
2. Write a survivorship rule for choosing a customer's phone number from three systems.
3. How does a golden record make a conformed dimension easier to build?
