import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pgeocode
import plotly.graph_objects as go
from decimal import Decimal
import seaborn as sns
import folium as fl
import io
from PIL import Image
import branca.colormap as cm

def fit_dat_and_plot(x, y, deg, label="", label_plot=False, log=False):

    # fits an arbitrary degree polynomial and then plots it
    if deg == "linear":
        deg = 1
    if deg == "quadratic":
        deg = 2
    
    if log:
        y = np.log(y)

    coeff = np.polynomial.polynomial.Polynomial.fit(x, y, deg).convert().coef
    pred = np.zeros(y.shape)
    poly_str = '%.1E' % Decimal(coeff[0])
    for i in range(deg + 1):
        pred += coeff[i] * (x ** i)
        if i > 0:
            poly_str = '%.1E' % Decimal(coeff[i]) +"x^" +str(i) +" + "  + poly_str

    if log:
        pred = np.exp(pred)

    if label_plot:
        plt.plot(x, pred, label=str(deg) + " degree polynomial best fit -- " + label, linewidth=6) 
    else: 
        plt.plot(x, pred, linewidth=9) 

    return coeff

# Creates a scatter plot as you'd expect with autogenerated title
def scatter_plot(x, y, texts=None, xlabel="", ylabel="", title=None, fit=None, label="", show=True, color="palegreen", log=False, label_fit=True, alpha=0.1, fontsize=None):

    dat = pd.DataFrame()
    dat['x'] = x
    dat['y'] = y
    dat = dat.dropna(axis=0)

    if fit is not None:
        dat = dat.sort_values("x")
        max_x = max(dat["x"])
        # dat["x"] /= max_x
        if type(fit) is int:
            fit = [fit]
        for deg in fit:
                fit_dat_and_plot(dat["x"].values, dat["y"].values, deg, label, label_plot=label_fit, log=log)

    plt.scatter(dat['x'], dat['y'], color=color, alpha=alpha, label=label)

    if texts is not None:
        # add labels to all points
        for (label, xi, yi) in zip(texts, x, y):
            plt.text(xi, yi*1.01, label, va='top', ha='center')

    if show:
        plt.xlabel(xlabel,fontsize=fontsize)
        plt.ylabel(ylabel,fontsize=fontsize)
        plt.legend()
        if title is None:
            plt.title(ylabel + " versus " + xlabel, fontsize=fontsize)
        else:
            plt.title(title, fontsize=fontsize)
        plt.show()

def q_binning(vals, key, q=4, legible_label="Value"):

    cutoffs = np.append(np.quantile(vals, np.arange(0,1,1/q)), np.max(vals))
    percentiles = np.round(np.arange(0,1+1/q,1/q), 2)
    bins = []
    for i in range(len(cutoffs) - 1):
        bins.append((key, (cutoffs[i], cutoffs[i+1]), legible_label + " in " + str(percentiles[i]) + " to " + str(percentiles[i+1]) + " percentile", None))

    return bins


def complex_scatter(combined_df, x, y, xlabel, ylabel, fit=[1], title=None, bins=[], masks=[], show=True, states=None, legend=True, fontsize=None):
    '''
    Inputs:
        Cenus_df : DataFrame object of all saved census data
        Solar_df : DataFrame object of all saved Proj Sunroof data
        x : The x axis for the plot (will be a col of either census or solar)
        y : Ditto but for the y axis
        bins: A list of tuples with (key:str, range:tuple, label:str, color:str)
            - key wil denote which col we are binning on, range will determine the range that we will mask the data for
            - label will be a label for plotting, color will be the color for the scatter plot
    '''


    keys = combined_df.keys()

    for (key, range, label, color) in bins:
        low, high = range
        if key in keys:
            mask1 = (low <= combined_df[key]) 
            df = combined_df[mask1] 
            mask2 = (df[key] < high)
            scatter_plot(x=x[mask1][mask2], y=y[mask1][mask2], fit=fit, show=False, label=label, color=color, label_fit=False,fontsize=fontsize)
        else:
            print("Key error in Complex Scatter on key:", key, " -- not a valid key for census or solar, skipping")

    for (mask, label, color) in masks:
        scatter_plot(x=x[mask], y=y[mask], fit=fit, show=False, label=label, color=color, label_fit=False,fontsize=fontsize)
        
    if show:
        plt.xlabel(xlabel, fontsize=fontsize)
        plt.ylabel(ylabel, fontsize=fontsize)
        if legend:
            plt.legend(fontsize=fontsize/2)
        if title is None:
            plt.title(ylabel + " versus " + xlabel, fontsize=fontsize)
        else:
            plt.title(title, fontsize=fontsize)
        plt.show()

# Creates a US map plot of the dat, edf should be provided, but if it isn't then it will be created as necessary using the zipcodes provided
def geo_plot(dat, color_scale, title, edf=None, zipcodes=None):

    # This should basically never get called since we define edf below, but if you were to import this you'd have to make sure zipcodes are provided to create the edf
    if edf is None:
        if zipcodes is None:
            print("invalid Geo Plotting, you must include an EDF or zipcode list")
            return -1
        else:
            nomi = pgeocode.Nominatim('us')
            edf = pd.DataFrame()
            edf['Latitude'] = (nomi.query_postal_code(zipcodes).latitude)
            edf['Longitude'] = (nomi.query_postal_code(zipcodes).longitude)
            edf['zip_code'] = zipcodes

    # For scaling of the bar, we do 15 ticks over the range of the data
    dat_range = max(dat) - min(dat)
    edf['dat'] = dat
    clean_dat = edf.dropna(axis=0)

    fig = go.Figure(data=go.Scattergeo(
            lon = clean_dat['Longitude'],
            lat = clean_dat['Latitude'],
            mode = 'markers',
            marker = dict(
            color = clean_dat['dat'],
            colorscale = color_scale,
            reversescale = True,
            opacity = 0.6,
            size = 20,
            colorbar = dict(
                titleside = "right",
                outlinecolor = "rgba(68, 68, 68, 0)",
                ticks = "outside",
                showticksuffix = "last",
                dtick = dat_range/15
            )
            )))

    fig.update_layout(
            title = title,
            geo_scope='usa',
            font=dict(
            family="Courier New, monospace",
            size=36,
            color="RebeccaPurple",
        )
        )
    fig.show()

def state_bar_plot(energy_gen_df, states=['Texas', 'Massachusetts', "California", 'New York', "US Total"], keys=['Clean', 'Bioenergy', 'Coal','Gas','Fossil','Solar','Hydro','Nuclear'], ylabel="Proportion of energy generation", title="Energy Generation Proportions by state", sort_by=None,stack=True,legend_loc="auto",fontsize=None):

    if states is not None:
        # Removes all states besides those in the 'states' list
        energy_gen_df = energy_gen_df[energy_gen_df['State'].isin(states)]
        
    # Drop Total Generation so it doesn't plot
    df =  energy_gen_df[keys + ['State code']]

    if sort_by is not None:
        df = df.sort_values(sort_by)

    if states is None:
        df = pd.concat([df[:5], df[-5:]])

    # removing the _prop part of the column names
    sources = df.columns
    df.columns = ["".join(x.split("_prop")) for x in sources]

    # sns.barplot(data=energy_gen_df,x= 'State')

    #set seaborn plotting aesthetics
    sns.set(style='white')

    #create stacked bar chart
    ax = df.set_index('State code').plot(kind='bar', stacked=stack, fontsize=fontsize)
    ax.set_xticklabels(df['State code'], rotation='horizontal') 

    if legend_loc == 'right':
        # Shrink current axis by 20%
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

        # Put a legend to the right of the current axis
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=fontsize/2)

    plt.xlabel("")
    plt.ylabel(ylabel)
    plt.title(title, fontsize=fontsize)
    plt.show()

def plot_state_map(stats_df, key, fill_color="BuPu", zoom=4.8, location=[38,-96.5], legend_name=None):

    url = (
        "https://raw.githubusercontent.com/python-visualization/folium/main/examples/data"
    )
    state_geo = f"{url}/us-states.json"

    m = fl.Map(location, zoom_start=zoom, zoom_control=False)

    if legend_name is None:
        legend_name = key

    fl.Choropleth(geo_data=state_geo, data=stats_df,
    columns=['State code', key],key_on='feature.id', fill_color=fill_color, line_weight=1, fill_opacity=0.7, line_opacity=.5,legend_name=legend_name).add_to(m)

    img_data = m._to_png(5)
    img = Image.open(io.BytesIO(img_data))
    img.save("Maps/" + key + '_by_state.png')
    img.show()

    # m.show_in_browser()

def bar_plot_demo_split(df, demos, key, type="avg value", stacked=False, xticks=None, title=None, ylabel=None, annotate=True):
    true_avg = np.mean(df[key].values)

    plt.style.use('fivethirtyeight')

    new_df = pd.DataFrame()
    low_avgs = []
    high_avgs = []
    
    for demo in demos:
        median = np.median(df[demo].values)
        low_avg = np.mean(df[df[demo] < median][key].values)
        high_avg = np.mean(df[df[demo] >= median][key].values)

        if type == "percent":
            low_avg = (low_avg/true_avg) - 1
            high_avg = (high_avg/true_avg) -1
        if type == "diff":
            low_avg = true_avg - low_avg
            high_avg = true_avg - high_avg

        low_avgs.append(low_avg)
        high_avgs.append(high_avg)
    
    new_df['demographic'] = demos
    new_df['Below median'] = low_avgs
    new_df['Above median'] = high_avgs


    ax = new_df.set_index('demographic').plot(kind='bar', stacked=stacked)

    if annotate:
        for p in ax.patches:
            ax.annotate(str(np.round(p.get_height(), 3)), (p.get_x() + p.get_width()/7 - ((p.get_height() < 0) * 0.01) , p.get_height() / 2 ))

    if type == "percent":
        true_avg = 0
    if type == "diff":
        true_avg = 0

    plt.axhline(y=true_avg, color='r', linestyle='--', label="National Average")
    plt.xlabel("")
    if title is not None:
        plt.title(title)
    else:
        plt.title("demographic relationship to " + key + " by " + type)
    if ylabel is not None:
        plt.ylabel(ylabel)
    else:
        plt.ylabel(key)
    if xticks is not None:
        ax.set_xticklabels(xticks, rotation='horizontal')    
    plt.show()




def plot_state_stats(stats_df, key, states=None, sort_by='mean'):

    if states is not None:
        # Removes all states besides those in the 'states' list
        stats_df = stats_df[stats_df['state_name'].isin(states)]

    stats_df = stats_df.sort_values(sort_by)

    if states is None:
        stats_df = pd.concat([stats_df[:5], stats_df[-5:]])

    stats_df.set_index('State code').plot(kind='bar', stacked=False)

    plt.ylabel(key)

    title_add = ""
    if key in ['solar_utilization', 'carbon_offset_metric_tons','existing_install_count']:
        title_add = " per capita"


    plt.title("States sorted by "+ sort_by +" of "+ key+ title_add +" -- (bottom and top 5)")
    plt.legend()
    plt.show()





