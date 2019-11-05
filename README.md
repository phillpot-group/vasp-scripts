# vasp-scripts
Scripts related to the Vienna Ab-initio Simulation Package

## Format
Script names should follow the general convention `purpose_software_platform` where, in this case, `software` will always be 'vasp'. Please comment your code __heavily__ as a courtesy to those who are not familiar with it.

## Descriptions

### runjob_vasp_hipergator.sh
Template for a vasp job submission script on hipergator. Execute it in the following way, assuming you have copied it into your simulation directory. 
```
$ sbatch runjob_vasp_hipergator.sh
```
