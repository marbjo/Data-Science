#Do something with scraped data

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main():
    #fields = ['']
    df = pd.read_csv('houses.csv', skipinitialspace=True)
    
    col_names = df.columns
    print(col_names)

    sz = df['Size(in m^2)'].astype(float)

    df['Price(in NOK)'] = df['Price(in NOK)'].str.normalize('NFKD') #Normalize unicode character
    df['Price(in NOK)'] = df['Price(in NOK)'].str.replace(' ','') #remove white space
    
    price = df['Price(in NOK)'].astype(float)

    plt.style.use('seaborn-dark')
    params = {'legend.fontsize': '20',
         'figure.figsize': (15, 5),
         'axes.labelsize': '20',
         'axes.titlesize': '20',
         'xtick.labelsize':'20',
         'ytick.labelsize':'20'}
    plt.rcParams.update(params)

    scaling = 1e6 #Millions

    plt.scatter(sz,price/scaling, label='Data', color = 'blue')
    plt.xlabel(col_names[2])
    plt.ylabel('Price (in millions NOK)')
    plt.title('Prices versus size for ' + str(len(sz)) + ' house listings from Finn.no')

    #Converting from Panda series to numpy array
    sz = sz.to_numpy()
    price = price.to_numpy() 

    sz = sz[~np.isnan(sz)] #Removing NaNs from array (mainly for polyfit)
    price = price[~np.isnan(price)]

    m,b = np.polyfit(sz,price,1)

    fit = (m*sz + b)/scaling
    name = 'Best fit = {:.1f}'.format(m+b)
    plt.plot(sz,fit, label=name, color='red')
    plt.legend()

    plt.show()


if __name__ == "__main__":
    main()