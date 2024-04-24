from math import floor


class GeodesyOps:

    @staticmethod
    def utm_srid_from_extent( west, south, east, north):
        """
            Calculate the UTM zone for a given extent.
            :param west: min longitude bounding box in degrees
            :param south: min latitude bounding box in degrees
            :param east: max longitude bounding box in degrees
            :param north: max latitude bounding box in degrees
        """

        center_long = (west + east) / 2
        utm_zone = int(((center_long + 180) / 6) % 60) + 1
        # Determine if it's in the northern or southern hemisphere
        hemisphere = 'north' if (south + north) / 2 > 0 else 'south'
        # Determine the EPSG code for the UTM projection
        epsg_code = 32600 + utm_zone if hemisphere == 'north' else 32700 + utm_zone
        return epsg_code

    @staticmethod
    def utm_srid_from_coord(long, lat):
        zone = (floor((long + 180) / 6) % 60) + 1
        dir = 6 if lat >= 0 else 7
        return int(f"32{dir}{zone}")

    @staticmethod
    def meter_2_dd(length: float):
        return length / (110 * 1000)
