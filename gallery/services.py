from rest_framework.response import Response


def get_data_response(serializer, items, many=True, check_valid=False, status=200):
    if not items:
        return Response([])

    items_serializer = serializer(items, many=many)

    if check_valid:
        items_serializer.is_valid(raise_exception=True)

    return Response(data=items_serializer.data, status=status)
