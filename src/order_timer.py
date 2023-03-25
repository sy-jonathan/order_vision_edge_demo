import time


class OrderTimer:
    def __init__(self):
        self.tot_strt_time = None
        self.ord_plcd_tm = None
        self.ord_strt_tm = None
        self.ord_fin_tm = None
        self.ord_pkup_tm = None 

    def place_order(self):
        """
        An order is placed, start total and first timer
        """
        if self.ord_plcd_tm is None:
            self.ord_plcd_tm = time.time()
            self.tot_strt_time = time.time()
        else:
            raise Exception("Order has already been placed")
    
    def start_making_order(self):
        """
        An order is started, start total and second timer
        """
        if self.ord_strt_tm is None:
            self.ord_strt_tm = time.time()
        else:
            raise Exception("Making of order has already been started")

    def finished_making_order(self):
        """
        An order is placed, start total and first timer
        """
        if self.ord_fin_tm is None:
            self.ord_fin_tm = time.time()
        else:
            raise Exception("Order has already been finished")

    def pickup_order(self):
        """
        An order is picked up, all time attributes should be filled
        """
        if self.ord_pkup_tm is None:
            self.ord_pkup_tm = time.time()
        else:
            raise Exception("Order has already been picked up")
    
    def get_order_placed_to_start_time(self):
        """
        Return current order placed to start time
        """
        if self.ord_strt_tm is None:
            cur = time.time()
            return (cur - self.ord_plcd_tm)
        else:
            return (self.ord_strt_tm - self.ord_plcd_tm)

    def get_order_assemble_time(self):
        """
        Return current order assembly time
        """
        if self.ord_fin_tm is None:
            cur = time.time()
            return (cur - self.ord_strt_tm)
        else:
            return (self.ord_fin_tm - self.ord_strt_tm)
        
    def get_order_pickup_wait_time(self):
        """
        Return current order pickup wait time
        """
        if self.ord_pkup_tm is None:
            cur = time.time()
            return (cur - self.ord_fin_tm)
        else:
            return (self.ord_pkup_tm - self.ord_fin_tm)
        
    def get_total_order_time(self):
        """
        Return the total time this order has taken. If the order is in progress is will return a running counter.
        """
        if self.ord_pkup_tm is None:
            cur = time.time()
            return (cur - self.tot_strt_time)
        else:
            return (self.ord_pkup_tm - self.tot_strt_time)