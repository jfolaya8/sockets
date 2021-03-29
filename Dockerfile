FROM ubuntu:latest
MAINTAINER EUGENIO jfolaya8@gmail.com
RUN apt-get update && apt-get -y install bash python3 python3-pip net-tools iputils-ping nano vim
RUN pip3 install sockets pickle-mixin enquiries threaded
expose 80