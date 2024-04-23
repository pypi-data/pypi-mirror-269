import threading

from snbpy.common.constant.snb_constant import OrderIdType
from snbpy.common.domain.response import HttpResponse
from snbpy.snb_api_client import TradeInterface
from threading import RLock
import time
import abc


class OrderStatusListener(object):
    @abc.abstractmethod
    def on_order_status_refreshed(self, order_status: HttpResponse):
        pass

    def on_order_removed(self, order_id: str):
        pass


class SimpleOrderStatusListener(OrderStatusListener):
    def __init__(self, callback, on_order_removed=None):
        self.callback = callback
        self.on_order_removed = on_order_removed

    def on_order_status_refreshed(self, order_status: HttpResponse):
        if self.callback is not None:
            self.callback(order_status)

    def on_order_removed(self, order_id: str):
        if self.on_order_removed is not None:
            self.on_order_removed(order_id)


class SnbAgentConfig(object):
    def __init__(self):
        self.auto_refresh_interval = 5
        self.remove_terminal_order = True


TERMINAL_STATUS = {"PART_WITHDRAW", "WITHDRAWED", "CONCLUDED", "INVALID", "EXPIRED"}


class SnbAgent(object):
    def __init__(self, client: TradeInterface, config: SnbAgentConfig = SnbAgentConfig()):
        self.client = client
        self.lock = RLock()
        self.order_lock = RLock()
        self.last_ts = 0
        self.sq = 0
        self.orderStatusListenerList = []
        self.order_map = {}
        self.refresh_orders_running = False
        self.refresh_thread = None
        self.config = config

    def gen_order_id(self):
        with self.lock:
            t = int(time.time())
            if self.last_ts == t:
                if self.sq == 999:
                    raise Exception("too many request in one second")
                else:
                    self.sq += 1
            else:
                self.last_ts = t
                self.sq = 0
            return "{}{:03}".format(self.last_ts, self.sq)

    def register_order_status_listener(self, listener: OrderStatusListener):
        self.orderStatusListenerList.append(listener)

    def unregister_order_status_listener(self, listener: OrderStatusListener):
        self.orderStatusListenerList.remove(listener)

    def add_order_to_auto_refresh(self, order_id: str, order_id_type: OrderIdType = OrderIdType.CLIENT):
        if order_id_type == OrderIdType.SNB:
            raise Exception("SNB order id is not supported")
        with self.order_lock:
            self.order_map[order_id] = order_id_type

    def remove_order_from_auto_refresh(self, order_id: str):
        with self.order_lock:
            try:
                self.order_map.pop(order_id)
                for listener in self.orderStatusListenerList:
                    listener.on_order_removed(order_id)
            except:
                pass

    def _notify_order_status_listener(self, order_status: HttpResponse):
        if not order_status.succeed():
            return
        if self.config.remove_terminal_order:
            if order_status.succeed() and order_status.data.get("status", "") in TERMINAL_STATUS:
                self.remove_order_from_auto_refresh(order_status.data.get("id", ""))
        for listener in self.orderStatusListenerList:
            listener.on_order_status_refreshed(order_status)

    def start_order_refresh_thread(self):
        def refresh_orders():
            while self.refresh_orders_running:
                with self.order_lock:
                    if len(self.orderStatusListenerList) != 0:
                        items = list(self.order_map.items())
                        for order_id, order_id_type in items:
                            order_status = self.client.get_order_by_id(order_id)
                            self._notify_order_status_listener(order_status)
                time.sleep(5 if self.config.auto_refresh_interval <= 1 else self.config.auto_refresh_interval)

        self.refresh_orders_running = True
        self.refresh_thread = threading.Thread(target=refresh_orders)
        self.refresh_thread.start()

    def stop_order_refresh_thread(self):
        self.refresh_orders_running = False
        if self.refresh_thread is not None:
            self.refresh_thread.join()
            self.refresh_thread = None
