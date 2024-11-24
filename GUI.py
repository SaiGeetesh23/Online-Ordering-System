import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import matplotlib.pyplot as plt
from datetime import datetime


PRODUCTS_FILE = 'products.txt'
USERS_FILE = 'users.txt'
ORDERS_FILE = 'orders.txt'


catalog = {
    1: {"name": "Customize T-shirts", "price": 50, "stock": 20, "category": "Clothing"},
    2: {"name": "Re-usable Bags", "price": 10, "stock": 40, "category": "Handmade Objects"},
    3: {"name": "Tote Bags", "price": 10, "stock": 30, "category": "Handmade Objects"},
    4: {"name": "Handmade Jewellery", "price": 50, "stock": 20, "category": "Accessories"},
    5: {"name": "Organic Hair Products", "price": 30, "stock": 10, "category": "Beauty Products"},
    6: {"name": "UpCycled Furniture", "price": 50, "stock": 10, "category": "Furniture"},
    7: {"name": "Customize Phone Cases", "price": 50, "stock": 10, "category": "Accessories"}
}
def save_products(products):
    with open(PRODUCTS_FILE, 'w') as f:
        for product_id, details in products.items():
            f.write(f"{product_id},{details['name']},{details['price']},{details['stock']},{details['category']}\n")

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        for username, details in users.items():
            f.write(f"{username}|{details['password']}|{details['role']}\n")

def save_orders(orders):
    with open(ORDERS_FILE, 'w') as f:
        for order in orders:
            f.write(f"{order['order_id']}|{order['username']}|{order['total']}|{order['address']}\n")

def initialize_files():
    try:
        with open(PRODUCTS_FILE, 'r') as f:
            pass
    except FileNotFoundError:
        save_products(catalog)
    
    try:
        with open(USERS_FILE, 'r') as f:
            pass
    except FileNotFoundError:
        with open(USERS_FILE, 'w') as f:
            pass
    
    try:
        with open(ORDERS_FILE, 'r') as f:
            pass
    except FileNotFoundError:
        with open(ORDERS_FILE, 'w') as f:
            pass

initialize_files()


def load_products():
    products = {}
    with open(PRODUCTS_FILE, 'r') as f:
        for line in f:
            if line.strip():
                product_id, name, price, stock, category = line.strip().split(',')
                products[int(product_id)] = {"name": name, "price": float(price), "stock": int(stock), "category": category}
    return products

def load_users():
    users = {}
    try:
        with open(USERS_FILE, 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    if len(parts) >= 3:
                        username, password, role = parts[0], parts[1], parts[2]
                        users[username] = {"password": password, "role": role, "address": "", "cart": {}}
    except FileNotFoundError:
        print(f"Error: The file '{USERS_FILE}' was not found.")
    return users

def load_orders():
    orders = []
    try:
        with open(ORDERS_FILE, 'r') as f:
            for line in f:
                if line.strip():
                    order_id, username, total, address = line.strip().split('|')
                    orders.append({"order_id": order_id, "username": username, "total": float(total), "address": address, "items": []})
    except FileNotFoundError:
        print(f"Error: The file '{ORDERS_FILE}' was not found.")
    return orders

class OnlineOrderingSystem(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Online Ordering System")
        self.geometry("800x500")
        self.configure(bg="#333333")

        self.users = load_users()
        self.products = load_products()
        self.orders = load_orders()
        self.current_user = None

        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure('TButton', font=('Helvetica', 12), padding=10)
        self.style.configure('TLabel', font=('Helvetica', 14))

        self.show_login_screen()

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        self.clear_screen()
        self.style = ttk.Style()
        self.style.configure("Custom.TFrame", background="#101314")
        self.style.configure("Custom.TLabel", background="#333333", foreground="#FFFFFF")
        self.style.configure("Custom.TButton", background="#FF3399", foreground="#FFFFFF", padding=6)
        frame = ttk.Frame(self, style="Custom.TFrame")
        frame.pack(pady=50)

        ttk.Label(frame, text="Login", style="Custom.TButton", font=("Arial", 30, "bold")).grid(row=0, column=0, columnspan=2, pady=20)
        ttk.Label(frame, text="Username", style="Custom.TButton").grid(row=1, column=0, padx=10, pady=10)
        username_entry = ttk.Entry(frame)
        username_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(frame, text="Password", style="Custom.TButton").grid(row=2, column=0, padx=10, pady=10)
        password_entry = ttk.Entry(frame, show='*')
        password_entry.grid(row=2, column=1, padx=10, pady=10)

        login_button = ttk.Button(frame, text="Login", style="Custom.TButton", command=lambda: self.login(username_entry.get(), password_entry.get()))
        login_button.grid(row=3, column=0, columnspan=2, pady=10)

        register_button = ttk.Button(frame, text="Register", style="Custom.TButton", command=self.show_register_screen)
        register_button.grid(row=4, column=0, columnspan=2, pady=10)

    def show_register_screen(self):
        self.clear_screen()
        self.style = ttk.Style()
        self.style.configure("Custom.TFrame", background="#101314")
        self.style.configure("Custom.TLabel", background="#333333", foreground="#FFFFFF")
        self.style.configure("Custom.TButton", background="#FF3399", foreground="#FFFFFF", padding=6)
        frame = ttk.Frame(self, style="Custom.TFrame")
        frame.pack(pady=50)

        ttk.Label(frame, text="Register", style="Custom.TButton", font=("Arial", 30, "bold")).grid(row=0, column=0, columnspan=2, pady=20)
        ttk.Label(frame, text="Username", style="Custom.TButton").grid(row=1, column=0, padx=10, pady=10)
        username_entry = ttk.Entry(frame)
        username_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(frame, text="Password", style="Custom.TButton").grid(row=2, column=0, padx=10, pady=10)
        password_entry = ttk.Entry(frame, show='*')
        password_entry.grid(row=2, column=1, padx=10, pady=10)

        ttk.Label(frame, text="Role (user/owner)", style="Custom.TButton").grid(row=3, column=0, padx=10, pady=10)
        role_entry = ttk.Entry(frame)
        role_entry.grid(row=3, column=1, padx=10, pady=10)

        register_button = ttk.Button(frame, text="Register", style="Custom.TButton", command=lambda: self.register(username_entry.get(), password_entry.get(), role_entry.get()))
        register_button.grid(row=4, column=0, columnspan=2, pady=10)

        back_to_login_button = ttk.Button(frame, text="Back to Login", style="Custom.TButton", command=self.show_login_screen)
        back_to_login_button.grid(row=5, column=0, columnspan=2, pady=10)

    def register(self, username, password, role):
        if username in self.users:
            messagebox.showerror("Error", "Username already exists.")
        else:
            self.users[username] = {'password': password, 'role': role, 'address': '', 'cart': {}}
            save_users(self.users)
            messagebox.showinfo("Success", "User registered successfully.")
            self.show_login_screen()

    def login(self, username, password):
        if username in self.users and self.users[username]['password'] == password:
            self.current_user = username
            role = self.users[username]['role']
            if role == 'owner':
                self.show_owner_dashboard()
            else:
                self.show_main_menu()
        else:
            messagebox.showerror("Error", "Invalid username or password.")


    def show_owner_dashboard(self):
        self.clear_screen()
        self.style = ttk.Style()
        self.style.configure("Custom.TFrame", background="#101314")
        self.style.configure("Custom.TLabel", background="#333333", foreground="#FFFFFF")
        self.style.configure("Custom.TButton", background="#FF3399", foreground="#FFFFFF", padding=6)
        frame = ttk.Frame(self, style="Custom.TFrame")
        frame.pack(pady=50)

        ttk.Label(frame, text="Owner Dashboard", style="Custom.TButton", font=("Arial", 24)).grid(row=0, column=0, columnspan=2, pady=20)
        ttk.Button(frame, text="Add Product", style="Custom.TButton", command=self.add_product_screen).grid(row=1, column=0, pady=10)
        ttk.Button(frame, text="View Products", style="Custom.TButton", command=self.show_products).grid(row=2, column=0, pady=10)
        ttk.Button(frame, text="Visualize Sales Data", style="Custom.TButton", command=self.visualize_order_statistics).grid(row=3, column=0, pady=10)
        ttk.Button(frame, text="Logout", style="Custom.TButton", command=self.show_login_screen).grid(row=4, column=0, pady=10)

    def add_product_screen(self):
        self.clear_screen()
        self.style = ttk.Style()
        self.style.configure("Custom.TFrame", background="#101314")
        self.style.configure("Custom.TLabel", background="#333333", foreground="#FFFFFF")
        self.style.configure("Custom.TButton", background="#FF3399", foreground="#FFFFFF", padding=6)
        frame = ttk.Frame(self, style="Custom.TFrame")
        frame.pack(pady=50)
        ttk.Label(frame, text="Add Product", style="Custom.TButton", font=("Arial", 24)).grid(row=0, column=0, columnspan=2, pady=20)

        ttk.Label(frame, text="Product Name", style="Custom.TButton").grid(row=1, column=0, padx=10, pady=10)
        name_entry = ttk.Entry(frame)
        name_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(frame, text="Price", style="Custom.TButton").grid(row=2, column=0, padx=10, pady=10)
        price_entry = ttk.Entry(frame)
        price_entry.grid(row=2, column=1, padx=10, pady=10)

        ttk.Label(frame, text="Stock", style="Custom.TButton").grid(row=3, column=0, padx=10, pady=10)
        stock_entry = ttk.Entry(frame)
        stock_entry.grid(row=3, column=1, padx=10, pady=10)

        ttk.Label(frame, text="category", style="Custom.TButton").grid(row=4, column=0, padx=10, pady=10)
        category_entry = ttk.Entry(frame)
        category_entry.grid(row=4, column=1, padx=10, pady=10)

        add_button = ttk.Button(frame, text="Add", style="Custom.TButton", command=lambda: self.add_product(name_entry.get(), price_entry.get(), stock_entry.get(),category_entry.get()))
        add_button.grid(row=5, column=0, columnspan=2, pady=10)

        back_button = ttk.Button(frame, text="Back", style="Custom.TButton", command=self.show_owner_dashboard)
        back_button.grid(row=6, column=0, columnspan=2, pady=10)


    def add_product(self, name, price, stock,category):
        try:
            price = float(price)
            stock = int(stock)
        except ValueError:
            messagebox.showerror("Error", "Invalid price or stock value.")
            return
    
        product_id = max(self.products.keys(), default=0) + 1
        self.products[product_id] = {"name": name, "price": price, "stock": stock,"category":category}
        print("Updated products:", self.products)  # Debugging line
    
        save_products(self.products)
        messagebox.showinfo("Success", "Product added successfully.")
        self.show_owner_dashboard()

    def visualize_order_statistics(self):
        order_totals = [order['total'] for order in self.orders]
        if not order_totals:
            messagebox.showerror("Error", "No orders to visualize.")
            return
        
        plt.figure(figsize=(10, 5))
        plt.plot(order_totals, marker='o')
        plt.title('Order Totals Over Time')
        plt.xlabel('Order Number')
        plt.ylabel('Total Amount ($)')
        plt.grid(True)
        plt.show()


    def show_main_menu(self):
        self.clear_screen()
        self.style = ttk.Style()
        self.style.configure("Custom.TFrame", background="#101314")
        self.style.configure("Custom.TLabel", background="#333333", foreground="#FFFFFF")
        self.style.configure("Custom.TButton", background="#FF3399", foreground="#FFFFFF", padding=6)
        frame = ttk.Frame(self, style="Custom.TFrame")
        frame.pack(pady=50)

        ttk.Label(frame, text="Main Menu", style="Custom.TButton", font=("Arial", 24)).grid(row=0, column=0, columnspan=2, pady=20)
        ttk.Button(frame, text="Browse Products", style="Custom.TButton", command=self.show_products).grid(row=1, column=0, columnspan=2, pady=10)
        ttk.Button(frame, text="View Cart", style="Custom.TButton", command=self.show_cart).grid(row=2, column=0, columnspan=2, pady=10)
        #ttk.Button(frame, text="Visualize Sales Data", style="Custom.TButton", command=self.visualize_order_statistics).grid(row=3, column=0,padx=40, pady=20)
        ttk.Button(frame, text="Previous Orders", style="Custom.TButton", command=self.show_orders).grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(frame, text="Logout", style="Custom.TButton", command=self.show_login_screen).grid(row=4, column=0, columnspan=2, pady=10)
    
    
    def show_products(self):
        self.clear_screen()
        self.style.configure("Custom.TFrame", background="#101314")
        frame = ttk.Frame(self, style="Custom.TFrame")
        frame.pack(pady=20)
    
    
        title_label = ttk.Label(frame, text="Product Catalog", style="Custom.TButton", font=("Arial", 24))
        title_label.grid(row=0, column=0, columnspan=2, pady=20)

        ttk.Label(frame, text="Filter by Category:", font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=10)
        category_combobox = ttk.Combobox(frame, values=["All"] + list({p['category'] for p in self.products.values()}))
        category_combobox.set("All")
        category_combobox.grid(row=1, column=1, padx=10, pady=10)
        category_combobox.bind("<<ComboboxSelected>>", lambda e: self.update_product_display(category_combobox.get()))

    
        product_list_frame = ttk.Frame(self)
        product_list_frame.pack(fill="both", expand=True)
    
        canvas = tk.Canvas(product_list_frame, borderwidth=0)
        scrollbar = ttk.Scrollbar(product_list_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
    
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.product_display_frame = scrollable_frame
        self.display_products(self.products, category_filter="All")

    
        self.back_button = ttk.Button(self, text="Back", command=self.go_back)
        self.back_button.pack(pady=20)


    def display_products(self, products, category_filter):
        """Displays products filtered by the selected category."""
        for widget in self.product_display_frame.winfo_children():
            widget.destroy()

        filtered_products = {k: v for k, v in products.items() if category_filter == "All" or v["category"] == category_filter}

        for row, (product_id, details) in enumerate(filtered_products.items(), start=2):
            product_frame = ttk.Frame(self.product_display_frame)
            product_frame.grid(row=row, column=0, sticky="ew", pady=5)

            product_label = ttk.Label(product_frame, text=f"{details['name']} - ${details['price']} - Stock: {details['stock']} - Category: {details['category']}")
            product_label.pack(side="left", padx=(0, 10), pady=5)
        
            add_to_cart_button = ttk.Button(product_frame, text="Add to Cart", command=lambda pid=product_id: self.add_to_cart(pid))
            add_to_cart_button.pack(side="right", padx=(10, 0), pady=5)



    def update_product_display(self, selected_category):
        """Updates the displayed products based on the selected category."""
        self.display_products(self.products, selected_category)


    def go_back(self):
        if self.current_user and self.users[self.current_user]['role'] == "owner":
            self.show_owner_dashboard()  # Return to the owner dashboard
        else:
            self.show_main_menu()  # Return to the user main page


    def add_to_cart(self, product_id):
        product = self.products[product_id]

    # Check if the product is out of stock
        if product['stock'] <= 0:
            messagebox.showerror("Error", "Product out of stock.")
            return

    # Prompt for the quantity
        def confirm_quantity():
            try:
                quantity = int(quantity_entry.get())
                if quantity <= 0:
                    raise ValueError("Quantity must be greater than zero.")
                if quantity > product['stock']:
                    messagebox.showerror("Error", f"Only {product['stock']} units available in stock.")
                    return
            
            # Add the product to the cart
                cart = self.users[self.current_user]['cart']
                if product_id in cart:
                    cart[product_id] += quantity
                else:
                    cart[product_id] = quantity
            
            # Deduct the stock
                product['stock'] -= quantity
                save_products(self.products)
                messagebox.showinfo("Success", f"{quantity} units of '{product['name']}' added to cart.")
                quantity_window.destroy()
            except ValueError as e:
                messagebox.showerror("Error", "Please enter a valid number.")

    # Create a new window for quantity input
        quantity_window = tk.Toplevel(self)
        quantity_window.title("Add to Cart")
        quantity_window.geometry("300x200")

        ttk.Label(quantity_window, text=f"Enter quantity for '{product['name']}':", font=("Arial", 14)).pack(pady=10)
    
        quantity_entry = ttk.Entry(quantity_window, font=("Arial", 12))
        quantity_entry.pack(pady=10)

        ttk.Button(quantity_window, text="Confirm", command=confirm_quantity).pack(pady=10)


    def show_cart(self):
        self.clear_screen()
        self.style = ttk.Style()
        self.style.configure("Custom.TFrame", background="#101314")  # purple background for cart
        self.style.configure("Custom.TLabel", background="#333333", foreground="#FFFFFF")
        self.style.configure("Custom.TButton", padding=6)

        frame = ttk.Frame(self, style="Custom.TFrame")
        frame.pack(pady=20)
        
        ttk.Label(frame, text="Your Cart", style="Custom.TButton", font=("Arial", 24)).pack(pady=10)
        total_cost = 0
        cart = self.users[self.current_user]['cart']
        
        for product_id, quantity in cart.items():
            product = self.products[product_id]
            product_frame = ttk.Frame(frame)
            product_frame.pack(pady=5, fill="x", padx=10)
            
            ttk.Label(product_frame, text=f"{product['name']} - ${product['price']} x {quantity}").pack(side="left")
            ttk.Button(product_frame, text="Remove", command=lambda pid=product_id: self.remove_from_cart(pid)).pack(side="right")
            
            total_cost += product['price'] * quantity
        
        ttk.Label(frame, text=f"Total: ${total_cost:.2f}", font=("Arial", 18)).pack(pady=20)
        
        checkout_button = ttk.Button(frame, text="Checkout", style="Custom.TButton", command=self.show_checkout_screen)
        checkout_button.pack(pady=10)
        
       # back_button = ttk.Button(frame, text="Back", command=self.show_main_menu)
       # back_button.pack(pady=10)
        back_button = ttk.Button(frame, text="Back", command=self.go_back)
        back_button.pack(pady=20)

    def remove_from_cart(self, product_id):
        cart = self.users[self.current_user]['cart']
        if product_id in cart:
            quantity = cart[product_id]
            if quantity > 1:
                cart[product_id] -= 1
            else:
                del cart[product_id]
            self.products[product_id]['stock'] += 1
            save_products(self.products)
            self.show_cart()

    def show_checkout_screen(self):
        self.clear_screen()
        frame = ttk.Frame(self, style="Custom.TFrame")
        frame.pack(pady=50)
        
        ttk.Label(frame, text="Checkout", style="Custom.TButton", font=("Arial", 24)).grid(row=0, column=0, columnspan=2, pady=20)
        
        ttk.Label(frame, text="Delivery Address").grid(row=1, column=0, padx=10, pady=10)
        address_entry = ttk.Entry(frame)
        address_entry.grid(row=1, column=1, padx=10, pady=10)
        
        place_order_button = ttk.Button(frame, text="Place Order", 
                                        command=lambda: self.place_order(address_entry.get()))
        place_order_button.grid(row=2, column=0, columnspan=2, pady=10)
        
        back_button = ttk.Button(frame, text="Back to Cart", command=self.show_cart)
        back_button.grid(row=3, column=0, columnspan=2, pady=10)

    def place_order(self, address):
        if not address:
            messagebox.showerror("Error", "Please enter a delivery address.")
            return

        order_id = f"{self.current_user}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        total_cost = sum(self.products[pid]['price'] * qty for pid, qty in self.users[self.current_user]['cart'].items())
        self.orders.append({"order_id": order_id, "username": self.current_user, "total": total_cost, "address": address})
        
        save_orders(self.orders)
        self.users[self.current_user]['cart'] = {}
        
        messagebox.showinfo("Success", f"Order placed successfully! Total: ${total_cost:.2f}")
        self.show_main_menu()

    def show_orders(self):
        self.clear_screen()
        frame = ttk.Frame(self, style="Custom.TFrame")
        frame.pack(pady=50)
        
        ttk.Label(frame, text="Your Previous Orders", style="Custom.TButton", font=("Arial", 24)).pack(pady=10)
        
        for order in self.orders:
            if order['username'] == self.current_user:
                order_frame = ttk.Frame(frame)
                order_frame.pack(pady=5, fill="x", padx=10)
                ttk.Label(order_frame, text=f"Order ID: {order['order_id']} - Total: ${order['total']:.2f}").pack(side="left")
                ttk.Label(order_frame, text=f"Address: {order['address']}").pack(side="right")
        
        back_button = ttk.Button(frame, text="Back", command=self.show_main_menu)
        back_button.pack(pady=20)
    
    

    def show_previous_orders(self):
        self.clear_screen()

        self.style = ttk.Style()
        self.style.configure("Custom.TFrame", background="#101314")
        self.style.configure("Custom.TLabel", background="#333333", foreground="#FFFFFF")
        self.style.configure("Custom.TButton", padding=6)

        frame = ttk.Frame(self, style="Custom.TFrame")
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        canvas = tk.Canvas(frame, background="#101314")
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        orders_frame = ttk.Frame(canvas, style="Custom.TFrame")
        canvas.create_window((0, 0), window=orders_frame, anchor="nw")

        ttk.Label(orders_frame, text="Previous Orders", font=("Arial", 24), style="Custom.TLabel").grid(row=0, column=0, columnspan=2, pady=20)

        user_orders = [order for order in self.orders if order['username'] == self.current_user]

        if not user_orders:
            ttk.Label(orders_frame, text="No previous orders found.", style="Custom.TLabel").grid(row=1, column=0, padx=10, pady=10)
        else:
            row = 1
            for order in user_orders:
                ttk.Label(orders_frame, text=f"Order ID: {order['order_id']} - Total: ${order['total']} - Address: {order['address']}", style="Custom.TLabel").grid(row=row, column=0, padx=10, pady=10)
                row += 1
            
                for item in order['items']:
                    product = self.products[item['product_id']]
                    ttk.Label(orders_frame, text=f"    {product['name']} - ${product['price']} x {item['quantity']}", style="Custom.TLabel").grid(row=row, column=0, padx=20, pady=5)
                    row += 1
        ttk.Button(orders_frame, text="Back", style="Custom.TButton", command=self.show_main_menu).grid(row=row, column=0, padx=10, pady=10)


app = OnlineOrderingSystem()
app.mainloop()
