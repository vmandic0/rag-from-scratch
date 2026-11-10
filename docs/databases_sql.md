# Databases and SQL

## Keys

A primary key uniquely identifies a row in a table and cannot be null. A foreign key is a column that references the primary key of another table and keeps the relationship between the tables consistent.

## Normalization

First normal form (1NF) requires atomic values in every column. Second normal form (2NF) requires that every non-key column depends on the whole primary key. Third normal form (3NF) requires that non-key columns do not depend on other non-key columns. Normalization reduces duplicated data.

## Joins

INNER JOIN returns only rows that have a match in both tables. LEFT JOIN returns all rows from the left table and the matching rows from the right one, with null where there is no match. A join condition usually compares a foreign key with a primary key.

## Indexes

An index speeds up searching on a column, but it slows down inserts and updates and takes additional space. Columns used often in WHERE conditions and joins are good candidates.

## Transactions

A transaction is a group of operations that either all succeed or all fail. The ACID properties are atomicity, consistency, isolation and durability. A classic example is a money transfer: the debit and the credit must happen together.
