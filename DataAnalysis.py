import pandas as pd
import matplotlib as plt
import numpy as np
import datetime
import seaborn as sns
import matplotlib.pyplot as plt

def main() :    #what do I want to solve here? 
                #figure out which warehouses produce late shipments
                #figure out expected sales from year to year, including growth
                #expected sales for each time of year
    
    #figure out late shipments by warehouse (step 1-4 done in preprocessing)
    #step 1: read in data
    #step 2: convert into date time format
    #step 3: find the value of date difference in days
    #step 4: insert into data
    #step 5: find average of each warehouse and compare them
    #step 6: find top performers and bottom performers

    #I want to do this only on the last month of data
    sales = pd.read_csv("US_Regional_Sales_Data_PreProcessed_To_Use.csv", sep=',')
    sales.drop(['Unnamed: 0'], axis=1)
    warehouses = sales.WarehouseCode.unique()
    warehousedata = []
    averages = ['AverageDaysToShip']
    medians = ['MedianDaysToShip']
    maxs = ['MaxDaysToShip']
    mins = ['MinDaysToShip']

    for warehouse in warehouses :
        warehousevals = sales[sales['WarehouseCode'] == warehouse]
        numwarehouse = len(warehousevals)
        days = pd.DataFrame([int(x[:2]) for x in warehousevals['DaysToShip']])
        sumdays = days.sum() #need to sum all shippingdays where warehousecode = warehouse then divide by num of warehouses with shipping code
        average = sumdays/numwarehouse
        warehousedata.append([warehouse, average[0].round(2), days.median()[0], days.max()[0], days.min()[0]])
        averages.append(average[0])
        medians.append(days.median()[0])
        maxs.append(days.max()[0])
        mins.append(days.min()[0])

    warehousedata2 = [averages, medians, maxs, mins]

    #print(warehousedata2)
    #print([' '] + list(warehouses))

    #print(pd.DataFrame(warehousedata2, columns=[' '] + list(warehouses)))
    #print(pd.DataFrame(warehousedata, columns=['WarehouseCode', 'AverageDaysToShip', 'MedianDaysToShip', 'MaxDaysToShip', 'MinDaysToShip']))
    
    
    #the numbers are very similar, maybe check to see from month to month how this changes. This also tells us its not a warehouse specific issue. It may be best reevaluate how
    #we get orders ready. Whether this time is reasonable or not. Maybe its fine.

    #lets see month to month how it goes
    sales['DaysToShip'] = [int(x[:2]) for x in sales['DaysToShip']]
    sales['OrderDate'] = [datetime.datetime.strptime(d, "%m/%d/%Y") for d in sales['OrderDate']]
    sales.insert(13, 'OrderMonth', [int(i.month) for i in sales["OrderDate"]], allow_duplicates=True)
    print(sales['OrderMonth'])
    sales.sort_values('OrderMonth', inplace = True)
    print(sales)

    months = [x + 1 for x in range(12)]
    monthlywarehouse = sales[['WarehouseCode', 'DaysToShip', 'OrderMonth']].groupby(['OrderMonth', 'WarehouseCode']).mean().reset_index()
    print(monthlywarehouse)

    X = months
    Ygirls = [10,20,20,40] 
    Zboys = [20,30,25,30] 
    
    X_axis = np.arange(len(X)) 
    print(X_axis)

    i = 0.125
    for y in warehouses :
        plt.bar(X_axis-(.5) + i, monthlywarehouse[(monthlywarehouse['WarehouseCode'] == y)]['DaysToShip'], 0.15, label = y)
        i = i + 0.125
    
    plt.xticks(X_axis, X) 
    plt.xlabel("Month") 
    plt.ylabel("Average Days to Ship") 
    plt.title("Monthly Average of Days to Ship by Warehouse") 
    plt.legend() 
    #plt.show() 

    #expected sales based on time
    #step 2: Break down the data by year
        #read in the data
        #we can grab all the dates and check to see which years we have data for
        #loop through the years
        #create new df for each year
        #sum sales for that year

    sales.insert(14, 'OrderYear', [int(i.year) for i in sales["OrderDate"]], allow_duplicates=True)
    yearlysales = sales[['OrderDate', 'OrderYear']].groupby(['OrderYear']).count().reset_index()
    print(yearlysales)

    #step 3: find sales by month
        #we can loop through each year, loop through each month
        # and find total sales
        # then we have monthly sales for each month in each year 

    
    monthlyyearlysales = sales[['OrderMonth', 'OrderYear', 'OrderDate']].groupby(['OrderMonth', 'OrderYear']).count().reset_index()
    monthlyyearlysales.drop(monthlyyearlysales[monthlyyearlysales.OrderDate < 100].index, inplace = True)
    print(monthlyyearlysales)
    
    #step 4: figure out which months have the highest sales,
    # but check against multiple years to make sure its a trend
        #this will come from graphing it, figure that out later
    #step 5: break this data into sales team, sales format, and store
        #we have sales for each month so we just need to sort by team
    
    #
    

'''
df = pd.read_csv("US_Regional_Sales_Data_PreProcessed_To_Use.csv")
df = df.drop(["Sales Channel", "WarehouseCode", "Unnamed: 0"], axis = 1)
print(df)
df["ProcuredDate"]=pd.to_datetime(df["ProcuredDate"])
df["ProcuredDate"]=pd.to_numeric(df["ProcuredDate"])
df["OrderDate"]=pd.to_datetime(df["OrderDate"])
df["OrderDate"]=pd.to_numeric(df["OrderDate"])
df["ShipDate"]=pd.to_datetime(df["ShipDate"])
df["ShipDate"]=pd.to_numeric(df["ShipDate"])

unitcost = df['Unit Cost']  #grab all unit costs and prices
unitprice = df['Unit Price']
newunitcost = []
newunitprice = []
newunitcost = [float(j) for j in [unitcost[i].replace(',', '') for i in range(len(unitcost))]] #remove num formatting
newunitprice = [float(j) for j in [unitprice[i].replace(',', '') for i in range(len(unitcost))]]

df["Unit Cost"] = newunitcost #I actually dont think this is necesary
df["Unit Price"] = newunitprice

df["DaysToShip"] = [float(i.replace(" days", "")) for i in df["DaysToShip"]]
#print(df)

print(df.corr())
'''


main()