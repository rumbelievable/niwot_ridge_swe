import matplotlib.pyplot as plt 
import folium
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import imageio

def create_folium_plot(loc=[40.047388, -105.599580], tiles='Stamen Terrain'):
    imap = folium.Map(loc, tiles, zoom_start=13)
    return imap

def add_site(imap, loc, tag, radius=150):

    '''
    Plot sites as circles on folium map.

    Parameters
    ----------
    imap : folium map
        Map to add to.
    loc : list
        Latitude and longitude of each site.
    tag : str
        Name of location.
    radius : int
        Size of circle marker.

    Returns
    -------
    New circle marker on folium map.
    '''
    color_dict = {'Saddle':'#E24A33','GL4':'#348ABD','GL5':'#988ED5','Navajo':'#777777','Martinelli':'#FBC15E',
            'Arikaree':'#8EBA42','Subnivean':'#FFB5B8','Albion':'#92C5DE','GL3':'#80CDC1','Tower Meadow':'#5E3C99',
            'Tower Tree Well':'#E66101','C1':'#F4A582','Soddie':'#B8E186'}
    folium.Circle(loc, radius, color=color_dict[tag], popup=tag).add_to(imap)

def add_black_site(imap, loc, tag, radius=125):
    '''
    Plot sites on folium map.

    Parameters
    ----------
    loc_name : list
        Names of sampling sites.
    lat_long : tuple
        Latitude and longitude of each site.

    Returns
    -------
    Folium map of sampling sites.
    '''
    folium.Circle(loc, radius, color='black', popup=tag, weight=10).add_to(imap)

def create_gif(files, gif_path_name, duration):
    '''
    Create gif from images.

    Parameters
    ----------
    files : list
        Filepath names of images.
    gif_path_name : str
        New filepath/name for returned gif.
    duration: int
        Delay on each image.

    Returns
    -------
    GIF 
    '''
    images = []
    for filename in files:
        images.append(imageio.imread(filename))
    images*10
    kwargs = { 'duration': 1 , 'loop': 20}
    imageio.mimsave(gif_path_name, images, 'GIF', **kwargs)



if __name__ == '__main__':

    ## Plot all sample sites and save html
    m = folium.Map(location=[40.0443, -105.5920],
                zoom_start=13,
                tiles='Stamen Terrain')
    m.add_child(folium.LatLngPopup())

    add_black_site(m, [40.05, -105.59], '<b>Saddle</b>')
    add_black_site(m, [40.047388, -105.599580], '<b>Albion</b>')
    add_black_site(m, (40.0558068932155, -105.61717784273749), '<b>GL4</b>')
    add_black_site(m, [40.0508, -105.630], '<b>GL5</b>')
    add_black_site(m, [40.052108, -105.635561], '<b>Navajo</b>')
    add_black_site(m, [40.05315986684726,-105.59667627824962], '<b>Martinelli</b>')
    add_black_site(m, [40.050791, -105.641416], '<b>Arikaree</b>')
    add_black_site(m, [40.054165, -105.588975], '<b>Subnivean</b>')
    add_black_site(m, [40.0512, -105.6128], '<b>GL3</b>')
    add_black_site(m, [40.052348, -105.583235], '<b>Tower Meadow</b>')
    add_black_site(m, [40.033371, -105.547389], '<b>Tower Tree Well</b>')
    add_black_site(m, [40.036162, -105.543529], '<b>C1</b>')
    add_black_site(m, [40.04, -105.57], '<b>Soddie</b>')

    lter = [(40.0595312337778, -105.54), (40.03, -105.645)]
    folium.vector_layers.Rectangle(
        bounds = lter,
        stroke=True,
        weight=5,
        opacity=1,
        color='black'
    ).add_to(m)
    m.save('lter_sites_black.html')

    ## Save screenshot of folium map
    # chrome_options = Options()
    # driver = webdriver.Chrome('/Users/annierumbles/Downloads/chromedriver')     
    # tmpurl = 'file:///Users/annierumbles/Desktop/Coding/galvanize/capstone_work/src/lter_sites.html'
    # driver.get(tmpurl)
    # delay = 5
    # time.sleep(delay)
    # driver.save_screenshot('lter_site.png')    
    # driver.quit()                                                                                                             
    
    filenames = ['s1.png','s2.png', 's3.png', 's4.png', 's5.png', 's6.png', 's7.png', 's7.png', 's8.png', 's9.png', 's10.png', 's11.png', 's12.png', 's13.png']
    create_gif(filenames,'/Users/annierumbles/Desktop/Coding/galvanize/capstone_work/images/sites_black_loop.gif', 1)
