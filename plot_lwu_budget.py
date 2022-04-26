import matplotlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

matplotlib.use('Agg')

from pywfm import IWFMBudget

def date_to_water_year(month, year):
    if month > 9:
        return int(year + 1)
    else:
        return int(year)

if __name__ == '__main__':


    lwu_budget_file = '../Results/C2VSimFG_L&WU_Budget.hdf'
    
    with IWFMBudget(lwu_budget_file) as bud:
        locations = bud.get_location_names()
        for i, l in enumerate(locations, start=1):
            df = bud.get_values(
                i,
                area_conversion_factor=1/43560,
                area_units='Acres',
                volume_conversion_factor=1/43560,
                volume_units='AF'
            )
    
            df['Month'] = df['Time'].dt.month
            df['Year'] = df['Time'].dt.year
    
            df['WY'] = df.apply(lambda row: date_to_water_year(row['Month'], row['Year']), axis=1)

            df.drop(labels=['Month', 'Year'], axis=1, inplace=True)

            df_annual = df.groupby('WY').sum()

            width = 0.35
            x = np.arange(len(df_annual))
            
            fig, (ax1, ax3) = plt.subplots(nrows=2, ncols=1, figsize=(11,17))
            ax1.bar(
                x - width/2, 
                df_annual['Ag. Deliveries'], 
                width, 
                color='#8FAADC', 
                label='Ag. Delivery (Supply)'
            )
            
            ax1.bar(
                x - width/2, 
                df_annual['Ag. Pumping'], 
                width,
                bottom=df_annual['Ag. Deliveries'],
                color='#BFBFBF', 
                label='Ag. Pumping (Supply)'
            )
            
            ax2 = ax1.twinx()
            ax2.plot(x, df_annual['Ag. Shortage'], 'r--', label='Ag. Shortage')
            ax2.set_ylabel("Shortage (AF)")
            
            ax1.bar(
                x + width/2, 
                df_annual['Ag. Supply Requirement'], 
                width, 
                color='#A9D18E', 
                label='Ag. Supply Requirement (Demand)'
            )
            ax1.set_xticks(x, df_annual.index)
            for label in ax1.get_xticklabels():
                label.set_rotation(90)
                
            ax1.grid()
            box = ax1.get_position()
            ax1.set_position([box.x0, box.y0 + 0.2 * box.height, box.width, box.height * 0.8])
            
            # Put a legend below the current axis
            ax1.legend(loc='lower center', ncol=4, fontsize=8, bbox_to_anchor=(0.5, -0.25), frameon=False)
            
            ax1.set_ylabel('Annual Volume (AF)')
            ax1.set_xlabel('Water Year')
            ax1.set_title("Agricultural Land and Water Use Budget\nfor Subregion {}".format(10))
            
            ax3.bar(
                x - width/2, 
                df_annual['Urban Deliveries'], 
                width, 
                color='#8FAADC', 
                label='Urban Delivery (Supply)'
            )
            
            ax3.bar(
                x - width/2, 
                df_annual['Urban Pumping'], 
                width,
                bottom=df_annual['Urban Deliveries'],
                color='#BFBFBF', 
                label='Urban Pumping (Supply)'
            )
            
            ax4 = ax3.twinx()
            ax4.plot(x, df_annual['Urban Shortage'], 'r--', label='Urban Shortage')
            
            ax3.bar(
                x + width/2, 
                df_annual['Urban Supply Requirement'], 
                width, 
                color='#A9D18E', 
                label='Urban Supply Requirement (Demand)'
            )
            ax3.set_xticks(x, df_annual.index)
            for label in ax3.get_xticklabels():
                label.set_rotation(90)
                
            ax3.grid()
            box = ax3.get_position()
            ax3.set_position([box.x0, box.y0 + 0.2 * box.height, box.width, box.height * 0.8])
            
            # Put a legend below the current axis
            ax3.legend(loc='lower center', ncol=4, fontsize=8, bbox_to_anchor=(0.5, -0.25), frameon=False)
            
            ax3.set_ylabel('Annual Volume (AF)')
            ax3.set_xlabel('Water Year')
            ax3.set_title('Urban Land and Water Use Budget\nfor Subregion {}'.format(10))
            plt.savefig('SR{}_LWU_alt.png'.format(l))
            plt.close()
            