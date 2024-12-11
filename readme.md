
# XTShop: E-Commerce Platform with Buyer and Seller Dashboards

XTShop is a fully functional e-commerce platform that provides separate dashboards for both buyers and sellers. The platform allows users to browse products, place orders, and manage sales efficiently. Sellers can manage their products, track sales, and generate shipping labels, while buyers can easily place orders and view their history.

## Key Features

### Buyer Features
1. **View Products**
   - Browse through a wide variety of products with details like name, price, description, and images.
   - Filter products based on categories, tags, and other attributes to make shopping easier.

2. **Place Orders**
   - Add products to the cart and proceed with checkout.
   - Choose payment methods and complete the purchase securely.

3. **Order History**
   - View past orders with details like order status, product list, and total price.
   - Track the status of current orders (e.g., "Pending", "Completed").

4. **Payment Integration**
   - Multiple payment options for smooth transactions during checkout.

---

### Seller Features
1. **Sales Dashboard**
   - View sales data broken down by time periods: *Today, Week, Month, Year, or All Time*.
   - Monitor total products sold and total revenue generated.
   - Get a breakdown of sales by product, including quantities sold and revenue.

2. **Order Management**
   - Manage orders by their status: *Pending Labels, Completed, or other custom statuses*.
   - Paginated order view for easy navigation through large order volumes.
   - Export orders to PDF with labels for shipping and logistics.

3. **Add New Products**
   - Add new products with comprehensive details including product name, price, MRP, brand, model name, color, tags, and images.
   - Link products to specific categories to make them easier to find.
   - Upload up to 5 images per product for detailed visuals.

4. **Order Details**
   - View order information including buyer details, product items, and order status.
   - Track the status of orders such as "Pending", "Completed", and more.

5. **PDF Label Generation**
   - Generate downloadable PDF labels for orders, making shipping and logistics easier.
---

## Technologies Used
- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: PostgreSQL or MySQL
- **PDF Generation**: xhtml2pdf
- **Pagination**: Django's built-in Paginator

## Setup and Installation


1. **Install dependencies:**
   Create a virtual environment and install the required Python packages.
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Set up the database:**
   - Set up PostgreSQL or MySQL and update the `DATABASES` settings in `settings.py`.
   - Run migrations:
     ```bash
     python manage.py migrate
     ```

3. **Create a superuser (for admin access):**
   ```bash
   python manage.py createsuperuser
   ```

4. **Run the development server:**
   ```bash
   python manage.py runserver 80
   ```

4. **Access the application:**
   Open your browser and go to `http://127.0.0.1`.

---

## Usage

- **Seller Dashboard:**  
   Sellers can log in to their account to manage products, track sales, and generate PDF labels for orders.

- **Buyer Dashboard:**  
   Buyers can browse products, place orders, and view their order history from their dashboard.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
