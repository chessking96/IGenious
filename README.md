# Master thesis - Sound Mixed Precision tuning
## Installation

#### Prerequsites
- IGen
- Precimonious
- HiFPTuner

#### Setup
From Ubuntu 20.04:
- Install IGen
- Install gcc/g++ 4.8
- Install precimonious
- Modify Precimonious:
  - copy/replace dd2.py from this repo into precimonious scripts folder
- Switch back to newer gcc version


## Usage
This example might run for a very long time.
```bash
./scripts/rerun.sh examples/DFT16/ DFT16.c DFT16 DFT16
```
