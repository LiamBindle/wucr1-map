FROM continuumio/miniconda3

COPY GRAY_LR_SR_W.tif /GRAY_LR_SR_W.tif

RUN conda install -c conda-forge matplotlib numpy scikit-image xarray palettable

# 
RUN conda install -c conda-forge cython proj geos shapely pyshp six

RUN apt-get install -y build-essential

RUN pip install git+https://github.com/SciTools/cartopy.git
# RUN git clone https://github.com/SciTools/cartopy.git \
# && cd cartopy \
# && python setup.py install