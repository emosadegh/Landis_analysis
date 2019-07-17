# -*- coding: utf-8 -*-
############################################################
# author: Ehsan Mosadegh
# usage: to analyze LANDIS data, spatial analysis
# date: June 07, 2019
# email: ehsan.mosadegh@gmail.com, ehsanm@dri.edu
# notes: to make spatial plots from LANDIS
############################################################
# import libraries

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import time
from netCDF4 import Dataset

#===========================================================
# get the starting time

start = time.time()

#===========================================================
# controlling options:

dpi_res= 300
# set the resolution of spatial plot
spatial_res= 'i' # 'l' , 'i' , 'f'
# set output format
plot_format='png'  # 'png' 'svg'
# select the domain
my_domain= 'zoomed_domain' # 'zoomed_domain' or 'cmaq_domain'
# save the plot or not?
save_plot= 'no'  # 'yes' or 'no'
# select scenario number
scenario_no = '1'
# fsize=9  # font-size
month_list = [ 'jul' , 'aug' , 'sep' , 'oct' , 'nov']

# define what type of spatial plot
spatial_plot_type='fires' # 'fires' or 'marker' or 'mesh'

mesh_type='sample_plot_of_study_region' # 'sample_mesh' or 'modeling_domain' or 'station_inside_cell' or 'stats_region' or 'sample_plot_of_study_region'

# for single scen/month plots
single_scen_per_month_plot = 'yes' 
save_plot_single_scen_per_month = 'yes'

plot_dir = '/Users/ehsan/Documents/Python_projects/USFS_fire/inputs/landis_inputs/plots/'

#===========================================================
# Basemap plot setting

zoomed_domain_zoomOut_scale_factor=10
cmaq_domain_zoomOut_scale_factor=1
mesh_domain_range= 50

### set the station location
stn_lon= -120
stn_lat= 39

### for a locatio
marker_lon=stn_lon		#-120.0324
marker_lat=stn_lat		#39.0968

### for statistics mesh
stats_region_ll_lon= -120.30 #-120.25
stats_region_ll_lat= 38.87 #38.87

### center of CMAQ domain
xcent_cmaq= -120.806 					# degrees, ref_lon from WPS namelist
ycent_cmaq= 38.45 							# degrees, ref_lat from WPS namelist

### center of my desired map== I like to set Lake Tahoe at the center
lon_of_desired_center=marker_lon		# center of the map; degrees
lat_of_desired_center=marker_lat		# center of the map; degrees

# # lower-left corner of desired map, which I set it based on CMAQ LATD, LOND
# lower_left_lon_list_of_fires=-122.0 # lower-left corner of the map; degrees, -120.1407
# lower_left_lon_list_of_fires=20.0# lower-left corner of the map; degrees, 37.60086

### domain size  for zoomed map
NROWS = 265*1000*cmaq_domain_zoomOut_scale_factor # height of the map; meters
NCOLS = 250*1000*cmaq_domain_zoomOut_scale_factor #

### domain size  for zoomed map
NROWS_zoom = 10000*zoomed_domain_zoomOut_scale_factor # height of the map; meters
NCOLS_zoom = 10000*zoomed_domain_zoomOut_scale_factor # width of the map; meters

# other settinggs
scenario_year = 30

print(f'-> save plot is= {save_plot} ')
print(f'-> plot domain is set to= {my_domain} ')
print(f'-> resolution is= ({spatial_res}) ')
print(f'-> spatial plot type is= {spatial_plot_type}')

#===========================================================
# define the input file

grid_dot_file_name = 'Scenario_'+scenario_no+'_year_30_latlon.csv'

grid_dot_file_path = '/Users/ehsan/Documents/Python_projects/USFS_fire/inputs/landis_inputs/landis_input_files_latlon_converted/' # '/' at the end of the path

grid_dot_file_full_path = grid_dot_file_path + grid_dot_file_name

#===========================================================
# read-in data

print(f'-> reading input file for scenario= {scenario_no}')

input_df = pd.read_csv( grid_dot_file_full_path , sep=',' , header=0 )#, names= ColumnList)# ,  index_listcol=0 ) why index_listcol does not work?

#===========================================================
# filter zero jdays

filter_nonZero_days = ( input_df['FireDay-30'] != 0 )

input_df_nonZero_days = input_df[ filter_nonZero_days ]

#===========================================================
# basemap 

# # upper-right corner
# upper_right_lon_list_of_fires=-118.0 # meters
# upper_right_lon_list_of_fires=40 # meters
print(" ")
print('-> making the map now ...')

# draw the map background --> map of whole domain
# desired_underlying_map= Basemap(projection='lcc' ,\
# 	llcrnrx=lower_left_lon_list_of_fires , llcrnry=lower_left_lon_list_of_fires ,\
# 	lon_list_of_fires_0=lon_list_of_fires_desired_cent , lon_list_of_fires_0=lon_list_of_fires_desired_cent ,\
# 	height=NROWS_zoom , width=NCOLS_zoom ,\
# 	 resolution='l' , area_thresh=0.5) # urcrnrx=upper_right_lon_list_of_fires , urcrnry=upper_right_lon_list_of_fires

# first, we plot a desired base-map, and then we plot our data on this map
if (my_domain=='cmaq_domain'):
	print(f'-> domain is= {my_domain}')
	print(" ")

	desired_underlying_map= Basemap(projection='lcc' ,\
		lat_0=ycent_cmaq , lon_0=xcent_cmaq ,\
		height=NROWS , width=NCOLS ,\
		resolution=spatial_res , area_thresh=0.5)

# new version of my map --> zoomed map
if(my_domain=='zoomed_domain'):
	print(f'-> domain is= {my_domain}')
	print(" ")

	desired_underlying_map= Basemap(projection='lcc' ,\
		lat_0=lat_of_desired_center , lon_0=lon_of_desired_center ,\
		height=NROWS_zoom , width=NCOLS_zoom ,\
		resolution=spatial_res , area_thresh=0.5) # 	urcrnrlon_list_of_fires=upper_right_lon_list_of_fires , urcrnrlon_list_of_fires=upper_right_lon_list_of_fires,\ , llcrnrlon_list_of_fires=lower_left_lon_list_of_fires , llcrnrlon_list_of_fires=lower_left_lon_list_of_fires ,\


### set the background type of the basemap with zorder=1
desired_underlying_map.fillcontinents( color='#CCCCCC' , lake_color='lightblue' , zorder=1 ) # ,
#desired_underlying_map.bluemarble( scale=4 , zorder=1 )
#desired_underlying_map.etopo( scale=2, alpha=0.5, zorder=1 )
#desired_underlying_map.shadedrelief( scale=2 , zorder=1 )

### draw other map characteristics
desired_underlying_map.drawmapboundary(color='k' )#, fill_color='#46bcec' ) #, fill_color='aqua')
desired_underlying_map.drawcoastlines(color = 'black' , zorder=2 )
desired_underlying_map.drawcounties(linewidth=0.5 , color='k' , zorder=3 )
desired_underlying_map.drawstates(zorder=4 )
#desired_underlying_map.drawrivers(zorder=5)


print(" ")
#===========================================================
# make plots for different spatial plot types

if ( spatial_plot_type == 'fires' ) :

	# define a dictionary for
	month_dict = {

		'jul' : [ 183 , 213 , 'v' , 'r'] ,
		'aug' : [ 214 , 244 , 'p' , 'r'] ,
		'sep' : [ 245 , 274 , '^' , 'r'] ,
		'oct' : [ 275 , 305 , '.' , 'r'] ,
		'nov' : [ 306 , 335 , 'd' , 'r']

		}

	# loop through months and and filter chunks

	for month in month_list :

		print( f'-> processing month= {month}' )

		beginning_of_month= ( input_df_nonZero_days[ 'FireDay-30' ] )
		end_of_month= ( input_df_nonZero_days[ 'FireDay-30' ] )

		filter_month =  ( beginning_of_month >= month_dict[month][0] ) &  ( end_of_month <= month_dict[month][1] )

		chunck_of_df = input_df_nonZero_days [ filter_month ]

		lat_list_of_fires = chunck_of_df ['Lat'].values
		print(f'-> no. of burned pixels in {month} in scen ({scenario_no})= {len(lat_list_of_fires)}')
		#print(lon_list_of_fires)

		lon_list_of_fires = chunck_of_df ['Long'].values
		#print(f'-> no. of fires in {month} = {len(lon_list_of_fires)}')

		#x_coord , y_coord = desired_underlying_map( lon_list_of_fires , lon_list_of_fires ) # order: x ,y; degrees to meters
		#desired_underlying_map.scatter( x_coord , y_coord , latlon=True , marker= month_dict[month][2] , s=10 , label=month) # If lon_list_of_fireslon_list_of_fires is False (default), x and y are assumed to be in map projection coordinates.
	#source: https://matplotlib.org/basemap/api/basemap_api.html

		if ( single_scen_per_month_plot == 'yes' ) :
		
			desired_underlying_map= Basemap(projection='lcc' ,\
			lat_0=lat_of_desired_center , lon_0=lon_of_desired_center ,\
			height=NROWS_zoom , width=NCOLS_zoom ,\
			resolution=spatial_res , area_thresh=0.5)

			#==================================================================================
			### set the background type of the basemap with zorder=1
			desired_underlying_map.fillcontinents( lake_color='lightblue' , zorder=1 ) # ,
			#desired_underlying_map.bluemarble( scale=4 , zorder=1 )
			#desired_underlying_map.etopo( scale=2, alpha=0.5, zorder=1 )
			#desired_underlying_map.shadedrelief( scale=2 , zorder=1 )

			### draw other map characteristics
			desired_underlying_map.drawmapboundary(color='k' )#, fill_color='#46bcec' ) #, fill_color='aqua')
			desired_underlying_map.drawcoastlines(color = 'black' , zorder=2 )
			desired_underlying_map.drawcounties(linewidth=0.5 , color='k' , zorder=3 )
			desired_underlying_map.drawstates(zorder=4 )
			#==================================================================================

			desired_underlying_map.scatter( lon_list_of_fires , lat_list_of_fires , latlon=True , marker= month_dict[month][2] , color= month_dict[month][3] , s=12 , label=month ,  zorder=5 ) # If lon_list_of_fireslon_list_of_fires is False (default), x and y are assumed to be in map projection coordinates.

			plt.legend( scatterpoints=1 , frameon=True , title= 'number of fires' , loc='center left', bbox_to_anchor=(1, 0.5) ,
		          fancybox=True )

			plt.title(f'Spatial distribution of fires in LANDIS scenario {scenario_no} in month {month}' , fontsize=10 )

			plot_name = 'spatial_distribution_of_fires_for_mon_'+month+'_and_scen_'+scenario_no+'_'+my_domain+'.'+plot_format

			#===========================================================
			# save the plot
			if ( save_plot_single_scen_per_month =='yes' ) :

				saved_plot = plot_dir+plot_name
				#extent = ax2.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
				plt.savefig(saved_plot , dpi=dpi_res , format=plot_format ) #, bbox_inches='tight')

				print(" ")
				print(f'-> plot saved at=')
				print(saved_plot)
				print(" ")
				plt.clf()
				plt.cla()
				plt.close()
				#plt.show()
				#del desired_underlying_map

		else:

			desired_underlying_map.scatter( lon_list_of_fires , lat_list_of_fires , latlon=True , marker= month_dict[month][2] , s=12 , label=month ,  zorder=5 ) # If lon_list_of_fireslon_list_of_fires is False (default), x and y are assumed to be in map projection coordinates.

			plt.legend( scatterpoints=1 , frameon=True , title= 'number of fires' , loc='center left', bbox_to_anchor=(1, 0.5) ,
			          fancybox=True )

			plt.title(f'Spatial distribution of fires in LANDIS scenario {scenario_no}' , fontsize=10 )

			plot_name = 'spatial_distribution_of_fires_for_allMonths_and_scen_'+scenario_no+'_'+my_domain+'.'+plot_format

#===========================================================

if (spatial_plot_type=='marker') :

 # plot for a position/place/marker
 	desired_underlying_map.plot( marker_lon , marker_lat , marker='.' , color='k' , latlon=True )

#===========================================================

if ( spatial_plot_type=='mesh' ) :

	# plot a mesh on the map
	dir_path='/Users/ehsan/Documents/Python_projects/USFS_fire/inputs/'

	grid_dot_file_name='GRIDDOT2D_161001'
	grid_cross_file_name='GRIDCRO2D_161001'

	grid_dot_file=dir_path+grid_dot_file_name
	grid_cross_file=dir_path+grid_cross_file_name

	print(f'-> GRID_DOT file is= {grid_dot_file}')
	print(f'-> GRID_CRO file is= {grid_cross_file}')

	grid_dot_open=Dataset( grid_dot_file , 'r')
	grid_cross_open=Dataset( grid_cross_file , 'r')

	print('-----------------------------------------')
	print(f'-> info for file {grid_dot_file_name} is=')
	print('-> dimension is= %s' %( str(grid_dot_open.variables['LOND'].dimensions ))) # f-string does not work for this syntax
	print('-> shape is= %s' %str(grid_dot_open.variables['LOND'].shape )) # and this
	print('-----------------------------------------')
	print(f'-> info for file {grid_cross_file_name} is=')
	print('-> dimension is= %s' %( str(grid_cross_open.variables['LON'].dimensions ))) # f-string does not work for this syntax
	print('-> shape is= %s' %str(grid_cross_open.variables['LON'].shape )) # and this
	print('-----------------------------------------')

	lon_dot_arr=np.array( grid_dot_open.variables['LOND'][0,0,:,:] )
	lat_dot_arr=np.array( grid_dot_open.variables['LATD'][0,0,:,:] )

	lon_cross_arr=np.array( grid_cross_open.variables['LON'][0,0,:,:] )
	lat_cross_arr=np.array( grid_cross_open.variables['LAT'][0,0,:,:] )

	# plot for different mesh type
	if ( mesh_type=='sample_mesh' ) :

		desired_underlying_map.scatter( lon_dot_arr , lat_dot_arr , marker='.' , color='b' , latlon=True , zorder=5 )
		desired_underlying_map.scatter( lon_cross_arr , lat_cross_arr , marker='+' , color='k' , latlon=True , zorder=6 )

	# plot for different mesh type
	if ( mesh_type=='modeling_domain') :

		lon_min=np.min( lon_dot_arr ) # get the min from dot arr
		lon_max=np.max( lon_dot_arr ) # get max of dot arr
		lat_min=np.min( lat_dot_arr ) # get min of lat dot arr
		lat_max=np.max( lat_dot_arr ) # get max of dot lat arr

		lon_coord_list=[lon_min , lon_min , lon_max , lon_max , lon_min ] # put the points in order to appear
		lat_coord_list=[lat_min , lat_max , lat_max , lat_min , lat_min ]

		desired_underlying_map.plot( lon_coord_list , lat_coord_list , color='r' , latlon=True , zorder=5 )  # for drawing line, don't use marker kwrd


	if ( mesh_type=='station_inside_cell' ) :

		lon_diff_arr=lon_cross_arr-stn_lon
		lat_diff_arr=lat_cross_arr-stn_lat

		#print(f'-> type of {lon_diff_arr} is= {type(lon_diff_arr)} ')

		total_diff_arr=np.abs( lon_diff_arr ) + np.abs( lat_diff_arr )

		tuple_of_row_col=np.argwhere( total_diff_arr==np.min(total_diff_arr) )[0]

		print(f'-> row/col of our cell is= {tuple_of_row_col} ')
		stn_row=tuple_of_row_col[0]
		stn_col=tuple_of_row_col[1]

		print(f'-> station row is= {stn_row}')
		print(f'-> station row is= {stn_col}')

		### get the corners of the cell that station falls inside it
		ll_lat=lat_dot_arr[ stn_row , stn_col ]
		ul_lat=lat_dot_arr[ stn_row+1 , stn_col ]
		ur_lat=lat_dot_arr[ stn_row+1 , stn_col+1 ]
		lr_lat=lat_dot_arr[ stn_row , stn_col+1 ]

		ll_lon=lon_dot_arr[ stn_row , stn_col ]
		ul_lon=lon_dot_arr[ stn_row+1 , stn_col ]
		ur_lon=lon_dot_arr[ stn_row+1 , stn_col+1 ]
		lr_lon=lon_dot_arr[ stn_row , stn_col+1 ]

		stn_cell_lon_list=[ ll_lon , ul_lon , ur_lon , lr_lon , ll_lon ]
		stn_cell_lat_list=[ ll_lat , ul_lat , ur_lat , lr_lat , ll_lat ]

		print('-> now plot the station and cell')

		desired_underlying_map.plot( stn_lon , stn_lat , marker='.' , color='k' , latlon=True , zorder=5 )

		desired_underlying_map.plot( stn_cell_lon_list , stn_cell_lat_list , color='r' , latlon=True , zorder=5 )


	if ( mesh_type=='stats_region' ) :

		lon_diff_arr=lon_cross_arr-stats_region_ll_lon
		lat_diff_arr=lat_cross_arr-stats_region_ll_lat

		#print(f'-> type of {lon_diff_arr} is= {type(lon_diff_arr)} ')

		total_diff_arr=np.abs( lon_diff_arr ) + np.abs( lat_diff_arr )

		tuple_of_row_col=np.argwhere( total_diff_arr==np.min(total_diff_arr) )[0]

		print(f'-> row/col of our cell is= {tuple_of_row_col} ')
		marker_row=tuple_of_row_col[0]
		marker_col=tuple_of_row_col[1]

		print(f'-> cell row is= {marker_row}')
		print(f'-> cell row is= {marker_col}')
		print(f'-> now plot the mesh from the starting cell= {marker_row , marker_col} ')

		for row in range( marker_row , marker_row + mesh_domain_range , 1 ) :
			for column in range( marker_col , marker_col + mesh_domain_range , 1 ) :

				#print(f'-> for row= {row} and col= {column}')
				desired_underlying_map.plot( lon_cross_arr[row , column] , lat_cross_arr[row , column] , marker='.' , color='grey' , latlon=True )


	if ( mesh_type == 'sample_plot_of_study_region') :

		### order is= ll,ul,ur,lr,and again ll
		LTB_lon_list=[ -120.30 , -120.30 , -119.83 , -119.83 , -120.30 ] 
		LTB_lat_list=[ 38.87 , 39.30 , 39.30 , 38.87 , 38.87 ]

		southLakeTahoe_lon_list=[ -120.05 , -120.05 , -119.95 , -119.95 , -120.05 ]
		southLakeTahoe_lat_list=[ 38.88 , 38.95 , 38.95 , 38.88 , 38.88 ]

		desired_underlying_map.plot( LTB_lon_list , LTB_lat_list , latlon=True , zorder=5 )
		x,y=desired_underlying_map(-119.82 , 39.3)
		plt.text( x , y , 'LTB' , fontsize=8 , color='r')

		desired_underlying_map.plot( southLakeTahoe_lon_list , southLakeTahoe_lat_list , latlon=True , zorder=5 )
		x,y=desired_underlying_map(-119.95 , 38.92)
		plt.text( x , y , 'SouthLakeTahoe' , fontsize=8 , color='r')

	plot_name = 'plot_for_'+spatial_plot_type+'_'+mesh_type+'.'+plot_format

#===========================================================
# save the plot
if (save_plot=='yes'):

	# plot_dir = '/Users/ehsan/Documents/Python_projects/USFS_fire/inputs/landis_inputs/plots/'

	saved_plot = plot_dir+plot_name
	#extent = ax2.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
	plt.savefig(saved_plot , dpi=300 , format=plot_format ) #, bbox_inches='tight')

	print(" ")
	print(f'-> plot saved at=')
	print(saved_plot)
	#plt.show()
	#===========================================================
	# calculon_list_of_firese run time

	end = time.time()

	print( f'-> run time= { (( end - start ) / 60 ) :.2f} min' )  # f-string

	#===========================================================
# show the plot
else:
	print(" ")
	print(f'-> save plot for non fires plotting is= NO! so we only show it here.')
	plt.show() # save the plot and then show it.