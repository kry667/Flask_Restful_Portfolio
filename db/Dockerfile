FROM mysql:latest

ENV MYSQL_ROOT_PASSWORD=my-secret-pw
ENV MYSQL_DATABASE=my-database
ENV MYSQL_USER=my-user
ENV MYSQL_PASSWORD=my-password

# COPY init.sql /docker-entrypoint-initdb.d/

EXPOSE 3306

CMD ["mysqld"]
