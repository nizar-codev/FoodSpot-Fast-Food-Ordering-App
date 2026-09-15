
import os
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.uix.popup import Popup 
from datetime import datetime
from kivy.core.window import Window
from kivy.properties import StringProperty, NumericProperty
Window.clearcolor = (0.96, 0.96, 0.96, 1)
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.factory import Factory
from kivy.utils import platform


from database import(
   create_database,save_user,
   get_user,show_users,
   get_logged_in_user,save_order, logout_user,show_orders,get_orders,delete_all_orders,add_invoice_column,delete_order
)

from kivy.utils import platform
if platform == "android":
    from jnius import autoclass
    from android.storage import primary_external_storage_path


class StartScreen(Screen):

    def on_enter(self):
        Clock.schedule_once(self.check_login, 8)

    def check_login(self, dt):
        user = get_logged_in_user()

        if user:
            self.manager.current = "home"
        else:
            self.manager.current = "login"

class LoginScreen(Screen):

    def on_enter(self):
        print("Login Screen Opened")
        
        user = get_logged_in_user()
        print("User found:", user)

        if user:
           self.ids.name_in.ids.field.text = user[1]
           self.ids.phone_in.ids.field.text = user[2]
           self.ids.email_in.ids.field.text = user[3]
           self.ids.pass_in.ids.field.text = user[4]
        
        else:
            self.ids.name_in.ids.field.text = ""
            self.ids.phone_in.ids.field.text = ""
            self.ids.email_in.ids.field.text = ""
            self.ids.pass_in.ids.field.text = ""


    def save_data(self,name,phone,email,password):
        if not name.strip() or not phone.strip() or not email.strip() or not password.strip():
            self.show_login_error("All fields are required.")
            return


        print("Name:", name)
        print("Phone:", phone)
        print("Email:", email)
        print("Password:", password)
       
        save_user(name, phone, email, password)
        show_users()

        print("User saved successfully!")

        self.manager.current = "home"

    def skip_login(self):
        print("User skipped login")
        self.manager.current = "home"
    

    def show_login_error(self, message):

        layout = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=[20, 30, 20, 15]
        )

        label = Label(
            text=f"[b]{message}[/b]\n\nOr tap 'Skip for now'.",
            markup=True,
            font_size="16sp",
            size_hint_y=None
        )
        label.bind(texture_size=lambda instance, value: setattr(instance, "height", value[1] + 10))

        ok_btn = Button(
            text="OK",
            bold=True,
            color=(1,1,1,1),
            background_normal="",
            background_down="",
            background_color=(0.93, 0.28, 0.05, 1),
            size_hint_y=None,
            height=40
        )

        layout.add_widget(label)
        layout.add_widget(ok_btn)

        popup = Popup(
            title="Login Required",
            content=layout,
            size_hint=(0.8, 0.25),
            auto_dismiss=False,
            separator_height=0,
            background="",
            background_color=(0.16, 0.16, 0.16, 1)
        )

        ok_btn.bind(on_press=popup.dismiss)

        popup.open()
    

class HomeScreen(Screen):
    pass

class MoreScreen(Screen):
    pass

class ProfileScreen(Screen):

    def on_enter(self):
        user = get_logged_in_user()

        if user:
            self.ids.name_field.value = user[1]
            self.ids.phone_field.value = user[2]
            self.ids.email_field.value = user[3]
            self.ids.password_field.value = "*" * len(user[4])
        
        else:
            self.ids.name_field.value = "Guest"
            self.ids.phone_field.value = "-"
            self.ids.email_field.value = "-"
            self.ids.password_field.value = "********"


    def logout(self):

        layout = BoxLayout(
            orientation="vertical",
            spacing=20,
            padding=15
        )

        label = Label(
            text="[b]Are you sure you want to logout?[/b]",
            markup=True,
            font_size="20sp",
            size_hint_y=None,
            height=70,
            halign="center",
            valign="middle",
            
        )
        label.bind(
            size=lambda instance, value: setattr(instance, "text_size", (instance.width, None))
        )
        

        buttons = BoxLayout(
            spacing=10,
            size_hint_y=None,
            height=50
)

        cancel_btn = Factory.RoundedPopupButton(text="Cancel")
        logout_btn = Factory.RoundedPopupButton(text="Logout")

        buttons.add_widget(cancel_btn)
        buttons.add_widget(logout_btn)

        layout.add_widget(label)
        layout.add_widget(buttons)

        popup = Popup(
            title="Logout",
            content=layout,
            size_hint=(0.8, 0.25),
            auto_dismiss=False,
            separator_height=0
        )

        cancel_btn.bind(on_press=popup.dismiss)

        def confirm(instance):
            logout_user()
            popup.dismiss()
            self.manager.current = "login"
        
        logout_btn.bind(on_press=confirm)
        popup.open()

from kivy.properties import StringProperty, NumericProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen

class ProductDetailScreen(Screen):
    prev_screen = StringProperty("home")
    quantity = NumericProperty(1)
    product_img = StringProperty("")
    product_name = StringProperty("")
    product_price = StringProperty("")


    def open(self, img, name, price, prev):
        self.prev_screen = prev
        self.quantity = 1

        self.product_img = img
        self.product_name = name
        self.product_price = price

        Clock.schedule_once(self.update_ui)

    def update_ui(self,dt):
        self.ids.detail_image.source = self.product_img
        self.ids.detail_name.text = self.product_name
        self.ids.detail_price.text = self.product_price
        self.ids.qty_label.text = "1"
        
        self._update_total()


    def _update_total(self):
        try:
            price_val = float(self.product_price.replace("Rs","").strip())
            total = price_val* self.quantity
            self.ids.total_label.text = f"Total : Rs {total}"
        
        except Exception as e:
            print("Total Error: ",e)
            self.ids.total_label.text = "Total : Rs"
            
    def change_qty(self, delta):
        self.quantity = max(1, self.quantity + delta)
        self.ids.qty_label.text = str(self.quantity)

        self._update_total()

    from kivy.app import App

    def add_to_cart(self):
        from kivy.app import App
        app = App.get_running_app()

        item = {
            "name": self.product_name,
            "price": float(self.product_price.replace("Rs", "")),
             "qty": self.quantity
              }

    # merge same item
        for i in app.cart:
            if i["name"] == item["name"]:
                i["qty"] += item["qty"]
                break
        else:
            app.cart.append(item)

    # update cart label
        home = self.manager.get_screen("home")
        total_items = sum(i["qty"] for i in app.cart)
        home.ids.cart_label.text = f"Cart: {total_items}"

        print("CART:", app.cart)   # 🔥 DEBUG

        self.quantity = 1
        self.manager.current = self.prev_screen


from kivy.uix.screenmanager import Screen


class OrderHistoryScreen(Screen):

    def on_enter(self):

        self.ids.history_layout.clear_widgets()

        orders = get_orders()

        if not orders:
            self.ids.history_scroll.opacity = 0
            self.ids.empty_state.opacity = 1
            return

        for order in orders:
            self.ids.history_scroll.opacity = 1
            self.ids.empty_state.opacity = 0


            card = Factory.OrderCard()

            card.ids.customer_lbl.text = order[0]
            card.ids.phone_lbl.text = "Phone: " + order[1]
            card.ids.address_lbl.text = "Address: " + order[2]
            card.ids.items_lbl.text = order[3]
            card.ids.total_lbl.text = "Total: Rs " + str(order[4])
            card.ids.date_lbl.text = order[5]
            card.invoice_path = order[6]

            self.ids.history_layout.add_widget(card)


class OrderDetailScreen(Screen):
    invoice_path = StringProperty("")

class CheckoutScreen(Screen):

    def on_enter(self):

        user = get_logged_in_user()

        if user:
            self.ids.name_input.ids.field.text = user[1]
            self.ids.phone_input.ids.field.text = user[2]
        else:
            self.ids.name_input.ids.field.text = ""
            self.ids.phone_input.ids.field.text = ""

        self.ids.address_input.ids.field.text = ""


from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior 
from kivy.properties import StringProperty

class FoodBox(ButtonBehavior,BoxLayout):
    img = StringProperty("")
    title = StringProperty("")
    price = StringProperty("")

    def on_press(self):   # 
        app = App.get_running_app()
        detail = app.root.get_screen("detail")

        detail.open(self.img, self.title, self.price, "more")
        app.root.current = "detail"


class MainApp(App):
    def build(self):
        Window.bind(on_keyboard=self.android_back)
        create_database()
        add_invoice_column()
        self.cart = []
        self.last_invoice_path = ""

        sm = ScreenManager()
        sm.add_widget(StartScreen(name="start"))
        sm.add_widget(LoginScreen(name = "login"))
        sm.add_widget(HomeScreen(name = "home"))
        sm.add_widget(MoreScreen(name="more"))
        sm.add_widget(ProductDetailScreen(name="detail"))
        sm.add_widget(CheckoutScreen(name="checkout")) 
        sm.add_widget(ProfileScreen(name="profile"))
        sm.add_widget(OrderHistoryScreen(name="order_history"))
        sm.add_widget(OrderDetailScreen(name="order_detail"))

        user = get_logged_in_user()
        print("Logged in user:", user)
        
        sm.current = "start"

        return sm
    
    def android_back(self, window, key, *args):
        if key == 27:

            if self.root.current == "order_detail":
                self.root.current = "order_history"
                return True

            elif self.root.current == "order_history":
                self.root.current = "more"
                return True
            
            elif self.root.current == "profile":
                self.root.current = "more"
                return True

            if self.root.current == "checkout":
               self.root.current = "more"
               return True

            elif self.root.current == "detail":
                self.root.current = "more"
                return True

            elif self.root.current == "more":
                self.root.current = "home"
                return True

        return False

    def open_checkout_from_cart(self):
        checkout = self.root.get_screen("checkout")

        order_list = checkout.ids.order_list
        order_list.clear_widgets()

        total = 0

        for item in self.cart:
            line_total = item["price"] * item["qty"]
            total += line_total

            row = BoxLayout(size_hint_y=None, height=50, padding=10)

            # background box
            with row.canvas.before:
                from kivy.graphics import Color, RoundedRectangle
                Color(1, 1, 1, 1)
                row.rect = RoundedRectangle(pos=row.pos, size=row.size, radius=[10])

            row.bind(pos=lambda i, v: setattr(row.rect, 'pos', v))
            row.bind(size=lambda i, v: setattr(row.rect, 'size', v))

            # LEFT: item name
            name_label = Label(
                text=f"{item['name']} x{item['qty']}",
                color=(0,0,0,1),
                halign="left"
        )

             # RIGHT: price
            price_label = Label(
                text=f"Rs {line_total}",
                color=(0,0.6,0,1),
                halign="right"
        )
            name_label.text_size = (200, None)
            price_label.text_size = (100, None)


            row.add_widget(name_label)
            row.add_widget(price_label)

            order_list.add_widget(row)

        if total >= 1000:
            delivery_charge = 0
            delivery_text = "FREE"
        else:
            delivery_charge = 100
            delivery_text = f"Rs {delivery_charge}"

        checkout.ids.total_bill.text = f"Total: Rs {total + delivery_charge}"

        self.root.current = "checkout"
    
    def generate_invoice(self, name, phone, address):
        checkout = self.root.get_screen("checkout")

        header = (
            f"Name: {name}\n"
            f"Phone: {phone}\n"
            f"Address: {address}"
)

        items_text = ""
        total = 0

        for item in self.cart:
            line_total = item["price"] * item["qty"]
            total += line_total
            items_text += (
                f"{item['name']}\n"
                f"Qty: {item['qty']}    Rs {line_total}\n\n"
)

        if total >= 1000:
            delivery_charge = 0
            delivery_text = "FREE"
        else:
            delivery_charge = 100
            delivery_text = f" {delivery_charge}"

        grand_total = total + delivery_charge

        total_text = (
            f"[size=16sp][color=000000]Subtotal: Rs {total}[/color][/size]\n"
            f"[size=16sp][color=000000]Delivery Charges: Rs {delivery_text}[/color][/size]\n"
            f"[b][size=24sp][color=ed470d]Total: Rs {grand_total}[/color][/size][/b]"
)

    # 🔥 UPDATE UI (NEW DESIGN)
        checkout.ids.invoice_header.text = header
        checkout.ids.invoice_items.text = items_text
        checkout.ids.invoice_total.text = total_text

        # Create Invoices folder
        from kivy.utils import platform

        if platform == "android":
            from android.storage import app_storage_path
            invoice_dir = os.path.join(app_storage_path(), "Invoices")
        else:
            invoice_dir = os.path.join(os.getcwd(), "Invoices")

        if not os.path.exists(invoice_dir):
            os.makedirs(invoice_dir)

        if not os.path.exists(invoice_dir):
            os.makedirs(invoice_dir)

        # Unique filename
        filename = os.path.join(
            invoice_dir,
            f"invoice_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        )
        order_date = datetime.now().strftime("%d-%m-%Y %H:%M")
        self.last_invoice_path = filename

        # Save after UI updates
        def save_invoice(dt):
            checkout.ids.invoice_card.export_to_png(filename)

        print("Invoice saved:", filename)

        save_order(
            name,
            phone,
            address,
            items_text,
            total,
            delivery_charge,
            grand_total,
            order_date,
            filename
        )

        print("Order saved successfully!")
        show_orders()
        Clock.schedule_once(save_invoice, 0.2)

        
        self.cart.clear()


        home = self.root.get_screen("home")
        home.ids.cart_label.text = "Cart: 0"


        checkout.ids.order_list.clear_widgets()
        checkout.ids.total_bill.text = "Total: Rs 0"

    def show_order_detail(self, card):

        detail = self.root.get_screen("order_detail")

        detail = self.root.get_screen("order_detail")
        detail.invoice_path = card.invoice_path

        self.root.current = "order_detail"

    # OPTIONAL: clear cart after invoice
        #self.cart.clear()

    def send_whatsapp_order(self):
        import webbrowser
        from urllib.parse import quote

        checkout = self.root.get_screen("checkout")

        name = checkout.ids.name_input.ids.field.text
        phone = checkout.ids.phone_input.ids.field.text
        address = checkout.ids.address_input.ids.field.text

        total = 0

        message = (
            "-----------------------------------\n"
            "            FOODSPOT              \n"
            "             INVOICE              \n"
            "-----------------------------------\n"
            f" Name    : {name}\n"
            f" Phone   : {phone}\n"
            f" Address : {address}\n"
            "-----------------------------------\n"
            " ITEMS                            \n"
            "-----------------------------------\n"
        )

        for item in self.cart:
            line_total = item["price"] * item["qty"]
            total += line_total

            message += (
                f" {item['name']}\n"
                f" Qty: {item['qty']}    Rs {line_total}\n"
                "-----------------------------------\n"
            )

        if total >= 1000:
            delivery_charge = 0
        else:
            delivery_charge = 100

        grand_total = total + delivery_charge

        message += (
            f" Subtotal : Rs {total}\n"
            f" Delivery : Rs {delivery_charge}\n"
            "-----------------------------------\n"
            f" TOTAL    : Rs {grand_total}\n"
            "-----------------------------------\n"
        )
    

        number = ""   # Replace with shop owner's WhatsApp number

        url = f"https://wa.me/{number}?text={quote(message)}"

        webbrowser.open(url)

    
    def delete_order(self, invoice_path):
        layout = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=15
        )

        label = Label(
            text="[b]Are you sure you want to delete this order?[/b]",
            markup=True,
            font_size="20sp",
            size_hint_y=None,
            bold=True,
            halign="center",
            valign="middle",
            height=70
        )
        label.bind(size=lambda instance, value: setattr(instance, "text_size", (instance.width, None)))

        buttons = BoxLayout(
            spacing=10,
            size_hint_y=None,
            height=50
        )

        cancel_btn = Factory.RoundedPopupButton(text="Cancel")
        delete_btn = Factory.RoundedPopupButton(text="Delete")

        buttons.add_widget(cancel_btn)
        buttons.add_widget(delete_btn)

        layout.add_widget(label)
        layout.add_widget(buttons)

        popup = Popup(
            title="Delete Order",
            content=layout,
            size_hint=(0.8, 0.25),
            auto_dismiss=False,
            separator_height=0
        )

        cancel_btn.bind(on_press=popup.dismiss)

        def confirm(instance):
            try:
                delete_order(invoice_path)

                if invoice_path and os.path.exists(invoice_path):
                    os.remove(invoice_path)

                popup.dismiss()

                self.root.current = "order_history"

                print("Order deleted successfully!")

            except Exception as e:
                print("Error deleting order:", e)

        delete_btn.bind(on_press=confirm)

        popup.open()

           
MainApp().run()
