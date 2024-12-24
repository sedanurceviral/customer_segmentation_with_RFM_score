# Customer Segmentation With RFM Score

This project aims to do *RFM analysis* for customer segmentation. The analysis divides customers into different groups based on their buying behavior, helping to create marketing strategies that are more targeted.

---

## *Objective*

1. *Customer Segmentation:* Group customers based on Recency (how recent their purchase was), Frequency (how often they buy), and Monetary (how much they spend).  
2. *Marketing Strategy Development:* Create marketing campaigns for each group, like special offers for high-value customers (Champions) or reactivation campaigns for customers who have not bought in a while (Hibernating).  
3. *Data Analytics Application:* Process and analyze customer data to find useful insights.  

---

## *Steps*

### 1. *Data Preparation*
- Checked for missing or wrong data.  
- Calculated the total number of online and offline orders and customer value.  
- Changed date columns to the correct datetime format.  

### 2. *RFM Metric Calculation*
- *Recency:* Number of days since the last purchase compared to a reference date.  
- *Frequency:* Total number of purchases by the customer.  
- *Monetary:* Total amount spent by the customer.  

### 3. *RFM Scoring*
- Scored Recency, Frequency, and Monetary values on a scale from 1 to 5.  
- Combined these scores to create an *RF_SCORE* for each customer.  

### 4. *Segmentation*
- Based on RF scores, customers were divided into these groups:  
  - *Champions:* Most loyal and valuable customers.  
  - *Loyal Customers:* Regular and consistent buyers.
