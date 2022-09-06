###############################################
## Arielle Simmons-Steffen                   ##
## Jason Hellums                             ##
##                                           ##
## USDA-NRCS                                 ##
## Date created: September 4, 2022           ##
## Date modified:                            ##
###############################################
## Complete the items set with 'ToDO'...final product must be a toolbox that works with ArcPro 2
## The librariers for DOWNSAMPLING (see example steps in the 'photoshop_setting_ex' should be
## included in the default ArcPro Py3 install. 
from PIL import Image, ImageFile 
from PIL.TiffTags import TAGS
import os
import glob
import arcpy
import logging
Image.MAX_IMAGE_PIXELS = 10000000000
print('start')
## ToDO: MAKE FOOTPRINT USER DETERMINED IN A ARCPRO TOOLBOX (work for 2.X PRO)
footprint = arcpy.GetParameterAsText(0)
files = glob.glob(footprint + '/**/*.tif', recursive=True)
logging.basicConfig(level=logging.INFO, filename='downsampling_failed.log', datefmt='%Y-%m-%d %H:%M:%S') #Create a log file
for file in files:
    data = file.rsplit('\\',1)
    path = data[0]
    im = data[1]
    im_data = im.rsplit('.',1)
    im_name = im_data[0]
    image = Image.open(file)
    meta_dict = {TAGS[key] : image.tag[key] for key in image.tag_v2}
    if 'Orientation' in meta_dict.keys():
        direction = image.tag[274][0]
    else:
        direction = None
    print(direction)
    if direction is None:
        image.save(os.path.join(path, f'{im_name}_downsampled.jpg'), dpi=(300,300))
    elif os.path.isfile(os.path.join(path, f'{im_name}_downsampled.jpg')):
        continue
    elif direction == 8:
        try:
            ### for standard 8 bit black and white
            image.mode = 'L'
            rotated = image.rotate(-90.0)
	    ## ToDO: AFTER ROTATION MUST SAVE THE .tif to a DOWNSAMPLED .jpg with the file name: '<original tif name>_downsampled.jpg'. THe 'downsampled.jpg' should be saved in the SAME Directory as the parent .tif file. CREATE A .txt LOG OF ALL FAILURES.
            rotated.convert('RGB').save(os.path.join(path, f'{im_name}_downsampled.jpg'), dpi=(300,300))
            print(file.replace('.tif', '.jpg'))
        except:
            try:
                ### for 24 bit rgb
                image.mode = 'RGB'
                rotated = image.rotate(-90.0)
	    ## ToDO: AFTER ROTATION MUST SAVE THE .tif to a DOWNSAMPLED .jpg with the file name: '<original tif name>_downsampled.jpg'. THe 'downsampled.jpg' should be saved in the SAME Directory as the parent .tif file. CREATE A .txt LOG OF ALL FAILURES.
                rotated.convert('RGB').save(os.path.join(path, f'{im_name}_downsampled.jpg'), dpi=(300,300))
                print(file.replace('.tif', '.jpg'))
            except Exception as e:
                message = str(f"Failed to downsample {im_name}.tif error: {e}")
                logging.info(message)

    else:
        try:
            image.mode = 'L'
            image.save(os.path.join(path, f'{im_name}_downsampled.jpg'), dpi=(300,300))
            print(file.replace('.tif', '.jpg'))
        except Exception as e:
            message = str(f"Failed to downsample {im_name}.tif error: {e}")
            logging.info(message)

print('complete')