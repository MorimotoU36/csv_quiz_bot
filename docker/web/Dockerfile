FROM centos:7

RUN yum -y update && yum clean all

# Apache2.4のインストール
RUN yum -y install httpd

# ドキュメントルートを設定する
ENV APACHE_DOCUMENT_ROOT /usr/src/app
# sedコマンドを使ってapacheのconfファイルのドキュメントルートの設定も書き換える必要があります。
RUN sed -i 's/\/var\/www\/html/\/usr\/src\/app/g' /etc/httpd/conf/httpd.conf
RUN sed -i 's/\/var\/www\//\/usr\/src\/app/g' /etc/httpd/conf/httpd.conf

# Apacheの自動起動設定
RUN systemctl enable httpd

CMD ["/sbin/init"]

# サーバーのアドレス設定
ENV SERVER http://localhost:8080/

# アプリケーションディレクトリを作成する
WORKDIR /usr/src/app

# nodejs npm パッケージをインストールします
RUN yum install -y epel-release
RUN yum install -y nodejs npm

# Install app dependencies (package.json and package-lock.json)
COPY package*.json ./
RUN npm install