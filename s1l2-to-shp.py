#!/usr/bin/env python
#
#   This little script converts Sentinel1 L2 NetCdf files in ESRI shapefile
#   by exctracting only wind direction/speed values. 
#
#   See documentation at:
#   https://sentinel.esa.int/documents/247904/349449/Sentinel-1_Product_Specification
#   Relevant part is about L2 OWI Components.
#
#   Copyright (C) 2018 Francesco P. Lovergine <francesco.lovergine@cnr.it>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import sys
import fiona
from fiona.crs import from_epsg
from netCDF4 import Dataset

def convert(target, outshp):
    # Open a collection for writing.
    with fiona.open(
            outshp, 'w',
            crs=from_epsg(4326),
            driver='ESRI Shapefile',
            schema = {
                'geometry': 'Point',
                'properties': {
                    'windspeed': 'float',
                    'winddir': 'float',
                    'ewindspeed': 'float',
                    'ewinddir': 'float'
                }
            }) as dest:

        nc = Dataset(target)
        lats = nc.variables['owiLat']
        lons = nc.variables['owiLon']
        ws = nc.variables['owiWindSpeed']
        wd = nc.variables['owiWindDirection']
        ews = nc.variables['owiEcmwfWindSpeed']
        ewd = nc.variables['owiEcmwfWindDirection']
        for i in range(lats.shape[0]):
            for j in range(lats.shape[1]):
                geom = {
                    'type': "Point",
                    'coordinates': [lons[i][j], lats[i][j]]}
                feature = {
                    'type': "Feature",
                    'geometry': geom,
                    'properties': {
                        'windspeed': float(ws[i][j]),
                        'winddir': float(wd[i][j]),
                        'ewindspeed': float(ews[i][j]),
                        'ewinddir': float(ewd[i][j])
                    }
                }
                dest.write(feature)


if __name__ == "__main__":
    ncs = sys.argv[1]
    outshp = sys.argv[2] + ".shp"
    convert(ncs, outshp)
