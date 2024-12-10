# FixToFlip 🏡💰
# <a name="https://fixtoflip.azurewebsites.net/">https://fixtoflip.azurewebsites.net/</a>
![Screenshot 2024-12-10 134813](https://github.com/user-attachments/assets/2e6ccbd2-fe19-46ae-8b00-2792355ebf4e)


# FixToFlip

**FixToFlip** is a Django-based web application designed to manage real estate investments. It provides users with the tools to manage properties, track expenses, create offers, and calculate credit details, all in a user-friendly environment.


## Features

### 1. **Accounts**
- User Authentication: Utilizes Allauth authentication system for secure user registration and login, including support for Google Login.
- Profile editing and account deletion.
  
![Screenshot 2024-12-10 141543](https://github.com/user-attachments/assets/cb3ad29b-c39b-4eb1-b466-8bded0f5fe48)

### 2. **Properties**

- Manage property details, including location, type, size, and other information.
- Record financial details such as purchase price and repair costs.
- Add and categorize property expenses with notes.
- REST API for managing property data.
  
![Screenshot 2024-12-10 142725](https://github.com/user-attachments/assets/b74e4cc6-7de0-4fb3-87a0-8f0ff2c0388a)
![Screenshot 2024-12-10 142821](https://github.com/user-attachments/assets/0a88fbed-f56f-41e2-84a2-9e9accbac28b)
![Screenshot 2024-12-10 145932](https://github.com/user-attachments/assets/df85a180-f895-468b-a57a-db78ea11261d)
![Screenshot 2024-12-10 145953](https://github.com/user-attachments/assets/43a1f170-38af-4968-bbcf-e596752ef725)

### 3. **Credits**

- Manage credits with principal amounts, interest rates, and monthly payments.
- Track credit payments and calculate remaining balances.
  
![Screenshot 2024-12-10 142316](https://github.com/user-attachments/assets/1fdaf20f-58c4-467d-9689-cc349ea6fcee)
![Screenshot 2024-12-10 142331](https://github.com/user-attachments/assets/edd86d0f-63c7-4cc9-aca1-3477f2150105)
![Screenshot 2024-12-10 142400](https://github.com/user-attachments/assets/95aeef01-0851-4603-ac81-824abf65af38)

### 4. **Offers**

- Create, edit, and manage property offers.
- Upload featured images for offers using Cloudinary.
- Publicly accessible REST API for viewing offers.

![Screenshot 2024-12-10 142612](https://github.com/user-attachments/assets/818d611c-8dad-4b90-8e7a-edd225ab296e)

### 5. **Blog**

- Create, read, update, and delete blog posts.
- Moderate and delete comments.
- Add comments with ReCaptcha protection.
- Categorize and tag blog posts for better organization.
- REST API for blog posts and categories.
  
![Screenshot 2024-12-10 141740](https://github.com/user-attachments/assets/7341e2cf-cd14-4bb7-a4a7-430b9eafb549)
![Screenshot 2024-12-10 142052](https://github.com/user-attachments/assets/a6eba91c-6cb4-4b8a-b416-4e2e124e740e)
![Screenshot 2024-12-10 142106](https://github.com/user-attachments/assets/3795ce7c-67d3-4a53-afc4-2c404f01e386)
![Screenshot 2024-12-10 142115](https://github.com/user-attachments/assets/241c7bac-2a83-428a-bf7e-07cad82fc65f)

## API Endpoints

The **FixToFlip** project provides RESTful APIs for interacting with various resources. Below is a list of available endpoints:

---

### **Accounts**
| Method | Endpoint                | Description                                 |
|--------|-------------------------|---------------------------------------------|
| POST   | `/api/token/`            | Authenticates a user and returns access and refresh tokens. |
| POST   | `/api/token/refresh/`    | Get new token with refresh token.                    |

---

### **Blog**
| Method | Endpoint                      | Description                                  |
|--------|-------------------------------|----------------------------------------------|
| GET    | `/api/blog/`            | Retrieves all blog posts.                   |
| GET    | `/api/blog/{slug}/`     | Retrieves a single blog post by slug.       |
| GET    | `/api/blog/categories/`       | Retrieves all blog categories.              |
| GET    | `/api/blog/categories/{id}/`  | Retrieves a single blog category by ID.     |

---

### **Offers**
| Method | Endpoint                      | Description                                  |
|--------|-------------------------------|----------------------------------------------|
| GET    | `/api/offers/`                | Retrieves all published offers.              |
| GET    | `/api/offers/{id}/`           | Retrieves details of a specific offer.       |

---

### **Properties**
| Method | Endpoint                          | Description                                  |
|--------|-----------------------------------|----------------------------------------------|
| GET    | `/api/properties/`                | Retrieves all owned properties.                   |
| GET    | `/api/properties/{id}/`           | Retrieves details of a specific owned property.   |
| GET    | `/api/properties/{id}/expenses/`  | Retrieves all expenses of a specific owned property.   |
| POST    | `/api/properties/{id}/expenses/add/`| Add expenses for a specific owned property.   |
| POST   | `/api/properties/`               | Creates a new property.                     |
| POST   | `/api/properties/bulk/`          | Creates bulk properties.                     |
---

## Key Technologies

- **Backend**: Django, Django REST Framework
- **Frontend**: HTML, CSS, JavaScript (Bootstrap-based templates)
- **Database**: PostgreSQL
- **Media Management**: Cloudinary
- **Asynchronous Tasks**: Celery with Redis
- **Security**: ReCaptcha, email verification

## Additional Applications and Libraries

The **FixToFlip** project utilizes the following third-party applications and libraries to extend its functionality:

### **Django Allauth**

- Used for user authentication, including email verification and Google login integration.

### **Django REST Framework (DRF)**

- Provides tools for building RESTful APIs, including serializers, viewsets, and permissions.

### **djmoney**

- Handles monetary fields with currency support, used in credits, offers, and properties.

### **Celery Beat**

- Extends Celery to manage periodic tasks, ensuring scheduled processes are executed correctly.

### **Redis**

- Acts as a message broker for Celery tasks.

### **Django Cities Light**

- Used for managing location data, such as countries and cities, in property-related functionality.

### **Django PhoneNumber**

- Provides support for validating and formatting phone numbers using the `phonenumbers` library.
- Ensures phone numbers are stored in a consistent format and are valid for their country.

### **Django Unfold**

- Enhances the Django admin interface with modern, responsive design.
- Provides better usability and a clean layout for managing the application through the admin panel.

---

## Installation

1. Make .env File

   * See SampleEnv.txt


2. To run FixToFlip locally, follow these steps:

   ```bash
   git clone https://github.com/your-username/FixToFlip.git
   
   cd FixToFlip
   
   python -m venv venv
   
   source venv\Scripts\activate
   
   pip install -r requirements.txt
   
   python manage.py migrate

   python manage.py collectstatic

   sudo systemctl start redis

   celery -A FixToFlip worker --loglevel=info

   celery -A FixToFlip beat --loglevel=info
   
   python manage.py update_rates
   
   python manage.py cities_light
   
   python manage.py runserver
   ```