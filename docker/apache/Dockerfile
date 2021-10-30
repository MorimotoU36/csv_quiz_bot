FROM centos:7

RUN yum -y update && yum clean all

# Apache2.4のインストール
RUN yum -y install httpd

# Apacheの自動起動設定
RUN systemctl enable httpd

CMD ["/sbin/init"]