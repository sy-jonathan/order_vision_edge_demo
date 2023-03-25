"""
Notes: 
- Add all Item objects to the order when the order is received (use the add_item method of the Order class)
- Need a dictionary of categories and the corresponding names to be displayed in the UI
- Could have a dictionary to define if each item category is a type of packaging
- If the model output identifies an object, set the status = "identified" (use update_item_status method in Order class)
- If the Item bounding box crosses into the Item.parent_item bounding box, then should set Item.status = "packaged"
- If model identifies an unknown object, new Item object should be created with required_in_order = False
  (refer to update_item_status method in Order class). The parent could be any/all packaging 
  since we don't know if they will put this unknown/new object into the burger box or directly in the brown bag?
- If required_in_order = False AND status in ("identified", "packaged"), display the item name in the order UI 
  in RED bold/italics with a "+" (e.g., "+Ketchup Packet"). Should be displayed even if display_in_order = False  
- If required_in_order = True AND status = "not_identified" AND parent_item.status = "packaged", display order 
  in RED bold/italics with a "-" (e.g., "-Cheese"). Should be displayed even if display_in_order = False 
  (e.g., if skipped top bun, should be displayed in RED) 
- If Item.parent_item = None AND the status of all child items is "packaged", then the order is complete with 100% accuracy
- update_item_status method in Order class currently assumes the order contains at most 1 item in each item category
- Without object tracking/more complex logic, this assumes the burger is built in the box, one item at a time
  (e.g., box, then bottom bun into box, then patty into box, etc.)
"""

category_names = {"burger_box": "Burger", 
                  "brown_bag": "Brown Bag", 
                  "burger_patty": "Single Patty", 
                  "":""} #need to add all the remaining categories here

class Order(object):
    order_number = "" #order number
    order_items = [] #list of Item objects in the order
    
    def __init__(self, order_number):
        self.order_number = order_number
     
    def add_item(self, name, item_category, child_items = [], parent_item = None, 
                 required_in_order = False, display_in_order = False, status = "not_identified"):
        new_item = Item(name, item_category, child_items, parent_item, required_in_order, display_in_order, status) 
        self.order_items.append(new_item)
        return new_item

    def update_item_status(self, item_category, new_status):
        """
            Assumption: the order contains at most 1 item in each item category
            Args: 
                item_category: category of the item (e.g., burger_box)
                new_status: status to set for the item (e.g, "identified", "packaged")
            Output: returns the item that has been updated
        """
        if self.order_items == []:
           return None
        for item in self.order_items: 
            if item.category == item_category: 
                item.status = new_status
                return item
        # if didn't find the item in the order_items list, create new item
        packaging_items = []
        for item in self.order_items: 
            if item.packaging == True: 
                packaging_items.append(item)
        new_item = self.add_item(
            name = category_names[item_category], 
            category = item_category, 
            child_items = None, 
            parent_item = packaging_items, #new item could have multiple parents since we don't know where it will be packaged?
            required_in_order = False, #item was not in the original order 
            display_in_order = False,  #since it wasn't in the order, don't automatically display. Only display if packaged?
            status = new_status
        )
        return new_item


class Item(object):
    name = "" #name of the object to be displayed in UI
    category = "" #category name from the model output
    packaging = False # is this item a type of packaging (e..g, brown_bag, burger_box)
    child_items = [] #list of child item objects (e.g., ingredients)
    parent_item = None #packaging for the item. If none, it is the final packaging to present to customer
    required_in_order = False #if the item is required to be included in the order
    display_in_order = False #if the item should be displayed in the UI item list
    status = "not_identified" #possible values: not_identified, identified, packaged

    def __init__(self, name, category):
        self.name = name 
        self.category = category
        self.status = "identified"
    
    def package(self):
        """Changes item's status to packaged"""
        self.status = "packaged"

    def add_child_item(self, Item):
        self.child_items.append(Item)



