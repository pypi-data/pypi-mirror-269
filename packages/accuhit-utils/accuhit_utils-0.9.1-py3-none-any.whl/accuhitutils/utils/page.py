# -*- coding: utf-8 -*-
from pydantic import Field

from accuhitutils.utils.model import BaseSupportModel


class Paging(BaseSupportModel):
    """
    :param page_no:pageNum: 目前頁數
    :param page_size:pageSize: 一頁顯示N筆數
    :param total_page:totalPage: 總共有幾頁
    """
    page_size: int = Field(default=10, alias="pageSize")
    page_no: int = Field(default=1, alias="pageNum")
    total_page: int = Field(default=0, alias="totalPage")

    def __init__(self, page_no=0, page_size=100, **kwargs):
        super().__init__(**kwargs)

        self.page_no = kwargs["pageNum"] if "pageNum" in kwargs and kwargs["pageNum"] else page_no
        self.page_size = kwargs["pageSize"] if "pageSize" in kwargs and kwargs["pageSize"] else page_size

    def get_skip(self, data_count):
        """
        取得偏移數
        :param data_count: 總資料數量
        :return: 偏移數
        """
        _page_no = self.page_no - 1 if self.page_no > 0 else 0
        total_page = self.get_total_page(data_count)

        if _page_no > 0 and _page_no >= total_page:
            _page_no = total_page - 1
            self.page_no = total_page

        skip = self.page_size * (self.page_no - 1)
        if skip > total_page:
            return total_page - 1
        else:
            return skip

    def get_total_page(self, data_count):
        """
        取得總頁數
        :param data_count: 總資料數量
        :return: 總頁數
        """
        self.total_page = int(data_count / self.page_size)
        if (data_count % self.page_size) > 0:
            self.total_page += 1
        return self.total_page

    def toJSON(self):
        return self.__dict__
