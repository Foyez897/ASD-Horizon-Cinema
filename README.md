Horizon Cinemas Booking System (HCBS)

Overview
Horizon Cinemas Booking System (HCBS) is a cinema ticket booking system designed to streamline the booking and cancellation process for users. The system includes features like film listings, showtimes, ticket booking, cancellations, and a user-friendly GUI. It supports multiple user roles including Admin, Manager, and Booking Staff. The project follows agile development principles and implements a full-stack system with backend and frontend functionalities.

Key Features:
	•	Film Listings & Showtimes: View films and their respective showtimes.
	•	Ticket Booking & Pricing: Book tickets with price calculations based on cinema, showtime, and seat type.
	•	Cancellations & Refund Rules: Support for booking cancellations with 50% refund if canceled at least 1 day before the showtime.
	•	Admin, Manager, and Booking Staff Views: Role-based views for managing bookings, films, and cinemas.
	•	Secure Login & Access Control: User authentication and access control for different roles.
	•	Database Management: SQLite database to manage bookings, users, cinemas, showtimes, and more.
	•	GUI Development: Simple, intuitive graphical interface using Tkinter (or another GUI library).
	•	Testing: Automated testing for booking, cancellation, and authentication.
	•	System Design: Use case diagrams, class diagrams, and sequence diagrams for the system architecture.

 Project Structure:
├── controllers/     # Logic handlers
├── views/           # GUI windows
├── models/          # Data abstraction
├── database/        # SQLite setup and DB file
├── static/          # Images/logos
├── tests/           # Unit & integration tests
├── main.py          # Entry point
├── README.md
└── requirements.txt

    
Installation
 1.	Clone the repository: git clone https://github.com/yourusername/horizon-cinemas-booking-system.git

    	
 2.	Navigate to the project directory:cd horizon-cinemas-booking-system

 3.	Create and activate the virtual environment: python3 -m venv .venv
source .venv/bin/activate  # For macOS/Linux
.venv\Scripts\activate     # For Windows

 4.	Install required dependencies: pip install -r requirements.txt
 
 
Usage
 1.	Start the GUI Application:
Run the main.py file to start the GUI for the cinema booking system: python main.py

 2.	Accessing the Database:
The database file horizon_cinemas.db is located in the database/ folder. Use SQLite to interact with it: sqlite3 database/horizon_cinemas.db

 3.	Testing the System:
You can run tests with the following command: PYTHONPATH=. python tests/test_booking.py

Database Structure
The project uses an SQLite database (horizon_cinemas.db) with the following tables:
	•	users: Stores user information (admin, manager, booking staff).
	•	cinemas: Information about the cinemas including city, location, and number of screens.
	•	films: Stores details about films like title, genre, age rating, etc.
	•	showtimes: Defines showtimes for films in each cinema.
	•	seats: Defines the seats for each showtime with availability and pricing.
	•	bookings: Stores booking records for each user, including seat allocation and total price.
	•	cancellations: Tracks canceled bookings and refund amounts.
	•	pricing: Defines pricing for different cinemas and showtimes.

▶️ Usage:
python main.py

Contributing
Contributions are welcome! Please fork this repository, create a new branch, and submit a pull request with your changes.

Steps to contribute:
	1.	Fork the repository.
	2.	Create a new feature branch (git checkout -b feature-name).
	3.	Commit your changes (git commit -m 'Add new feature').
	4.	Push to the branch (git push origin feature-name).
	5.	Open a pull request.

License
This project is licensed under the MIT License - see the LICENSE file for details.