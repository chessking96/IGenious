FROM ubuntu:14.04

WORKDIR /root
Run sudo apt-get -y update -y
Run sudo apt-get install wget
Run sudo apt-get install python-pip -y

Run sudo apt-get install dialog apt-utils -y
Run sudo apt-get install build-essential -y
Run sudo apt-get install git -y
Run sudo apt-get install software-properties-common -y
Run sudo apt-get install vim -y
Run sudo apt-get install python-dev -y

Run wget http://llvm.org/releases/3.0/clang+llvm-3.0-x86_64-linux-Ubuntu-11_10.tar.gz && \
   tar -xzvf clang+llvm-3.0-x86_64-linux-Ubuntu-11_10.tar.gz && \
   mv clang+llvm-3.0-x86_64-linux-Ubuntu-11_10 llvm-3.0 && \
   rm -f clang+llvm-3.0-x86_64-linux-Ubuntu-11_10.tar.gz

Run wget http://releases.llvm.org/3.8.0/clang+llvm-3.8.0-x86_64-linux-gnu-ubuntu-14.04.tar.xz && \
   tar -xvf clang+llvm-3.8.0-x86_64-linux-gnu-ubuntu-14.04.tar.xz && \
   mv clang+llvm-3.8.0-x86_64-linux-gnu-ubuntu-14.04 llvm-3.8 && \
   rm -f clang+llvm-3.8.0-x86_64-linux-gnu-ubuntu-14.04.tar.xz

Run echo "export LLVM_VERSION=llvm-3.0" >> ~/.bashrc && \
   echo "export PATH=$HOME/\$LLVM_VERSION/bin:$PATH" >> ~/.bashrc && \
   echo "export LD_LIBRARY_PATH=$HOME/\$LLVM_VERSION/lib:$LD_LIBRARY_PATH" >> ~/.bashrc && \
   echo "export CPATH=$HOME/\$LLVM_VERSION/include:." >> ~/.bashrc && \
   echo "export LLVM_COMPILER=clang" >> ~/.bashrc
 
ENV LLVM_VERSION=llvm-3.0
ENV	PATH="/root/$LLVM_VERSION/bin:${PATH}"
ENV LD_LIBRARY_PATH="/root/$LLVM_VERSION/lib:${LD_LIBRARY_PATH}"
ENV LLVM_COMPILER=clang
ENV CORVETTE_PATH="/root/precimonious"

Run cd
Run wget -qnc http://prdownloads.sourceforge.net/scons/scons-2.4.0.tar.gz && \
   tar xzvf scons-2.4.0.tar.gz && \
   rm -f scons-2.4.0.tar.gz && \
   mv scons-2.4.0 scons && \
   cd scons && \
   sudo python2.7 setup.py install && \
   cd ..

Run git clone https://github.com/ucd-plse/precimonious.git && \
   cd precimonious && \
   echo "export CORVETTE_PATH=$HOME/precimonious" >> ~/.bashrc && \
   cd ..

ENV CORVETTE_PATH="/root/precimonious"

Run cd $HOME/precimonious/src && \
   sed -i "s/SHLINKFLAGS='-Wl',/SHLINKFLAGS='',/g" SConscript && \
   sed -i "s/LIBS='LLVM-\$llvm_version'/#LIBS='LLVM-\$llvm_version'/g" SConscript && \
   echo $PATH && \
   printenv && \
   scons -Uc && \
   scons -U && \
   scons -U test && \
   cd

Run sudo apt-get -y install curl 
Run curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py
Run sudo python get-pip.py

Run sudo apt-get install -y graphviz 
Run sudo apt-get install -y graphviz-dev 
Run sudo apt-get install -y libgraphviz-dev 
Run sudo apt-get install -y python-matplotlib
Run sudo pip install 'decorator==4.3.0'
Run sudo pip install 'networkx==2.2'
Run sudo pip install python-louvain
Run sudo pip install graphviz
Run sudo pip install pygraphviz
   
Run sudo apt-get install -y bc

Run cd && git clone https://github.com/ucd-plse/HiFPTuner.git

Run echo "export HIFPTUNER_PATH=$HOME/HiFPTuner" >> ~/.bashrc && \
   echo "export HIFP_PRECI=$HOME/HiFPTuner/precimonious" >> ~/.bashrc && \
   echo "export LD_LIBRARY_PATH=\$HIFP_PRECI/logging:\$LD_LIBRARY_PATH" >> ~/.bashrc && \
   echo "export LIBRARY_PATH=\$HIFP_PRECI/logging" >> ~/.bashrc

ENV HIFPTUNER_PATH="$HOME/HiFPTuner"


Run cd $HOME/HiFPTuner/precimonious/logging && \
   make clean; make && cd

ENV LLVM_VERSION=llvm-3.8
ENV	PATH="/root/$LLVM_VERSION/bin:${PATH}"
ENV LD_LIBRARY_PATH="/root/$LLVM_VERSION/lib"
ENV CPATH="/root/$LLVM_VERSION/include:."
   

Run cd $HOME/HiFPTuner/src/varDeps && \
   make clean; make
