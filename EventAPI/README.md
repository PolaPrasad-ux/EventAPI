
# **Event Management and Ticketing System**

This project is a robust Event Management and Ticketing System built using Django, with APIs for user registration, event creation, and ticket purchasing. It includes role-based access control (Admin/User) and uses JWT for secure authentication.

---

## **Features**

### **User Management**
- **User Registration**:
  - Admin and regular users can register via API.
- **JWT Authentication**:
  - Secure login with `access` and `refresh` tokens.
- **Role-Based Permissions**:
  - Admins can create and manage events.
  - Users can view events and purchase tickets.

### **Event Management**
- **Admin-Only Features**:
  - Create and manage events.
- **Event Details**:
  - View all events (Admins and Users).

### **Ticket Purchasing**
- **User-Only Features**:
  - Purchase tickets for an event.
- **Validation**:
  - Ensures ticket availability before processing purchases.
- **Database Consistency**:
  - Uses atomic transactions to maintain data integrity.

### **Optimized Querying**
- SQL queries are optimized for large datasets, such as retrieving the top events by tickets sold.

---

## **Technologies Used**

### **Backend**
- **Django**: Framework for API development.
- **Django REST Framework (DRF)**: To create RESTful APIs.
- **JWT**: For secure user authentication and session management.

### **Database**
- **SQLite** (default, replaceable with PostgreSQL/MySQL for production).
- Indexed and optimized queries for better performance.

### **Tools**
- **Postman**: API testing and validation.

---

## **Installation Instructions**

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/event-management-system.git
   cd event-management-system
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate     # For Windows
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run the Server**:
   ```bash
   python manage.py runserver
   ```

6. **Access the APIs**:
   - API documentation can be tested via tools like **Postman**.

---

## **API Endpoints**

### **User Management**
- **Register**: `POST /register/`
- **Login**: `POST /login/`

### **Event Management**
- **Create Event**: `POST /events/` (Admin only)
- **View Events**: `GET /events/`

### **Ticket Purchasing**
- **Purchase Tickets**: `POST /events/<id>/purchase/` (User only)

---

## **Usage Examples**

### **1. Register a User**
**Endpoint**: `POST /register/`  
**Request Body**:
```json
{
    "username": "testuser",
    "password": "testpassword",
    "role": "User"
}
```

### **2. Create an Event (Admin Only)**
**Endpoint**: `POST /events/`  
**Request Body**:
```json
{
    "name": "Tech Conference 2024",
    "date": "2024-11-20",
    "total_tickets": 300
}
```

### **3. Purchase Tickets (User Only)**
**Endpoint**: `POST /events/<id>/purchase/`  
**Request Body**:
```json
{
    "quantity": 2
}
```

---

## **Database Schema**

### **1. User Table**
| Field        | Type       | Description           |
|--------------|------------|-----------------------|
| `id`         | Integer    | Primary key.          |
| `username`   | String     | Unique username.      |
| `password`   | String     | User password.        |
| `role`       | String     | `Admin` or `User`.    |
| `is_staff`   | Boolean    | Staff privilege.      |
| `is_superuser` | Boolean | Superuser privilege.  |

### **2. Event Table**
| Field          | Type       | Description                          |
|----------------|------------|--------------------------------------|
| `id`           | Integer    | Primary key.                        |
| `name`         | String     | Event name.                         |
| `date`         | Date       | Event date.                         |
| `total_tickets` | Integer   | Total tickets available.            |
| `tickets_sold` | Integer    | Number of tickets sold.             |

### **3. Ticket Table**
| Field          | Type       | Description                          |
|----------------|------------|--------------------------------------|
| `id`           | Integer    | Primary key.                        |
| `user_id`      | ForeignKey | Reference to the `User` table.      |
| `event_id`     | ForeignKey | Reference to the `Event` table.     |
| `quantity`     | Integer    | Number of tickets purchased.        |
| `purchase_date`| DateTime   | Timestamp of ticket purchase.       |


