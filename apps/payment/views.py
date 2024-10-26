from django.conf import settings 
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_400_BAD_REQUEST
from authorizenet import apicontractsv1
from authorizenet.apicontrollers import createTransactionController
from .serializers.InputSerializers import PaymentSerializer

class PaymentView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data

        credit_card_number = data['credit_card_number']
        expiration_date = data['expiration_date']
        card_code = data['card_code']
        amount = data['amount']

        merchant_auth = apicontractsv1.merchantAuthenticationType()
        merchant_auth.name = settings.AUTHORIZE_NET_API_LOGIN_ID
        merchant_auth.transactionKey = settings.AUTHORIZE_NET_TRANSACTION_KEY

        credit_card = apicontractsv1.creditCardType()
        credit_card.cardNumber = credit_card_number
        credit_card.expirationDate = expiration_date
        credit_card.cardCode = card_code

        payment = apicontractsv1.paymentType()
        payment.creditCard = credit_card

        transaction_request = apicontractsv1.transactionRequestType()
        transaction_request.transactionType = "authCaptureTransaction"
        transaction_request.amount = amount
        transaction_request.payment = payment

        create_request = apicontractsv1.createTransactionRequest()
        create_request.merchantAuthentication = merchant_auth
        create_request.transactionRequest = transaction_request

        controller = createTransactionController(create_request)

        if settings.AUTHORIZE_NET_SANDBOX: #! -------------- TEST Mode --------------
            controller.setenvironment('https://apitest.authorize.net/xml/v1/request.api')
        else:
            controller.setenvironment('https://api2.authorize.net/xml/v1/request.api')

        controller.execute()

        response = controller.getresponse()
        # print(response , "+++++++++++++++++++++++++++++++++++++++++++")
        
        if response is not None and response.messages.resultCode == "Ok":
            return Response({"status": "success", "transaction_id": response.transactionResponse.transId})
        else:
            error_message = "Error processing transaction."
            if response is not None and response.transactionResponse is not None:
                if response.transactionResponse.errors is not None:
                    error_message = response.transactionResponse.errors.error[0].errorText
            return Response({"status": "error", "message": error_message}, status=HTTP_400_BAD_REQUEST)
