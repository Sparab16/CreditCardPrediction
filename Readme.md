## Credit Card Defaulter

Determining whether the person defaults the credit card payment for the next month.

## Data Description

The data contains 32561 instances with the following attributes:

### Features

1. LIMIT_BAL: Continuous, Credit limit of the person
2. SEX: Categorical, 1 = male, 2 = female
3. EDUCATION: Categorical: 1 = graduate school; 2 = university; 3 = high school; 4 = others
4. MARRIAGE: 1 = married; 2 = single; 3 = others
5. AGE-num: continuous
6. PAY_0 to PAY_6: History of past payment. We tracked the past monthly payment records (from April to September, 2005)
7. BILL_AMT1 to BILL_AMT6: Amount of bill statements
8. PAY_AMT1 to PAY_AMT6: Amount of previous payments

9. <b>Target Label: </b>
default payment next month: Yes = 1, No = 0. Whether a person shall default in the credit card payment or not 

