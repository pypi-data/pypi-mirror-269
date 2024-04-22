from gyerpsdkcore.api.base import BaseApi


class NewStock(BaseApi):
    KEY = "gy.erp.new.stock"

    def get(self, **kwargs):
        return self._post(
            func_name='get',
            **kwargs
        )

    def add(self, **kwargs):
        return self._post(
            func_name='add',
            **kwargs
        )

