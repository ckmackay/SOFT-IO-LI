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

FLEXPART_auto uses the contents of FLEXPART_templates to create a FLEXPART
directory for each flight.

This is located in
/o3p/user/SOFT-IO-LI/flexpart10.4/flexpart_v10.4_3d7eebf/src/exercises/soft-io-li/YYYY/MM/flight_id/

It then uses the outputs from the first programme to create the following
control files required by FLEXPART which are unique for each flight.

- AVAILABLE

- COMMAND

- pathnames

- RELEASES

Once these are all in place it checks the meteo files are stored locally and
if so launches the FLEXPART simulation.

If they are not (at present we are waiting for ERA5 to be available to us) a
warning is given.

They can then be launched seperately using the submit_FLEXPART.ipynb programme.

### 3. 

********************************************************************************
## User Guide

SOFT-IO-LI is written in Python 3 and can be run either as batch jobs on nuwa
using the .py files, or alternatively, interactively using JupyterLab on nuwa
using the .ipynb files. JupyterLab allows you to view plots immediately and is
quick even when running over many flights.

SOFT-IO-LI files and directories are stored on nuwa in the iagos space:
/o3p/iagos/SOFT-IO-LI/

Please do not edit the .ipynb or .py files here.
To test changes please edit copies in your user space.
A copy of this version is available from Github in case of problems:
https://github.com/ckmackay/SOFT-IO-LI.git

In order to run the SOFT-IO-LI programmes in JupyterLab follow the
instructions given for using conda and launching JupyterLab on nuwa
(http://nuwa.aero.obs-mip.fr/CondaNuwa).

On nuwa in your own space /home/user/ create a SOFT-IO-LI directory.

Make a copy of /o3p/iagos/SOFT-IO-LI/ locally, for example /o3p/user/SOFT-IO-LI/

The environment used for SOFT-IO-LI is saved in environment.yml

Create the environment where you will launch JupyterLab from, for example,
/home/user/SOFT-IO-LI using:

	conda env create -f environment.yml

Activate the environment, which is called hvenv, using:

	conda activate hvenv

Verify the environment is installed correctly using:

	conda env list

hvenv should now be in your list of conda environments.

At the start of each session to use SOFT-IO-LI, activate the hvenv environment
using:
	conda activate hvenv

(hvenv) will now appear at the start of each command line.

Copy the SOFT-IO-LI files to your local directory /home/user/SOFT-IO-LI/

If you are using Jupyter lab copy the *.ipynb files, otherwise copy the .py
and corresponding .sh files.

Each programme contains the imports first and if the hvenv environment is
correctly activated there will be no problems with the imports.

The paths are set next.

You will need the change the /user/ to your user id for the paths.

Once this is done you should be able to run the programmes and see the output.

Any problems send a mail to catherine.mackay@aero.obs_mip.fr

********************************************************************************
## FLEXPART requirements

SOFT-IO-LI uses FLEXPART release 10.4 and the following files in the source code
were modified:

### par_mod.f was modified at line 143 to allow for the 0.5?? ERA5 ECMWF data.

flexpart10.4/flexpart_v10.4_3d7eebf/src/ contains 3 FLEXPART compilations:

- FLEXPART for 1??:
integer,parameter :: nxmax=361,nymax=181,nuvzmax=138,nwzmax=138,nzmax=138,nxshift=359 ! 1.0 degree 138 level

- FLEXPART_05 for 0.5??:
integer,parameter :: nxmax=721,nymax=361,nuvzmax=138,nwzmax=138,nzmax=138,nxshift=359  ! 0.5 degree 138 level

- FLEXPART 0.25 for 0.25??
integer,parameter :: nxmax=1441,nymax=721,nuvzmax=138,nwzmax=138,nzmax=138,nxshift=359  ! 0.25 degree 138 level

SOFT-IO-LI uses FLEXPART_05 as default.

### makefile was modified to allow compilation on nuwa.



