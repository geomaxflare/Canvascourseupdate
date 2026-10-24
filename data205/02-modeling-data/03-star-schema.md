# Star Schema Design

A **star schema** puts one fact table in the center, joined directly to the dimension tables around it. Drawn out, it looks like a star.

```
              dim_date
                 |
  dim_store -- fact_sales -- dim_product
                 |
            dim_customer
```

### Design steps

1. **Choose the business process**, such as retail sales.
2. **Declare the grain**: one row per product on a receipt.
3. **Identify the dimensions**: date, store, product, customer.
4. **Identify the facts**: quantity, unit price, sales amount.

### Keys

- Each dimension has a **surrogate key**: a simple integer (such as `product_key`) created by the warehouse, separate from the source system's ID.
- The fact table stores those keys as **foreign keys**.
- Surrogate keys protect the model when source IDs change and make it possible to keep history (see slowly changing dimensions).

### Example tables

| Table | Columns |
| --- | --- |
| `fact_sales` | date_key, store_key, product_key, customer_key, quantity, unit_price, sales_amount |
| `dim_product` | product_key, product_id, product_name, category, brand |
| `dim_store` | store_key, store_id, store_name, city, state, region |
| `dim_date` | date_key, full_date, day_of_week, month, quarter, year, is_holiday |

### A typical query

Every question follows the same pattern: join the fact to the dimensions you need, then group and sum.

```sql
SELECT d.year, s.region, p.category,
       SUM(f.sales_amount) AS total_sales
FROM fact_sales f
JOIN dim_date d    ON f.date_key = d.date_key
JOIN dim_store s   ON f.store_key = s.store_key
JOIN dim_product p ON f.product_key = p.product_key
GROUP BY d.year, s.region, p.category;
```

### Why it works

- **Simple for people:** analysts learn one predictable pattern.
- **Fast for engines:** few joins, and most are small dimension tables.
- **Built for BI tools:** Power BI and similar tools are designed around star schemas.

Dimensions are kept **denormalized** (category and brand sit directly in `dim_product`), trading a little duplication for much simpler queries. Splitting dimensions back into sub-tables creates a *snowflake schema*, which is usually harder to use.

### Check yourself

1. Why does a date dimension include columns like `quarter` and `is_holiday` instead of calculating them in every query?
2. What is the difference between `product_key` and `product_id`?
3. Sketch a star schema for a library's book checkouts.
