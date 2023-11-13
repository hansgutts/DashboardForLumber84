import pandas as pd
import matplotlib as plt
import numpy as np
import datetime
import seaborn as sns
import matplotlib.pyplot as plt

def main() :
    #get the sales data
    sales = pd.read_csv("US_Regional_Sales_Data_PreProcessed_To_Use.csv", sep=',')
    sales.drop(['Unnamed: 0'], axis=1, inplace=True) #drop the extra index column that got added to the data
    print(sales)

    #get the # of days to ship from the string DaysToShip
    sales['DaysToShip'] = [int(x[:2]) for x in sales['DaysToShip']]
    
    #sales['OrderDate'] = [datetime.datetime.strptime(d, "%Y/%m/%d") for d in sales['OrderDate']] #get the orderdate in datetime format

    #insert new data we will use for ananlysis
    sales.insert(12, 'OrderMonth', [int(i[5:7]) for i in sales["OrderDate"]], allow_duplicates=True)
    sales.insert(13, 'OrderYear', [int(i[0:4]) for i in sales["OrderDate"]], allow_duplicates=True)
    sales.insert(14, 'Profits', [float(float(quan) * ((float(price) * (1-float(disc))) - float(cost))) for [quan, cost, price, disc] in zip(sales["Order Quantity"],sales["Unit Cost"], sales["Unit Price"], sales["Discount Applied"])])
    #sales['Unit Cost'] = [float(unitcost.replace(',', '')) for unitcost in sales['Unit Cost']]
    sales.sort_values('OrderMonth', inplace = True)
    sales = sales.drop(sales[(sales['OrderMonth'] == 5) & (sales['OrderYear'] == 2018)].index)

    #get sales by month and year
    monthlyyearlysales = sales[['OrderMonth', 'OrderYear', 'Order Quantity']].groupby(['OrderMonth', 'OrderYear']).sum().reset_index()
    monthlyyearlysales.drop(monthlyyearlysales[monthlyyearlysales['Order Quantity'] < 100].index, inplace = True)  #if we sold less than 100 in a month, its not accurate
                                                                                                                   #month 5 2018 in particular is not well recorded
    #get an array of months for X axis
    months = [x + 1 for x in range(12)]
    X = months
    X_axis = np.arange(1, 13, 1) 

    #create a new plot most recent 6 month warehouse delivery averages 
    plt.figure()

    warehouses = sales.WarehouseCode.unique()
    warehousedata = []
    averages = ['AverageDaysToShip'] #average is about the same
    medians = ['MedianDaysToShip']   #the median value is about the same
    maxs = ['MaxDaysToShip']         #max of 28 for all (not valuable)
    mins = ['MinDaysToShip']         #min of 28 for all (not valuable)

    for warehouse in warehouses :
        warehousevals = sales[(sales['WarehouseCode'] == warehouse) & (sales['OrderYear'] == 2020) & (sales['OrderMonth'] >= 6)]
        numwarehouse = len(warehousevals)
        days = pd.DataFrame(warehousevals['DaysToShip'])# pd.DataFrame([int(x[:2]) for x in warehousevals['DaysToShip']])
        sumdays = days.sum() #need to sum all shippingdays where warehousecode = warehouse then divide by num of warehouses with shipping code
        average = sumdays/numwarehouse
        warehousedata.append([warehouse, average[0].round(2), days.median()[0], days.max()[0], days.min()[0]])
        averages.append(average[0])
        medians.append(days.median()[0])
        maxs.append(days.max()[0])
        mins.append(days.min()[0])

    

    #get the data from above and create a new dataframe to work with
    warehousedata = pd.DataFrame(warehousedata, columns=['WarehouseCode', 'AverageDaysToShip', 'MedianDaysToShip', 'MaxDaysToShip', 'MinDaysToShip'])

    #make bar graph of the warehouse code and average days to ship
    plt.bar(warehousedata['WarehouseCode'], warehousedata['AverageDaysToShip']) 
    plt.ylabel("Average Days to Ship Order")
    plt.xlabel("Warehouse Code")
    plt.title("Last 6 Months Average of Days to Ship by Warehouse")
    





    #do all time shipping
    plt.figure()

    warehousedata = []
    for warehouse in warehouses :
        warehousevals = sales[(sales['WarehouseCode'] == warehouse)]
        numwarehouse = len(warehousevals)
        days = pd.DataFrame(warehousevals['DaysToShip'])# pd.DataFrame([int(x[:2]) for x in warehousevals['DaysToShip']])
        sumdays = days.sum() #need to sum all shippingdays where warehousecode = warehouse then divide by num of warehouses with shipping code
        average = sumdays/numwarehouse
        warehousedata.append([warehouse, average[0].round(2), days.median()[0], days.max()[0], days.min()[0]]) #this data is returned in an array, so get it out
        averages.append(average[0]) #didn't end up using this data. wasn't very telling of much
        medians.append(days.median()[0])
        maxs.append(days.max()[0])
        mins.append(days.min()[0])

    #get the data from above and create a new dataframe to work with
    warehousedata = pd.DataFrame(warehousedata, columns=['WarehouseCode', 'AverageDaysToShip', 'MedianDaysToShip', 'MaxDaysToShip', 'MinDaysToShip'])

    plt.bar(warehousedata['WarehouseCode'], warehousedata['AverageDaysToShip']) 
    plt.ylabel("Average Days to Ship Order")
    plt.xlabel("Warehouse Code")
    plt.title("Average of Days to Ship by Warehouse (All time)")


    #Here I want to plot the relationship between shipping delay and number of orders

    #plot monthly sales
    monthlywarehouse = sales[['DaysToShip', 'OrderMonth']].groupby(['OrderMonth']).mean().reset_index() #break down warehouse delivery delays by month and year
    monthlysales = sales[['OrderYear', 'OrderMonth', 'Order Quantity']].groupby(['OrderMonth', 'OrderYear']).sum().reset_index() #count number of items sold
    monthlysales = monthlysales[['OrderMonth', 'Order Quantity']].groupby(['OrderMonth']).mean().reset_index() #take the average over the years

    plt.figure() #create new plot

    plt.plot(X, monthlysales['Order Quantity'], color = 'black')
    plt.scatter(X, monthlysales['Order Quantity'], color = 'black')

    plt.xlabel("Month") 
    plt.ylabel("Total Number of Items Sold") 
    plt.title("Monthly Sales and Average Days to Ship Over 3 Years (data for months 1-5 2018 not recorded)") 
    plt.legend(fontsize = 5)
    plt.xticks(np.arange(len(X_axis)+1))

    #plot warehouse shipping times
    ax2_twin = plt.twinx()
    ax2_twin.plot(X, monthlywarehouse['DaysToShip'], color = 'red')
    ax2_twin.scatter(X, monthlywarehouse['DaysToShip'], color = 'red')
    ax2_twin.spines['right'].set_color('red')
    ax2_twin.set_ylabel('Average Days to Ship')
    plt.xticks(np.arange(len(X_axis)+1))
    


    #Plot our profits over the three years (see growth or stagnation)

    #do over months, three different lines (three years)
    plt.figure()   
    monthlyyearly = sales[['OrderYear', 'OrderMonth', 'Order Quantity']].groupby(['OrderYear', 'OrderMonth']).sum().reset_index()

    for year in [2018, 2019, 2020] :
        df = monthlyyearly[monthlyyearly['OrderYear'] == year]
        if len(df) != 12 :
            plt.plot(X[12-len(df):], df['Order Quantity'], label=year)
            plt.scatter(X[12-len(df):], df['Order Quantity'])
        else :
            plt.plot(X, df['Order Quantity'], label=year)
            plt.scatter(X, df['Order Quantity'])
    
    plt.xticks(np.arange(len(X_axis) + 1))
    plt.xlabel("Month")
    plt.ylabel("Order Quantity")
    plt.legend()
    plt.title("Order Quantity From 2018-2020 (2018 missing data for first 5 months)")


    #Figure out what channels account for the most sales
    #then figure out year to year
    saleschannel = sales[['Sales Channel', 'Order Quantity', 'OrderMonth', 'OrderYear']]
    saleschanneldata = saleschannel.groupby(['Sales Channel', 'OrderYear']).sum().reset_index()
    channels = sales['Sales Channel'].unique()

    plt.figure()
    plt.title('Breakdown of Sales Channel in 2018')
    plt.pie(saleschanneldata[saleschanneldata['OrderYear'] == 2018]['Order Quantity'], labels = channels, autopct='%1.1f%%')
    

    plt.figure()
    plt.title('Breakdown of Sales Channel in 2019')
    plt.pie(saleschanneldata[saleschanneldata['OrderYear'] == 2019]['Order Quantity'], labels = channels, autopct='%1.1f%%')
    
    plt.figure()
    plt.title('Breakdown of Sales Channel in 2020')
    plt.pie(saleschanneldata[saleschanneldata['OrderYear'] == 2020]['Order Quantity'], labels = channels, autopct='%1.1f%%')

    
    
    saleschanneldata = saleschannel[['Sales Channel', 'Order Quantity']].groupby(['Sales Channel']).sum().reset_index()


    plt.figure()
    plt.pie(saleschanneldata['Order Quantity'], labels = channels, autopct='%1.1f%%')
    plt.title("Breakdown of Sales by Sales Channel (all time)")


    plt.figure()

    saleschannelmonthly = saleschannel.groupby(['Sales Channel', 'OrderMonth', 'OrderYear']).sum().reset_index()
    saleschannelmonthly = saleschannelmonthly.groupby(['Sales Channel', 'OrderMonth']).mean().reset_index()

    colors=['blue', 'red', 'green', 'orange']
    i = 0
    for channel in saleschannelmonthly['Sales Channel'].unique() :
        y = saleschannelmonthly[(saleschannelmonthly['Sales Channel'] == channel)]['Order Quantity']
        plt.plot(X_axis, y, label = channel, color=colors[i])
        z = np.polyfit(X, y, 1)
        p = np.poly1d(z)
        plt.plot(X, p(X), color=colors[i], linestyle='dashed')
        #ax1.plot(X_axis-(.5) + i, monthlywarehouse[(monthlywarehouse['WarehouseCode'] == y)]['DaysToShip'], 0.1, label = y)
        i = i + 1
    plt.xticks(np.arange(len(X_axis)+1))
    plt.title("Monthly Sales for Each Sales Channel")
    plt.legend()

    #look at unit cost changes over the years 
    #Plot our unit costs over the three years

    #do over months, three different lines (three years)
    plt.figure()   
    monthlyyearlyunit = sales[['OrderYear', 'OrderMonth', 'Unit Cost']].groupby(['OrderYear', 'OrderMonth']).mean().reset_index()
    for year in [2018, 2019, 2020] :
        df = monthlyyearlyunit[monthlyyearlyunit['OrderYear'] == year]
        if len(df) != 12 :
            plt.plot(X[12-len(df):], df['Unit Cost'], label=year)
            plt.scatter(X[12-len(df):], df['Unit Cost'])
        else :
            plt.plot(X, df['Unit Cost'], label=year)
            plt.scatter(X, df['Unit Cost'])
    
    plt.xticks(np.arange(len(X_axis) + 1))
    plt.xlabel("Month")
    plt.ylabel("Unit Cost in $")
    plt.legend()
    plt.title("Unit Cost Month to Month in $ From 2018-2020 (2018 missing data for first 5 months)")

    #plot average of all three years
    plt.figure()   
    yearlyunit = monthlyyearlyunit.groupby(['OrderMonth']).mean().reset_index()
    plt.plot(X, yearlyunit['Unit Cost'])
    plt.scatter(X, yearlyunit['Unit Cost'])
    
    plt.xticks(np.arange(len(X_axis) + 1))
    plt.xlabel("Month")
    plt.ylabel("Unit Cost in $")
    plt.legend()
    plt.title("Average Unit Cost Month to Month in $")

    #Compare unit costs to sales trends

    #do over months, three different lines (three years)
    monthlyyearly = sales[['OrderYear', 'OrderMonth', 'Order Quantity']].groupby(['OrderYear', 'OrderMonth']).sum().reset_index()

    #I want to compare unit costs and sales quantity year by year month by month
    #do years on seperate graphs to make it more readable

    for year in [2018, 2019, 2020] :
        plt.figure()
        plt.title("Unit Costs and Quantity of Items Sold in " + str(year))
        plt.xticks(np.arange(len(X_axis) + 1))
        plt.ylabel("AVG Unit Cost in $")
        plt.xlabel("Month")
        dfunit = monthlyyearlyunit[monthlyyearlyunit['OrderYear'] == year]
        dfquant = monthlyyearly[monthlyyearly['OrderYear'] == year]
        plt.plot(X[12-len(dfunit):], dfunit['Unit Cost'], color = 'black')
        plt.scatter(X[12-len(dfunit):], dfunit['Unit Cost'], color = 'black')
        ax = plt.twinx()
        ax.plot(X[12-len(dfunit):], dfquant['Order Quantity'], color = 'red')
        ax.scatter(X[12-len(dfunit):], dfquant['Order Quantity'], color = 'red')
        ax.set_xticks(np.arange(len(X_axis) + 1))
        ax.set_ylabel("Number of Items Ordered", color = 'red')
        ax.spines['right'].set_color('red')
        plt.legend()





    #analyze the data from sales teams. analyze raw sales (not use item quantity), items sold, and, profits 

    salesteam = sales[['_SalesTeamID', 'Order Quantity', 'Unit Cost', 'Unit Price', 'Discount Applied']] #we can use these fields to find ^
    salesteamraw = salesteam[['_SalesTeamID', 'Order Quantity']].groupby('_SalesTeamID').count().reset_index()
    salesteamtotal = salesteam[['_SalesTeamID', 'Order Quantity']].groupby('_SalesTeamID').sum().reset_index()
    
    salesteamprofits = pd.DataFrame([(steam, round(float(float(quan) * ((float(price) * (1-float(disc))) - float(cost))), 2)) for [steam, quan, cost, price, disc] in zip(salesteam['_SalesTeamID'], salesteam["Order Quantity"],salesteam["Unit Cost"], salesteam["Unit Price"], salesteam["Discount Applied"])], columns=['SalesTeam', 'Profits']).groupby('SalesTeam').sum().reset_index()

    salesteamraw.sort_values('Order Quantity', ascending=False, inplace=True)
    #not super helpful as a sale of 15 things is more valuable than a sale of 1

    salesteamtotal.sort_values('Order Quantity', ascending=False,  inplace=True)
    salesteamprofits.sort_values('Profits', ascending=False, inplace=True)

    plt.figure() #graph raw sales (even if quantity > 1, it counts as 1)
    plt.bar(np.arange(len(salesteamraw['_SalesTeamID'])), salesteamraw['Order Quantity'], label = salesteamraw['_SalesTeamID'])
    plt.xticks(np.arange(len(salesteamraw)), list(salesteamraw['_SalesTeamID']))
    plt.xlabel("Sales Team")
    plt.ylabel("Number of Sales")
    plt.title("Raw Sales by Sales Team")

    plt.figure() #graph total items sold by team
    plt.bar(np.arange(len(salesteamtotal['_SalesTeamID'])), salesteamtotal['Order Quantity'], label = salesteamtotal['_SalesTeamID'])
    plt.xticks(np.arange(len(salesteamtotal)), list(salesteamtotal['_SalesTeamID']))
    plt.xlabel("Sales Team")
    plt.ylabel("Number of Items Sold")
    plt.title("Quantity of Items Sold by Sales Team")


    plt.figure()
    plt.bar(np.arange(len(salesteamprofits['SalesTeam'])), salesteamprofits['Profits'], label = salesteamprofits['SalesTeam'])
    plt.xticks(np.arange(len(salesteamprofits)), list(salesteamprofits['SalesTeam']))
    plt.xlabel("Sales Team")
    plt.ylabel("Profits From Items Sold $")
    plt.title("Total Profits of Items Sold by Sales Team")

    plt.show() 


main()