import sys
sys.path.insert(0, './src/')
from aTeam_PySparkLibrary.generate_dim_date_table import generate_dim_date_table


print(generate_dim_date_table(start='01-01-2020', end='12-31-2025', frequency='D', wanted_columns=['y', 'm', 'd', 'dow_om', 'tot_weekd_in_mo', 'is_d_leapyr']))