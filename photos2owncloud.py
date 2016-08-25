import piexif
import os
import sys
import datetime
import logging

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)

basedir = "/Users/david/Downloads/project/images/"
completed_dir = basedir + "complete/"
image_extensions = ['.jpg', '.jpeg', '.png']


def directory_shit(year, month):
    yeardir = completed_dir + year
    monthdir = yeardir + '/' + month + '/'
    if not os.path.exists(yeardir):
        os.makedirs(yeardir)
    if not os.path.exists(monthdir):
        os.makedirs(monthdir)
    return monthdir

def get_exif_date(image):
    try:
        exif_data = piexif.load(basedir + image)
        date_time_original = exif_data["Exif"][36867]
        if date_time_original:
            logging.info("original datetime found!")
            return date_time_original
    except:
        logging.warn("unable to find original datestamp for {0}".format(image))

    try:
        exif_data = piexif.load(basedir + image)
        date_time_digitized = exif_data["Exif"][36868]
        if date_time_digitized:
            logging.info("digitized datetime found!")
            return date_time_digitized
    except:
        logging.warn("unable to find digitized datestamp for {0}".format(image))
        return None


def main():
    logging.info("Warming up image processor...")
    files = os.listdir(basedir)
    if len(files) == 0:
        logging.error("No images to process.")
        sys.exit(1)
    for file in files:
        for ext in image_extensions:
            if file.lower().endswith(ext):
                exif_date = get_exif_date(file)
                if exif_date:
                    print "Working on file '{0}'...".format(file),
                    fmt_dto = exif_date.replace(":","-").replace(" ","_")
                    year = exif_date.split(':')[0]
                    month = exif_date.split(':')[1]
                    destdir = directory_shit(year, month)
                    cur_epocht = int(datetime.datetime.now().strftime("%s"))
                    old_epocht = int(datetime.datetime.strptime(fmt_dto, "%Y-%m-%d_%H-%M-%S").strftime("%s"))
                    try:
                        print "touching...",
                        os.utime(basedir + file, (cur_epocht, old_epocht))
                        print "moving...",
                        os.rename(basedir + file, destdir + fmt_dto + "_" + file)
                        print "Done."
                    except Exception as e:
                        logging.error("Some error occurred: {}".format(e))
                        continue
                break
            else:
                logging.error("No exif data found for '{0}'".format(file))
                continue
    logging.info("No more files to process.")

if __name__ == "__main__":
    sys.exit(main())