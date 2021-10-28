#使うDockerイメージ
FROM mysql

#ポートの設定
EXPOSE 3306

#ロケール設定
RUN apt-get update
RUN apt-get -y install locales-all

ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8

#MySQL設定ファイルをコピー
COPY ./my.cnf /etc/mysql/conf.d/my.cnf

#docker run時の実行コマンド
CMD ["mysqld"]