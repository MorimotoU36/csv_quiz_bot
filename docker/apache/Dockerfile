FROM centos:7

RUN yum -y update && yum clean all

# Apache2.4のインストール
RUN yum -y install httpd

# Apacheの自動起動設定
RUN systemctl enable httpd

CMD ["/sbin/init"]

# Python3のインストール
RUN yum install python3 -y

# ディレクトリの指定
WORKDIR /usr/src/app
# Flaskの設定
ENV FLASK_APP=app

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:ja
ENV LC_ALL en_US.UTF-8

# requirements.txtのコピー
COPY flask/requirements.txt ./

# Flaskインストール（requirements.txtをもとに）
RUN pip3 install -r requirements.txt