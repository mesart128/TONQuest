from pytoniq_core import Address


class SystemAddress(Address):
    def to_raw(self):
        return self.to_str(is_user_friendly=False)

    def to_non_bounceable(self):
        # default readable business address
        return self.to_str(is_user_friendly=True, is_bounceable=False, is_url_safe=True)

    def __repr__(self):
        if self.anycast is not None:
            return f"SystemAddress<{self.to_non_bounceable()} with {self.anycast}>"
        return f"SystemAddress<{self.to_non_bounceable()}>"
