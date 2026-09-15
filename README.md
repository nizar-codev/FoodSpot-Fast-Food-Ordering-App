# 🍔 FoodSpot – Fast Food Ordering App

**FoodSpot** is a fast-food ordering mobile application built with **Python and Kivy**. It provides a complete local ordering workflow, including food browsing, product selection, cart management, checkout, invoice generation, order history, and WhatsApp order sharing.

---

## 📱 About the Project

FoodSpot was developed as a university software development project to demonstrate mobile application development using Python and the Kivy framework.

The application allows users to browse food items, select quantities, add items to a cart, enter delivery information, generate invoices, save orders locally, view previous orders, and share order details through WhatsApp.

---

## ✨ Features

### 🏠 User Interface

* Splash/start screen
* Login screen
* Home screen
* Popular food items
* Full menu
* Product details screen
* Checkout screen
* Profile screen
* Order history screen
* Order details screen
* Scrollable layouts
* Modern card-based UI
* Rounded buttons and input fields

### 👤 User Profile

* Save customer name
* Save phone number
* Save email
* Save password
* Persistent login state
* Display saved profile information
* Skip login option
* Logout with confirmation

### 🍔 Food Ordering

* Browse popular food items
* Browse full menu
* View product images
* View product prices
* Open product details
* Increase or decrease quantity
* Add products to cart
* Automatically merge duplicate products in the cart

### 🛒 Shopping Cart

* Add multiple products
* Quantity management
* Automatic item totals
* Automatic cart item count
* Order summary
* Checkout from cart
* Cart reset after invoice generation

### 💳 Checkout

Customers can enter:

* Full name
* Phone number
* Delivery address

The checkout screen displays:

* Ordered items
* Quantities
* Individual item prices
* Subtotal
* Delivery charges
* Grand total

### 🚚 Delivery Charges

FoodSpot currently uses the following delivery rules:

| Order Subtotal   |   Delivery |
| ---------------- | ---------: |
| Rs 1000 or above |   **FREE** |
| Below Rs 1000    | **Rs 100** |

### 🧾 Invoice Generation

The application generates an invoice containing:

* FoodSpot branding
* Customer information
* Delivery address
* Ordered items
* Quantities
* Item prices
* Subtotal
* Delivery charges
* Grand total

Invoices are saved locally as **PNG images** inside the application's `Invoices` directory.

### 📚 Order History

Orders are stored locally using SQLite and can be viewed later.

Each saved order contains:

* Customer name
* Phone number
* Delivery address
* Ordered items
* Grand total
* Order date
* Invoice path

The newest orders are displayed first.

### 🔍 Order Details

Users can open a saved order to:

* View the generated invoice
* View order information
* Delete the order

When an order is deleted, the corresponding database record is removed and the saved invoice file is also deleted when available.

### 📱 WhatsApp Integration

The application can prepare an order message for WhatsApp containing:

* Customer name
* Phone number
* Delivery address
* Ordered items
* Quantities
* Item prices
* Subtotal
* Delivery charges
* Grand total

The generated WhatsApp link opens the order through the device's browser/WhatsApp handling.

---

## 💾 Local Database

FoodSpot uses **SQLite** for local data storage.

### `users` table

Stores:

* User ID
* Name
* Phone
* Email
* Password
* Login status

### `orders` table

Stores:

* Order ID
* Customer name
* Phone
* Address
* Ordered items
* Subtotal
* Delivery charge
* Grand total
* Order date
* Invoice path

The database is automatically created when the application starts.

---

## 🛠️ Technologies

* **Python 3**
* **Kivy**
* **Kivy Language**
* **SQLite**
* **Buildozer**
* **PyJNIus**
* **WhatsApp URL Integration**

---

## 📂 Project Structure

```text
FoodSpot/
│
├── main.py
├── main.kv
├── database.py
├── buildozer.spec
├── requirements.txt
├── README.md
│
├── images/
│   ├── food images
│   ├── menu images
│   ├── splash screen
│   └── login screen
│
└── Invoices/
    └── generated invoice images
```

> `foodspot.db` is generated locally by the application and should not be committed to GitHub if it contains personal or customer data.

---

## 🚀 Application Flow

```text
Start
  ↓
Login / Skip Login
  ↓
Home
  ↓
Food Menu
  ↓
Product Details
  ↓
Add to Cart
  ↓
Checkout
  ↓
Generate Invoice
  ↓
Save Order
  ↓
Order History
  ↓
View / Delete Order
```

---

## 📊 Current Project Status

🚧 **Under Development**

The current version provides a functional local food-ordering system with:

* User/profile management
* Food menu
* Product details
* Shopping cart
* Checkout
* Delivery charge calculation
* SQLite database
* Local order storage
* Invoice generation
* Invoice viewing
* Order history
* Order deletion
* WhatsApp order integration
* Android back-button navigation

---

## 🔮 Future Improvements

Potential future improvements include:

* Secure password hashing
* Improved authentication system
* Multiple user accounts
* Admin dashboard
* Product management
* Category management
* Search and filtering
* Cloud database
* Firebase integration
* Online payments
* Order status tracking
* Real-time order tracking
* Push notifications
* Backend/API integration

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/FoodSpot.git
```

### 2. Open the Project

```bash
cd FoodSpot
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python main.py
```

The SQLite database will be created automatically when the application starts.

---

## 📱 Android Build

The project uses **Buildozer** to package the Kivy application for Android.

Android build configuration is provided in:

```text
buildozer.spec
```

---

## 👨‍💻 Developer

**Nizar**

FoodSpot – Fast Food Ordering Application
