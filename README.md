# vasp-scripts
Scripts related to the Vienna Ab-initio Simulation Package

## Format
Script names should follow the general convention `purpose_software_platform` where, in this case, `software` will always be 'vasp'. Please comment your code __heavily__ as a courtesy to those who are not familiar with it.

## Descriptions

### compile_vasp_hipergator.sh
Compiles the vasp executable and creates a `VASP_BIN` environment variable which points to its location. This script dynamically installs the `makefile.include` located in the `resources` directory at runtime so any changes to that file may break this script. The script expects the path to the vasp tarball as its first and only command line argument as shown below.
```
# I strongly recommend installing in ~/usr/local

$ cd ~/usr/local
$ bash compile_vasp_hipergator.sh vasp.5.4.4.tar.gz # or some other path
```

### runjob_vasp_hipergator.sh
Template for a vasp job submission script on hipergator. Execute it in the following way, assuming you have copied it into your simulation directory. 
```
$ sbatch runjob_vasp_hipergator.sh
```
