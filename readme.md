# E-hotels

E-hotels is a web application for customers and employees of hotel chains to use.

The application allows customers to search for hotel rooms based of certain criteria such as price, hotel chain, hotel rating, room capacity, and location. Customers can also book rooms and manager their bookings.

The application allows employees to manage hotels of a hotel chain, hotel rooms, and customer bookings.

The web application was built using Typescript and Next JS for the frontend and Python, Flask, and PostgreSQL for the backend.

## Installing Project

To install the project, follow these steps:

Clone the repository to your local machine: `git@github.com:alexander-azizi-martin/e-hotel.git`

Navigate to the project directory: `cd e-hotel`

## Frontend

### Prerequisites

Before you begin, ensure you have met the following requirements:

- [Node.js](https://nodejs.org/en) installed
- [Yarn](https://yarnpkg.com/) installed

Yarn can be installed by running: `npm install -g yarn`

### Installing Frontend

To install the frontend dependencies, follow these steps:

Navigate to the frontend directory: `cd frontend`

Install dependencies: `yarn install`

### Running the Frontend

To run the project, follow these steps:

Start the development server: `yarn dev`

Open your browser and go to http://localhost:3000

Create a `.env` file in the `/frontend` directory.

In the file, include the following lines: 

```
NEXT_PUBLIC_URL=(the URL the backend is running on. The flash app should print to the consol running on URL. Use that URL here.)
```

### Building the Frontend for Production

To build the project for production, follow these steps:

Run the build command: `yarn build`

Start the server: `yarn start`

Open your browser and go to http://localhost:3000

## Backend

### Prerequisites

Before you begin, ensure you have met the following requirements:

- [Python](https://www.python.org/doc/) installed
- [PostgreSQL](https://www.postgresql.org/) installed

### Installing the backend

To install the backend dependencies, follow these steps:

Navigate to the backend directory: `cd backend`

Install dependencies by running the following in your command line: `pip install -r requirements.txt`

Setup an environment variable file of format `.env` in the root backend directory.

In the file, include the following lines: 

```
DB_HOST=localhost
DB_PORT=(add your postgresql database port here -- typically 5432)
DB_NAME=(add your postgresql database name here)
DB_USER=(add your postgresql database user here -- typically postgres)
DB_PASSWORD=(add your database password here)
SECRET_KEY=mysecretkey
DEBUG=False
JWT_SECRET_KEY=mynotsosecretkey
```

### Running the Backend

To run the project, follow these steps:

Start the development server: run `python backend/core_api/run.py` in the root directionry