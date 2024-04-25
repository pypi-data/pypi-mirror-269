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

from ...DataModels.Geosteering.Pick import Pick
from ...DataModels.Geospatial.GeoLocation import GeoLocation
from ...DataModels.Geospatial.Coordinate import Coordinate
from ...Zonevu import Zonevu
from ...Services.Client import ZonevuError
from ...Services.WellService import WellData
from ...DataModels.Geosteering.Calcs import create_extended_picks
from tabulate import tabulate


def main_geosteering_picks(zonevu: Zonevu, well_name: str):
    """
    Retrieve well data from ZoneVu
    For the first geosteering interpretation, create flattened geosteering picks.
    """
    well_svc = zonevu.well_service
    well = well_svc.get_first_named(well_name)
    if well is None:
        raise ZonevuError.local('Could not find the well "%s"' % well_name)

    well_name = well.full_name
    print('Well named "%s" was successfully found' % well_name)
    well_svc.load_well(well, {WellData.geosteering})  # Load surveys and geosteering into well
    wellbore = well.primary_wellbore  # Get reference to wellbore
    if wellbore is None:
        print('Well has no wellbores, so exiting')
        return

    # If available, plot the starred or first geosteering interpretation
    interpretations = wellbore.interpretations
    has_geosteering = len(interpretations) > 0
    if has_geosteering:
        strat_col = zonevu.strat_service.find_stratcolumn(well.strat_column.id)
        interp = next((g for g in interpretations if g.starred),
                      interpretations[0])  # Get starred or first interpretation
        picks = interp.picks
        extended_picks = create_extended_picks(interp, strat_col, well.elevation)
        table = []
        n = 0
        for p in extended_picks:
            n += 1
            table.append([n, p.md, p.latitude, p.longitude, '', ''])
            for h in p.horizon_depths:
                table.append([n, '', '', '', h.formation.symbol, round(h.elevation, 1)])

        headers = ['N', 'MD', "Latitude", "Longitude", "Formation", "Elevation"]
        print(tabulate(table, headers=headers, tablefmt='plain'))





