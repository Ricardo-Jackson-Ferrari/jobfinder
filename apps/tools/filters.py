from rest_framework.filters import OrderingFilter


class CustomOrderFilter(OrderingFilter):
    def get_ordering(self, request, queryset, view):
        if sort := request.query_params.get('sort'):
            order = request.query_params.get('order')
            return [f'-{sort}' if order == 'desc' else sort]
        if order_fields_bt := [
            v for k, v in request.query_params.items() if 'sortName' in k
        ]:
            order_direction_bt = [
                v for k, v in request.query_params.items() if 'sortOrder' in k
            ]
            return [
                f'{order_fields_bt[i]}'
                if d == 'asc'
                else f'-{order_fields_bt[i]}'
                for i, d in enumerate(order_direction_bt)
            ]
        return self.get_default_ordering(view)
