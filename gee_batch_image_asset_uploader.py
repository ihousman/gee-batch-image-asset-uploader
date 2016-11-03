from gee_batch_image_asset_uploader_lib import *
###############################################
#User input parameters
cwd = os.getcwd().replace('\\','/')+'/'

#Path to EE asset image collection directory
#Currently hard-coded to be an image collection and not just a folder
#Needs users/username piece to exist, but can create the collection directory on-the-fly
asset_dir = 'users/ianhousman/testCollection5'

#Google cloud storage bucket
#Must be created ahead of time
#ACL (permissions) does not need to be updated as long as the unsername for the cloud storage bucket and EE account are the same
#If acl does need changed use: gsutil acl ch -u AllUsers:W gs://bucket-path
gs_bucket = 'gs://image-upload-test2/'

#This is generally hard-coded with EE
#User gdal_translate for fast conversion to tif
image_extension = '.tif'

#For pyramiding of GEE assets- not reprojecting
#Generally MEAN for continuous and MODE or SAMPLE for thematic
#Also available methods are: MIN, MAX, and SAMPLE
resample_method = 'MEAN'

#Band names for EE images
#Assumes all input images have the same band number and should assume the same names
band_names =['blue','green','red','nir','swir1','swir2','temp']

#Directory where images are to be uploaded are located
image_dir =cwd + 'image_dir/'

#Parsing indices
#These are used to parse date info from image name
#They may need changed depending on name format
year_parsing_indices = [9,13]
julian_day_parsing_indices = [13,16]
############################################################
#Get the tifs
tifs = glob(image_dir,image_extension)

#Parse out the relevant date information from the image names
#Dates just need to be in milliseconds (since 1-1-1970)
dates = [[base(i)[year_parsing_indices[0]:year_parsing_indices[1]],base(i)[julian_day_parsing_indices[0]:julian_day_parsing_indices[1]]]  for i in tifs]
dates = [year_month_day_to_seconds(julian_to_calendar(i[1], i[0]))*1000 for i in dates]

#Get the id names
system_index_list = [base(i).split('_')[0] for i in tifs]

#Iterate through and create a property dictionary for each image
property_list = [{'id':i[0], 'system:time_start':i[1]} for i in zip(system_index_list,dates)]

#Call on wrapper function for uploading found in the image_uploader_lib
upload_to_gee(image_dir,gs_bucket,asset_dir,image_extension, resample_method = resample_method,band_names =band_names,property_list = property_list)