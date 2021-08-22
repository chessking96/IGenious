# Sound Mixed-Precision tuning
## Installation
### Prerequsites
- IGen: https://github.com/joaoriverd/IGen
- Precimonious: https://github.com/corvette-berkeley/precimonious
  - LLVM-3.0
  - gcc/g++ 4.8
  - python2.7
- HiFPTuner:  https://github.com/ucd-plse/HiFPTuner
- Docker


### Instructions
We tested this installation guide on Ubuntu 20.04:
- Clone this repository
- Clone IGen and follow the install instructions
- Clone Precimonious
- Clone HiFPTuner repository

#### Install LLVM-3.0 and precimonious
(Instruction from HiFPTuner repository)

Make sure that gcc/g++-4.8 is installed and active, otherwise the following script will not work. Also make sure that python 2.7 is installed.
Run the following statement:

```bash
cd $HOME && \
wget http://llvm.org/releases/3.0/clang+llvm-3.0-x86_64-linux-Ubuntu-11_10.tar.gz && \
tar -xzvf clang+llvm-3.0-x86_64-linux-Ubuntu-11_10.tar.gz && \
mv clang+llvm-3.0-x86_64-linux-Ubuntu-11_10 llvm-3.0 && \
rm -f clang+llvm-3.0-x86_64-linux-Ubuntu-11_10.tar.gz && \
echo "export LLVM_VERSION=llvm-3.0" >> ~/.bashrc && \
echo "export PATH=$HOME/\$LLVM_VERSION/bin:$PATH" >> ~/.bashrc && \
echo "export LD_LIBRARY_PATH=$HOME/\$LLVM_VERSION/lib:$LD_LIBRARY_PATH" >> ~/.bashrc && \
echo "export CPATH=$HOME/\$LLVM_VERSION/include:." >> ~/.bashrc && \
echo "export LLVM_COMPILER=clang" >> ~/.bashrc && \
sudo apt-get install python-dev -y && \
cd && \
wget -qnc http://prdownloads.sourceforge.net/scons/scons-2.4.0.tar.gz && \
tar xzvf scons-2.4.0.tar.gz && \
rm -f scons-2.4.0.tar.gz && \
mv scons-2.4.0 scons && \
cd scons && \
sudo python2.7 setup.py install && \
cd .. && \
cd $HOME/precimonious/src && \
sed -i "s/SHLINKFLAGS='-Wl',/SHLINKFLAGS='',/g" SConscript && \
sed -i "s/LIBS='LLVM-\$llvm_version'/#LIBS='LLVM-\$llvm_version'/g" SConscript && \
echo $PATH && \
printenv && \
scons -Uc && \
scons -U && \
scons -U test && \
cd
```

Now switch back to current version of gcc/g++ and python3.

#### Install HiFPTuner
- Pull docker container and run
```bash
docker pull hguo15/hifptuner:v0
docker run -ti --name=hi hguo15/hifptuner:v0
```

#### Install IGenious
- Replace ~/precimonious/scripts/dd2.py with ~/IGenious/src/dd2.py
- Replace ~/HiFPTuner/precimonious/scripts/dd2_prof.py with ~/IGenious/src/dd2_prof.py
- Set environment variables: $IGEN_PATH: /path/IGen, $SOURCE_PATH: /path/to/IGenious, $HIFP_PATH: /path/to/HiFPTuner, $CORVETTE_PATH: /path/to/precimonious
- Substitute in the **docker container** each occurence of '$auto_tuning' in /root/HiFPTuner/scripts/analyze.sh and in root/HiFPTuner/scripts/compile.sh with '/root/HiFPTuner'

## Usage
### Tuning
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
