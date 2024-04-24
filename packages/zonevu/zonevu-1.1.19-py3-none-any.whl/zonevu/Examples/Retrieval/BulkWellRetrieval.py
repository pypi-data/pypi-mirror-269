#  Copyright (c) 2024 Ubiterra Corporation. All rights reserved.
#  #
#  This ZoneVu Python SDK software is the property of Ubiterra Corporation.
#  You shall use it only in accordance with the terms of the ZoneVu Service Agreement.
#  #
#  This software is made available on PyPI for download and use. However, it is NOT open source.
#  Unauthorized copying, modification, or distribution of this software is strictly prohibited.
#  #
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
#  PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
#  FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
#  ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
#
#
#

from ...Zonevu import Zonevu
from typing import List
from ...DataModels.Wells.Well import WellEntry
from typing import Optional
from ...Services.WellService import WellData
from ...Services.Client import ZonevuError
import time


def main(zonevu: Zonevu, exact_match: bool = True, name: Optional[str] = None):
    print('List wells in ZoneVu account with geosteering interpretations')
    well_svc = zonevu.well_service
    geosteer_svc = zonevu.geosteering_service
    wells = well_svc.find_by_name(name, exact_match)
    well_data_types = {WellData.geosteering}
    print('Number of wells retrieved = %s' % len(wells))
    counter = 2000
    num_wells = len(wells)
    num_with_geosteering = 0
    for index, well_entry in enumerate(wells):
        well = well_svc.find_by_id(well_entry.id)
        wellbore = well.primary_wellbore
        if wellbore is not None:
            geosteering_entries = geosteer_svc.get_interpretations(wellbore.id)
            has_geosteering = len(geosteering_entries) > 0
            if has_geosteering:
                print('%s - %s - %s geosteer interps' % (index, well_entry.full_name, len(geosteering_entries)))
                num_with_geosteering += 1
                for geosteer_entry in geosteering_entries:
                    try:
                        interp = geosteer_svc.get_interpretation(geosteer_entry.id)
                        # print('  # geosteering interpretations = %s' % len(geosteering_entries))
                    except ZonevuError as err:
                        print('  Could not retrieve geosteering interp = %s (%s) because %s' %
                              (geosteer_entry.name, geosteer_entry.id, err.message))
                    time.sleep(1)  # Give zonevu a break
        if index > counter:
            break



