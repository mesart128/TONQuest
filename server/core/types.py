from pytoniq_core import Address


class SystemAddress(Address):
    def to_system(self):
        return self.to_str(is_user_friendly=False)

    def to_response(self):
        return self.to_str(is_user_friendly=True, is_bounceable=False)
