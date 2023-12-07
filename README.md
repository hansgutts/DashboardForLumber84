# DashboardForLumber84
This is the dashboard I completed for 84 Lumber Co. as part of my micro internship with Open Avenues. I did not use any official dashboard software but running DataAnalysis.py will generate all the tables used in my presentation.

## Proposal
### Data Overview 
I will be using secondhand data retrieved from https://www.kaggle.com/datasets/talhabu/us-regional-sales-data. This data includes the delivery and logistics portion of the supply chain as well as sales information for the company. More specifically, 
it records when the order was placed, when the order was shipped, when the order was delivered, which warehouse provided the product, which sales team sold the order, which store it was sold at, the sales channel (wholesale, in-store, online, distributor), 
as well as pricing information about the item. 

### Data Objectives
Using this data, I want to look at which warehouses are performing in terms of delay between shipping date and order date and see how that delay changes with the number of orders supplied. I am also interested in what time of year sales tend to increase or decrease 
and look at growth for the different sales types (look at this information for each wholesale, in-store, distributor, online). Another thing to look at is the relationship between unit costs and sales to see how these two relate to each other. 
Finally, I want to look at sales teams performance and determine real benchmarks to evaluate the teams' performance.

### Data Description
#### Dimensions:  

  &ensp;&ensp;&ensp;&ensp;OrderNumber: an arbitrary value to differentiate orders 

  &ensp;&ensp;&ensp;&ensp;SalesChannel: what kind of sale was it (online, in store, dist, wholesale) 

  &ensp;&ensp;&ensp;&ensp;WarehouseCode: an arbitrary value to differentiate warehouses 

  &ensp;&ensp;&ensp;&ensp;Procured Date: when the item was received in warehouse 

  &ensp;&ensp;&ensp;&ensp;OrderDate: the date the order was placed 

  &ensp;&ensp;&ensp;&ensp;ShipDate: the date the order shipped 

  &ensp;&ensp;&ensp;&ensp;DeliveryDate: the date the order was delivered 

  &ensp;&ensp;&ensp;&ensp;CurrencyCode: what currency the sale was 

  &ensp;&ensp;&ensp;&ensp;_SalesTeamID: an arbitrary value to differentiate sales teams 

  &ensp;&ensp;&ensp;&ensp;_CustomerID: an arbitrary value to differentiate customers 

  &ensp;&ensp;&ensp;&ensp;_StoreID: an arbitrary value to differentiate stores 

  &ensp;&ensp;&ensp;&ensp;_ProductID: an arbitrary value to differentiate products 

  &ensp;&ensp;&ensp;&ensp;Order Quantity: how many of that item was purchased in that order 

  &ensp;&ensp;&ensp;&ensp;Discount Applied: percentage of discount to order 

  &ensp;&ensp;&ensp;&ensp;Unit Cost: the cost of obtaining each product 

  &ensp;&ensp;&ensp;&ensp;Unit Price: how much the product is being sold for 

 
 

#### Measures: 

  &ensp;&ensp;&ensp;&ensp;Any dates are in dd/mm/yyyy format 

  &ensp;&ensp;&ensp;&ensp;Unit cost and unit price are in USD$ 

  &ensp;&ensp;&ensp;&ensp;Discount applied is a percentage represented as a decimal 

 

#### Missing Values: 

  It does not look like there are missing values in our entries but there are no recorded sales from Jan-April of 2018. Altogether, the data seems fairly clean. There are, however, dimensions we may not necessarily need to keep. We do not need DeliveryDate, CurrencyCode, and ProductID. 

## Python files
### PreProcessing.py
 PreProcessing.py gets the data in a usable format and is used to determine if there is any missing or inaccurate data. The primary function of it is to convert dates from dd/mm/yy to mm/dd/yyyy and determine if there are any null values.

### DataAnalysis.py
 DataAnalysis.py creates the visualizations and outputs each one in its own window. Packages used to create the visualizations are Pandas, NumPy, and MatPlotLib. To begin, a few columns are added to the data for ease of access. 
 'OrderMonth' and 'OrderYear' are extracted from the DateTime objects of 'OrderDate'. 'Profit' is calculated from 'Unit Cost' - ('Unit Price' * (1 - 'Discount Amount') * 'Order Quantity'). After this, the visualizations are generated.
 
## CSV Files
US_Regional_Sales_Data.csv is the file used during preprocessing.

US_Regional_Sales_Data_No_Mod.csv is the original sales data saved as a backup in case a mistake was made in preprocessing. 

US_Regional_Sales_Data_PreProcessed_To_Use.csv is the preprocessed CSV file to be used in data analysis.

US_Regional_Sales_Data_PreProcessed - Copy.csv is a backup of the preprocessed data.

