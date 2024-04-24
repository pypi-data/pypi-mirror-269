import os
from datetime import datetime, timedelta
import requests
from pyproj import Proj, transform

class Modis:
    @staticmethod
    def latlon_to_modis_tile(lat, lon):
        # Convert latitude and longitude to MODIS sinusoidal projection coordinates
        modis_proj = Proj(init='epsg:4326')
        modis_x, modis_y = transform(modis_proj, {'proj': 'sinu', 'lon_0': 0, 'x_0': 0, 'y_0': 0}, lon, lat)

        # Calculate MODIS tile coordinates (h, v)
        tile_h = int((modis_x + 1111950.519667) / 1111950.519667)
        tile_v = int((modis_y + 1111950.519667) / 1111950.519667)

        return tile_h, tile_v

    @staticmethod
    def download_modis_data(year, day_of_year, tile_h, tile_v, output_dir):
        url = f'https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/6/MOD13Q1/{year}/{day_of_year:03d}/MOD13Q1.A{year}{day_of_year:03d}.h{tile_h:02d}v{tile_v:02d}.006.NDVI.006.hdf'
        filename = f'MOD13Q1_A{year}{day_of_year:03d}_h{tile_h:02d}v{tile_v:02d}_006_NDVI.hdf'

        response = requests.get(url, stream=True)
        with open(os.path.join(output_dir, filename), 'wb') as file:
            for chunk in response.iter_content(chunk_size=128):
                file.write(chunk)

        print(f'Downloaded: {filename}')

    def execute_download(self, extent, output_dir):
        # Bounding box for Pakistan
        # extent = [23.6345, 60.872, 37.0841, 77.8375]  # [min_lat, min_lon, max_lat, max_lon]

        # Determine MODIS tiles for the bounding box
        tile_min_h, tile_min_v = self.latlon_to_modis_tile(extent[0], extent[1])
        tile_max_h, tile_max_v = self.latlon_to_modis_tile(extent[2], extent[3])

        # Define the date range
        start_date = datetime(2022, 1, 1)
        end_date = datetime(2022, 12, 31)

        # Iterate over each day in the date range
        current_date = start_date
        while current_date <= end_date:
            year = current_date.year
            day_of_year = current_date.timetuple().tm_yday

            # Download MODIS data for each tile within the specified bounding box
            for tile_h in range(tile_min_h, tile_max_h + 1):
                for tile_v in range(tile_min_v, tile_max_v + 1):
                    self.download_modis_data(year, day_of_year, tile_h, tile_v, output_dir)

            current_date += timedelta(days=1)
