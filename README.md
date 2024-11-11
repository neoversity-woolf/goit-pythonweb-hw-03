# Web Application with Python

This is a simple Python-based web application that serves two HTML pages (index.html and message.html). The application also handles form submissions, saves messages to a JSON file, and displays them on a separate page. The app runs on port 3000.

## Features

- Routing:
  - The application serves two pages: `index.html` and `message.html`.
  - It handles static files like `style.css` and `icons`.
- Form Handling:
  - On the `message.html` page, users can submit their `username` and `message`.
  - The form data is converted into a dictionary and stored in a JSON file (`data.json`) in the `storage` directory. The timestamp of each submission is used as the key.
- Displaying Messages:
  - The `/read` route returns a page that lists all stored messages from data.json using a Jinja2 template.
- Error Handling:
  - If a 404 error occurs (i.e., an invalid URL), the app serves a custom `error.html` page.
- Storage:
  - The messages are stored in `storage/data.json`, where the key is the timestamp when the message was submitted.

 ## Folder Structure

 The project structure looks like this:
```
/goit-pythonweb-hw-03
├── assets/
│   ├── favicon.png
│   ├── logo.png
│   └── style.css
├── storage/
│   └── data.json
├── webserver/
│   └── main.py
├── .dockerignore
├── docker-compose.yaml
├── Dockerfile
├── index.html
├── message.html
├── read.html
├── error.html
└── requirements.txt
```

## How to Run the Application Locally

### 1. Clone the Repository

```bash
git clone https://github.com/neoversity-woolf/goit-pythonweb-hw-03
cd goit-pythonweb-hw-03
```
### 2. Install Dependencies
Install the required Python dependencies:

```bash
pip install -r requirements.txt
```

### 3. Run the Application
To run the app locally, use the following command:

```bash
python3 webserver/main.py
```

This will start the Python server on http://localhost:3000.

### 4. Access the Application

- Open your browser and go to `http://localhost:3000/` to access the homepage (`index.html`).
- You can submit a message on the `message.html` page, and the message will be saved in `storage/data.json`.
- To view all stored messages, visit `http://localhost:3000/read`.
- If you visit an invalid route, the app will show a custom `error.html` page.

## Docker Compose (Optional)

If you'd like to use Docker Compose for managing the Docker containers:

### 1. Build the Docker Image
```bash
docker-compose up
```

This will start the application inside a container and make it available at `http://localhost:3000`.


## License

This project is open-source and available under the [MIT License](LICENSE).


