import pandas
import datetime

#this reads in the dataset as a dataframe
salesdata = pandas.read_csv("US_Regional_Sales_Data_No_Mod.csv")

#this is the function I used to drop the rows I felt we did not need    
def DropRows(df) :
    if isinstance(df, pandas.DataFrame) :
        df = df.drop(['OrderNumber', 'DeliveryDate', 'CurrencyCode', '_ProductID', '_CustomerID'], axis=1) #remove the specified dimensions
        return df
    else :
        return -1 #if there was a previous error just send the error down the line

def ExportCSV(df) :
    if isinstance(df, pandas.DataFrame) : #if no errors (still in dataframe format)
        df.to_csv("US_Regional_Sales_Data_PreProcessed_To_Use.csv") #export to csv
    else :
        print("Error. Not exporting df.") #there was an error somewhere, we shouldn't send this to csv and lose old data

#I want to check to make sure that Unit Cost never exceeds Unit Price (o.w. we are selling at a loss)
def CheckCostvsPrice(df) :
    if isinstance(df, pandas.DataFrame) :
        unitcost = df.loc[:,'Unit Cost']  #grab all unit costs and prices
        unitprice = df.loc[:, 'Unit Price']
        newunitcost = []
        newunitprice = []
        if len(unitprice) == len(unitcost) : #make sure we have same amount of entries (something went wrong ow)
            for i in range(len(unitprice)) : #loop through all entries 
                cost = float(unitcost[i].replace(',', '')) #remove num formatting
                price = float(unitprice[i].replace(',', ''))
                newunitcost.append(cost) #make new list for cost and price
                newunitprice.append(price)
                if cost > price : #make sure we aren't selling something for less than we paid to make/get it
                    print("Unit cost greater than price at " + str(i)) #error message
                    print("Unit cost: " + str(unitcost[i]))
                    print("Unit price: " + str(unitprice[i]))
                    return -1 #return non dataframe so we know not to export csv
            df["Unit Cost"] = newunitcost #I actually dont think this is necesary
            df["Unit Price"] = newunitprice
        else :
            print("There is a value count mismatch")
            return -1 #return non dataframe so we know not to export csv
        return df
    else :
        return -1 #if there was a previous error just send the error down the line

def ConvertDates(df) : #change date fromat from eu to us (dd/mm/yyyy -> mm/dd/yyyy)
    if isinstance(df, pandas.DataFrame) :
        df['OrderDate'] = [datetime.datetime.strptime(d, "%d/%m/%y").strftime("%m/%d/%y") for d in df['OrderDate']]
        df['ShipDate'] = [datetime.datetime.strptime(d, "%d/%m/%y").strftime("%m/%d/%y") for d in df['ShipDate']]
        df['ProcuredDate'] = [datetime.datetime.strptime(d, "%d/%m/%y").strftime("%m/%d/%y") for d in df['ProcuredDate']]
        for date in df["OrderDate"] : #make sure each date column doesn't have a month exceeding 12 (indicates we succesfully converted them)
            if int(date[0:2]) > 12 :
                print("Error parsing order dates. Month exceeds 12")
                return -1 #return non dataframe so we know not to export csv
        for date in df["ShipDate"] :
            if int(date[0:2]) > 12 :
                print("Error parsing ship dates. Month exceeds 12")
                return -1 #return non dataframe so we know not to export csv
        for date in df["ProcuredDate"] :
            if int(date[0:2]) > 12 :
                print("Error parsing ship dates. Month exceeds 12")
                return -1 #return non dataframe so we know not to export csv
        df['OrderDate'] = pandas.to_datetime(df['OrderDate'])
        df['ShipDate'] = pandas.to_datetime(df['ShipDate'])
        df['DaysToShip'] = df[['ShipDate', 'OrderDate']].apply(lambda x : x[0] - x[1], axis=1) 
        for days in df["DaysToShip"] :
            if days <  pandas.to_timedelta(0, unit='D') or days >  pandas.to_timedelta(60, unit='D'):
                print("Error parsing days to ship. less than 0")
                return -1 #return non dataframe so we know not to export csv
        return df #everything worked, return modified dataframe
    else :
        return -1 #if there was a previous error just send the error down the line

#process the dataframe
salesdata.isnull().sum()

salesdata = DropRows(salesdata) 
salesdata = CheckCostvsPrice(salesdata)
salesdata = ConvertDates(salesdata)
ExportCSV(salesdata)