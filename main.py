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
from history.history_screen import HistoryScreen
from history.finished_rental_info import FinishedRentalScreen
from inventory.inv_row_widget import RowWidget as InvRowWidget
from rentals.rent_row_widget import RowWidget as RentRowWidget
from rentals.add_rental_row_widget import AddRentalRowWidget
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

        self.history_screen = HistoryScreen(name="history_screen")


        


        # Button functionality
        self.rentals_screen.layout.go_to_inventory_btn.bind(on_release=self.move_screen_to("inventory_screen"))
        self.rentals_screen.layout.add_rental_btn.bind(on_release=self.new_rental_click)
        self.rentals_screen.layout.go_to_history_btn.bind(on_release=self.move_screen_to("history_screen"))
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
        

        self.history_screen.layout.go_back_btn.bind(on_release=self.move_screen_to("rentals_screen"))
        for row_widget in self.history_screen.row_widgets.values():
            row_widget.client_name_btn.bind(on_release=self.finished_rental_clicked)


        # Add screens to screen manager
        self.screen_manager.add_widget(self.rentals_screen)
        self.screen_manager.add_widget(self.add_rental_screen)
        

        self.screen_manager.add_widget(self.inventory_screen)
        self.screen_manager.add_widget(self.add_item_screen)

        self.screen_manager.add_widget(self.history_screen)
        

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
            
            if current == "rentals_screen" and screen_name == "history_screen":
                self.screen_manager.transition.direction = "up"
            
            if current == "history_screen" and screen_name == "rentals_screen":
                self.screen_manager.transition.direction = "down"

            if current == "history_screen" and screen_name == "finished_rental_screen":
                self.screen_manager.transition.direction = "up"

            if current == "finished_rental_screen" and screen_name == "history_screen":
                self.screen_manager.transition.direction = "down"
            
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
        

        # create items_rented
        items_rented = {}
        for item_no in self.add_rental_screen.row_widgets:
            item_name = self.inventory_screen.items_stored.get(item_no)["item_name"]
            hourly_rate = self.inventory_screen.items_stored.get(item_no)["hourly_rate"]
            stock = int(self.inventory_screen.items_stored.get(item_no)["stock"])
            quantity = self.add_rental_screen.row_widgets[item_no].quantity_text_input.text

            if quantity == "":
                continue
            else:
                try:
                    int_quantity = int(quantity)
                    if int_quantity <= 0:
                        errors.append("invalid_quantity")

                    if int_quantity > int(stock):
                        errors.append("not_enough_stock")

                    if 0 < int_quantity <= stock:
                        items_rented[item_no] = {
                        "item_name": item_name,
                        "hourly_rate": hourly_rate,
                        "quantity": quantity
                        }

                except:
                    errors.append("invalid_quantity")

            



        # create client id
        client_id = 0
        for id in self.rentals_screen.rentals_stored.keys():
            if int(id) > client_id:
                client_id = int(id)
        client_id = str(client_id + 1)

        # create hourly prices
        hourly_price = self.rentals_screen.compute_hourly_price(self.add_item_screen, items_rented) # NEED TO CHANGE FUNCTION

        


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
        if items_rented == {}:
            errors.append("no_items")


        
        if errors == []:

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


            # update stocks
            for item_no in items_rented:
                stock = int(self.inventory_screen.items_stored.get(item_no)["stock"])  
                int_quantity = int(items_rented[item_no]["quantity"])
                new_stock = str(stock - int_quantity)
                self.inventory_screen.items_stored.delete(item_no)
                self.inventory_screen.items_stored.put(
                    item_no, 
                    item_name = items_rented[item_no]["item_name"],
                    hourly_rate = items_rented[item_no]["hourly_rate"],
                    stock = new_stock
                )
                
            

            self.refresh_items_scroll_view(self.inventory_screen)

            self.move_screen_to("rentals_screen")(instance)

            self.add_rental_screen.layout.name_text_input.text = ""
            self.add_rental_screen.layout.hour_text_input.text = ""
            

            for item_no in self.add_rental_screen.row_widgets:
                self.add_rental_screen.row_widgets[item_no].quantity_text_input.text = ""

            
        
            if self.add_rental_screen.layout.error_time_label in self.add_rental_screen.layout.children:
                self.add_rental_screen.layout.remove_widget(self.add_rental_screen.layout.error_time_label)

            if self.add_rental_screen.layout.error_items_label in self.add_rental_screen.layout.children:
                self.add_rental_screen.layout.remove_widget(self.add_rental_screen.layout.error_items_label)

            if self.add_rental_screen.layout.error_stock_label in self.add_rental_screen.layout.children:
                self.add_rental_screen.layout.remove_widget(self.add_rental_screen.layout.error_stock_label)

            if self.add_rental_screen.layout.error_quantity_label in self.add_rental_screen.layout.children:
                self.add_rental_screen.layout.remove_widget(self.add_rental_screen.layout.error_quantity_label)


        
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

        if "not_enough_stock" in errors:
            if self.add_rental_screen.layout.error_stock_label not in self.add_rental_screen.layout.children:
                self.add_rental_screen.layout.add_widget(self.add_rental_screen.layout.error_stock_label)

        if "not_enough_stock" not in errors:
            if self.add_rental_screen.layout.error_stock_label in self.add_rental_screen.layout.children:
                self.add_rental_screen.layout.remove_widget(self.add_rental_screen.layout.error_stock_label)

        if "invalid_quantity" in errors:
            if self.add_rental_screen.layout.error_quantity_label not in self.add_rental_screen.layout.children:
                self.add_rental_screen.layout.add_widget(self.add_rental_screen.layout.error_quantity_label)

        if "invalid_quantity" not in errors:
            if self.add_rental_screen.layout.error_quantity_label in self.add_rental_screen.layout.children:
                self.add_rental_screen.layout.remove_widget(self.add_rental_screen.layout.error_quantity_label)





    

    
    

    def refresh_items_scroll_view(self, screen):
        # screen is either add_rental_screen, edit_rental_screen, inventory_screen
        # this function deletes the current row_widgets in screen.layout.scroll_view and recreates the scroll_view based on
        # the items that are currently stored in inventory_screen.items_stored

        for item_no in screen.row_widgets.keys():
            screen.layout.scroll_layout.remove_widget(screen.row_widgets[item_no])
            
       
        screen.row_widgets = {}


        item_no_list = list(map(lambda x: int(x), self.inventory_screen.items_stored.keys()))
        item_no_list.sort()

        if screen == self.inventory_screen:
            for item_no in item_no_list:
                item_no = str(item_no)
                row = InvRowWidget(
                    item_no,
                    self.inventory_screen.items_stored.get(item_no)["item_name"],
                    f"\u20ac{self.inventory_screen.items_stored.get(item_no)['hourly_rate']}",
                    str(self.inventory_screen.items_stored[item_no]['stock']),
                )
                screen.row_widgets[item_no] = row
                screen.layout.scroll_layout.add_widget(row)

                screen.row_widgets[item_no].item_name_btn.bind(on_release=self.edit_item_clicked)
        else:
            for item_no in item_no_list:
                item_no = str(item_no)
                row = AddRentalRowWidget(
                    item_no,
                    self.inventory_screen.items_stored.get(item_no)["item_name"],
                    f"\u20ac{self.inventory_screen.items_stored.get(item_no)['hourly_rate']}",
                    str(self.inventory_screen.items_stored[item_no]['stock']),
                    screen.window_height
                )
                screen.row_widgets[item_no] = row
                screen.layout.scroll_layout.add_widget(row)

                
                

            
                


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


            row = RentRowWidget(
                client_id,
                self.rentals_screen.rentals_stored.get(client_id)["client_name"],
                self.rentals_screen.rentals_stored.get(client_id)['start_time'],
                f"\u20ac{hourly_price}"
            )
            self.rentals_screen.row_widgets[client_id] = row
            self.rentals_screen.layout.scroll_layout.add_widget(row)

            self.rentals_screen.row_widgets[client_id].client_name_btn.bind(on_release=self.edit_rental_clicked)



    def refresh_history_scroll_view(self):
        for date in self.history_screen.finished_rentals_stored:
            if date in self.history_screen.row_widgets:
                self.history_screen.layout.scroll_layout.remove_widget(
                    self.history_screen.row_widgets[date]
                )
            
        self.history_screen.row_widgets = {}  


        date_list = list(self.history_screen.finished_rentals_stored.keys())
        date_list.sort(key=self.history_screen.absolute_date, reverse=True)
        
        for date in date_list:
            simple_date = date.split(".")[0]
            row = RentRowWidget(
                simple_date,
                self.history_screen.finished_rentals_stored.get(date)["client_name"],
                self.history_screen.finished_rentals_stored.get(date)['start_time'],
                f"\u20ac{self.history_screen.finished_rentals_stored.get(date)['total']}",
            )
            row.date = date
            self.history_screen.row_widgets[date] = row
            self.history_screen.layout.scroll_layout.add_widget(row)  

            self.history_screen.row_widgets[date].client_name_btn.bind(on_release=self.finished_rental_clicked)    

        


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
        if self.rentals_screen.rentals_stored.get(client_id).get("subtotal", 0) != 0:
            rental["subtotal"] = self.rentals_screen.rentals_stored.get(client_id)["subtotal"]

        

        associated_rental = {client_id: rental}

        

        self.edit_rental_screen = EditRentalScreen(self.inventory_screen, associated_rental, name="edit_rental_screen")
        self.screen_manager.add_widget(self.edit_rental_screen)

        

        self.edit_rental_screen.layout.name_text_input.text = rental["client_name"]
        self.edit_rental_screen.layout.hour_text_input.text = rental["start_time"]

        
        


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

        self.add_rental_screen.layout.name_text_input.text = ""
        self.add_rental_screen.layout.hour_text_input.text = ""
        
        for item_no in self.add_rental_screen.row_widgets:
            self.add_rental_screen.row_widgets[item_no].quantity_text_input.text = ""

        

        self.add_rental_screen.items_to_rent = {}
        
        if self.add_rental_screen.layout.error_time_label in self.add_rental_screen.layout.children:
            self.add_rental_screen.layout.remove_widget(self.add_rental_screen.layout.error_time_label)

        if self.add_rental_screen.layout.error_items_label in self.add_rental_screen.layout.children:
            self.add_rental_screen.layout.remove_widget(self.add_rental_screen.layout.error_items_label)

        if self.add_rental_screen.layout.error_stock_label in self.add_rental_screen.layout.children:
            self.add_rental_screen.layout.remove_widget(self.add_rental_screen.layout.error_stock_label)

        if self.add_rental_screen.layout.error_quantity_label in self.add_rental_screen.layout.children:
            self.add_rental_screen.layout.remove_widget(self.add_rental_screen.layout.error_quantity_label)

        
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

            

            if not self.add_item_screen.verify_stock_entry(new_stock):
                errors.append("invalid_stock")

            

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
            
            errors = []     # list of errors
            
            # create new_items_to_rent
            new_items_to_rent = {}
            for item_no in self.edit_rental_screen.row_widgets:
                item_name = self.inventory_screen.items_stored.get(item_no)["item_name"]
                hourly_rate = self.inventory_screen.items_stored.get(item_no)["hourly_rate"]
                stock = int(self.inventory_screen.items_stored.get(item_no)["stock"])
                current_quantity = int(
                    self.rentals_screen.rentals_stored.get(client_id)["items_rented"].get(item_no, {"quantity": 0})["quantity"]
                )
                new_quantity = self.edit_rental_screen.row_widgets[item_no].quantity_text_input.text

                if new_quantity == "":
                    continue
                else:
                    try:
                        int_new_quantity = int(new_quantity)
                        if int_new_quantity <= 0:
                            errors.append("invalid_quantity")

                        if int_new_quantity > current_quantity + stock:
                            errors.append("not_enough_stock")

                        if 0 < int_new_quantity <= current_quantity + stock:
                            new_items_to_rent[item_no] = {
                            "item_name": item_name,
                            "hourly_rate": hourly_rate,
                            "quantity": new_quantity
                            }

                    except:
                        errors.append("invalid_quantity")



            

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
            if new_items_to_rent == {}:
                errors.append("no_items")

            
            if errors == []:
                
                # return stocks of old items
                for item_no in self.edit_rental_screen.items_rented:
                    stock = int(self.inventory_screen.items_stored.get(item_no)["stock"])  
                    int_quantity = int(self.edit_rental_screen.items_rented[item_no]["quantity"])
                    new_stock = str(stock + int_quantity)
                    self.inventory_screen.items_stored.delete(item_no)
                    self.inventory_screen.items_stored.put(
                        item_no, 
                        item_name = self.edit_rental_screen.items_rented[item_no]["item_name"],
                        hourly_rate = self.edit_rental_screen.items_rented[item_no]["hourly_rate"],
                        stock = new_stock
                    )

                # take stocks of new items
                for item_no in new_items_to_rent:
                    stock = int(self.inventory_screen.items_stored.get(item_no)["stock"])  
                    int_quantity = int(new_items_to_rent[item_no]["quantity"])
                    new_stock = str(stock - int_quantity)
                    self.inventory_screen.items_stored.delete(item_no)
                    self.inventory_screen.items_stored.put(
                        item_no, 
                        item_name = new_items_to_rent[item_no]["item_name"],
                        hourly_rate = new_items_to_rent[item_no]["hourly_rate"],
                        stock = new_stock
                    )

                
                

                # create hourly price
                new_hourly_price = self.rentals_screen.compute_hourly_price(self.add_item_screen, new_items_to_rent)

                subtotal = self.rentals_screen.rentals_stored.get(client_id).get("subtotal", 0)

                self.rentals_screen.rentals_stored.delete(client_id)
                self.rentals_screen.layout.scroll_layout.remove_widget(self.rentals_screen.row_widgets[client_id])
                del self.rentals_screen.row_widgets[client_id]


                
                if subtotal == 0:
                    self.rentals_screen.rentals_stored.put(
                        client_id, 
                        client_name = new_client_name, 
                        start_time = new_start_time,
                        hourly_price = new_hourly_price,
                        items_rented = new_items_to_rent
                    )
                else:
                    self.rentals_screen.rentals_stored.put(
                        client_id, 
                        client_name = new_client_name, 
                        start_time = new_start_time,
                        hourly_price = new_hourly_price,
                        subtotal = subtotal,
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

            if "not_enough_stock" in errors:
                if self.edit_rental_screen.layout.error_stock_label not in self.edit_rental_screen.layout.children:
                    self.edit_rental_screen.layout.add_widget(self.edit_rental_screen.layout.error_stock_label)

            if "not_enough_stock" not in errors:
                if self.edit_rental_screen.layout.error_stock_label in self.edit_rental_screen.layout.children:
                    self.edit_rental_screen.layout.remove_widget(self.edit_rental_screen.layout.error_stock_label)

            if "invalid_quantity" in errors:
                if self.edit_rental_screen.layout.error_quantity_label not in self.edit_rental_screen.layout.children:
                    self.edit_rental_screen.layout.add_widget(self.edit_rental_screen.layout.error_quantity_label)

            if "invalid_quantity" not in errors:
                if self.edit_rental_screen.layout.error_quantity_label in self.edit_rental_screen.layout.children:
                    self.edit_rental_screen.layout.remove_widget(self.edit_rental_screen.layout.error_quantity_label)


        return confirm
    

    def cancel_edit_item(self, item_no):
        def cancel(instance):
            self.move_screen_to("inventory_screen")(instance)
            self.screen_manager.remove_widget(self.edit_item_screen)
        return cancel
    

    def cancel_edit_rental(self, associated_rental):
        def cancel(instance):
            self.move_screen_to("rentals_screen")(instance)
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
            for item_no in self.edit_rental_screen.items_rented:
                item_name = self.inventory_screen.items_stored.get(item_no)["item_name"]
                hourly_rate = self.inventory_screen.items_stored.get(item_no)["hourly_rate"]
                stock = int(self.inventory_screen.items_stored.get(item_no)["stock"])
                int_quantity = int(self.edit_rental_screen.items_rented[item_no]["quantity"])
                new_stock = str(stock + int_quantity)  
                self.inventory_screen.items_stored.delete(item_no)
                self.inventory_screen.items_stored.put(
                    item_no, 
                    item_name = item_name,
                    hourly_rate = hourly_rate,
                    stock = new_stock
                )


            
            

            self.refresh_items_scroll_view(self.inventory_screen)
            


            self.rentals_screen.rentals_stored.delete(client_id)
            self.rentals_screen.layout.scroll_layout.remove_widget(self.rentals_screen.row_widgets[client_id])
            del self.rentals_screen.row_widgets[client_id]


            

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
            self.finish_rental_screen.layout.recalculate_btn.bind(on_release=self.finish_rental_screen.recalculate(self.inventory_screen))
            self.finish_rental_screen.layout.finish_btn.bind(on_release=self.confirm_finish_rental(client_id))
            self.finish_rental_screen.layout.cancel_btn.bind(on_release=self.cancel_finish_rental)
            
        return finish
    

    
    def cancel_finish_rental(self, instance):
        self.move_screen_to("edit_rental_screen")(instance)
        self.screen_manager.remove_widget(self.finish_rental_screen)



    def confirm_finish_rental(self, client_id):
        def confirm(instance):
            
            errors = []
            # validate hour format
            new_start_time = self.finish_rental_screen.layout.hour_text_input.text
            new_end_time = self.finish_rental_screen.layout.end_time_text_input.text
            list = new_start_time.split(":")
            try:
                hour = int(list[0])
                minutes = int(list[1])

                if hour < 0 or hour >= 24 or minutes < 0 or minutes >= 60:  
                    errors.append("invalid_start_time")
            except:
                errors.append("invalid_start_time")


            list = new_end_time.split(":")
            try:
                hour = int(list[0])
                minutes = int(list[1])

                if hour < 0 or hour >= 24 or minutes < 0 or minutes >= 60:  
                    errors.append("invalid_end_time")
            except:
                errors.append("invalid_end_time")

            # create finished items
            items_to_finish = {}
            for item_no in self.finish_rental_screen.row_widgets:
                
                quantity_to_finish = self.finish_rental_screen.row_widgets[item_no].quantity_text_input.text
                quantity_rented = int(self.edit_rental_screen.items_rented[item_no]["quantity"])

                if quantity_to_finish == "":
                    continue
                else:
                    try:
                        int_quantity_to_finish = int(quantity_to_finish)
                        if int_quantity_to_finish <= 0:
                            errors.append("invalid_quantity")

                        if int_quantity_to_finish > quantity_rented:
                            errors.append("invalid_quantity")

                        if 0 < int_quantity_to_finish <= quantity_rented:
                            item_name = self.inventory_screen.items_stored.get(item_no)["item_name"]
                            hourly_rate = self.inventory_screen.items_stored.get(item_no)["hourly_rate"]
                            
                            items_to_finish[item_no] = {
                            "item_name": item_name,
                            "hourly_rate": hourly_rate,
                            "quantity_to_finish": quantity_to_finish
                            }

                    except:
                        errors.append("invalid_quantity")
            
            

            if errors == []:
                # return stock
                for item_no in items_to_finish:
                    item = items_to_finish[item_no]
                    
                    stock = int(self.inventory_screen.items_stored.get(item_no)["stock"])
            
                    new_stock = str(stock + int(item["quantity_to_finish"]))  
                    self.inventory_screen.items_stored.delete(item_no)
                    self.inventory_screen.items_stored.put(
                        item_no, 
                        item_name = item["item_name"],
                        hourly_rate = item["hourly_rate"],
                        stock = new_stock
                    )

                self.refresh_items_scroll_view(self.inventory_screen)
                self.refresh_items_scroll_view(self.add_rental_screen)


                # check if it is a partial finish
                partial_finish = False
                for row in self.finish_rental_screen.row_widgets.values():
                    quantity_to_finish = row.quantity_text_input.text
                    quantity_rented = int(row.stock)
                    if quantity_to_finish == "":
                        partial_finish = True
                    elif int(quantity_to_finish) < quantity_rented:
                        partial_finish = True

                if partial_finish:
                    # add subtotal to rental
                    current_subtotal = self.finish_rental_screen.subtotal(new_start_time, new_end_time)
                    previous_subtotal = float(self.rentals_screen.rentals_stored.get(client_id).get("subtotal", 0))
                    subtotal = round(current_subtotal + previous_subtotal, 2)
                    
                    client_name = self.rentals_screen.rentals_stored.get(client_id)["client_name"]
                    client_start_time = self.rentals_screen.rentals_stored.get(client_id)["start_time"]
                    
                    new_items_rented = {}
                    for item_no in self.edit_rental_screen.items_rented:
                        quantity_to_finish = self.finish_rental_screen.row_widgets[item_no].quantity_text_input.text
                        if quantity_to_finish == "":
                            item_name = self.edit_rental_screen.items_rented[item_no]["item_name"]
                            hourly_rate = self.edit_rental_screen.items_rented[item_no]["hourly_rate"]
                            quantity = self.edit_rental_screen.items_rented[item_no]["quantity"]
                            new_items_rented[item_no] = {
                                "item_name": item_name,
                                "hourly_rate": hourly_rate,
                                "quantity": quantity
                            }

                        elif int(quantity_to_finish) < int(self.finish_rental_screen.row_widgets[item_no].stock):
                            item_name = self.edit_rental_screen.items_rented[item_no]["item_name"]
                            hourly_rate = self.edit_rental_screen.items_rented[item_no]["hourly_rate"]
                            quantity = self.edit_rental_screen.items_rented[item_no]["quantity"]
                            new_items_rented[item_no] = {
                                "item_name": item_name,
                                "hourly_rate": hourly_rate,
                                "quantity": str(int(quantity) - int(quantity_to_finish))
                            }

                    # save finished rental to history
                    date = str(datetime.now())
                    self.history_screen.finished_rentals_stored.put(
                        date,
                        client_name = client_name,
                        start_time = client_start_time,
                        end_time = new_end_time,
                        total = current_subtotal, 
                        items_finished = items_to_finish
                    )
                    
                    self.refresh_history_scroll_view()
                    

                    # update rental storage 
                    new_hourly_price = self.rentals_screen.compute_hourly_price(self.add_item_screen, new_items_rented)
                    self.rentals_screen.rentals_stored.delete(client_id)
                    self.rentals_screen.rentals_stored.put(
                        client_id,
                        client_name = client_name,
                        start_time = client_start_time,
                        hourly_price = new_hourly_price,
                        subtotal = subtotal,
                        items_rented = new_items_rented,
                    )

                    self.refresh_rentals_scroll_view()



                    self.move_screen_to("rentals_screen")(instance)

                    self.screen_manager.remove_widget(self.finish_rental_screen)
                    self.screen_manager.remove_widget(self.edit_rental_screen)
                    
                else:             
                    # save finished rental to history
                    client_name = self.rentals_screen.rentals_stored.get(client_id)["client_name"]
                    client_start_time = self.rentals_screen.rentals_stored.get(client_id)["start_time"]
                    current_subtotal = self.finish_rental_screen.subtotal(new_start_time, new_end_time)
                    date = str(datetime.now())
                    self.history_screen.finished_rentals_stored.put(
                        date,
                        client_name = client_name,
                        start_time = client_start_time,
                        end_time = new_end_time,
                        total = current_subtotal, 
                        items_finished = items_to_finish
                    )   

                    
                    self.refresh_history_scroll_view()

                    # remove rental from rental screen and from active rentals storage
                    self.rentals_screen.rentals_stored.delete(client_id)
                    self.rentals_screen.layout.scroll_layout.remove_widget(self.rentals_screen.row_widgets[client_id])
                    del self.rentals_screen.row_widgets[client_id]

                    
                    self.move_screen_to("rentals_screen")(instance)

                    self.screen_manager.remove_widget(self.finish_rental_screen)
                    self.screen_manager.remove_widget(self.edit_rental_screen)


            if "invalid_start_time" in errors or "invalid_end_time" in errors:
                if self.finish_rental_screen.layout.error_time_label not in self.finish_rental_screen.layout.children:
                    self.finish_rental_screen.layout.add_widget(self.finish_rental_screen.layout.error_time_label)

        
            if "invalid_start_time" not in errors and "invalid_end_time" not in errors:
                if self.finish_rental_screen.layout.error_time_label in self.finish_rental_screen.layout.children:
                    self.finish_rental_screen.layout.remove_widget(self.finish_rental_screen.layout.error_time_label)

            if "invalid_quantity" in errors:
                if self.finish_rental_screen.layout.error_quantity_label not in self.finish_rental_screen.layout.children:
                    self.finish_rental_screen.layout.add_widget(self.finish_rental_screen.layout.error_quantity_label)

        
            if "invalid_quantity" not in errors:
                if self.finish_rental_screen.layout.error_quantity_label in self.finish_rental_screen.layout.children:
                    self.finish_rental_screen.layout.remove_widget(self.finish_rental_screen.layout.error_quantity_label)

            

        return confirm

    
    def finished_rental_clicked(self, instance):
        for row_widget in self.history_screen.row_widgets.values():
            if row_widget.client_name_btn == instance:
                date = row_widget.date        

        self.finished_rental_screen = FinishedRentalScreen(date, self.history_screen, name="finished_rental_screen")
        self.screen_manager.add_widget(self.finished_rental_screen)

        

        self.finished_rental_screen.layout.name_text_input.text = self.history_screen.finished_rentals_stored.get(date)["client_name"]
        self.finished_rental_screen.layout.start_time_text_input.text = self.history_screen.finished_rentals_stored.get(date)["start_time"]
        self.finished_rental_screen.layout.end_time_text_input.text = self.history_screen.finished_rentals_stored.get(date)["end_time"]

        

        self.move_screen_to("finished_rental_screen")(instance)

        # Button functionality in Finished Rental Screen
        self.finished_rental_screen.layout.remove_finished_rental_btn.bind(on_release=self.remove_finished_rental(date))
        self.finished_rental_screen.layout.go_back_btn.bind(on_release=self.finished_rental_back)
        


    def finished_rental_back(self, instance):
        self.move_screen_to("history_screen")(instance)
        self.screen_manager.remove_widget(self.finished_rental_screen)



    def remove_finished_rental(self, date):
        def remove(instance):
            self.history_screen.finished_rentals_stored.delete(date)
            self.history_screen.layout.scroll_layout.remove_widget(self.history_screen.row_widgets[date])
            del self.history_screen.row_widgets[date]

            self.move_screen_to("history_screen")(instance)
            self.screen_manager.remove_widget(self.finished_rental_screen)

        return remove




if __name__ == "__main__":
    MainApp().run()


