FROM ubuntu:20.04 AS build
WORKDIR /app
COPY ./requirements.txt /app
RUN apt-get update && apt-get install python3 -y && apt-get install python3-pip -y && pip install --upgrade pip
RUN pip install -r ./requirements.txt

FROM ubuntu:20.04
RUN apt-get update && apt-get install python3 -y && apt-get install libgomp1
RUN echo /opt/serving/lib > /etc/ld.so.conf.d/faceapi.conf && ldconfig
COPY --from=build /usr/local/lib/python3.8/dist-packages /usr/local/lib/python3.8/dist-packages
VOLUME ["/Users/aichao/Desktop/serving","/opt/serving"]
WORKDIR /opt/serving
ENV PYTHONPATH=/usr/local/lib/python3.8/dist-packages
EXPOSE 9026
#CMD ["/bin/bash"]
CMD ["python3","run.py"]