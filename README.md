# JWST Ramp Visualizer
Visualize MULTIACCUM Ramp Patterns for JWST.
Note the many different possible modes: RAPID, BRIGHT1, BRIGHT2, SHALLOW2, SHALLOW4, MEDIUM2, MEDIUM8, DEEP2 and DEEP8.

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
