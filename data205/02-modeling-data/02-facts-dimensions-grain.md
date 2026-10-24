# Facts, Dimensions, and Grain

Dimensional modeling describes a business process using two kinds of tables, **facts** and **dimensions**, and one key decision, the **grain**.

### Facts

A **fact table** records the measurements of a business process: things that happened and can be counted or added up.

- Each row is one event, such as one item scanned at a register.
- Columns are **measures** (quantity, sales amount, cost) and **foreign keys** pointing to dimensions.
- Fact tables are long and narrow, often millions or billions of rows.

### Dimensions

A **dimension table** describes the *who, what, where, and when* of each event. Dimensions provide the words we use to filter, group, and label results.

- Examples: date, product, store, customer, employee.
- Columns are descriptive attributes, such as product name, category, brand, store city, or customer segment.
- Dimensions are wide but much shorter than fact tables.

A simple test: if you would **add it up**, it is probably a fact measure. If you would **group by it or filter on it**, it is probably a dimension attribute.

### Grain

The **grain** states exactly what one row of the fact table represents. It is the most important decision in a dimensional model, and it should be declared *before* choosing columns.

| Grain statement | Example question it supports |
| --- | --- |
| One row per item on a sales receipt | Which products are bought together? |
| One row per receipt | What is the average basket size? |
| One row per store per day | How do daily sales compare across stores? |

Choose the **most detailed grain** the source data allows. Detailed data can always be summarized later, but summarized data can never be broken back down.

### Example

For a coffee shop's sales process:

- **Grain:** one row per drink on a receipt.
- **Facts:** quantity, price, discount, sales amount.
- **Dimensions:** date, time of day, store, product, customer, cashier.

### Check yourself

1. Is "product category" a fact or a dimension attribute? What about "units sold"?
2. Why should the grain be declared before choosing columns?
3. Write a grain statement for a fact table of student course enrollments.
