import datetime
import os
import platform
import locale

def store_header(text, option1, option2):
    header = f"{option1.ljust(40)}{option2.rjust(33)}"
    store_name = f"{Constants.STORE_NAME} {text}"
    print_line()
    print(f"#{store_name.center(75)}#")
    print_line()
    print(f"# {header} #")
    print(f"# Date: {str(Constants.DATE).ljust(38)}Cart Items: {str(len(Cart.items)).rjust(3, '0')} | {format_currency(Cart.total_price)} #")
    print_line()

def format_currency(amount):
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    return locale.currency(amount, grouping=True).rjust(11, ' ')

class Inventory:
    items = []

    def print_list(self):
        print(f"PRODUCT ID".ljust(12) + "PRODUCT NAME".ljust(32) + "PRICE".ljust(24) + "QUANTITY")
        for product_id, product, price, stock in self.items:
            if stock <= Constants.MIN_INVENTORY_AMT:
                low_stock= "(LOW STOCK)"
            else:
                low_stock =""
            print(f"{str(product_id).ljust(6)}\t\t{product.ljust(20)}\t\t\t{price}\t\t\t\t\t{int(stock)} {low_stock}")

    def add_to_cart(self, productId, productAmt):
        for i, item in enumerate(inventory.items):
            
             #check if the item if already in the cart and update it
            for index, citem in enumerate(Cart.items):
                if productId == citem[0]:
                    
                    #update existing cart info
                    Cart.items[index] = (citem[0], productAmt + citem[1])
                    #update cart total price
                    addedPrice = item[2] * productAmt
                    Cart.total_price += addedPrice
                
                    self.items[index] = (item[0], item[1], item[2], item[3]-productAmt)
                    
                    return
            
            if item[0] == productId:
                if productAmt <= item[3]:
                    Cart.items.append((item[0], productAmt))
                    Cart.total_price += productAmt * item[2]
                    self.items[i] = (item[0], item[1], item[2], item[3]-productAmt)
                else:
                    print("Product amount not available")
                return
        print("Product not found")

    def add_to_inventory(self, name, price, quantity):
        self.items.append((len(self.items)+1, name, price, int(quantity)))

    def load_inventory(self):
        init_list = [
            (1, "Chicken", 1200.00, 10),
            (2, "Bread", 125.00, 50),
            (3, "Butter", 150.00, 30),
            (4, "Ice Cream", 250.00, 50),
            (5, "Laundry Detergent", 780.00, 40),
            (6, "Mop", 160.00, 25),
            (7, "Broom", 150.00, 20),
            (8, "Sheet Set", 1500.00, 10),
            (9, "Pillows", 700.00, 35),
            (10, "Towels", 675.00, 18)
        ]

        for item in init_list:
            self.items.append(item)
        print("")

class Cart:
    items = []
    total_price = 0.0
    subtotal_price = 0.0
    payment = 0.0

    def print_list(self):
        print(f"PRODUCT ID".ljust(25) + "PRODUCT NAME".ljust(20) + "PRICE".ljust(23) + "QUANTITY")
        for key, amt in self.items:
            for item_id, name, price, stock in inventory.items:
                if item_id == key:
                    print(f"{str(item_id).ljust(25)}{str(name).ljust(20)}{str(price).ljust(23)}{int(amt)}")
                    break  # end loop once found.

    def clear(self):
        self.items = []
        self.total_price = 0.0
        self.subtotal_price = 0.0
        self.payment = 0.0

class Constants:
    STORE_NAME = "Best Buy Retail Store"
    MIN_INVENTORY_AMT = 5
    SALES_TAX = 1.10
    DATE = datetime.date.today()

inventory = Inventory()
inventory.load_inventory()
cart = Cart()

def store_front():
    store_header("(STORE FRONT)","Press [I] To View Inventory [X] to Exit", "Press [C] To View Cart")
    inventory.print_list()

def store_cart():
    store_header("(CART)","Press [S] View Store [R] Remove Item", "Press [P] To Check Out")
    cart.print_list()

def store_inventory():
    store_header("(INVENTORY)","Press [S] To View Store", "Press [A] To Add Item")
    inventory.print_list()

def valid_input(label, opt=None):
    while True:
        try:
            key_input = input(label)
            if opt is None:
                opt = [-999]
            if key_input.upper() in opt:
                return key_input.upper()
            else:
                value = float(key_input)
                if value <= 0.0:
                    print("Invalid amount must be greater than 0 (" + str(value) + ")")
                else:
                    return value
        except ValueError:
            print("Invalid input, please retry")

def show_invoice():
    store_header("(RECEIPT)", "Please Come Back", "Thanks For Shopping")
    cart.print_list()
    print_line()
    discount = 0.0
    Cart.subtotal_price = Cart.total_price
    Cart.sales_tax = Cart.subtotal_price * Constants.SALES_TAX
    Cart.total_price = Cart.total_price * Constants.SALES_TAX
    if Cart.total_price > 5000:
      discount = Cart.total_price * 0.05
      Cart.total_price -= discount
    print(f"SUBTOTAL COST: ".ljust(18) + str(format_currency(Cart.subtotal_price)))
    print(f"SALES TAX (10%): ".ljust(18) + str(format_currency(Cart.sales_tax)))
    if discount > 0:
      print(f"DISCOUNT (5%): ".ljust(18) + str(format_currency(discount)))
    print(f"TOTAL COST: ".ljust(18) + str(format_currency(Cart.total_price)))
    print("CUSTOMER PAYMENT: ".ljust(18) + str(format_currency(Cart.payment)))
    print("CUSTOMER CHANGE: ".ljust(18) + str(format_currency(Cart.payment - Cart.total_price)))
    print_line()
    print("THANKS FOR SHOPPING".center(75))
    print_line()
    input("\nPress any key to continue!!!!")
    #cart.clear()
    Cart.total_price = 0.0
    Cart.payment = 0.0
    Cart.items = []


def remove_from_cart():
    prdId = valid_input("Enter Product ID to remove: ",)
    for i, (item_id, qty) in enumerate(Cart.items):
        if item_id == prdId:
            prdAmt = valid_input(f"Enter Amount to remove (max {qty}): ",)
            if prdAmt <= qty:
                Cart.items[i] = (item_id, qty-prdAmt)
                Cart.total_price -= prdAmt* next(item [2] for item in inventory.items if item [0] == item_id)
                for j, item in enumerate(inventory.items):
                    if item[0] == prdId:
                        inventory.items[j] = (item[0], item[1], item[2], item[3] + prdAmt)
                        break
                    if Cart.items[i][1] == 0:
                        Cart.items.pop(i)
                        print("Product removed from cart.")
                        store_cart()
                        return
                    else:
                        print("Product amount not available.")
                        return
    print("Product not found in cart.")

def is_string(variable):
    return isinstance(variable, str)
def print_line():
    print("".center(77, '#'))


screen = 'F'
while True:
    if screen == 'F':
        store_front()
        prdId = valid_input("ENTER PRODUCT ID TO ADD TO CART or [I/C/X]: ", ['I','C','X'])
        if is_string(prdId):
            if prdId.upper() in ['I','C','X']:
                screen = prdId
                continue
        prdAmt = valid_input("ENTER AMOUNT : ",)
        inventory.add_to_cart(prdId,prdAmt)
    elif screen == 'C':
        store_cart()
        val = valid_input(">>: ", ['S', 'P', 'R'])
        if is_string(val):
            if val.upper() in ['S','P', 'R']:
                screen = val
                continue
    elif screen == 'I':
        store_inventory()
        val = valid_input(">>: ", ['S', 'A'])
        if is_string(val):
            if val.upper() in ['S','A']:
                if val.upper() == 'A':
                    name = input("Enter Product Name: ")
                    price = valid_input("Enter Product Price: ")
                    quantity = valid_input("Enter Product Quantity: ")
                    inventory.add_to_inventory(name, price, quantity)
                screen = val
                continue
    elif screen == 'P':
        Cart.payment = valid_input("Enter Customer Payment Amount: H for home screen: ", ['H'])
        if is_string(Cart.payment):
            if Cart.payment.upper() in ['H']:
                screen = 'F'
                continue
        elif Cart.payment < Cart.total_price:
            print(f"Can not process payment value of {Cart.payment} is less then total {Cart.total_price}")
        else:
            screen = 'V'
    elif screen == 'R':
        remove_from_cart()
        screen = 'C'
    elif screen == 'V':
        show_invoice()
        screen = 'F'
    elif screen == 'X':
        print("Goodbye")
        exit()
    else:
        screen = 'F'