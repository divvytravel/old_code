__author__ = 'indieman'

from tastypie.paginator import Paginator


class TripPaginator(Paginator):
    def page(self):
        output = super(TripPaginator, self).page()
        # output['meta']['max_price']
        output['meta']['min_price'], output['meta']['max_price'] = self.get_max_min_price()
        return output

    def get_max_min_price(self):
        min_price = 100500
        max_price = 0

        for object in self.objects:
            if object.price > max_price:
                max_price = object.price
            if object.price < min_price:
                min_price = object.price

        return min_price, max_price