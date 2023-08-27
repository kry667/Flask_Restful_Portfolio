FROM mysql:latest

ENV MYSQL_DATABASE my-database

COPY init.sql /docker-entrypoint-initdb.d/

EXPOSE 3306

CMD ["mysqld"]