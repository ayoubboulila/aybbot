FROM ubuntu:trusty

#RUN apt-get install xz-utils

RUN 	apt-get update \ 
	
	&& apt-get install -y nodejs \ 
	&& apt-get install -y npm \ 
	&&  ln -s /usr/bin/nodejs /usr/bin/node && node -v && npm -v \
	&& apt-get install -y nano \
	
	&& apt-get clean

ADD nodeApp /opt/nodeApp
ADD startup.sh /opt/startup.sh
RUN chmod +x /opt/startup.sh
EXPOSE 80
ENTRYPOINT /opt/startup.sh
