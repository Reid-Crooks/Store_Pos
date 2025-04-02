import datetime
import os
import platform
import locale

def store_header(text, option1, option2):
    header = f"{option1.ljust(40)}{option2.rjust(45)}"
    store_name = f"{Constants.STORE_NAME} {text}"
    print("\n\n\n\n\n\n")
    print_line()
    print(f"#{store_name.center(90)}#")
    print_line()
    print(f"# {header} #")
    print(f"# Date: {str(Constants.DATE).ljust(50)}Cart Items: {str(len(cart.items)).rjust(3, '0')} | {format_currency(cart.total_price)} #")
    print_line()

def format_currency(amount):
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    return locale.currency(amount, grouping=True).rjust(11, ' ')

class Inventory:
    items = []

    def print_list(self):
        print(f"PRODUCT ID"  + "PRODUCT NAME".ljust(32) + "PRICE".ljust(24) + "QUANTITY")
        for product_id, product, price, stock in self.items:
            print(f"{str(product_id).ljust(6)}\t\t{product.ljust(20)}\t\t\t{price}\t\t\t\t\t{int(stock)}")

    def add_to_cart(self, productId, productAmt):
                
        for i, item in enumerate(inventory.items):
                
            if item[0] == productId:
                
                if productAmt > item[3]:
                    print("Quantity cannot be more that inventory stock")
                    return
                                    
                #check if the item if already in the cart and update it
                for index, citem in enumerate(cart.items):
                    if productId == citem[0]:
                     
                        #update existing cart info
                        cart.items[index] = (citem[0], productAmt + citem[1])
                        #update cart total price
                        addedPrice = item[2] * productAmt
                        cart.total_price += addedPrice
                    
                        self.items[index] = (item[0], item[1], item[2], item[3]-productAmt)
                        
                        if item[3]-productAmt < 5 : 
                            #print low inventory alert 
                            print("\n")
                            print("####" + "ALERT".center(60) + "####")
                            print("\n Inventory Low!!!".rjust(50))
                            print("\n")
                        
                        return
                        
                #adds a new entry to the cart
                if productAmt <= item[3]:
                    cart.items.append((item[0], productAmt))
                    cart.total_price += productAmt * item[2]
                    self.items[i] = (item[0], item[1], item[2], item[3]-productAmt)
                        
                    if item[3]-productAmt < 5:
                        #print low inventory alert 
                        print("\n")
                        print("#" + "ALERT".center(60) + "#")
                        print("\n Inventory Low!!!")
                        print("\n")
                    
                else:
                    print("Product amount not available")
                return
        print("Product not found")

    def remove_from_cart(self, productId, quantity):
        for index, item in enumerate(cart.items):
            if productId == item[0]:
                
                for i, inventoryItem in enumerate(inventory.items):
                    
                    if productId == inventoryItem[0]:
                        if quantity > item[1]:
                            print("Quantity cannot be greater than the total amount in the cart ")
                            return 
                        
                        #removes only a specific number of items from the cart
                        if quantity < item[1]:
                            #reduce item amount in cart
                            cart.items[index] = (item[0], item[1] - quantity)      
                            #update total price
                            a = inventoryItem[2] * quantity
                            cart.total_price -= a
                            #update inventory stock
                            self.items[i] = (inventoryItem[0], inventoryItem[1], inventoryItem[2], inventoryItem[3]+quantity)      
                            return

                        #remove item from cart
                        cart.items.pop(index)                        
                        #adjust cart total price
                        total = item[1] * inventoryItem[2]
                        cart.total_price = cart.total_price-total
                        #adjust inventory stock
                        self.items[i] = (inventoryItem[0], inventoryItem[1], inventoryItem[2], inventoryItem[3]+item[1])
                        return
                        
                return
            else:
                print("Product not found")
                
    def add_to_inventory(self, name, price, quantity):
        self.items.append((len(self.items)+1, name, price, int(quantity)))

    def load_inventory(self):
        init_list = [
            (1, "Chicken", 1200.00, 10),
            (2, "Bread", 125.00, 50),
            (3, "Butter", 150.00, 30),
            (4, "Ice Cream", 250.00, 20),
            (5, "Laundry Detergent", 780.00, 40),
            (6, "Mop", 160.00, 25),
            (7, "Broom", 150.00, 15),
            (8, "Sheet Set", 1500.00, 100),
            (9, "Pillows", 700.00, 35),
            (10, "Towels", 675.00, 18)
        ]

        for item in init_list:
            self.items.append(item)
        print("")

class Cart:
    items = []
    total_price = 0.0
    payment = 0.0

    def print_list(self):
        print(f"PRODUCT ID".ljust(25) + "PRODUCT NAME".ljust(20) + "PRICE".ljust(23) + "QUANTITY")
        for key, amt in self.items:
            for item_id, name, price, stock in inventory.items:
                if item_id == key:
                    print(f"{str(item_id).ljust(25)}{str(name).ljust(20)}{str(price).ljust(23)}{str(amt)}")
                    break  # end loop once found.

    def clear(self):
        self.items = []
        self.total_price = 0.0
        self.payment = 0.0

class Constants:
    STORE_NAME = "Best Buy Retail Store"
    MIN_INVENTORY_AMT = 5
    DATE = datetime.date.today()

inventory = Inventory()
inventory.load_inventory()
cart = Cart()

def store_front():
    store_header("(STORE FRONT)","Press [I] to view Inventory", "Press [C] to view Cart OR Press [X] to Leave store")
    inventory.print_list()

def store_cart():
    store_header("(CART)","Press [S] to view store", "Press [P] to check out   Press [R] to remove an item")
    cart.print_list()

def store_inventory():
    store_header("(INVENTORY)","Press [S] to view Store", "Press [A] to add item")
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
    store_header("(RECEIPT)", "Please come back", "Thanks for shopping")
    cart.print_list()
    total = cart.total_price
    
    if cart.total_price > 5000:
        discount = (5/100) * cart.total_price
        total = cart.total_price - discount
        print("Customer Discount: ",discount)
        
    gct = (10/100)* total
    total = gct + total
    
    print_line()
    print(f"TOTAL COST {total}")
    print(f"CUSTOMER PAYMENT {cart.payment}")
    print(f"CUSTOMER CHANGE {cart.payment - total}")
    print(f"G.C.T: {gct}")
    print_line()
    print("THANKS FOR SHOPPING".center(75))
    print_line()
    input("\nPress any key to continue!!!!")
    #cart.clear()
    cart.total_price = 0.0
    cart.payment = 0.0
    cart.items = []

def is_string(variable):
    return isinstance(variable, str)
def print_line():
    print("".center(90, '#'))


screen = 'F'
while True:
    if screen == 'F':
        store_front()
        prdId = valid_input("ENTER PRODUCT ID TO ADD TO CART or [I, C, X]: ", ['I','C','X'])
        if is_string(prdId):
            if prdId.upper() == "X":
                print_line()
                print("\nGoodbye and shop with us again soon !!!\n")
                print_line()
                break
            
            if prdId.upper() in ['I','C']:
                screen = prdId
                continue
        prdAmt = valid_input("ENTER AMOUNT : ",)
        inventory.add_to_cart(prdId,prdAmt)
    elif screen == 'C':
        store_cart()
        val = valid_input(">>: ", ['S', 'P', 'R'])
        if is_string(val):
            if val.upper() == 'R':
                productID = valid_input("Please enter the ID of the product you would like to remove: ")
                quantity = valid_input("Please enter the quantity of items you would like to remove: ")
                inventory.remove_from_cart(productID, quantity)
                
            if val.upper() in ['S','P']:
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
        Cart.payment = valid_input("Enter Customer Payment Amount: X to exit: ", ['X'])
        if is_string(Cart.payment):
            if Cart.payment.upper() in ['X']:
                screen = 'F'
                continue
        elif Cart.payment < cart.total_price:
            print(f"Cannot process payment value of {Cart.payment} is less then total {cart.total_price}")
        else:
            screen = 'R'
    elif screen == 'R':
        show_invoice()
        screen = 'F'
    else:
        screen = 'F'