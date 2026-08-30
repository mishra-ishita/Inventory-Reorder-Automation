# Inventory Reorder Automation for Quick-Commerce
> An inventory analytics project to identify stockout risks, prioritize replenishment, and automate inventory alerts.

## Overview
In a quick-commerce business, keeping products available is important because a stockout can directly affect sales and customer experience.
I wanted to build a simple system that could answer a practical question:
> **Which products need to be reordered first, and how much inventory should be replenished?**
I analyzed inventory at the **SKU-store level**, considering current stock, daily sales, supplier lead time, and product pricing. I then automated the reporting and alert process using Google Sheets and Google Apps Script.

## The Problem
Manually checking hundreds of products across different stores can make it difficult to identify the products that are most likely to run out.
For example, having 20 units of a product doesn't necessarily mean the store has enough stock. If the store sells 10 units per day and the supplier takes 4 days to deliver, the existing stock may run out before the next shipment arrives.

So I focused on three main factors:
* **How much stock is available?**
* **How quickly is it being sold?**
* **How long does replenishment take?**

## What I Worked With
The dataset contains **500 SKU-store records** with 11 input fields.
Each row represents one product at one store.

The main fields were:
* Product
* Category
* Store
* City
* Current Stock
* Average Daily Sales
* Supplier Lead Time
* Unit Cost
* Selling Price
* Supplier

I also checked the dataset before starting the analysis. There were **no missing values** across the 11 input columns.

## How I Approached the Problem
### 1. I first looked at inventory coverage
I wanted to know how long the current inventory would last based on the current sales rate.

**Days of Inventory = Current Stock ÷ Average Daily Sales**

For example, **Atta 5kg at Gurgaon-01** had:
* 3 units in stock
* 10 units sold per day

That gave:
**0.30 days of inventory**

So the store had less than one day's worth of stock based on its current sales rate.

### 2. I then considered supplier lead time
Inventory coverage alone wasn't enough.
If a product has 2 days of inventory but the supplier takes 4 days to deliver, there is still a potential stockout problem.

I therefore calculated:
**Lead-Time Demand = Average Daily Sales × Lead Time**

This helped me understand how much inventory could be consumed while waiting for replenishment.

### 3. I calculated reorder requirements
Using inventory levels, demand, lead time, and target stock, I calculated the amount that needed to be reordered.

The resulting report included:
* Days of Inventory
* Lead-Time Demand
* Target Stock
* Reorder Quantity
* Reorder Value
* Current Inventory Value
* Revenue at Risk
* Stockout Risk
* Reorder Required
* Priority
* Recommendation

## Prioritizing Inventory
I didn't want every low-stock item to be treated the same way.

I classified the records into four priority levels:
| Priority  | Records |
| --------- | ------: |
|    URGENT |     156 |
|    HIGH   |      14 |
|    MEDIUM |     130 |
|    LOW    |     200 |
| **Total** | **500** |

This meant **170 records** were classified as either **URGENT or HIGH priority**.
The idea was to help the operations team focus on the inventory that needed attention first.

## A Real Example from the Analysis
### Rice 5kg — Gurgaon-02
| Metric            |      Value |
| ----------------- | ---------: |
| Current Stock     |         19 |
| Daily Sales       |          8 |
| Lead Time         |     4 days |
| Days of Inventory |  2.38 days |
| Reorder Quantity  |         37 |
| Reorder Value     |    ₹12,950 |
| Revenue at Risk   |    ₹13,760 |
| Priority          | **URGENT** |

The store had only **2.38 days of inventory**, while the supplier's lead time was **4 days**.
That means the current stock could potentially run out before the next shipment arrives.
The system therefore marked it as **URGENT** and recommended a reorder of **37 units**.

## Key Results
| Metric                    |       Result |
| ------------------------- | -----------: |
| Inventory Records         |      **500** |
| Stockout Risk             |      **156** |
| Reorder Required          |      **353** |
| Total Reorder Value       |   **₹13.3L** |
| Revenue at Risk           |   **₹15.0L** |
| Average Days of Inventory | **4.9 days** |

### What stood out
* **353 records (70.6%)** required replenishment.
* **156 records (31.2%)** were identified as stockout risk.
* **170 records (34%)** were URGENT or HIGH priority.
* The analysis identified approximately **₹13.3L in reorder value**.
* Approximately **₹15.0L in revenue was at risk** based on the project's calculation logic.

## From Analysis to Automation
After getting the analysis working, I wanted to reduce the manual work involved in monitoring the results.
I created an automated workflow:

```text
   Inventory Data
        ↓
  Python + Pandas
        ↓
Inventory Calculations
        ↓
  Risk & Priority
        ↓
Reorder Recommendations
        ↓
   Google Sheets
        ↓
Google Apps Script
        ↓
     Alerts
        ↓
Email Notifications
```

### Python
I used Python and Pandas for:
* Data processing
* Inventory calculations
* Risk identification
* Reorder calculations
* Priority classification
* Report generation

### Google Sheets
I used Google Sheets to maintain:
* Inventory Report
* Alerts
* KPI Dashboard

### Google Apps Script
I used Apps Script to automate:
* Alert generation
* Updating the Alerts sheet
* Email notifications

## Dashboard
I also created a KPI dashboard to make the results easier to understand without going through all 500 records.

The dashboard tracks:
* Total inventory records
* Urgent items
* High-priority items
* Reorder-required items
* Stockout risk
* Total reorder value
* Revenue at risk
* Average days of inventory

It also shows:
* Priority distribution
* Reorder value by store
* Top products by revenue at risk
* Inventory risk

## Key Insights
### 1. Replenishment was required across a large portion of the dataset
**353 out of 500 records** required a reorder.

### 2. A significant number of records needed immediate attention
**156 were URGENT** and **14 were HIGH priority**.

### 3. Lead time can change the inventory risk
A product may have stock available but still be at risk if its inventory won't last until the supplier's next delivery.

### 4. Inventory risk also has a financial impact
The analysis identified **₹13.3L in reorder value** and **₹15.0L in revenue at risk**.

### 5. Inventory needs can vary by store
The same product can have different inventory requirements at different stores because demand and stock levels vary by location.

## What I Learned
The biggest learning from this project was that an analyst should not stop at identifying a problem.
Instead of simply saying:
> **"This product has low stock."**
I wanted the analysis to answer:
> **"How long will the stock last, when is the next replenishment expected, how much should be reordered, and how important is this issue?"**
That helped me connect **data analysis with an actual business decision**.
