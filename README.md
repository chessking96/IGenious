# Sound Mixed-Precision tuning
## Installation
### Prerequsites
- IGen: https://github.com/joaoriverd/IGen
- Precimonious: https://github.com/corvette-berkeley/precimonious
- HiFPTuner:  https://github.com/ucd-plse/HiFPTuner
- Docker
- LLVM-3.0

### Instructions
We tested this installation guide on Ubuntu 20.04:
- Clone this repository
- Clone IGen and follow the install instructions:
- Clone Precimonious
- Clone HiFPTuner repository

### Install LLVM-3.0
(Instruction from HiFPTuner repository)

cd $HOME && \
wget http://llvm.org/releases/3.0/clang+llvm-3.0-x86_64-linux-Ubuntu-11_10.tar.gz && \
tar -xzvf clang+llvm-3.0-x86_64-linux-Ubuntu-11_10.tar.gz && \
mv clang+llvm-3.0-x86_64-linux-Ubuntu-11_10 llvm-3.0 && \
rm -f clang+llvm-3.0-x86_64-linux-Ubuntu-11_10.tar.gz

#### Install HiFPTuner
- Pull docker container and run
```bash
docker pull hguo15/hifptuner:v0
docker run -ti --name=hi hguo15/hifptuner:v0
```

#### Install IGenious
- Replace ~/precimonious/scripts/dd2.py with ~/IGenious/src/dd2.py
- Replace ~/HiFPTuner/precimonious/scripts/dd2_prof.py with ~/IGenious/src/dd2_prof.py
- Set environment variables: $SOURCE_PATH: /path/to/IGenious, $HIFP_PATH: /path/to/HiFPTuner, $CORVETTE_PATH: /path/to/precimonious
- Substitute in the <mark>docker container<mark/> each occurence of '$auto_tuning' in /root/HiFPTuner/scripts/analyze.sh and in root/HiFPTuner/scripts/compile.sh with '/root/HiFPTuner/'

## Usage
This examples does sound mixed-precision tuning on dot.c, an implementation of the dot product.

```bash
python scripts/run_igenious examples/dot settings
```

When the tuning is done, there is a file called 'out_dot.c', a sound and tuned version of 'dot.c'.

### Settings file
In the settings file are important information for the tuning process. 4 declarations are mandatory:
- file_name: The file name of the input program, for example dot.c
- entry_function: The name of the entry function, for example dot
- arguments: Providing information about the arguments
- return: Providing information about the return type

The following declarations are optional:
- repetitions_input: The number of different random inputs generated and tested, standard is 100
- target_accuracy: The target accuracy of the output, standard is 10
- error_type: 'highest_relative' or 'highest_absolute', standard is 'highest_relative'
- vectorized: use vectorized or non-vectorized version of IGen, standard is 'yes'
- max_iterations: The maximal number of explorations of Precimonious/HiFPTuner after they timeout, standard is 500
- tuning_algorithm: 'hifptuner' or 'precimonious', standard is 'precimonious'
- input_precision: 'dd' or 'd', standard is 'dd'
- input_range: The range, of which numbers are generated, standard is 10.

For an example of a settings file look at the example folder.
