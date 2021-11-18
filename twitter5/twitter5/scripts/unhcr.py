
import pandas as pd

import matplotlib.pyplot as plt

class Unhcr:
    
    def exploration(self):    
        df = pd.read_csv("files/csvs/population.csv", header=13)
    
        df = df.drop(columns=['Country of origin', 'Country of origin (ISO)', 'Venezuelans displaced abroad'])
    
        labels = ['year', 
                  'country_of_asylum', 
                  'country_of_asylum_ISO', 
                  'refugees', 
                  'asylum_seekers', 
                  'IDPs', 
                  'stateless',
                  'others']
    
        df.columns = labels
    
        print(df.head(5))
    
        print('Number of rows and columns:',df.shape)
        print('Name of the features:\n', df.columns)
        print(df.info())
    
        print('\nStatistical info:\n', df.drop(columns=['year', 'country_of_asylum', 'country_of_asylum_ISO']).describe())
    
        # Top 10 countries of destination
        df_2 = df.query("country_of_asylum != 'Pakistan' and country_of_asylum != 'Iran (Islamic Rep. of)'")
        sums = df_2.groupby(['country_of_asylum'])[['refugees']].aggregate('sum')
    
        top_10_countries_of_asylum = sums.refugees.sort_values(ascending=False)[:10]
        chart = top_10_countries_of_asylum.plot.barh(
            figsize = [16, 8], 
            fontsize = 14, 
            title = 'Top 10 Countries of asylum (2006-2020)', 
            color = 'blue')
        chart.set_ylabel('')
        chart.show()

        def select_country(country):
            return df.query("country_of_asylum == {}").format(country)
    
        italy = df.query("country_of_asylum == 'Italy'")
        pakistan = df.query("country_of_asylum == 'Pakistan'")
        uk = df.query("country_of_asylum == 'United Kingdom of Great Britain and Northern Ireland'")
        sweden = df.query("country_of_asylum == 'Sweden'")
        austria = df.query("country_of_asylum == 'Austria'")
        australia = df.query("country_of_asylum == 'Australia'")
        netherlands = df.query("country_of_asylum == 'Netherlands'")
        india = df.query("country_of_asylum == 'India'")
        germany = df.query("country_of_asylum == 'Germany'")
        iran = df.query("country_of_asylum == 'Iran (Islamic Rep. of)'")
    
    
    
        fig = plt.figure(figsize=(12,8))
        ax = plt.axes()
    
        plt.plot(germany.year, germany.refugees, label = 'Germany')
        plt.plot(sweden.year, sweden.refugees, label = 'Sweden')
        plt.plot(italy.year, italy.refugees, label = 'Italy')
        plt.plot(uk.year, uk.refugees, label = 'UK')
        plt.plot(austria.year, austria.refugees, label = 'Austria')
        plt.plot(australia.year, australia.refugees, label = 'Australia')
        plt.plot(netherlands.year, netherlands.refugees, label = 'Netherlands')
        plt.plot(india.year, india.refugees, label = 'India')
        plt.plot(iran.year, iran.refugees, label = 'Iran')
        plt.plot(pakistan.year, pakistan.refugees, label = 'Pakistan')
    
    
        plt.title("Refugees times series by country (2006-2020)")
        ax.legend(frameon=False)
    
        #Lets see the top 8
        fig = plt.figure(figsize=(12,8))
        ax = plt.axes()
    
    
        plt.plot(sweden.year, sweden.refugees, label = 'Sweden')
        plt.plot(italy.year, italy.refugees, label = 'Italy')
        plt.plot(uk.year, uk.refugees, label = 'UK')
        plt.plot(austria.year, austria.refugees, label = 'Austria')
        plt.plot(australia.year, australia.refugees, label = 'Australia')
        plt.plot(netherlands.year, netherlands.refugees, label = 'Netherlands')
        plt.plot(india.year, india.refugees, label = 'India')
    
        plt.title("Refugees times series by country (2006-2020) without Pakistan, Iran and Germany")
        ax.legend(frameon=False)
