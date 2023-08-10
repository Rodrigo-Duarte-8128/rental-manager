from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.utils import get_color_from_hex as hex
from rentals.rentals_screen import RentalsScreen
from rentals.add_rental_screen import AddRentalScreen
from rentals.edit_rental_screen import EditRentalScreen
from rentals.finish_screen import FinishRentalScreen
from inventory.inventory_screen import InventoryScreen
from inventory.add_item_screen import AddItemScreen
from inventory.edit_item_screen import EditItemScreen
from inventory.inv_row_widget import RowWidget as InvRowWidget
from rentals.rent_row_widget import RowWidget as RentRowWidget
from datetime import datetime



# Define colors
back_light_grey = (211/255,211/255,211/255, 1)
light_grey = hex("#F3F2ED")
green = hex("#01311F")
yellow = hex("#C6AA58")
banner_green = (0, 1, 1, 1)




class MainApp(App):
    def build(self):

        # Screen Manager
        self.screen_manager = ScreenManager()


        # Screens 
        self.inventory_screen = InventoryScreen(name="inventory_screen")
        self.add_item_screen = AddItemScreen(name="add_item_screen")

        self.rentals_screen = RentalsScreen(name="rentals_screen")
        self.add_rental_screen = AddRentalScreen(self.inventory_screen, name="add_rental_screen")
        


        # Button functionality
        self.rentals_screen.layout.go_to_inventory_btn.bind(on_release=self.move_screen_to("inventory_screen"))
        self.rentals_screen.layout.add_rental_btn.bind(on_release=self.new_rental_click)
        for row_widget in self.rentals_screen.row_widgets.values():
            row_widget.client_name_btn.bind(on_release=self.edit_rental_clicked)

        self.inventory_screen.layout.go_to_rentals_btn.bind(on_release=self.move_screen_to("rentals_screen"))
        self.inventory_screen.layout.add_item_btn.bind(on_release=self.move_screen_to("add_item_screen"))
        for row_widget in self.inventory_screen.row_widgets.values():
            row_widget.item_name_btn.bind(on_release=self.edit_item_clicked)

        self.add_item_screen.layout.add_item_btn.bind(on_release=self.add_item)
        self.add_item_screen.layout.cancel_btn.bind(on_release=self.cancel_add_item)

        self.add_rental_screen.layout.add_rental_btn.bind(on_release=self.add_rental)
        self.add_rental_screen.layout.cancel_btn.bind(on_release=self.cancel_add_rental)
        for row_widget in self.add_rental_screen.row_widgets.values():
            row_widget.item_name_btn.bind(on_release=self.click_item_to_rent(self.add_rental_screen))

        
        

        # Add screens to screen manager
        self.screen_manager.add_widget(self.rentals_screen)
        self.screen_manager.add_widget(self.add_rental_screen)
        

        self.screen_manager.add_widget(self.inventory_screen)
        self.screen_manager.add_widget(self.add_item_screen)
        

        return self.screen_manager
    

    def move_screen_to(self, screen_name):
        def move(instance):
            current = self.screen_manager.current 
            if (current == "add_item_screen" or current == "edit_item_screen") and screen_name == "inventory_screen":
                self.screen_manager.transition.direction = "right"
            if current == "inventory_screen" and (screen_name == "add_item_screen" or screen_name == "edit_item_screen"):
                self.screen_manager.transition.direction = "left"
            if current == "inventory_screen" and screen_name == "rentals_screen":
                self.screen_manager.transition.direction = "right"
            if current == "rentals_screen" and screen_name == "inventory_screen":
                self.screen_manager.transition.direction = "left"
            if current == "rentals_screen" and (screen_name == "add_rental_screen" or screen_name == "edit_rental_screen"):
                self.screen_manager.transition.direction = "right"
            if (current == "add_rental_screen" or current == "edit_rental_screen") and screen_name == "rentals_screen":
                self.screen_manager.transition.direction = "left"
            if current == "edit_rental_screen" and screen_name == "finish_rental_screen":
                self.screen_manager.transition.direction = "right"
            if current == "finish_rental_screen" and (screen_name == "edit_rental_screen" or screen_name == "rentals_screen"):
                self.screen_manager.transition.direction = "left"
            
            self.screen_manager.current = screen_name
        return move
    

        
    def add_item(self, instance):

        this_item_no, error = self.inventory_screen.add_item(
        self.add_item_screen.get_item_values()["item_name"],
        self.add_item_screen.get_item_values()["hourly_rate"],
        self.add_item_screen.get_item_values()["stock"],
        self.add_item_screen,
        self.add_rental_screen
        )


        if error == []:
            self.move_screen_to("inventory_screen")(instance)

            self.add_item_screen.layout.name_text_input.text = ""
            self.add_item_screen.layout.rate_text_input.text = ""
            self.add_item_screen.layout.stock_text_input.text = ""

            self.inventory_screen.row_widgets[this_item_no].item_name_btn.bind(on_release=self.edit_item_clicked)

            self.refresh_items_scroll_view(self.inventory_screen)

        


        if "invalid_name" in error:
            if self.add_item_screen.layout.error_add_label not in self.add_item_screen.layout.children:
                self.add_item_screen.layout.add_widget(self.add_item_screen.layout.error_add_label)

        if "invalid_rate" in error:
            if self.add_item_screen.layout.error_rate_label not in self.add_item_screen.layout.children:
                self.add_item_screen.layout.add_widget(self.add_item_screen.layout.error_rate_label)

        if "invalid_stock" in error:
            if self.add_item_screen.layout.error_stock_label not in self.add_item_screen.layout.children:
                self.add_item_screen.layout.add_widget(self.add_item_screen.layout.error_stock_label)

        if "invalid_name" not in error:
            if self.add_item_screen.layout.error_add_label in self.add_item_screen.layout.children:
                self.add_item_screen.layout.remove_widget(self.add_item_screen.layout.error_add_label)

        if "invalid_rate" not in error:
            if self.add_item_screen.layout.error_rate_label in self.add_item_screen.layout.children:
                self.add_item_screen.layout.remove_widget(self.add_item_screen.layout.error_rate_label)

        if "invalid_stock" not in error:
            if self.add_item_screen.layout.error_stock_label in self.add_item_screen.layout.children:
                self.add_item_screen.layout.remove_widget(self.add_item_screen.layout.error_stock_label)

         
    


    def new_rental_click(self, instance):
        self.refresh_items_scroll_view(self.add_rental_screen)
        self.add_rental_screen.layout.hour_text_input.text = ":".join(datetime.now().strftime("%H:%M:%S").split(":")[:-1])
        self.move_screen_to("add_rental_screen")(instance)


    
    def add_rental(self, instance):
        
        errors = []

        client_name = self.add_rental_screen.layout.name_text_input.text
        start_time = self.add_rental_screen.layout.hour_text_input.text
        items_rented = self.add_rental_screen.items_to_rent

        # create client id
        client_id = 0
        for id in self.rentals_screen.rentals_stored.keys():
            if int(id) > client_id:
                client_id = int(id)
        client_id = str(client_id + 1)

        # create hourly prices
        hourly_price = self.rentals_screen.compute_hourly_price(self.add_item_screen, items_rented)

        # max_no_rates = 0
        # for item in items_rented.values():
        #     no_rates = len(self.add_item_screen.parse_rate_entry(item["hourly_rate"])[0])
        #     if  no_rates > max_no_rates:
        #         max_no_rates = no_rates


        # hourly_prices_list = [[]]
        # for hour_rate_no in range(max_no_rates):
        #     price_for_this_hour = 0
        #     for item in items_rented.values():
        #         parsed_item_rates = self.add_item_screen.parse_rate_entry(item["hourly_rate"])
        #         if hour_rate_no < len(parsed_item_rates[0]):
        #             price_for_this_hour += float(parsed_item_rates[0][hour_rate_no])
        #         else:
        #             price_for_this_hour += float(parsed_item_rates[0][-1])

            
        #     hourly_prices_list[0].append(str(price_for_this_hour))



        #     hourly_price += float(item["hourly_rate"])
        # hourly_price = str(round(hourly_price, 2))

        # hourly_price = ", ".join(hourly_prices_list)


        # validate hour format
        list = start_time.split(":")
        try:
            hour = int(list[0])
            minutes = int(list[1])

            if hour < 0 or hour >= 24 or minutes < 0 or minutes >= 60:  
                errors.append("invalid_hour")
        except:
            errors.append("invalid_hour")
        
        

        
        # check for the existence of items to rent
        if self.add_rental_screen.items_to_rent == {}:
            errors.append("no_items")


        
        if errors == []:

            self.update_rentals_stock()

            self.rentals_screen.rentals_stored.put(
                client_id, 
                client_name = client_name, 
                start_time = start_time,
                hourly_price = hourly_price,
                items_rented = items_rented
            )

            new_row = RentRowWidget(
                    client_id,
                    client_name,
                    start_time,
                    f"\u20ac{hourly_price}"
                )
            self.rentals_screen.layout.scroll_layout.add_widget(new_row)
            self.rentals_screen.row_widgets[client_id] = new_row

            self.rentals_screen.row_widgets[client_id].client_name_btn.bind(on_release=self.edit_rental_clicked)

            self.refresh_items_scroll_view(self.inventory_screen)

            self.move_screen_to("rentals_screen")(instance)

            self.add_rental_screen.layout.name_text_input.text = ""
            self.add_rental_screen.layout.hour_text_input.text = ""
            self.add_rental_screen.layout.added_items_label.text = ""

            self.add_rental_screen.items_to_rent = {}
            
            if self.add_rental_screen.layout.error_time_label in self.add_rental_screen.layout.children:
                self.add_rental_screen.layout.remove_widget(self.add_rental_screen.layout.error_time_label)

            if self.add_rental_screen.layout.error_items_label in self.add_rental_screen.layout.children:
                self.add_rental_screen.layout.remove_widget(self.add_rental_screen.layout.error_items_label)


        
        if "invalid_hour" in errors:
            if self.add_rental_screen.layout.error_time_label not in self.add_rental_screen.layout.children:
                self.add_rental_screen.layout.add_widget(self.add_rental_screen.layout.error_time_label)

        if "invalid_hour" not in errors:
            if self.add_rental_screen.layout.error_time_label in self.add_rental_screen.layout.children:
                self.add_rental_screen.layout.remove_widget(self.add_rental_screen.layout.error_time_label)

        if "no_items" in errors:
            if self.add_rental_screen.layout.error_items_label not in self.add_rental_screen.layout.children:
                self.add_rental_screen.layout.add_widget(self.add_rental_screen.layout.error_items_label)

        if "no_items" not in errors:
            if self.add_rental_screen.layout.error_items_label in self.add_rental_screen.layout.children:
                self.add_rental_screen.layout.remove_widget(self.add_rental_screen.layout.error_items_label)


    def update_rentals_stock(self):
        # updates the stock levels stored in active_rentals.json based on the stock levels in inventory_items.json
        # to be called whenever we make changes to stock levels in inventory_items.json that need to be tracked by the rentals
        
        for client_id in self.rentals_screen.rentals_stored.keys():
            new_client_name = self.rentals_screen.rentals_stored.get(client_id)["client_name"]
            new_start_time = self.rentals_screen.rentals_stored.get(client_id)["start_time"]
            new_hourly_price = self.rentals_screen.rentals_stored.get(client_id)["hourly_price"]
            new_items = {}
            
            for item_no in self.rentals_screen.rentals_stored.get(client_id)["items_rented"]:
                item = self.rentals_screen.rentals_stored.get(client_id)["items_rented"][item_no]
                item_name = item["item_name"]
                hourly_rate = item["hourly_rate"]
                stock = self.inventory_screen.items_stored.get(item_no)["stock"]

                new_items[item_no] = {
                    "item_name": item_name, 
                    "hourly_rate": hourly_rate,
                    "stock": stock
                }

            self.rentals_screen.rentals_stored.delete(client_id)
            self.rentals_screen.rentals_stored.put(
                client_id,
                client_name = new_client_name,
                start_time = new_start_time,
                hourly_price = new_hourly_price,
                items_rented = new_items
            )



    def click_item_to_rent(self, screen):
        # if the item doesn't exist in rows_rented then add it, otherwise remove it
        def click(instance):
            for item_no, item in self.inventory_screen.items_stored.find(item_name=instance.text):
                associated_item = {item_no: item}

            item_no = list(associated_item.keys())[0]
            item = associated_item[item_no]

            if item_no in screen.items_to_rent:
                del screen.items_to_rent[item_no]

                new_string = ""

                for idx, number in enumerate(screen.layout.added_items_label.text.split(", ")):
                    if number != item_no:
                        if idx == 0 or (idx == 1 and screen.layout.added_items_label.text.split(", ")[0] == item_no):
                            new_string += str(number)
                        else:
                            new_string += f", {number}"

                screen.layout.added_items_label.text = new_string


                stock = int(item["stock"])
            
                new_stock = str(stock + 1)
                self.inventory_screen.items_stored.delete(item_no)
                self.inventory_screen.items_stored.put(
                    item_no, 
                    item_name = item["item_name"],
                    hourly_rate = item["hourly_rate"],
                    stock = new_stock
                )
                self.refresh_items_scroll_view(self.inventory_screen)
                self.refresh_items_scroll_view(screen)
            
            else:
                stock = int(item["stock"])
                if stock >= 1:

                    new_stock = str(stock - 1)
                    self.inventory_screen.items_stored.delete(item_no)
                    self.inventory_screen.items_stored.put(
                        item_no, 
                        item_name = item["item_name"],
                        hourly_rate = item["hourly_rate"],
                        stock = new_stock
                    )
                    
                    
                    self.refresh_items_scroll_view(screen)
                    self.refresh_items_scroll_view(self.inventory_screen)

                    

                    if screen.items_to_rent == {}:
                        screen.items_to_rent[item_no] = {
                            "item_name": item["item_name"],
                            "hourly_rate": item["hourly_rate"],
                            "stock": new_stock
                        }
                        screen.layout.added_items_label.text += f"{item_no}"
                    else:
                        screen.items_to_rent[item_no] = {
                            "item_name": item["item_name"],
                            "hourly_rate": item["hourly_rate"],
                            "stock": new_stock
                        }
                        screen.layout.added_items_label.text += f", {item_no}"

        return click

    
    

    def refresh_items_scroll_view(self, screen):
        # screen is either add_rental_screen, edit_rental_screen, inventory_screen
        # this function deletes the current row_widgets in screen.layout.scroll_view and recreates the scroll_view based on
        # the items that are currently stored in inventory_screen.items_stored

        for item_no in screen.row_widgets.keys():
            screen.layout.scroll_layout.remove_widget(screen.row_widgets[item_no])
            
       
        screen.row_widgets = {}


        item_no_list = list(map(lambda x: int(x), self.inventory_screen.items_stored.keys()))
        item_no_list.sort()

        for item_no in item_no_list:
            item_no = str(item_no)
            row = InvRowWidget(
                item_no,
                self.inventory_screen.items_stored.get(item_no)["item_name"],
                f"\u20ac{self.inventory_screen.items_stored.get(item_no)['hourly_rate']}",
                str(self.inventory_screen.items_stored[item_no]['stock'])
            )
            screen.row_widgets[item_no] = row
            screen.layout.scroll_layout.add_widget(row)

            if screen == self.inventory_screen:
                screen.row_widgets[item_no].item_name_btn.bind(on_release=self.edit_item_clicked)

            else: 
                screen.row_widgets[item_no].item_name_btn.bind(on_release=self.click_item_to_rent(screen))


    def refresh_rentals_scroll_view(self):

        for client_id in self.rentals_screen.rentals_stored.keys():
            self.rentals_screen.layout.scroll_layout.remove_widget(
                self.rentals_screen.row_widgets[client_id]
            )
            
        self.rentals_screen.row_widgets = {}        

        client_id_list = list(map(lambda x: int(x), self.rentals_screen.rentals_stored.keys()))
        client_id_list.sort()

        for client_id in client_id_list:
            client_id = str(client_id)

            items_rented = self.rentals_screen.rentals_stored[client_id]["items_rented"]
            hourly_price = self.rentals_screen.compute_hourly_price(self.add_item_screen, items_rented)

            # hourly_price = 0
            # for item in self.rentals_screen.rentals_stored[client_id]["items_rented"].values():
            #     hourly_price += float(item["hourly_rate"])
            # hourly_price = str(round(hourly_price, 2))

            row = RentRowWidget(
                client_id,
                self.rentals_screen.rentals_stored.get(client_id)["client_name"],
                self.rentals_screen.rentals_stored.get(client_id)['start_time'],
                f"\u20ac{hourly_price}"
            )
            self.rentals_screen.row_widgets[client_id] = row
            self.rentals_screen.layout.scroll_layout.add_widget(row)

            self.rentals_screen.row_widgets[client_id].client_name_btn.bind(on_release=self.edit_rental_clicked)


    def edit_rental_clicked(self, instance):

        for row_widget in self.rentals_screen.row_widgets.values():
            if row_widget.client_name_btn == instance:
                client_id = row_widget.client_id
                rental = {
                    "client_name": row_widget.client_name,
                    "hourly_price": row_widget.hourly_price,
                    "start_time": row_widget.start_time
                }

        rental["items_rented"] = self.rentals_screen.rentals_stored.get(client_id)["items_rented"]

        

        associated_rental = {client_id: rental}

        

        self.edit_rental_screen = EditRentalScreen(self.inventory_screen, associated_rental, name="edit_rental_screen")
        self.screen_manager.add_widget(self.edit_rental_screen)

        

        self.edit_rental_screen.layout.name_text_input.text = rental["client_name"]
        self.edit_rental_screen.layout.hour_text_input.text = rental["start_time"]

        for row_widget in self.edit_rental_screen.row_widgets.values():
            row_widget.item_name_btn.bind(on_release=self.click_item_to_rent(self.edit_rental_screen)) 
        


        self.move_screen_to("edit_rental_screen")(instance)

        # Button functionality in Edit Rental Screen
        self.edit_rental_screen.layout.remove_rental_btn.bind(on_release=self.remove_rental(client_id))
        self.edit_rental_screen.layout.cancel_btn.bind(on_release=self.cancel_edit_rental(associated_rental))
        self.edit_rental_screen.layout.save_changes_btn.bind(on_release=self.confirm_edit_rental(client_id))
        self.edit_rental_screen.layout.finish_rental_btn.bind(on_release=self.finish_rental(associated_rental))


    def cancel_add_item(self, instance):
        self.move_screen_to("inventory_screen")(instance)
        self.add_item_screen.layout.name_text_input.text = ""
        self.add_item_screen.layout.rate_text_input.text = ""
        self.add_item_screen.layout.stock_text_input.text = ""

        
        
        if self.add_item_screen.layout.error_rate_label in self.add_item_screen.layout.children:
            self.add_item_screen.layout.remove_widget(self.add_item_screen.layout.error_rate_label)

        if self.add_item_screen.layout.error_stock_label in self.add_item_screen.layout.children:
            self.add_item_screen.layout.remove_widget(self.add_item_screen.layout.error_stock_label)

        if self.add_item_screen.layout.error_add_label in self.add_item_screen.layout.children:
            self.add_item_screen.layout.remove_widget(self.add_item_screen.layout.error_add_label)


    def cancel_add_rental(self, instance):
        self.move_screen_to("rentals_screen")(instance)

        # reset stock levels
        for item_no in self.add_rental_screen.items_to_rent.keys():
            item = self.add_rental_screen.items_to_rent[item_no]
            stock = int(item["stock"])
            new_stock = str(stock + 1)
            self.inventory_screen.items_stored.delete(item_no)
            self.inventory_screen.items_stored.put(
                item_no, 
                item_name = item["item_name"],
                hourly_rate = item["hourly_rate"],
                stock = new_stock
            )
        
        self.refresh_items_scroll_view(self.inventory_screen)
        self.refresh_items_scroll_view(self.add_rental_screen)


        self.add_rental_screen.layout.name_text_input.text = ""
        self.add_rental_screen.layout.hour_text_input.text = ""
        self.add_rental_screen.layout.added_items_label.text = ""

        self.add_rental_screen.items_to_rent = {}
        
        if self.add_rental_screen.layout.error_time_label in self.add_rental_screen.layout.children:
            self.add_rental_screen.layout.remove_widget(self.add_rental_screen.layout.error_time_label)

        if self.add_rental_screen.layout.error_items_label in self.add_rental_screen.layout.children:
            self.add_rental_screen.layout.remove_widget(self.add_rental_screen.layout.error_items_label)

        
    def edit_item_clicked(self, instance):
         
        for item_no, item in self.inventory_screen.items_stored.find(item_name=instance.text):
            associated_item = {item_no: item}
        
        self.edit_item_screen = EditItemScreen(associated_item, name="edit_item_screen")
        self.screen_manager.add_widget(self.edit_item_screen)

        item_no = list(associated_item.keys())[0]
        item = associated_item[item_no]

        self.edit_item_screen.layout.item_no_text_input.text = str(item_no)
        self.edit_item_screen.layout.name_text_input.text = str(item["item_name"])
        self.edit_item_screen.layout.rate_text_input.text = str(item["hourly_rate"])
        self.edit_item_screen.layout.stock_text_input.text = str(item["stock"])


        self.move_screen_to("edit_item_screen")(instance)

        # Button functionality in Edit Item Screen
        self.edit_item_screen.layout.remove_item_btn.bind(on_release=self.remove_item(item_no))
        self.edit_item_screen.layout.cancel_btn.bind(on_release=self.cancel_edit_item(item_no))
        self.edit_item_screen.layout.save_changes_btn.bind(on_release=self.confirm_edit_item(item_no, item))


    def confirm_edit_item(self, item_no, item):

        '''
        item_no is a string of the item number of the item associated with this edit item screen

        item is a dictionary {"item_name": item_name, "hourly_rate": hourly_rate, "stock": stock}
        '''

        def confirm(instance):
            
            new_item_no = self.edit_item_screen.layout.item_no_text_input.text 
            new_item_name = self.edit_item_screen.layout.name_text_input.text
            new_rate = self.edit_item_screen.layout.rate_text_input.text
            new_stock = self.edit_item_screen.layout.stock_text_input.text

            errors = []     # list of errors

            for number in self.inventory_screen.items_stored.keys():
                if number != item_no:
                    if new_item_no == number or self.inventory_screen.items_stored.get(number)["item_name"] == new_item_name:
                        if new_item_no == number:
                            errors.append("item_no_exists.")
                        if self.inventory_screen.items_stored.get(number)["item_name"] == new_item_name:
                            errors.append("item_name_exists.")
                        break

            try:
                int_new_item_no = int(new_item_no)
                if int_new_item_no < 0:
                    errors.append("invalid_item_no")
            except:
                errors.append("invalid_item_no")


            if not self.add_item_screen.verify_rate_entry(new_rate):
                errors.append("invalid_hourly_rate")

            # try:
            #     float_new_rate = float(new_rate)
            #     if float_new_rate < 0:
            #         errors.append("invalid_hourly_rate")
            # except:
            #     errors.append("invalid_hourly_rate")

            if not self.add_item_screen.verify_stock_entry(new_stock):
                errors.append("invalid_stock")

            # try:
            #     int_new_stock = int(new_stock)
            #     if int_new_stock < 0:
            #         errors.append("invalid_stock")
            # except:
            #     errors.append("invalid_stock")

            if self.rentals_screen.row_widgets != {}:
                errors.append("active_rentals")


            if errors == []:

                self.inventory_screen.layout.scroll_layout.remove_widget(self.inventory_screen.row_widgets[item_no])
                self.inventory_screen.remove_item(item_no)

                self.inventory_screen.items_stored.put(new_item_no, item_name=new_item_name, hourly_rate=new_rate, stock=new_stock)

                new_row = InvRowWidget(
                        new_item_no,
                        new_item_name,
                        f"\u20ac{new_rate}",
                        new_stock
                    )
                
                self.inventory_screen.layout.scroll_layout.add_widget(new_row)
                self.inventory_screen.row_widgets[new_item_no] = new_row
                self.inventory_screen.row_widgets[new_item_no].item_name_btn.bind(on_release=self.edit_item_clicked)

                self.refresh_items_scroll_view(self.inventory_screen)
                self.refresh_items_scroll_view(self.add_rental_screen)
                self.refresh_rentals_scroll_view()

                


                self.move_screen_to("inventory_screen")(instance)

                self.screen_manager.remove_widget(self.edit_item_screen)

            
            if "item_no_exists." in errors:
                if self.edit_item_screen.layout.error_no_label not in self.edit_item_screen.layout.children:
                    self.edit_item_screen.layout.add_widget(self.edit_item_screen.layout.error_no_label)

            if "invalid_item_no" in errors:
                if self.edit_item_screen.layout.error_invalid_no_label not in self.edit_item_screen.layout.children:
                    self.edit_item_screen.layout.add_widget(self.edit_item_screen.layout.error_invalid_no_label)

            if "item_name_exists." in errors:
                if self.edit_item_screen.layout.error_name_label not in self.edit_item_screen.layout.children:
                    self.edit_item_screen.layout.add_widget(self.edit_item_screen.layout.error_name_label)

            if "invalid_hourly_rate" in errors:
                if self.edit_item_screen.layout.error_rate_label not in self.edit_item_screen.layout.children:
                    self.edit_item_screen.layout.add_widget(self.edit_item_screen.layout.error_rate_label)

            if "invalid_stock" in errors:
                if self.edit_item_screen.layout.error_stock_label not in self.edit_item_screen.layout.children:
                    self.edit_item_screen.layout.add_widget(self.edit_item_screen.layout.error_stock_label)
            
            if "active_rentals" in errors:
                if self.edit_item_screen.layout.error_rentals_label not in self.edit_item_screen.layout.children:
                    self.edit_item_screen.layout.add_widget(self.edit_item_screen.layout.error_rentals_label)



            if "item_no_exists." not in errors:
                if self.edit_item_screen.layout.error_no_label in self.edit_item_screen.layout.children:
                    self.edit_item_screen.layout.remove_widget(self.edit_item_screen.layout.error_no_label)

            if "invalid_item_no" not in errors:
                if self.edit_item_screen.layout.error_invalid_no_label in self.edit_item_screen.layout.children:
                    self.edit_item_screen.layout.remove_widget(self.edit_item_screen.layout.error_invalid_no_label)

            if "item_name_exists." not in errors:
                if self.edit_item_screen.layout.error_name_label in self.edit_item_screen.layout.children:
                    self.edit_item_screen.layout.remove_widget(self.edit_item_screen.layout.error_name_label)

            if "invalid_hourly_rate" not in errors:
                if self.edit_item_screen.layout.error_rate_label in self.edit_item_screen.layout.children:
                    self.edit_item_screen.layout.remove_widget(self.edit_item_screen.layout.error_rate_label)

            if "invalid_stock" not in errors:
                if self.edit_item_screen.layout.error_stock_label in self.edit_item_screen.layout.children:
                    self.edit_item_screen.layout.remove_widget(self.edit_item_screen.layout.error_stock_label)

            if "active_rentals" not in errors:
                if self.edit_item_screen.layout.error_rentals_label in self.edit_item_screen.layout.children:
                    self.edit_item_screen.layout.remove_widget(self.edit_item_screen.layout.error_rentals_label)

            

        return confirm
    

    def confirm_edit_rental(self, client_id):
        def confirm(instance):
            new_client_name = self.edit_rental_screen.layout.name_text_input.text 
            new_start_time = self.edit_rental_screen.layout.hour_text_input.text
            
            
            # create new_items_to_rent
            new_items_to_rent = {}
            no_list = self.edit_rental_screen.layout.added_items_label.text.split(", ")
            for item_no in self.inventory_screen.items_stored.keys():
                if item_no in no_list:
                    new_items_to_rent[item_no] = self.inventory_screen.items_stored.get(item_no)

            


            errors = []     # list of errors

            # create hourly price

            new_hourly_price = self.rentals_screen.compute_hourly_price(self.add_item_screen, new_items_to_rent)

            # new_hourly_price = 0
            # for item in new_items_to_rent.values():
            #     new_hourly_price += float(item["hourly_rate"])
            # new_hourly_price = str(round(new_hourly_price, 2))


            # validate hour format
            list = new_start_time.split(":")
            try:
                hour = int(list[0])
                minutes = int(list[1])

                if hour < 0 or hour >= 24 or minutes < 0 or minutes >= 60:  
                    errors.append("invalid_hour")
            except:
                errors.append("invalid_hour")
            
            

            
            # check for the existence of items to rent
            if self.edit_rental_screen.items_to_rent == {}:
                errors.append("no_items")

            
            if errors == []:

                self.rentals_screen.rentals_stored.delete(client_id)
                self.rentals_screen.layout.scroll_layout.remove_widget(self.rentals_screen.row_widgets[client_id])
                del self.rentals_screen.row_widgets[client_id]


                self.update_rentals_stock()
                

                self.rentals_screen.rentals_stored.put(
                    client_id, 
                    client_name = new_client_name, 
                    start_time = new_start_time,
                    hourly_price = new_hourly_price,
                    items_rented = new_items_to_rent
                )

                new_row = RentRowWidget(
                        client_id,
                        new_client_name,
                        new_start_time,
                        f"\u20ac{new_hourly_price}"
                    )
                self.rentals_screen.layout.scroll_layout.add_widget(new_row)
                self.rentals_screen.row_widgets[client_id] = new_row

                self.rentals_screen.row_widgets[client_id].client_name_btn.bind(on_release=self.edit_rental_clicked)

                self.refresh_items_scroll_view(self.inventory_screen)
                self.refresh_rentals_scroll_view()

                self.move_screen_to("rentals_screen")(instance)

                self.screen_manager.remove_widget(self.edit_rental_screen)


            
            if "invalid_hour" in errors:
                if self.edit_rental_screen.layout.error_time_label not in self.edit_rental_screen.layout.children:
                    self.edit_rental_screen.layout.add_widget(self.edit_rental_screen.layout.error_time_label)

            if "invalid_hour" not in errors:
                if self.edit_rental_screen.layout.error_time_label in self.edit_rental_screen.layout.children:
                    self.edit_rental_screen.layout.remove_widget(self.edit_rental_screen.layout.error_time_label)

            if "no_items" in errors:
                if self.edit_rental_screen.layout.error_items_label not in self.edit_rental_screen.layout.children:
                    self.edit_rental_screen.layout.add_widget(self.edit_rental_screen.layout.error_items_label)

            if "no_items" not in errors:
                if self.edit_rental_screen.layout.error_items_label in self.edit_rental_screen.layout.children:
                    self.edit_rental_screen.layout.remove_widget(self.edit_rental_screen.layout.error_items_label)
        return confirm
    

    def cancel_edit_item(self, item_no):
        def cancel(instance):
            self.move_screen_to("inventory_screen")(instance)
            self.screen_manager.remove_widget(self.edit_item_screen)
        return cancel
    

    def cancel_edit_rental(self, associated_rental):
        def cancel(instance):
            self.move_screen_to("rentals_screen")(instance)

            
            # need to undo the changes to items_to_rent
            for item_no in list(self.edit_rental_screen.items_to_rent.keys()):
                if item_no not in list(self.edit_rental_screen.items_rented.keys()):
                    item = self.edit_rental_screen.items_to_rent[item_no]
                    stock = int(item["stock"])
            
                    new_stock = str(stock + 1)
                    self.inventory_screen.items_stored.delete(item_no)
                    self.inventory_screen.items_stored.put(
                        item_no, 
                        item_name = item["item_name"],
                        hourly_rate = item["hourly_rate"],
                        stock = new_stock
                    )
                    

            for item_no in list(self.edit_rental_screen.items_rented.keys()):
                if item_no not in list(self.edit_rental_screen.items_to_rent.keys()):
                    item = self.edit_rental_screen.items_rented[item_no]
                    stock = item["stock"]
            
                    #new_stock = str(stock - 1) no need to subtract here because the stock level is coming from 
                    # active_rentals.json that wasn't modified when clicking in the edit_rental_screen
                    self.inventory_screen.items_stored.delete(item_no)
                    self.inventory_screen.items_stored.put(
                        item_no, 
                        item_name = item["item_name"],
                        hourly_rate = item["hourly_rate"],
                        stock = stock
                    )
              

            self.refresh_items_scroll_view(self.inventory_screen)
            self.refresh_items_scroll_view(self.add_rental_screen)
            self.screen_manager.remove_widget(self.edit_rental_screen)
        return cancel
    

    def remove_item(self, item_no):
        def remove(instance):
            
            if self.rentals_screen.row_widgets != {}:
                if self.edit_item_screen.layout.error_rentals_label not in self.edit_item_screen.layout.children:
                    self.edit_item_screen.layout.add_widget(self.edit_item_screen.layout.error_rentals_label)
            
            else:
                self.inventory_screen.layout.scroll_layout.remove_widget(self.inventory_screen.row_widgets[item_no])
                self.add_rental_screen.layout.scroll_layout.remove_widget(self.add_rental_screen.row_widgets[item_no])
                self.inventory_screen.remove_item(item_no)
                
                self.move_screen_to("inventory_screen")(instance)

                self.screen_manager.remove_widget(self.edit_item_screen)

        return remove
    

    def remove_rental(self, client_id):
        def remove(instance):
            # reset stocks
            # the stock of the items that were removed from the edit screen have already been returned
            # so we only need to return the items in items_to_rent
            for item_no in self.edit_rental_screen.items_to_rent.keys():
                item = self.edit_rental_screen.items_to_rent[item_no]
                stock = int(item["stock"])
        
                new_stock = str(stock + 1)  
                self.inventory_screen.items_stored.delete(item_no)
                self.inventory_screen.items_stored.put(
                    item_no, 
                    item_name = item["item_name"],
                    hourly_rate = item["hourly_rate"],
                    stock = new_stock
                )


            
            

            self.refresh_items_scroll_view(self.inventory_screen)
            self.refresh_items_scroll_view(self.add_rental_screen)


            self.rentals_screen.rentals_stored.delete(client_id)
            self.rentals_screen.layout.scroll_layout.remove_widget(self.rentals_screen.row_widgets[client_id])
            del self.rentals_screen.row_widgets[client_id]


            self.update_rentals_stock()

            self.move_screen_to("rentals_screen")(instance)

            self.screen_manager.remove_widget(self.edit_rental_screen)

        return remove



    def finish_rental(self, associated_rental):
        def finish(instance):
            self.finish_rental_screen = FinishRentalScreen(self.inventory_screen, associated_rental, name="finish_rental_screen")
            self.screen_manager.add_widget(self.finish_rental_screen)

            client_id = list(associated_rental.keys())[0]
            rental = associated_rental[client_id]


            self.finish_rental_screen.layout.name_text_input.text = rental["client_name"]
            self.finish_rental_screen.layout.hour_text_input.text = rental["start_time"]

             
        
            self.move_screen_to("finish_rental_screen")(instance)

            # Button functionality in Finish Rental Screen
            self.finish_rental_screen.layout.recalculate_btn.bind(on_release=self.finish_rental_screen.recalculate)
            self.finish_rental_screen.layout.finish_btn.bind(on_release=self.confirm_finish_rental(client_id))
            self.finish_rental_screen.layout.cancel_btn.bind(on_release=self.cancel_finish_rental)
            
        return finish
    

    
    def cancel_finish_rental(self, instance):
        self.move_screen_to("edit_rental_screen")(instance)
        self.screen_manager.remove_widget(self.finish_rental_screen)



    def confirm_finish_rental(self, client_id):
        def confirm(instance):
            
            # return stock
            for item_no in self.edit_rental_screen.items_to_rent.keys():
                item = self.edit_rental_screen.items_to_rent[item_no]
                stock = int(item["stock"])
        
                new_stock = str(stock + 1)  
                self.inventory_screen.items_stored.delete(item_no)
                self.inventory_screen.items_stored.put(
                    item_no, 
                    item_name = item["item_name"],
                    hourly_rate = item["hourly_rate"],
                    stock = new_stock
                )

        
            self.refresh_items_scroll_view(self.inventory_screen)
            self.refresh_items_scroll_view(self.add_rental_screen)

            
            self.rentals_screen.rentals_stored.delete(client_id)
            self.rentals_screen.layout.scroll_layout.remove_widget(self.rentals_screen.row_widgets[client_id])
            del self.rentals_screen.row_widgets[client_id]

            self.update_rentals_stock()
            self.move_screen_to("rentals_screen")(instance)

            self.screen_manager.remove_widget(self.finish_rental_screen)
            self.screen_manager.remove_widget(self.edit_rental_screen)

        return confirm

    



if __name__ == "__main__":
    MainApp().run()


