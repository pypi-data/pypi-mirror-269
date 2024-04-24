# -*- coding: utf-8 -*-

class Paging(object):

    def __init__(self, page_no=0, limit=100, data_count=0):
        """
        :param pageNo: 目前頁數
        :param limit: 一頁顯示N筆數
        """
        _page_no = page_no - 1 if page_no > 0 else 0
        self.limit = limit
        self.total_page = 0
        self.page_no = page_no
        if data_count > 0:
            self.get_total_page(data_count)
        if self.total_page == 0:
            _page_no = 0
            self.page_no = 1
        if _page_no > 0 and _page_no >= self.total_page:
            _page_no = self.total_page - 1
            self.page_no = self.total_page
        self.start = _page_no * limit

    def get_total_page(self, data_count):
        """
        取得總頁數
        :param totalDataCount: 總資料數量
        :return: 總頁數
        """
        self.total_page = int(data_count / self.limit)
        if (data_count % self.limit) > 0:
            self.total_page += 1
        return self.total_page

    def toJSON(self):
        return self.__dict__
