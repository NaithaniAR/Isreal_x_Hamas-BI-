
import chardet
import sys
sys.path.append('../')

# Detect encoding

with open(r'/home/marktine/data Vis/Isreal_x_Hamas-BI-/libs/misic/data-points/spreadsheets/xslx/palestine_hrp_civilian_targeting_events_and_fatalities_by_month-year_as-of-29may2024.xlsx', 'rb') as f:
    result = chardet.detect(f.read())
    print(result)