FROM guillaumeflorent/miniconda-pythonocc:3-0.18.3

MAINTAINER Guillaume Florent <florentsailing@gmail.com>

# For wx : libgtk2.0-0 libxxf86vm1
# Funily, installing libgtk2.0-0 seems to solve the XCB plugin not found issue for Qt !!
# For pyqt : libgl1-mesa-dev libx11-xcb1
# RUN apt-get update && apt-get install -y libgtk2.0-0 libxxf86vm1 libgl1-mesa-dev libx11-xcb1 && rm -rf /var/lib/apt/lists/*

# Other conda packages
# RUN conda install -y numpy wxpython pyqt matplotlib jinja2 pytest
RUN conda install -y numpy matplotlib jinja2 pytest
RUN conda install -y -c gflorent ccad

# ccad
#WORKDIR /opt
## ADD https://api.github.com/repos/osv-team/ccad/git/refs/heads/master version.json
#RUN git clone --depth=1 https://github.com/osv-team/ccad
#WORKDIR /opt/ccad
#RUN python setup.py install

# party
WORKDIR /opt
# ADD https://api.github.com/repos/osv-team/party/git/refs/heads/master version.json
RUN git clone --depth=1 https://github.com/osv-team/party
WORKDIR /opt/party
RUN python setup.py install
