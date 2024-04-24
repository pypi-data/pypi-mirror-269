import pprint
from datetime import datetime
from typing import Union

import ee

# from dateparser.data.date_translation_data import ee

from digitalarztools.pipelines.gee.core.auth import GEEAuth
from digitalarztools.pipelines.gee.core.image import GEEImage
from digitalarztools.pipelines.gee.core.image_collection import GEEImageCollection
from digitalarztools.pipelines.gee.core.region import GEERegion
from digitalarztools.utils.logger import da_logger


class Precipitation:
    """
    Extrat data from different sources
    """

    @staticmethod
    def chirps_data_using_gee(gee_auth: GEEAuth, region: GEERegion, start_date: Union[str, datetime],
                           end_date: Union[str, datetime], how='mean') -> GEEImage:
        """
        Extract CHIRPS data using following code
        https://developers.google.com/earth-engine/datasets/catalog/UCSB-CHG_CHIRPS_DAILY
        :param gee_auth: authentiation
        :param gdv: for define AOI
        :param start_date:
        :param end_date:
          :param how: choices are 'median', 'max', 'mean', 'first', 'cloud_cover'
        :return:
        """

        if gee_auth.is_initialized:
            date_range = (start_date, end_date)
            img_collection = GEEImageCollection(ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY'))
            img_collection.set_date_range(date_range)
            img_collection.set_region(region)

            # img_collection = GEEImageCollection(region, 'UCSB-CHG/CHIRPS/DAILY', date_range)
            img_collection.select_dataset('precipitation')
            return GEEImage(img_collection.get_image(how))
        else:
            da_logger.error("Please initialized GEE before further processing")


    # @staticmethod
    # def precipitation_and_et_combined():
    @staticmethod
    def precipitation_with_et(i_date=None, f_date=None, no_of_days=10):
        """
        :param i_date: inital date (2023-01-01)
        :param f_date:  final date like 2023-12-07
        :return:
        """
        if f_date is None:
            f_date =datetime.date.today()
        if i_date is None:
            # first = today.replace(day=1)
            i_date = f_date - datetime.timedelta(days=no_of_days)
            # date_range = (start_date.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d"))

        pr = GEEImageCollection.from_tags("UCSB-CHG/CHIRPS/DAILY", (i_date, f_date))
        pr.select_bands(["precipitation"])

        pet = GEEImageCollection.from_tags("MODIS/006/MOD16A2", (i_date, f_date))
        pet.select_bands(["PET", "ET_QC"])

        # local_pr = pr.get_image_info_within_poi(poi, scale)
        # pprint.pprint(local_pr[:5])

        pr_m = pr.sum_resampler(pr.img_collection, 1, "month", 1, "pr")

        # # Evaluate the result at the location of interest.
        # pprint.pprint(pr_m.getRegion(poi, scale).getInfo()[:5])

        """
        For evapotranspiration, we have to be careful with the unit. The dataset gives us an 8-day sum and a scale factor of 10 is applied. Then, to get a homogeneous unit, we need to rescale by dividing by 8 and 10: 1/(8*10) = 0.0125
        .
        """
        # Apply the resampling function to the PET dataset.
        pet_m = pet.sum_resampler(pet.img_collection.select(["PET"]), 1, "month", 0.0125, "pet")

        # # Evaluate the result at the location of interest.
        # pprint.pprint(pet_m.getRegion(poi, scale).getInfo()[:5])

        meteo = pr_m.combine(pet_m)
        return meteo

