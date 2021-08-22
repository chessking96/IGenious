# Sound Mixed-Precision tuning
## Installation
### Prerequsites
- IGen: https://github.com/joaoriverd/IGen
- Precimonious: https://github.com/corvette-berkeley/precimonious
- HiFPTuner:  https://github.com/ucd-plse/HiFPTuner
- Docker

We tested this installation guide on Ubuntu 20.04.
- Clone this repository
- Clone IGen and follow the install instructions:
- Clone Precimonious

### Install HiFPTuner
- Clone HiFPTuner
```bash
docker pull hguo15/hifptuner:v0
docker run -ti --name=hi hguo15/hifptuner:v0
```

### Install IGenious
- Replace ~/precimonious/scripts/dd2.py with ~/IGenious/src/dd2.py
- Replace ~/HiFPTuner/precimonious/scripts/dd2_prof.py with ~/IGenious/src/dd2_prof.py




- Install gcc/g++ 4.8
- Install precimonious
- Modify Precimonious:
  - copy/replace dd2.py from this repo into precimonious scripts folder
- Switch back to newer gcc version


## Usage
This example might run for a very long time.
```bash
python3 scripts/rerun.py examples/example/ example.c func example
```
