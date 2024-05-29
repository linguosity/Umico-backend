
# Umico App Backend

🌐 **Live Demo**: [Umico App Backend](https://umicoframes-4f015aefac88.herokuapp.com/)

## 📜 Description

The backend of Umico is built using Django and provides robust support for managing orders, user roles, and artwork documentation. It ensures secure access and efficient processing of data to enhance user experience and operational efficiency.

## 🛠️ Technologies Used

- **Django**: v5.0.6
- **Django REST framework**: v3.15.1
- **Gunicorn**: v22.0.0
- **PostgreSQL**: via `psycopg2-binary` v2.9.9
- **Whitenoise**: v6.4.0
- **Python**: v3.x

## 🚀 Getting Started

### Installation

1. **Clone the repo**:
   ```sh
   git clone https://github.com/yourusername/umico-backend.git
   cd umico-backend
   ```

2. **Create and activate a virtual environment**:
   ```sh
   python -m venv env
   source env/bin/activate
   ```

3. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

4. **Run migrations**:
   ```sh
   python manage.py migrate
   ```

5. **Start the development server**:
   ```sh
   python manage.py runserver
   ```

## 📐 Entity Relationship Diagrams

_(Add ERD images here)_

## 📝 User Stories / MVP

### Order Management
- **Creating Different Types of Orders**: Support for scans, prints, frames, and custom requests.
- **Order Details**: Provide detailed views of each order to keep track of necessary information.
- **Due Dates and Client Information**: Maintain comprehensive records of clients’ personal and transaction details.
- **Advanced User Roles and Permissions**: Manage different user roles to control access levels.

### Access Control
- **Secure and appropriate access**: Secure and appropriate access to the application’s features.

### Artwork Handling
- **Work Order Visibility**: Allow both staff and clients to view work orders for tracking progress and outcomes.
- **Art Documentation**: Capability for recording and storing images of artwork before and after processing.

## 🚧 Future Features
- **Repeating Orders**: Facilitate easy reordering of previous orders.
- **Order Status Tracking**: Enable real-time tracking of order statuses.
- **Rush Orders**: Prioritize orders based on due dates.
- **Calculating Frame/Matte Size**: Automated calculations for framing processes.
- **Manual Input of Prices**: Allow manual entry of pricing information.
- **Tracking Deposits and Balance Payments**: Keep records of all financial transactions.
- **Float Requirement Calculation**: Automatically calculate the necessary float based on art and frame specifications.
- **Frame Size Calculation**: Determine the needed frame size when matting is included.

🧑‍🤝‍🧑 Link to User Stories
