### Image Browsing App

This project is part of my coursework assignment. It is a simple image browsing web application built with Flask and Bootstrap. The application allows users to upload, manage, and explore images with a seamless masonry layout and lazy loading functionality.

### Features

- User authentication (login, signup, and logout)
- Image upload and management
- Explore images in a masonry layout
- Lazy loading of images to optimize performance
- Prevents reloading of already loaded images

### Technologies Used

- Flask (Python web framework)
- Bootstrap (CSS framework for responsive design)
- JavaScript (for dynamic content loading)
- Jinja2 (for templating)
- Flask-Login (for user session management)
- MySQL (for data storage)

### Prerequisites

- Python 3.x
- pip (Python package installer)
- MySQL database

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/image-browsing-app.git
   cd image-browsing-app
   ```

2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```

### Configuration

1. Create the MySQL database and user:
   ```sql
   CREATE DATABASE photogallery;
   USE photogallery;
   CREATE USER 'photogallery'@'%' IDENTIFIED BY 'asdasdasd123123123';
   CREATE TABLE users (
       NAME CHAR(20) NOT NULL,
       PASSWORD CHAR(32) NOT NULL,
       PRIVILEGE CHAR(5) NOT NULL,
       EMAIL CHAR(32) NOT NULL,
       PRIMARY KEY (NAME)
   );
   ```

2. Create a file named `.env` in the root directory of the project and add the following configuration:
   ```plaintext
   SECRET_KEY=your_secret_key
   SQLALCHEMY_DATABASE_URI=mysql+pymysql://photogallery:asdasdasd123123123@localhost/photogallery
   ```

3. Ensure the `static/uploads` directory exists:
   ```sh
   mkdir -p static/uploads
   ```

### Running the Application

1. Start the Flask application:
   ```sh
   flask run
   ```

2. Open your web browser and navigate to `http://127.0.0.1:5000/`.

### Project Structure

```plaintext
image-browsing-app/
│
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── static/
│   ├── css/
│   │   └── styles.css     # Custom CSS styles
│   ├── js/
│   │   └── scripts.js     # Custom JavaScript
│   └── uploads/           # Uploaded images
└── templates/
    ├── base.html          # Base template
    ├── index.html         # Home page template
    ├── login.html         # Login page template
    ├── signup.html        # Signup page template
    ├── manage.html        # Image management page template
    └── explore.html       # Image exploration page template
```

### Routes

- `/` - Home page
- `/login` - Login page
- `/signup` - Signup page
- `/logout` - Logout route
- `/manage` - Image management page (requires login)
- `/explore` - Image exploration page
- `/random_images` - API endpoint to fetch random images for lazy loading

### Contributing

1. Fork the repository.
2. Create a new branch: `git checkout -b my-feature-branch`.
3. Make your changes and commit them: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin my-feature-branch`.
5. Submit a pull request.

### License

This project is licensed under the MIT License.

### Acknowledgements

- [Flask](https://flask.palletsprojects.com/)
- [Bootstrap](https://getbootstrap.com/)
- [Masonry](https://masonry.desandro.com/)
- [ImagesLoaded](https://imagesloaded.desandro.com/)
