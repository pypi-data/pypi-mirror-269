from gyerpsdkcore.api.base import BaseApi


class NewStock(BaseApi):
    KEY = "gy.erp.new.stock"

    def get(self, params):
        return self._post(
            func_name='get',
            params=params
        )

    def add(self, params):
        return self._post(
            func_name='add',
            params=params
        )


