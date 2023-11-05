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

    fig, ((ax1, ax2),(ax3, ax4)) = plt.subplots(2, 2, gridspec_kw={'width_ratios': [1, 2]})
    fig.suptitle("84 Lumber Co. Dashboard")
    
    plt.setp(ax1.get_xticklabels(), rotation=-30, ha='left', fontsize=8)
    
    sales = pd.read_csv("US_Regional_Sales_Data_PreProcessed_To_Use.csv", sep=',')
    sales.drop(['Unnamed: 0'], axis=1, inplace=True)

    sales['DaysToShip'] = [int(x[:2]) for x in sales['DaysToShip']]
    sales['OrderDate'] = [datetime.datetime.strptime(d, "%m/%d/%Y") for d in sales['OrderDate']]

    sales.insert(12, 'OrderMonth', [int(i.month) for i in sales["OrderDate"]], allow_duplicates=True)
    sales.insert(13, 'OrderYear', [int(i.year) for i in sales["OrderDate"]], allow_duplicates=True)
    sales.insert(14, 'Profits', [float(float(quan) * ((float(price.replace(",", "")) * (1-float(disc))) - float(cost.replace(",", "")))) for [quan, cost, price, disc] in zip(sales["Order Quantity"],sales["Unit Cost"], sales["Unit Price"], sales["Discount Applied"])])

    #sales.drop(sales[sales['OrderYear'] == 2018].index, inplace = True)

    #figure out late shipments by warehouse (step 1-4 done in preprocessing)
    #step 1: read in data
    #step 2: convert into date time format
    #step 3: find the value of date difference in days
    #step 4: insert into data
    #step 5: find average of each warehouse and compare them
    #step 6: find top performers and bottom performers

    #I want to do this only on the last month of data
    warehouses = sales.WarehouseCode.unique()
    warehousedata = []
    averages = ['AverageDaysToShip']
    medians = ['MedianDaysToShip']
    maxs = ['MaxDaysToShip']
    mins = ['MinDaysToShip']

    for warehouse in warehouses :
        warehousevals = sales[sales['WarehouseCode'] == warehouse]
        numwarehouse = len(warehousevals)
        days = pd.DataFrame(warehousevals['DaysToShip'])# pd.DataFrame([int(x[:2]) for x in warehousevals['DaysToShip']])
        sumdays = days.sum() #need to sum all shippingdays where warehousecode = warehouse then divide by num of warehouses with shipping code
        average = sumdays/numwarehouse
        warehousedata.append([warehouse, average[0].round(2), days.median()[0], days.max()[0], days.min()[0]])
        averages.append(average[0])
        medians.append(days.median()[0])
        maxs.append(days.max()[0])
        mins.append(days.min()[0])

    #warehousedata2 = [averages, medians, maxs, mins]

    #print(pd.DataFrame(warehousedata2, columns=[' '] + list(warehouses)))
    warehousedata = pd.DataFrame(warehousedata, columns=['WarehouseCode', 'AverageDaysToShip', 'MedianDaysToShip', 'MaxDaysToShip', 'MinDaysToShip'])
    ax1.bar(warehousedata['WarehouseCode'], warehousedata['AverageDaysToShip'], label='Warehouse Code')
    ax1.set_ylabel("Average Days to Ship Order")
    ax1.set_title("Average of Days to Ship by Warehouse")
    
    
    #the numbers are very similar, maybe check to see from month to month how this changes. This also tells us its not a warehouse specific issue. It may be best reevaluate how
    #we get orders ready. Whether this time is reasonable or not. Maybe its fine.
    
    sales.sort_values('OrderMonth', inplace = True)

    months = [x + 1 for x in range(12)]
    monthlywarehouse = sales[['DaysToShip', 'OrderMonth']].groupby(['OrderMonth']).mean().reset_index()
    #print(monthlywarehouse)



    X = months
    
    X_axis = np.arange(1, 13, 1) 

    #ax2.plot(X, monthlywarehouse['DaysToShip'])
    #ax2.set_xticks(np.arange(len(X_axis)+1))

    ax2_twin = ax2.twinx()
    ax2_twin.plot(X, monthlywarehouse['DaysToShip'], color = 'red')
    ax2_twin.scatter(X, monthlywarehouse['DaysToShip'], color = 'red')
    ax2_twin.spines['right'].set_color('red')
    ax2_twin.set_ylabel('Average Days to Ship')

    ax2.set_xticks(np.arange(len(X_axis)+1))

    #add trendline to plot
    '''
    i = 0.1
    for ware in warehouses :
        y = monthlywarehouse[(monthlywarehouse['WarehouseCode'] == ware)]['DaysToShip']
        z = np.polyfit(X, y, 4)
        p = np.poly1d(z)
        ax2.plot(X, y, label = ware)
        #ax2.plot(X, p(X))
        #ax1.plot(X_axis-(.5) + i, monthlywarehouse[(monthlywarehouse['WarehouseCode'] == y)]['DaysToShip'], 0.1, label = y)
        i = i + 0.1

    ax2.set_xlabel("Month") 
    ax2.set_ylabel("Average Days to Ship Order") 
    ax2.set_title("Monthly Average of Days to Ship by Warehouse") 
    ax2.legend(fontsize = 6)
    
    '''

    #expected sales based on time
    #step 2: Break down the data by year
        #read in the data
        #we can grab all the dates and check to see which years we have data for
        #loop through the years
        #create new df for each year
        #sum sales for that year
    '''
    yearlysales = sales[['Order Quantity', 'OrderYear']].groupby(['OrderYear']).sum().reset_index()
    print(yearlysales)

    ax3.scatter(yearlysales['OrderYear'], yearlysales['Order Quantity'], label="Profits Year to Year (2018-2020)")
    ax3.set_xticks(list(yearlysales['OrderYear']))
    ax3.set_xlabel("Year")
    ax3.set_ylabel("Profits in $")
    ax3.set_title("Profits in $ From 2018-2020 (2018 missing data for first 5 months)")
    ''' #this stuff just doesn't seem useful due to the missing data


    #step 3: find sales by month
        #we can loop through each year, loop through each month
        # and find total sales
        # then we have monthly sales for each month in each year 

    #print([(quan, cost, price, disc) for [quan, cost, price, disc] in zip(sales["Order Quantity"],sales["Unit Cost"], sales["Unit Price"], sales["Discount Applied"]) if float(float(quan) * ((float(price.replace(",", "")) * (1-float(disc))) - float(cost.replace(",", "")))) < 0])
    
    monthlyyearlysales = sales[['OrderMonth', 'OrderYear', 'Order Quantity']].groupby(['OrderMonth', 'OrderYear']).sum().reset_index()
    monthlyyearlysales.drop(monthlyyearlysales[monthlyyearlysales['Order Quantity'] < 100].index, inplace = True)
    ys = []
    for year in np.sort(monthlyyearlysales['OrderYear'].unique()) :
        y = monthlyyearlysales[(monthlyyearlysales['OrderYear'] == year)]['Order Quantity']
        z = np.polyfit(X[12-len(y):], y, 1)
        p = np.poly1d(z)
        #i = 12-len(y)
        j = 12-len(y) + 1
        while len(y) < 12 :
            #print(p(i))
            
            y = [int(p(j))] + list(y)
            #print(str(j) + " is " + str(int(p(j))))
            j = j - 1
            ys.append([j, 2018, p(j)])

    monthlyyearlysales = pd.concat([monthlyyearlysales, pd.DataFrame(ys, columns=['OrderMonth', 'OrderYear', 'Order Quantity'])], ignore_index=True)
    #print("--------------")
    #print(monthlyyearlysales)

    yearlysales = monthlyyearlysales [['OrderYear', 'Order Quantity']].groupby(['OrderYear']).sum().reset_index()
    #print(yearlysales)
    #ax2.plot(yearlysales['OrderYear'], yearlysales['Order Quantity'], label = "idk")

    #print("-----")
    #print(monthlyyearlysales.sort_values('OrderMonth'))   

    #ax3.scatter(np.sort(sales['OrderYear'].unique()), ys)

    monthlysales = sales[['OrderMonth', 'Order Quantity']].groupby(['OrderMonth']).sum().reset_index()
    monthlysales.drop(monthlysales[monthlysales['Order Quantity'] < 100].index, inplace = True)
    #print(monthlysales)

    ax2.plot(X, monthlysales['Order Quantity'], color = 'black')
    ax2.scatter(X, monthlysales['Order Quantity'], color = 'black')

    '''
    i = 0.3
    for year in np.sort(monthlyyearlysales['OrderYear'].unique()) :
        y = monthlyyearlysales[(monthlyyearlysales['OrderYear'] == year)]['Order Quantity']
        z = np.polyfit(X[12-len(y):], y, 1)
        p = np.poly1d(z)
        #i = 12-len(y)
        j = 12-len(y)
        while len(y) < 12 :
            #print(p(i))
            y = [int(p(j))] + list(y)
            print(str(j) + " is " + str(int(p(j))))
            j = j - 1
        
        #print(len(y))
        print(y)
        y = list(y)
        #ax4.bar(X, y, label = year)
        #ax4.plot(X, p(X))s
        ax4.bar(X_axis-(.465) + i, y, 0.33/2, label = str(year))
        i = i + (0.33/2)
    '''

    ax2.set_xlabel("Month") 
    ax2.set_ylabel("Total Number of Items Sold") 
    ax2.set_title("Monthly Sales Over 3 Years (data for months 1-5 2018 generated by best fit)") 
    ax2.legend(fontsize = 5)
    ax2.set_xticks(np.arange(len(X_axis)+1))

    


      


    #step 4: figure out which months have the highest sales,
    # but check against multiple years to make sure its a trend
        #this will come from graphing it, figure that out later


    #step 5: break this data into sales team, sales format, and store
        #we have sales for each month so we just need to sort by team
        #group by month, sales format
        #group by month, store
    #

    saleschannel = sales[['Sales Channel', 'Order Quantity', 'OrderMonth']]
    channels = sales['Sales Channel'].unique()
    saleschanneldata = saleschannel[['Sales Channel', 'Order Quantity']].groupby(['Sales Channel']).sum().reset_index()
    ax3.pie(saleschanneldata['Order Quantity'], labels = channels)
    ax3.set_title("Breakdown of Sales by Sales Channel")

    saleschannelmonthly = saleschannel.groupby(['Sales Channel', 'OrderMonth']).sum().reset_index()
    print(saleschannelmonthly)

    colors=['blue', 'red', 'green', 'orange']
    i = 0
    for channel in saleschannelmonthly['Sales Channel'].unique() :
        y = saleschannelmonthly[(saleschannelmonthly['Sales Channel'] == channel)]['Order Quantity']
        ax4.plot(X_axis, y, label = channel, color=colors[i])
        z = np.polyfit(X, y, 1)
        p = np.poly1d(z)
        ax4.plot(X, p(X), color=colors[i], linestyle='dashed')
        #ax1.plot(X_axis-(.5) + i, monthlywarehouse[(monthlywarehouse['WarehouseCode'] == y)]['DaysToShip'], 0.1, label = y)
        i = i + 1
    ax4.set_xticks(np.arange(len(X_axis)+1))
    ax4.legend()

    #look at unit cost changes over the years 

    #analyze the data from sales teams. analyze raw sales (not use item quantity), items sold, and, profits 

    salesteam = sales[['_SalesTeamID', 'Order Quantity', 'Unit Cost', 'Unit Price', 'Discount Applied']] #we can use these fields to find ^
    salesteamraw = salesteam[['_SalesTeamID', 'Order Quantity']].groupby('_SalesTeamID').count().reset_index()
    salesteamtotal = salesteam[['_SalesTeamID', 'Order Quantity']].groupby('_SalesTeamID').sum().reset_index()
    
    salesteamprofits = pd.DataFrame([(steam, round(float(float(quan) * ((float(price.replace(",", "")) * (1-float(disc))) - float(cost.replace(",", "")))), 2)) for [steam, quan, cost, price, disc] in zip(salesteam['_SalesTeamID'], salesteam["Order Quantity"],salesteam["Unit Cost"], salesteam["Unit Price"], salesteam["Discount Applied"])], columns=['SalesTeam', 'Profits']).groupby('SalesTeam').sum().reset_index()
    
    
    print("-------------------------")
    print(salesteam)
    print(salesteamraw.sort_values('Order Quantity', ascending=False))
    print(salesteamtotal.sort_values('Order Quantity', ascending=False))
    print(salesteamprofits.sort_values('Profits', ascending=False))

    
    fig.tight_layout()
    plt.show() 


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