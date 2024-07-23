from plot_util import *
from data_load_util import *

scl = [0,"rgb(150,0,90)"],[0.125,"rgb(0, 0, 200)"],[0.25,"rgb(0, 25, 255)"],\
[0.375,"rgb(0, 152, 255)"],[0.5,"rgb(44, 255, 150)"],[0.625,"rgb(151, 255, 0)"],\
[0.75,"rgb(255, 234, 0)"],[0.875,"rgb(255, 111, 0)"],[1,"rgb(255, 0, 0)"]

Hot_color_scale = ["rgb(255, 0, 0)","rgb(255, 111, 0)","rgb(255, 234, 0)","rgb(151, 255, 0)","rgb(44, 255, 150)","rgb(0, 152, 255)","rgb(0, 25, 255)","rgb(0, 0, 200)","rgb(150,0,90)"]
scl =["rgb(150,0,90)","rgb(0, 0, 200)","rgb(0, 25, 255)","rgb(0, 152, 255)","rgb(44, 255, 150)","rgb(151, 255, 0)","rgb(255, 234, 0)","rgb(255, 111, 0)","rgb(255, 0, 0)"]

# color scales : "hot", "deep", 'rainbow'    ## Add _r to reverse

'''
Full list of color scales:
'aggrnyl', 'agsunset', 'algae', 'amp', 'armyrose', 'balance',
'blackbody', 'bluered', 'blues', 'blugrn', 'bluyl', 'brbg',
'brwnyl', 'bugn', 'bupu', 'burg', 'burgyl', 'cividis', 'curl',
'darkmint', 'deep', 'delta', 'dense', 'earth', 'edge', 'electric',
'emrld', 'fall', 'geyser', 'gnbu', 'gray', 'greens', 'greys',
'haline', 'hot', 'hsv', 'ice', 'icefire', 'inferno', 'jet',
'magenta', 'magma', 'matter', 'mint', 'mrybm', 'mygbm', 'oranges',
'orrd', 'oryel', 'oxy', 'peach', 'phase', 'picnic', 'pinkyl',
'piyg', 'plasma', 'plotly3', 'portland', 'prgn', 'pubu', 'pubugn',
'puor', 'purd', 'purp', 'purples', 'purpor', 'rainbow', 'rdbu',
'rdgy', 'rdpu', 'rdylbu', 'rdylgn', 'redor', 'reds', 'solar',
'spectral', 'speed', 'sunset', 'sunsetdark', 'teal', 'tealgrn',
'turbo', 'twilight', 'viridis', 'ylgn', 'ylgnbu', 'ylorbr',
'ylorrd'
'''

zip_codes, solar_df, census_df, pos_df = load_data()

combined_df = pd.concat([solar_df, census_df, pos_df], axis=1)

print("Removing Outliers")

# Remove outliers for carbon offset (4 outliers in this case)
# mask = combined_df['carbon_offset_metric_tons'] < 50 * ( combined_df['Total_Population'])
# combined_df = combined_df[mask]

# # Removing outliers for existing install counts (~90)
# mask = combined_df['existing_installs_count'] < 600
# combined_df = combined_df[mask]

# mask = combined_df['existing_installs_count'] > 0
# combined_df = combined_df[mask]

# mask = combined_df['count_qualified'] > 0
# combined_df = combined_df[mask]

# mask = combined_df['state_name'] != 'California'
# combined_df = combined_df[mask]

print("zips after removing outliers:", len(combined_df))

# Current working metric of "solar utilization", should be ~ current carbon offset
combined_df['solar_utilization'] = (combined_df['existing_installs_count'] / combined_df['number_of_panels_total']) * combined_df['carbon_offset_metric_tons']
combined_df['panel_utilization'] = (combined_df['existing_installs_count'] / combined_df['number_of_panels_total'])
combined_df['existing_installs_count_per_capita'] = (combined_df['existing_installs_count'] / combined_df['Total_Population'])

combined_df['carbon_offset_metric_tons_per_panel'] = (combined_df['carbon_offset_metric_tons'] / (combined_df['number_of_panels_total'] - combined_df['existing_installs_count'] ) )
combined_df['carbon_offset_metric_tons_per_capita'] = combined_df['carbon_offset_metric_tons']/ combined_df['Total_Population']

asian_prop = (combined_df['asian_population'].values / combined_df['Total_Population'].values)
white_prop = (combined_df['white_population'].values / combined_df['Total_Population'].values)
black_prop = (combined_df['black_population'].values / combined_df['Total_Population'].values)

combined_df['asian_prop'] = asian_prop 
combined_df['white_prop'] = white_prop 
combined_df['black_prop'] = black_prop

combined_df['percent_below_poverty_line'] = combined_df['households_below_poverty_line'] / combined_df['total_households']

pop_bins_quartile = q_binning(combined_df['Total_Population'].values, 'Total_Population', q=4, legible_label="Population")
white_prop_bins_quartile = q_binning(combined_df['white_prop'].values, 'white_prop', q=4, legible_label="White Proportion")
asain_prop_bins_quartile = q_binning(combined_df['asian_prop'].values, 'asian_prop', q=4, legible_label="Asian Proportion")
black_prop_bins_med = q_binning(combined_df['black_prop'].values, 'black_prop', q=2, legible_label="Black Proportion")
black_prop_bins_quartile = q_binning(combined_df['black_prop'].values, 'black_prop', q=4, legible_label="Black Proportion")
income_bins_quartile = q_binning(combined_df['Median_income'].values, 'Median_income', q=4, legible_label="Median Income")

# combined_df.to_csv('Clean_Data/data_by_zip.csv')

# Increase Font size
font = {'family' : 'DejaVu Sans',
    'weight' : 'bold',
    'size'   : 35}

matplotlib.rc('font', **font)


# mask = combined_df['existing_installs_count_per_capita'] < 0.06
# combined_df = combined_df[mask]

state_df = load_state_data(combined_df, load=True)

# bar_plot_demo_split(state_df, demos=["black_prop", "Median_income", "Republican_prop"], key="carbon_offset_metric_tons")
# bar_plot_demo_split(state_df, demos=["black_prop", "Median_income", "Republican_prop"], key="existing_installs_count_per_capita")
# bar_plot_demo_split(state_df, demos=["black_prop", "white_prop", "asian_prop", "Median_income", "Republican_prop"], key="carbon_offset_metric_tons_per_capita", type="percent", stacked=True, xticks=['Black', 'White','Asian', 'Median income', 'Republican'], ylabel="Carbon Offset Per Capita (Percent above average)", title="")
# bar_plot_demo_split(state_df, demos=["black_prop", "white_prop", "asian_prop", "Median_income", "Republican_prop"], key="existing_installs_count_per_capita", type="percent", stacked=True,  xticks=['Black', 'White','Asian', 'Median income', 'Republican'], ylabel="Existing Installs Per Capita (Percent above average)", title="")
# bar_plot_demo_split(state_df, demos=["black_prop", "white_prop", "asian_prop", "Median_income", "Republican_prop"], key="panel_utilization", type="percent", stacked=True,  xticks=['Black', 'White','Asian', 'Median income', 'Republican'], ylabel="Panel Utilization (Percent above average)", title="")
# bar_plot_demo_split(state_df, demos=["black_prop", "Median_income", "Republican_prop"], key="carbon_offset_metric_tons", type="diff")
# bar_plot_demo_split(state_df, demos=["black_prop", "Median_income", "Republican_prop"], key="existing_installs_count_per_capita",type="diff")

# bar_plot_demo_split(state_df, demos=["black_prop", "white_prop", "Median_income", "yearly_sunlight_kwh_kw_threshold_avg", "Republican_prop"], xticks=['Black', 'White', 'Median income', 'Yeary Sunlight', 'Republican'], key="carbon_offset_metric_tons_per_panel", type="percent", stacked=True, ylabel="", title="Carbon Offset Per Panel vs National Average")
# bar_plot_demo_split(state_df, demos=["black_prop", "white_prop","Median_income", "yearly_sunlight_kwh_kw_threshold_avg", "Republican_prop"], key="panel_utilization", xticks=['Black', 'White','Median income', 'Yeary Sunlight', 'Republican'] , type="percent", stacked=True, ylabel="", title="Panel Utilization vs National Average")

# quit()

# for key in ['carbon_offset_metric_tons_per_panel', 'carbon_offset_metric_tons']:
    # state_stats = stats_for_states(combined_df, key)
    # plot_state_stats(state_df, states=None, key=key, sort_by='std')

# log_solar_pot = np.log((solar_df['solar_potential_per_capita'].values + 0.001))
# log_solar_util = np.log((solar_df['solar_potential_per_capita'].values * solar_df['existing_installs_count']) + 0.001)

# geo_plot(log_solar_pot,'hot', "log solar potential per capita", pos_df)
# geo_plot(census_df['Median_income'], 'mint', "Median income", pos_df)
# geo_plot(log_solar_util,'hot', "log solar utilization", pos_df)
# geo_plot(np.log(asian_prop),'rainbow', "Log Asian Population Proportion", pos_df)
# geo_plot(white_prop,'rainbow', "Log White Population Proportion", pos_df)
# geo_plot(np.log(black_prop),'rainbow', "Log Black Population Proportion", pos_df)
# geo_plot(np.log((combined_df['carbon_offset_metric_tons']/ combined_df['Total_Population'].values) + 0.001) ,'rainbow', "Log Carbon offset per capita", pos_df)
# geo_plot(combined_df['percent_covered'] ,'rainbow', "Carbon offset", pos_df)
# geo_plot(combined_df['existing_installs_count'] ,'rainbow', "Existing Install count", pos_df)


# Xs = [(asian_prop, "Proportional of people which are asian"), (white_prop, "Proportional of people which are white"), (black_prop, "Proportional of people which are black"), (census_df['Median_income'].values, "Median Income")]
# Ys = [(np.log(solar_df['solar_potential_per_capita'].values), "Log Solar Potential Per Capita"), ((solar_df['carbon_offset_metric_tons']/ census_df['Total_Population'].values), "Carbon Offset if all panels built (metric tons) per capita")]

# for x, xname in Xs:
#     for y, yname in Ys:
#         scatter_plot(x, y, xlabel=xname, ylabel=yname, fit=[1,5,10])

# for key in ['carbon_offset_metric_tons_per_panel', 'Median_income', 'solar_potential_per_capita', 'solar_utilization', 'panel_utilization']:

# # Example Geo Plot (map of us)
# geo_plot(combined_df['carbon_offset_metric_tons_per_panel'] ,'rainbow', "Carbon offset per panel", pos_df)
# geo_plot(combined_df['existing_installs_count'] ,'rainbow', "Existing Installs", pos_df)
# geo_plot(combined_df['number_of_panels_total'] ,'rainbow', "Panel Total", pos_df)
# geo_plot(combined_df['panel_utilization'] ,'rainbow', "Panel Util", pos_df)
# geo_plot(np.log(combined_df['solar_potential_per_capita']) ,'rainbow', "Log Solar potential per capita", pos_df)

#### MAIN PLOTS FOR PAPER ############

print("Plotting")

##### INTRO PLOTS #########

# Demonstrates there is an issue of panel locations
# states = ['California']
# combined_df = combined_df[combined_df['state_name'].isin(states)]
# scatter_plot(x=np.log(combined_df['carbon_offset_metric_tons']), y=np.log(combined_df['existing_installs_count']), xlabel="Log Potential carbon offset", ylabel="Log Existing Panel Count", title=None, fit=[1,2], log=False, color="red")
# co_bins_quartile = q_binning(combined_df['carbon_offset_metric_tons'].values, 'carbon_offset_metric_tons', q=2, legible_label="Carbon Offset" )
# co_per_bins_quartile = q_binning(combined_df['carbon_offset_metric_tons_per_panel'].values, 'carbon_offset_metric_tons_per_panel',q=4, legible_label="Carbon Offset Per Panel")
# complex_scatter(combined_df=combined_df, x=combined_df['carbon_offset_metric_tons'], y=combined_df['existing_installs_count'], xlabel="Potential carbon offset (Metric Tons)", ylabel="Existing Installed Panels", title=None, bins=co_bins_quartile, fit=[2], legend=True)
# scatter_plot(x=combined_df['carbon_offset_metric_tons_per_panel'], y=combined_df['existing_installs_count_per_capita'], xlabel="Potential carbon offset per panel", ylabel="Existing Panel Count Per Capita", title=None, fit=[2], log=False, color="red")

# Shows where we should put panels
# geo_plot(np.log(combined_df['carbon_offset_metric_tons'] * combined_df['existing_installs_count']) ,'rainbow', "Carbon offset Per Capita", pos_df)

#######################################

##### EXEMPLAR STATE CHOOSING #######

# Exemplar states carbon offset to demo why we picked them


# state_energy_df = load_state_energy_dat(keys=['Clean','Fossil','Solar', 'Bioenergy', 'Coal','Gas','Hydro','Nuclear','Wind', 'Other Renewables', 'Other Fossil', 'Total Generation'], load=True)
# for key in ['carbon_offset_metric_tons_per_panel', 'carbon_offset_metric_tons']:
#     state_stats = pd.concat([stats_for_states(combined_df, key),state_energy_df['State code']])
#     plot_state_stats(state_stats, states=None, key=key, sort_by='mean')
# energy_gen_bar_plot(state_energy_df,states=None, keys=['Clean_prop','Fossil_prop'], sort_by="Clean_prop")

# # state_energy_df = load_state_energy_dat(keys=['Solar', 'Bioenergy', 'Coal','Gas','Hydro','Nuclear','Wind', 'Other Renewables', 'Other Fossil', 'Total Generation'], load=False)
# energy_gen_bar_plot(state_energy_df,states=None, keys=['Solar_prop', 'Bioenergy_prop', 'Coal_prop','Gas_prop','Hydro_prop','Nuclear_prop','Wind_prop', 'Other Renewables_prop', 'Other Fossil_prop'], sort_by="Solar_prop")

exemplar_states = ['Texas', 'California', 'Mississippi', 'Delaware', 'Massachusetts', 'US Total']
# exemplar_states = ['California', 'Florida', 'Vermont', 'Texas']

##################################################


# Exemplar states carbon offset to demo why we picked them
# for key in ['carbon_offset_metric_tons_per_panel', 'existing_installs_count_per_capita', 'Median_income']:
#     state_bar_plot(state_df, states=exemplar_states, keys=[key], ylabel=key, title="By state stats")

# state_bar_plot(state_df, states=exemplar_states, keys=['carbon_offset_metric_tons_per_panel', 'existing_installs_count_per_capita', 'Median_income'], sort_by='carbon_offset_metric_tons_per_panel', ylabel=key, title="By state stats")

no_dc = state_df['State code'].isin(["DC", "HI"])

state_df_no_dc = state_df[~no_dc]

# plot_state_map(state_df, key='carbon_offset_metric_tons_per_panel', fill_color='OrRd', legend_name="Carbon Offset Per Panel")
# plot_state_map(state_df, key='Fossil_prop')
# plot_state_map(state_df[no_dc], key='Democrat_prop')
# plot_state_map(state_df_no_dc, key='panel_utilization', fill_color='OrRd', legend_name="Panel Utilization")
# plot_state_map(state_df, key='Republican_prop', legend_name="Republican Voter Proportion")
# plot_state_map(state_df, key='Median_income', legend_name="Median Income") 
# plot_state_map(state_df, key='black_prop', legend_name="Black Population Proportion")
# plot_state_map(state_df, key='white_prop')  
# plot_state_map(state_df, key='carbon_offset_metric_tons')
# plot_state_map(state_df[no_dc], key='existing_installs_count')
# plot_state_map(state_df, key='yearly_sunlight_kwh_kw_threshold_avg', legend_name="Yearly Average Sunlight")
# plot_state_map(state_df, key='Clean_prop', legend_name="Clean Energy Gen Proportion")
# plot_state_map(state_df, key='Solar_prop')

# Supporting plots (shows energy generation Splits)
# state_bar_plot(state_df,states=exemplar_states, keys=['Clean_prop','Fossil_prop'], sort_by="Clean_prop")
# energy_gen_bar_plot(state_energy_df,states=exemplar_states, keys=['Solar_prop', 'Bioenergy_prop', 'Coal_prop','Gas_prop','Hydro_prop','Nuclear_prop','Wind_prop', 'Other Renewables_prop', 'Other Fossil_prop'], sort_by="Solar_prop")


################# END OF VERY IMPORTANT PLOTS ######################################################3

# Scatter Plot exmple

# scatter_plot(x=combined_df['households_below_poverty_line'].values, y=np.log(combined_df['panel_utilization']), xlabel="Percent below poverty line", ylabel="panel utilization", title=None,fit=[1])
# scatter_plot(x=combined_df['black_prop'], y=combined_df['panel_utilization'], xlabel="Black proportion of pop", ylabel='Existing installs', fit=[1])
# scatter_plot(x=combined_df['black_prop'], y=combined_df['carbon_offset_metric_tons'], xlabel="Black proportion of pop", ylabel='Carbon Offset (metric tons)', fit=[1])


exem_state_df = state_df[state_df['State'].isin(exemplar_states)]

# for df in [state_df, exem_state_df]:
#     scatter_plot(x=df['Republican_prop'], y=df['carbon_offset_metric_tons'],xlabel="Preportion republican voter", ylabel='Carbon offset (metric tons) per capita', title="Republican preportion vs Carbon offset" ,fit=[1],color="blue", alpha=1)
#     scatter_plot(x=df['Republican_prop'], y=df['existing_installs_count'], xlabel="Preportion republican voter", ylabel='Existing install count', fit=[1],color="blue",alpha=1)
#     scatter_plot(x=df['Median_income'], y=df['carbon_offset_metric_tons'],xlabel="Median income", ylabel='Carbon offset (metric tons) per capita', title="Median income vs Carbon offset" ,fit=[1],color="blue", alpha=1)
#     scatter_plot(x=df['Median_income'], y=df['existing_installs_count'], xlabel="Median income", ylabel='Existing install count', fit=[1],color="blue",alpha=1)
#     scatter_plot(x=df['black_prop'], y=df['carbon_offset_metric_tons'],xlabel="Black population preportion", ylabel='Carbon offset (metric tons) per capita', title="Black preportion vs Carbon offset" ,fit=[1],color="blue", alpha=1)
#     scatter_plot(x=df['black_prop'], y=df['existing_installs_count'], xlabel="Black population preportion", ylabel='Existing install count', fit=[1],color="blue",alpha=1)



# scatter_plot(x=combined_df['carbon_offset_metric_tons_per_capita'], y=np.log(combined_df['Median_income']), xlabel="Carbon Offset per capita", ylabel='Log Median Income', fit=[2])
# scatter_plot(x=combined_df['households_below_poverty_line'], y=np.log(combined_df['Median_income']), xlabel="Households below poverty line", ylabel='Log Median Income', fit=[2])


# Complex scatter plot example with separation for total pop and racial proportions separated by quartiles:
# This section just sets up the bins for each



# carbon_offset_outlier_removal = [('carbon_offset_metric_tons_per_capita', (0.01, 200), "carbon offset per capita below 200 and above 0", 'blue')]

# Because we want to run over each one of these binnings we concat them
bins_list = [pop_bins_quartile, white_prop_bins_quartile, asain_prop_bins_quartile, black_prop_bins_quartile, income_bins_quartile, co_bins_quartile]

bins_list = [black_prop_bins_quartile]


# Then run them together (fit here is 1 giving a linear fit)
# for bins in bins_list:
#     complex_scatter(combined_df=combined_df, x=combined_df['carbon_offset_metric_tons'], y=combined_df['existing_installs_count_per_capita'], xlabel="Potential carbon offset (Metric Tons)", ylabel="Existing Installed Panels", title=None, bins=bins, fit=[2])
#     complex_scatter(combined_df=combined_df, x=combined_df['Median_income'], y=combined_df['existing_installs_count'], xlabel="Median Income", ylabel="Existing Installed Panels", title=None, bins=bins, fit=[2])
#     # complex_scatter(combined_df=combined_df, x=combined_df['percent_below_poverty_line'].values, y=combined_df['panel_utilization'], xlabel="Percent below poverty line", ylabel="panel utilization", title=None, bins= bins, fit=[4])
#     # complex_scatter(combined_df=combined_df, x=combined_df['percent_below_poverty_line'].values, y=combined_df['carbon_offset_metric_tons_per_panel'].values, xlabel="Percent below pverty line", ylabel="Carbon offset per panel", title=None, bins=bins, fit=[4])
#     complex_scatter(combined_df=combined_df, x=combined_df['carbon_offset_metric_tons_per_panel'], y=combined_df['existing_installs_count_per_capita'], xlabel="Potential carbon offset (Metric Tons) per panel", ylabel="Existing Installed Panels", title=None, bins=bins, fit=[2], legend=True)