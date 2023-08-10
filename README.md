# Rental Manager
A kivy app that manages rentals. This app was inspired by the needs of a small business that rents surfing related materials. The app allows for the management of an inventory and for the creation of rental instances. When a rental is finished, the app displays the total amount the client owes for the items rented and the time they were rented for. 

Notes:
 - The app assumes that items are rented and returned in the same day.
 - The app does not allow for item edits while there are active rentals. This is to prevent unexpected behaviour when modifying the underlying items of an active rental.
 - The user should not terminate the app whenever adding a rental, editing a rental or finishing a rental. When in one of these screens, the user should always either cancel or confirm the changes before quitting the app. If this instruction is not followed, this may result in unexpected stock levels.

## Pricing Options

There are several options for choosing prices that the app supports.
- The simplest option is to just use one floating point number. That is, if the user add an item and chooses an hourly rate which is the string "10.5", then this means that each hour a client rents this item for will cost 10.5mu. For example, if a client rents this for 2.5 hours, then this amounts to a total of 26.25mu.
- Another option is to introduce several prices separated by commas. For example, if the hourly rate is "10.5, 7", then this means that the first hour costs 10.5mu, the second hour costs 7mu and any hour above that also costs 7mu. In this example, if this item is rented for 2.5 hours, then the total would be 21mu. This corresponds to 10.5mu for the first hour, 7mu for the second and 7*0.5 for half of the third hour. The user can choose to add more prices if they so desire. For example, "10.5, 7, 5, 3" is a valid hourly rate.
- The third option that the app supports is the introduction of a daily rate. For example, if the user introduces the hourly rate "10.5, 7 - 20", then this means that the first hour costs 10.5mu, the second hour costs 7mu and any amount of time above that costs 20mu. That is, a value that follows a hyphen stands for the daily rate of that item.
