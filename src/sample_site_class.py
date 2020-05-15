import pandas as pd
import numpy as np 

class SampleSite(object):
    def __init__(self, site_name, main_df):
        self.site_name = site_name
        self.main_df = main_df
        self.df = self._make_df()
        self.local_site_names = self._local_names()
        # self.site_location = site_location
        self.local_site_codes = self._site_codes()
        # self.mean = self._swe_mean()

    # def __repr__(self):
    #     return '{}'.format(self.site_name)

    # def __str__(self):
    #     return '{}'.format(self.site_name)

    def _make_df(self): 
        mask = self.main_df['local_site'] == self.site_name
        self.df = self.main_df[mask]
        self.df.reset_index(drop=True, inplace=True)
        return self.df

    def _local_names(self):
        self.local_site_names = list(self.df['samp_loc'].unique())
        return self.local_site_names 

    def _site_codes(self):
        self.local_site_codes = list(self.df['loc_code'].unique())
        return self.local_site_codes

    def total_mean_swe(self):
        self.mean = np.mean(self.df['swe'])
        return self.mean

    def yearly_mean_swe(self):
        dct = {}
        years = np.arange(1993, 2021, 1)
        for i in years:
            vals = []
            for j in range(0, len(self.df['date'])):
                if self.df['date'][j].year == i:
                    if self.df['swe'][j] == 'nan':
                        continue
                    else:
                        vals.append(self.df['swe'][j])
                dct[str(i)] = np.mean(vals)
        return dct

    def monthly_mean_swe(self):
        dct = {}
        months = np.arange(1, 13, 1)
        for mn in months:
            vals = []
            for j in range(0, len(self.df['date'])):
                if self.df['date'][j].month == mn:
                    vals.append(self.df['swe'][j])
                dct[str(mn)] = np.mean(vals)
        return dct

if __name__ == '__main__':
    df_swe = pd.read_csv('/Users/annierumbles/Desktop/Coding/galvanize/capstone_work/data/latest_knb-lter-nwt.96.16/snowateq.mw.data.16.csv')
    df_swe['date'] = pd.to_datetime(df_swe['date'])
    df_swe.dropna(axis=0, how='all', inplace=False)
    df_swe.dropna(axis=0, how='any', subset=['swe'], inplace=True)
    df_swe.sort_values(['date', 'local_site'], inplace=True)
    df_swe.reset_index(drop=True, inplace=True)

    # Making list of objects
    names = list(df_swe['local_site'].unique())
    # lowered = [n.lower() for n in names]
    objs = [SampleSite(i, df_swe) for i in names]
    # FIGURE OUT HOW TO AUTOMATE BELOW:
    saddle =objs[0] 
    gl4 = objs[1] 
    gl5 = objs[2] 
    navajo = objs[3] 
    martinelli = objs[4] 
    arikaree = objs[5] 
    subnivean = objs[6] 
    albion = objs[7] 
    gl3 = objs[8] 
    tower_meadow = objs[9] 
    tower_tree_hill = objs[10] 
    c1 = objs[11] 
    soddie = objs[12] 
    # obj_names = [saddle, gl4, gl5, navajo, martinelli, arikaree, subnivean, albion, gl3, tower_meadow, tower_tree_hill, c1, soddie, nan]




