FROM debian:latest

RUN apt-get update
RUN apt-get -y install build-essential git
RUN apt-get -y install wget

# Cinnamon
RUN apt-get -y install task-cinnamon-desktop

# Nutmeg
RUN git clone https://github.com/kitizz/nutmeg.git \
    && cd nutmeg \
    && git submodule init \
    && git submodule update

# Ginger
RUN wget https://github.com/Ginger-Automation/Ginger/releases/download/v4.5-Official/GingerRuntime.4.5.0.0.tar.gz \
    && gunzip GingerRuntime.4.5.0.0.tar.gz

# Cloves
RUN git clone https://github.com/Hey-Developer/cloves

# Allspice
RUN git clone https://github.com/igoryen/allspice
