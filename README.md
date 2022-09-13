# SOFT-IO-LI
SOFT-IO-LI code September 2022
SOFT-IO-LI v1

Catherine Mackay 2022
catherine.mackay@aero.obs-mip.fr (Until end of 2022)
ck8mackay@gmail.com

## SOFT-IO-LI is split into three seperate programmes.

### 1. Auto_plume_ID.ipynb

This searches the IAGOS database for new flights measuring either NOx
(using the pack P2b IAGOS CORE) or NO and NO2 (using the pack PC2 CARIBIC).

The flight data is then analysed, only the cruise data is retained for
further analysis. NOx plumes in excess of the 75th percentile, that do not
contain statospheric influences and where the CO and O3 are NOT > 100 ppb are retained.

Plumes due to aircraft emissions are removed by ensuring that plumes with a
width of < 12 km  are excluded. (Schumann 2007)
Nb. it would be interesting to perhaps keep these if the total NOx value was
low, but for now they are all assumed to be due to aircraft.

The final plumes are then analysed and saved into a seperate txt file for each
flight. For each plume identified the following information is saved:

- Plume start ID

- Plume end ID

- Date start

- Time start

- Date end

- Time end

- Longitude start

- Longitude end

- Latitude start

- Latitude end

- Pressure start

- Pressure end

- Altitude start

- Altitude end

The txt files are stored in /o3p/iagos/SOFT-IO-LI/Plume_info_all_cuts/ and used by
programme 2.

At the same time the date and time for the arrival of each flight is stored in
/o3p/iagos/SOFT-IO-LI/flight_time_txt/ as:

- year

- month

- day

- hour

This is used in programme 2 to set the start and end times and dates of the
backward simulation.

If plumes are found and validated then the flight variables and isolated
plumes are plotted and saved in /o3p/iagos/SOFT-IO-LI/plots. It is a good idea
to check these plots to make sure the plumes look sensible, so far so good.

### 2. FLEXPART_auto.ipynb

### 3. 

********************************************************************************
## FLEXPART requirements

SOFT-IO-LI uses FLEXPART release 10.4 and the following files in the source code
were modified:

### par_mod.f was modified at line 143 to allow for the 0.5° ERA5 ECMWF data.

flexpart10.4/flexpart_v10.4_3d7eebf/src/ contains 3 FLEXPART compilations:

- FLEXPART for 1°:
integer,parameter :: nxmax=361,nymax=181,nuvzmax=138,nwzmax=138,nzmax=138,nxshift=359 ! 1.0 degree 138 level

- FLEXPART_05 for 0.5°:
integer,parameter :: nxmax=721,nymax=361,nuvzmax=138,nwzmax=138,nzmax=138,nxshift=359  ! 0.5 degree 138 level

- FLEXPART 0.25 for 0.25°
integer,parameter :: nxmax=1441,nymax=721,nuvzmax=138,nwzmax=138,nzmax=138,nxshift=359  ! 0.25 degree 138 level

SOFT-IO-LI uses FLEXPART_05 as default.

### makefile was modified to allow compilation on nuwa.



