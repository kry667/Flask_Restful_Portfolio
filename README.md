# Flask_Restful_Portfolio
Learning and training with flask, flask-restful and communication between microservices while creating a portfolio web application.


Web Application Overview:

Welcome to the Web Application Documentation for our microservices-based platform. This application is designed to manage employees and customers' data efficiently. It's divided into multiple microservices, each with a specific role and function. Below, we provide an overview of each microservice and how they work together to deliver a seamless user experience.

Microservices:

1. App
The App microservice is responsible for the application's front-end, including HTML and CSS, as well as the back-end built with Flask. It acts as the user interface, receiving queries from users and sending them as requests to other services such as employee_crud, customers_crud, and auth. The App service does not connect directly to the database but relies on other microservices to retrieve and manipulate data. It also renders HTML with the queried data.

2. Employee CRUD
Employee CRUD serves as a middleman between the SQL database and the rest of the services. It's built using Flask, RESTful API principles, and SQLAlchemy. This microservice handles Create, Read, Update, and Delete (CRUD) operations on employee records. It receives HTTP requests, performs the necessary database operations, and returns requested data or status responses. To protect its resources, it utilizes Flask-JWT-Extended for authentication and authorization.

3. Customers CRUD
Similar to Employee CRUD, the Customers CRUD microservice is responsible for CRUD operations on customer records. It interacts with the SQL database, processes HTTP requests, and returns data or status responses. It also employs Flask-JWT-Extended for resource protection.

4. DB (Database)
The DB microservice represents the MySQL database where both employee and customer data are stored. It serves as the central repository for all data operations. Other microservices interact with this database to retrieve and manipulate data. The DB microservice is crucial for data persistence and integrity.

5. Auth
Auth is responsible for user authentication and token generation. It's built with Flask and plays a pivotal role in generating JSON Web Tokens (JWT) upon successful login. These tokens are securely stored in a shared Redis database under an identifier, which is then saved in flask session to be accessible for all servises. The tokens are used for subsequent authentication when accessing protected resources.

6. Redis
Redis serves as a shared database used for storing JWT tokens and facilitating communication between microservices. It ensures that tokens are accessible across all services and can be efficiently validated for secure user access.

Deployment
All microservices are containerized in separate Docker containers and communicate within a common Docker network. To simplify installation, we provide a Docker Compose file (docker-compose.yml) that builds and runs these containers. You can follow these steps to set up and run the application:

# Installation:

1. Ensure Docker is installed on your system.

2. Create a Docker network:

```
docker network create my-network1
```
3. Clone this repository.

4. Create .env with:
```
MYSQL_HOST=db
MYSQL_USER=user
MYSQL_PASSWORD=password
MYSQL_DB=my-database
MYSQL_ROOT_PASSWORD=secret-pass
JWT_SECRET_KEY=jwt-secret-key
```

5. Inside repo folder use the provided docker-compose.yml file to build and run the images:
```
docker-compose build
```
```
docker-compose up -d
```

The images required for the web application are hosted on Docker Hub, so no additional image building is necessary.
