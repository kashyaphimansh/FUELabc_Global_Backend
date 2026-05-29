from rest_framework.views import APIView

class AddVehicleView(
    APIView
):

    permission_classes = []

    def post(self, request):
        return APIResponse.success(

            message='Vehicle added successfully'
        )


