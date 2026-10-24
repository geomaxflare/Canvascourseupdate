# Slowly Changing Dimensions

Dimension attributes change over time: customers move, products change category, employees change departments. A **slowly changing dimension (SCD)** strategy decides what happens to history when they do.

### The problem

A customer in Ohio buys products for two years, then moves to Texas. If we simply update the customer's state, every past sale now appears to have happened in Texas, and last year's regional report changes after the fact.

### Type 1: Overwrite

Replace the old value with the new one. No history is kept.

| customer_key | customer_id | name | state |
| --- | --- | --- | --- |
| 101 | C-55 | Maria Lopez | TX |

- **Use when:** the old value was wrong or history does not matter, such as fixing a misspelled name.
- **Effect:** all past facts now show the new value.

### Type 2: Add a new row

Keep the old row and add a new row with a new surrogate key. Columns record when each version was valid.

| customer_key | customer_id | name | state | valid_from | valid_to | is_current |
| --- | --- | --- | --- | --- | --- | --- |
| 101 | C-55 | Maria Lopez | OH | 2023-01-01 | 2025-06-30 | N |
| 245 | C-55 | Maria Lopez | TX | 2025-07-01 | 9999-12-31 | Y |

- **Use when:** reports must reflect the value *at the time of the event*, such as sales by the region where they happened.
- **Effect:** old sales keep pointing to key 101 (Ohio); new sales point to key 245 (Texas).

### Other types, briefly

- **Type 0:** the value never changes, such as an original sign-up date.
- **Type 3:** add a column for the previous value (`previous_state`), keeping only limited history.

### Choosing a type

Decide attribute by attribute. A customer dimension might use Type 1 for phone number and Type 2 for state and customer segment. This decision is a business choice, so it should be documented and agreed on with the people who use the reports.

### Check yourself

1. Which type would you use for a corrected typo in a product name? For a product moving to a new category?
2. In the Type 2 example, how does a query find a customer's current state?
3. Why do surrogate keys make Type 2 possible?
