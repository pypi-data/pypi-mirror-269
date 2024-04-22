# use sky launch to create a VM with base image
# then run this script to setup the VM

conda install -n base --override-channels -c conda-forge mamba 'python_abi=*=*cp*'


# install miniforge
wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh -O $HOME/Miniforge3-Linux-x86_64.sh
bash $HOME/Miniforge3-Linux-x86_64.sh -b -p $HOME/miniforge3
echo 'export PATH=$HOME/miniforge3/bin:$PATH' >>$HOME/.bashrc
source $HOME/.bashrc
rm -f $HOME/Miniforge3-Linux-x86_64.sh
mamba init bash
exec bash

which python

conda config --add channels defaults
conda config --add channels bioconda
conda config --add channels pytorch
conda config --add channels conda-forge

# optional tools
sudo apt update -y
sudo apt install -y npm
sudo npm install -g vtop

# filestore
sudo apt-get install -y nfs-common
sudo mkdir -p /mnt/filestore
sudo chmod 777 /mnt/filestore
sudo mount 192.168.179.186:/filestore /mnt/filestore

# install tools
pip install --upgrade pip

# torch
mamba install -y pytorch torchvision torchaudio -c pytorch -c nvidia

# other tools
mamba install -y cupy macs2 macs3 gh pandas dask jupyterlab mallet pytables \
scikit-learn seaborn xarray zarr pyarrow htslib samtools pysam pyBigWig pynndescent \
pyranges snakemake ipywidgets transformers black gcsfs isort pybedtools biopython nvtop nodejs pillow
pip install bioframe snapatac2==2.6 allcools wmb jupyterlab-code-formatter \
jupyterlab_execute_time cooler leidenalg opentsne papermill scanpy bolero wandb pre-commit 

# clean
conda clean -a -y
mamba clean -a -y
pip cache purge
