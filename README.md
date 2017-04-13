# JWST Ramp Visualizer
Visualize MULTIACCUM Ramp Patterns for JWST

## Usage
The notebook `ramp_visualizer_usage.ipynb` shows example usage.

Here is an example in iPython
```
from ramp_vis import plot_ramps, multiaccum, compare_ramps
%matplotlib
ramp = multiaccum('SHALLOW4',nint=4,ngroup=5)
plot_ramps(ramp)
```
![Alt text](/docs/shallow4_example.png?raw=true "SHALLOW4 example")
