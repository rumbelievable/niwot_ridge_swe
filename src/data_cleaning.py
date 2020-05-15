import numpy as np 
import pandas as pd 
import scipy.stats as stats
import matplotlib.pyplot as plt
from sample_site_class import SampleSite
plt.style.use('ggplot')

def import_csv_pd(filepath='/Users/annierumbles/Desktop/Coding/galvanize/capstone_work/data/latest_knb-lter-nwt.96.16/snowateq.mw.data.16.csv'):
    '''
    Import csv to pandas dataframe.

    Parameters
    ----------
    filepath: str
        Path to csv file
    
    Returns
    -------
    pandas dataframe
    '''
    df = pd.read_csv(filepath)
    return df

def clean_swe_df(filepath='/Users/annierumbles/Desktop/Coding/galvanize/capstone_work/data/latest_knb-lter-nwt.96.16/snowateq.mw.data.16.csv'):
    '''
    Clean snow water equivalent dataframe, drop nan values in swe column, sort by date then local_site.

    Parameters
    ----------
    filepath: str

    Returns
    -------
    Cleaned pandas dataframe
    '''
    df = import_csv_pd(filepath)
    df_swe = df.copy()
    df_swe['date'] = pd.to_datetime(df_swe['date'])
    df_swe.dropna(axis=0, how='all', inplace=False)
    df_swe.dropna(axis=0, how='any', subset=['swe'], inplace=True)
    df_swe.sort_values(['date', 'local_site'], inplace=True)
    df_swe.reset_index(drop=True, inplace=True)
    return df_swe

def get_names_for_objects(df=clean_swe_df()):
    '''
    Make list of local_site names to make objects out of.

    Parameters
    ----------
    df: dataframe (cleaned df_swe)

    Returns
    -------
    list of strings
    '''
    names = list(df['local_site'].unique())
    names.pop(-1)
    return names

def create_object_list(df=clean_swe_df()):
    '''
    Create SampleSite objects from local_site name list.

    Parameters
    ----------
    df: dataframe (cleaned df_swe)

    Returns
    -------
    List of objects
    '''
    names = get_names_for_objects(df)
    # new_names = [x.lower().replace(' ', '_') for x in names]
    return [SampleSite(i, df) for i in names]

def get_yearly_means_per_site(sample_object):
    '''
    Create dictionary of annual means for passed in SampleSite object.

    Parameters
    ----------
    sample_object: SampleSite object

    Returns
    -------
    Dictionary
    '''
    dct = {}
    years = np.arange(1993, 2021, 1)
    for i in years:
        vals = []
        for j in range(0, len(sample_object.df['date'])):
            if sample_object.df['date'][j].year == i:
                vals.append(sample_object.df['swe'][j])
            dct[str(i)] = np.mean(vals)
    return dct

def get_monthly_means(sample_object):
    '''
    Create dictionary of monthly means for passed in SampleSite object.

    Parameters
    ----------
    sample_object: SampleSite object

    Returns
    -------
    Dictionary
    '''
    dct = {}
    months = np.arange(1, 13, 1)
    for mn in months:
        vals = []
        for j in range(0, len(sample_object.df['date'])):
            if sample_object.df['date'][j].month == mn:
                vals.append(sample_object.df['swe'][j])
            dct[str(mn)] = np.mean(vals)
    return dct

def get_yearly_means_of_all_sites(df=clean_swe_df()):
    '''
    Create dictionary of yearly means for all sites.

    Parameters
    ----------
    df: cleaned pandas df

    Returns
    -------
    Dictionary
    '''
    dct = {}
    years = np.arange(1993, 2021, 1)
    for i in years:
        vals = []
        for j in range(0, len(df['date'])):
            if df['date'][j].year == i:
                vals.append(df['swe'][j])
            dct[str(i)] = np.mean(vals)
    return dct

def lin_regress(x, y):
    '''
    Perform linear regression.
    '''
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    return slope, intercept, r_value, p_value, std_err

## Plotting functions
def plot_yearly_mean_swe(mean_dicts):
    labels = ['Saddle','GL4','GL5','Navajo','Martinelli','Arikaree','Subnivean','Albion','GL3','Tower Meadow',
    'Tower Tree Well','C1','Soddie']
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_title('Average Yearly Snow Water Equivalent - All Sites', fontsize=20)
    ax.set_ylabel('SWE (m)', fontsize=20)
    ax.tick_params(labelsize='x-large')
    ax.set_prop_cycle('color',['#E24A33', '#348ABD', '#988ED5', '#777777', '#FBC15E', '#8EBA42', '#FFB5B8', '#92C5DE', '#80CDC1', '#5E3C99', '#E66101', '#F4A582', 'B8E186'])

    for i, dct in enumerate(mean_dicts):
        x = np.arange(1993, 2021, 1)
        y = [v for v in dct.values()]
        ax.plot(x, y, marker='o', mew=1, linewidth=.75, label=labels[i])
    ax.legend(labels, loc='upper right', bbox_to_anchor=(1.16,1), fontsize='medium')
    return fig

def plot_monthly_mean_swe(month_mean_dicts):
    labels = ['Saddle','GL4','GL5','Navajo','Martinelli','Arikaree','Subnivean','Albion','GL3','Tower Meadow',
    'Tower Tree Well','C1','Soddie']
    fig, ax = plt.subplots(figsize=(10,6))
    ax.set_title('Monthly Averages All Time', fontsize=20)
    ax.set_ylabel('SWE (m)', fontsize=20)
    ax.tick_params(labelsize='x-large')
    x = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July',
              'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
    ax.set_xticklabels(x, rotation=45)
    ax.set_prop_cycle('color',['#E24A33', '#348ABD', '#988ED5', '#777777', '#FBC15E', '#8EBA42', '#FFB5B8', '#92C5DE', '#80CDC1', '#5E3C99', '#E66101', '#F4A582', 'B8E186'])

    for i, dct in enumerate(month_mean_dicts):
        y = [v for v in dct.values()]
        ax.plot(x, y, marker='o', mew=1, linewidth=.75, label=str(labels[i]))
                
    ax.legend(labels, loc='upper right', bbox_to_anchor=(1.125,.8), ncol=2, fancybox=True, shadow=True)
    return fig

def plot_all_sites(object_list, name_list):
    fig, ax = plt.subplots(figsize=(12,6))
    ax.set_title('SWE Across All Sites')
    ax.set_ylabel('meters')
    # ax.legend(loc='best')
    for i in range(0, len(object_list)):
        x = object_list[i].df['date']
        y = object_list[i].df['swe']
        ax.plot(x,y,label=name_list[i])
    return fig

if __name__ == '__main__':

    df_swe = clean_swe_df()
    names = get_names_for_objects()
    snake_names = [x.lower().replace(' ', '_') for x in names]
    objects = create_object_list(df_swe)
    ## Assigning SampleSite objects to values
    saddle = objects[0] 
    gl4 = objects[1] 
    gl5 = objects[2] 
    navajo = objects[3] 
    martinelli = objects[4] 
    arikaree = objects[5] 
    subnivean = objects[6] 
    albion = objects[7] 
    gl3 = objects[8] 
    tower_meadow = objects[9] 
    tower_tree_hill = objects[10] 
    c1 = objects[11] 
    soddie = objects[12]
    objects = [saddle, gl4, gl5, navajo, martinelli, arikaree, subnivean, albion, gl3, tower_meadow, tower_tree_hill, c1, soddie]
    color_dict = {'Saddle':'#E24A33','GL4':'#348ABD','GL5':'#988ED5','Navajo':'#777777','Martinelli':'#FBC15E',
        'Arikaree':'#8EBA42','Subnivean':'#FFB5B8','Albion':'#92C5DE','GL3':'#80CDC1','Tower Meadow':'#5E3C99',
        'Tower Tree Well':'#E66101','C1':'#F4A582','Soddie':'#B8E186'}

    # Plot ALL points
    new_names = [x.lower().replace(' ', '_') for x in names]
    
    # plot_all_sites(objects, new_names)

    ## Get every mean per year per site
    saddle_means = saddle.yearly_mean_swe()
    gl4_means = gl4.yearly_mean_swe()
    gl5_means = gl5.yearly_mean_swe()
    navajo_means = navajo.yearly_mean_swe()
    martinelli_means = martinelli.yearly_mean_swe()
    arikaree_means = arikaree.yearly_mean_swe()
    subnivean_means = subnivean.yearly_mean_swe()
    albion_means = albion.yearly_mean_swe()
    gl3_means = gl3.yearly_mean_swe()
    tower_meadow_means = tower_meadow.yearly_mean_swe()
    tower_tree_hill_means = tower_tree_hill.yearly_mean_swe()
    c1_means = c1.yearly_mean_swe()
    soddie_means = soddie.yearly_mean_swe()

    ## Plot yearly means over all sites
    list_of_yearly_mean_dicts = [saddle_means, gl4_means, gl5_means, navajo_means, martinelli_means, arikaree_means,
                 subnivean_means, albion_means, gl3_means, tower_meadow_means, tower_tree_hill_means,
                 c1_means, soddie_means]
    fig = plot_yearly_mean_swe(list_of_yearly_mean_dicts)
    fig.tight_layout(pad=1)
    fig.savefig('average_yearly_swe_allsites80.png', dpi=80)

    # # Get linear regression for combined site means over all years
    # all_means = get_yearly_means_of_all_sites(df_swe)
    # x_all = np.arange(1993, 2020, 1)
    # y_all = [v for v in all_means.values()]
    # y_all.pop(-1) 
    # m, b, r_value, p_value, std_err = lin_regress(x_all, y_all)
    # ## Plot combined site means over all years
    # fig, ax = plt.subplots(figsize=(12,6))
    # ax.set_title('Average Yearly Snow Water Equivalent - Combined for All Sites', pad=15, fontsize=20)
    # ax.set_ylabel('SWE (m)', fontsize=20)

    # x = np.arange(1993, 2021, 1)
    # y = [v for v in all_means.values()]
    # ax.plot(x, y, c= '#3489eb',marker='o', mew=3, linewidth=1, label='Yearly Mean')
    # ax.plot(x_all, b + m*x_all, color='#E24A33', linewidth=1, label='p-value = .112')
    # ax.tick_params(labelsize='x-large')
    # ax.legend(loc='upper center', fancybox=True, shadow=True, fontsize='x-large', bbox_to_anchor=(.7, 1))
    # # plt.show()
    # fig.savefig('average_yearly_swe_combined80.png', dpi=80)

    # # Plot number of sample locations per site
    # capitalize_names = [name.capitalize() for name in names]
    # local_site_count_dct = {}
    # for i, obj in enumerate(objects):
    #     count = len(obj.local_site_names)
    #     local_site_count_dct[capitalize_names[i]] = count
    # sorted_dict = {k: v for k, v in sorted(local_site_count_dct.items(), key=lambda item: item[1])}
    # fig, ax = plt.subplots(figsize=(10,5))
    # x = [k for k in sorted_dict.keys()]
    # y = [v for v in sorted_dict.values()]
    # ax.barh(x, y, color='#3489eb')
    # ax.yaxis.grid(False)
    # ax.set_xticks(np.arange(1,22,1))
    # ax.set_title('Number of Sample Locations')

    # ## Plot monthly site means over all years
    # saddle_monthly = saddle.monthly_mean_swe()
    # gl4_monthly = gl4.monthly_mean_swe()
    # gl5_monthly = gl5.monthly_mean_swe()
    # navajo_monthly = navajo.monthly_mean_swe()
    # martinelli_monthly = martinelli.monthly_mean_swe()
    # arikaree_monthly = arikaree.monthly_mean_swe()
    # subnivean_monthly = subnivean.monthly_mean_swe()
    # albion_monthly = albion.monthly_mean_swe()
    # gl3_monthly = gl3.monthly_mean_swe()
    # tower_meadow_monthly = tower_meadow.monthly_mean_swe()
    # tower_tree_hill_monthly = tower_tree_hill.monthly_mean_swe()
    # c1_monthly = c1.monthly_mean_swe()
    # soddie_monthly = soddie.monthly_mean_swe()
    # month_dicts = [saddle_monthly, gl4_monthly, gl5_monthly, navajo_monthly, martinelli_monthly, arikaree_monthly,
    #              subnivean_monthly, albion_monthly, gl3_monthly, tower_meadow_monthly, tower_tree_hill_monthly,
    #              c1_monthly, soddie_monthly]
    # fig = plot_monthly_mean_swe(month_dicts)
    # fig.savefig('monthly_means80_8by4.png', dpi=80)
    

    # # Plot total samples per site
    # for i, obj in enumerate(objects):
    #     count = len(obj.df)
    #     local_site_count_dct[capitalize_names[i]] = count
    # sorted_totals = {k: v for k, v in sorted(local_site_count_dct.items(), key=lambda item: item[1])}
    # sorted_totals
    # fig, ax = plt.subplots(figsize=(10,6))
    # formal_names = ['Saddle','GL4','GL5','Navajo','Martinelli','Arikaree','Subnivean','Albion','GL3','Tower Meadow',
    #     'Tower Tree Well','C1','Soddie']
    # objects
    # x = [k for k in sorted_totals.keys()]
    # y = [v for v in sorted_totals.values()]
    # ax.barh(x, y, color='#3489eb')

    # ax.set_title('Total Samples per Site')
    # ax.set_xlabel('Number of Samples')
    # plt.show()

    # ## Plot site makeup (total samples and total sample locations)
    # fig, ax = plt.subplots(figsize=(8,6))
    # formal_names = ['Albion','GL3','Tower Tree Well','Tower Meadow','Soddie','Martinelli','Navajo','Arikaree','GL5','GL4',
    #     'C1','Subnivean','Saddle']
    # objects
    # x = [k for k in sorted_totals.keys()]
    # y = [v for v in sorted_totals.values()]
    # y_sample_sites = [v for v in sorted_dict.values()]
    # # ax.set_prop_cycle('color',['#E24A33', '#348ABD', '#988ED5', '#777777', '#FBC15E', '#8EBA42', '#FFB5B8', '#92C5DE', '#80CDC1', '#5E3C99', '#E66101', '#F4A582', 'B8E186'])
    # # #3489eb
    # ax.barh(x, y, color='#3489eb', label='Number of \nSamples')
    # ax.barh(x, y_sample_sites, color='#3fd9d4', label='Number of \nSample Locations')
    

    # ax.set_title('Sample Site Composition', pad=15, fontsize=20)
    # ax.set_xlabel('Count')
    # ax.set_yticklabels(formal_names, fontsize=14)
    # ax.tick_params(labelsize='x-large')
    # ax.legend(loc='center right', fontsize='x-large')
    # fig.tight_layout(pad=1)
    # # fig.savefig('sample_site_composition80_8by6.png', dpi=80)

    # ## Get all linear regressions
    # top_sites = [saddle_means, subnivean_means, c1_means, gl4_means, gl5_means, arikaree_means, navajo_means]
    # top_colors = [color_dict['Saddle'], color_dict['Subnivean'], color_dict['C1'], color_dict['GL4'],
    #           color_dict['GL5'], color_dict['Arikaree'],color_dict['Navajo']]
    # top_names = ['Saddle', 'Subnivean', 'C1', 'GL4', 'GL5', 'Arikaree', 'Navajo']
    # x = []
    # for k, v in top_sites[0].items():
    #     if str(v) != 'nan':
    #         x.append(int(k))
    #     else:
    #         pass
    # y = np.array([v for v in top_sites[0].values()])
    # y = y[~np.isnan(y)]
    # x = np.array(x)
    # m, b, r_value, p_value, std_err = lin_regress(x,y)
    # lin_regresses = [[-0.003906325102151978, 8.349419629869915, 0.5236700119739848], 
    #              [0.005574586252507653, -10.526383881925533, 0.2772141025494249],
    #             [0.0077428338572561595, -15.331905622614242, 0.11056127771258156],
    #             [0.0015959806359015206, -2.444305311472887, 0.6706143053095486],
    #             [-0.0034535183543882397, 7.72724589938305, 0.3316218041756759],
    #             [0.0024907513944714384, -4.228435453992933, 0.5281068861253063],
    #             [-0.0009094397769027527, 2.586988247942623, 0.8616436667990759]]
    # ## Plotting all linear regressions and averages
    # ## MAKE FUNCTIONS FOR THIS
    # fig, axs = plt.subplots(2,3,figsize=(12, 7),sharey=True, sharex=True)
    # x = np.arange(1993, 2021, 1)
    # i = 0
    # fig.suptitle('Average Yearly Snow Water Equivalent - Top 6', fontsize=20)

    # for ax in axs.flatten():
    #     y = [v for v in top_sites[i].values()]
    #     x_site = []
    #     for k, v in top_sites[i].items():
    #         if str(v) != 'nan':
    #             x_site.append(int(k))
    #         else:
    #             pass
    #     x_site=np.array(x_site)
    #     ax.scatter(x, y, color=top_colors[i])
    #     ax.plot(x_site, lin_regresses[i][1] + x_site*lin_regresses[i][0], c='black',
    #     label='p-value = {}'.format(str(round(lin_regresses[i][2],2))), linewidth=1)
    #     ax.set_title('{}'.format(top_names[i]), fontsize=18)
    #     ax.legend(loc='best', fontsize='medium')
    #     ax.tick_params(labelsize='large')
    #     i +=1
    # fig.text(0.06, 0.5, 'SWE (m)', ha='center', va='center', rotation='vertical', fontsize=18)
    # # fig.savefig('av?erage_yearly_swe_top6_12by7.png', dpi=80)





