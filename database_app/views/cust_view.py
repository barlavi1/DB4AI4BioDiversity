from rest_framework import mixins, viewsets


# created a generic view set excluding the option to delete from db
class NoDeleteViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      viewsets.GenericViewSet):
    pass

