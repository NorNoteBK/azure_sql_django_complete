# Teaching Guide: Django Store & Product API

This guide is designed to help you explain and demonstrate the Django Store and Product API project.

## 1. Project Overview
This project is a RESTful API built with **Django** and **Django REST Framework (DRF)**.
It manages two main resources:
*   **Stores**: Physical locations.
*   **Products**: Items for sale (independent of stores).

## 2. Key Concepts to Explain

### A. Models (`api/models.py`)
- **What they are**: The blueprint for your database tables.
- **Code Highlights**:
    - `Store`: Has `store_id` and `store_location`.
    - `Product`: Has `name`, `description`, `price`.
    - `__str__`: Explain how this method makes object representation readable (e.g., in Admin).

### B. Serializers (`api/serializers.py`)
- **What they are**: Translators that convert complex data (Model instances) into native Python datatypes (and then JSON) and vice-versa.
- **Code Highlights**:
    - `StoreSerializer`, `ProductSerializer`.
    - `ModelSerializer`: Reduces boilerplate code by automatically creating fields from the Model.

### C. Views (`api/views.py`)
- **What they are**: The logic that handles HTTP requests and returns responses.
- **Code Highlights**:
    - `generics.ListCreateAPIView`: Handles `GET` (list) and `POST` (create).
    - `generics.RetrieveUpdateDestroyAPIView`: Handles `GET` (single), `PUT/PATCH`, and `DELETE`.
    - `api_root`: A custom functional view to show the API entry points at `/`.

### D. URLs (`azure_project/urls.py` & `api/urls.py`)
- **What they are**: The router. It matches the incoming URL path to a specific View.
- **Code Highlights**:
    - `api/urls.py`: Defines endpoints like `stores/`, `products/`.
    - `azure_project/urls.py`: The main entry point, including `api.urls` and the Admin site.

## 3. Lesson Plan & Demo Script

### Phase 1: Exploring the Existing Store API
*Goal: Understand how Django REST Framework works using the pre-built Store API.*

1.  **Start the Server**: `python manage.py runserver 8000`
2.  **Explore URL**: Go to `http://127.0.0.1:8000/api/stores/`.
    *   Explain the **List** view: Data comes from the database.
    *   Explain the **JSON** format.
3.  **Code Walkthrough**:
    *   **Model** (`api/models.py`): Show `Store` class.
    *   **Serializer** (`api/serializers.py`): Show `StoreSerializer`.
    *   **View** (`api/views.py`): Show `StoreList`.
    *   **URL** (`api/urls.py`): Show the path mapping.
    *   **Admin**: Show `Store` in Django Admin.

### Phase 2: Live Coding - Building the Product API
*Goal: Students follow along to build the Product API from scratch.*

#### Step 1: Create the Model
*   Open `api/models.py`.
*   **Task**: Create `Product` model with `name`, `description`, `price`.
*   **Action**: Add `Product` class.
*   **Migration**: Run `makemigrations` and `migrate`.

#### Step 2: Create the Serializer
*   Open `api/serializers.py`.
*   **Task**: Create `ProductSerializer`.
*   **Explain**: Inheriting from `ModelSerializer`.

#### Step 3: Create the Views
*   Open `api/views.py`.
*   **Task**: Create `ProductList` (for users to see products).
*   **Task**: Create `ProductDetail` (for updating/deleting).

#### Step 4: Wire up the URLs
*   Open `api/urls.py`.
*   **Task**: Add paths for `products/` and `products/<int:id>/`.

#### Step 5: Verification
*   Go to `http://127.0.0.1:8000/api/products/`.
*   Test creating a new Product (e.g., "Latte").

## 4. Common Questions
*   **Q: Why separate `api/urls.py`?**
    *   A: For modularity. If we had multiple apps, we'd want each to manage its own URLs.
*   **Q: What is `venv`?**
    *   A: It isolates this project's Python libraries from the rest of your system.
