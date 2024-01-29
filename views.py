from django.http import JsonResponse

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .serializers import AddressByXpubSerializer
from .serializers import GenerateWalletSerializer
from .serializers import MnemonicPrivateKeySerializer
from .serializers import DeleteTatumSubscriptionSerializer
from .serializers import ExchangeRateForCurrencySerializer
from .serializers import GenerateTatumSubscriptionSerializer

from .xcodes import AddressByXpubXcodeAutoSchema
from .xcodes import GenerateWalletXcodeAutoSchema
from .xcodes import BlockchainChoicesXcodeAutoSchema
from .xcodes import RemoveTatumSubscriptionXcodeAutoSchema
from .xcodes import GetPrivateKeyByMnemonicXcodeAutoSchema
from .xcodes import GenerateTatumSubscriptionXcodeAutoSchema
from .xcodes import GetExchangeRateForCurrencyXcodeAutoSchema

from .utils import generate_wallet, get_address_by_xpub, generate_tatum_subscription, remove_tatum_subscription, \
    generate_private_by_mnemonic, get_exchange_rate_for_currency

from .enums import Blockchain


class GenerateWallet(APIView):
    """
    API endpoint for generating a wallet.

    This endpoint allows the generation of a wallet for a specified blockchain.
    It expects a POST request with valid input data in the request body.

    Attributes:
        swagger_schema: An instance of the custom schema for Swagger documentation.

    Methods:
        post: Handles the POST request for generating a wallet.

    Example:
        To generate a wallet, make a POST request to this endpoint with the required data.
    """

    swagger_schema = GenerateWalletXcodeAutoSchema

    @swagger_auto_schema(
        operation_description="Generate a wallet",
        request_body=GenerateWalletSerializer,
        responses={
            201: openapi.Response('Created', content_type='application/json'),
            400: openapi.Response('Bad request', content_type='application/json'),
            500: openapi.Response("Internal Server Error", content_type="application/json"),
        },
    )
    def post(self, request):
        """
        Handle POST requests for generating a wallet.

        Args:
            request: The HTTP request object.

        Returns:
            Response: The HTTP response containing the generated wallet data or error messages.
        """
        serializer = GenerateWalletSerializer(data=request.data)
        if serializer.is_valid():
            blockchain_name = serializer.validated_data['blockchain_name']

            data = generate_wallet(blockchain_name=blockchain_name.strip())
            data["blockchain_name"] = blockchain_name

            return Response({'wallet_data': data}, status=status.HTTP_201_CREATED, content_type='application/json')

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddressByXpub(APIView):
    swagger_schema = AddressByXpubXcodeAutoSchema

    @swagger_auto_schema(
        operation_description="Generate a wallet",
        request_body=AddressByXpubSerializer,
        responses={
            201: openapi.Response('Created', content_type='application/json'),
            400: openapi.Response('Bad request', content_type='application/json'),
            500: openapi.Response("Internal Server Error", content_type="application/json"),
        },
    )
    def post(self, request):
        serializer = AddressByXpubSerializer(data=request.data)
        if serializer.is_valid():
            blockchain_name = serializer.validated_data['blockchain_name']
            xpub = serializer.validated_data['xpub']
            index = serializer.validated_data['index']

            address = get_address_by_xpub(blockchain=blockchain_name.strip(), xpub=xpub, index=index)

            return Response({'address': address}, status=status.HTTP_200_OK, content_type='application/json')

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GenerateTatumSubscription(APIView):
    swagger_schema = GenerateTatumSubscriptionXcodeAutoSchema

    @swagger_auto_schema(
        operation_description="Generate Tatum subscription",
        request_body=GenerateTatumSubscriptionSerializer,
        responses={
            201: openapi.Response('Created', content_type='application/json'),
            400: openapi.Response('Bad request', content_type='application/json'),
            500: openapi.Response("Internal Server Error", content_type="application/json"),
        },
    )
    def post(self, request):
        serializer = GenerateTatumSubscriptionSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            print(serializer.validated_data)
            address = serializer.validated_data['address']
            chain = serializer.validated_data['chain']
            subscription_type = serializer.validated_data['subscription_type']
            subscription_object = generate_tatum_subscription(address=address, chain=chain,
                                                              subscription_type=subscription_type)
            return Response({'subscription_data': subscription_object}, status=status.HTTP_201_CREATED,
                            content_type='application/json')

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemoveTatumSubscription(APIView):
    swagger_schema = RemoveTatumSubscriptionXcodeAutoSchema

    @swagger_auto_schema(
        operation_description="Remove Tatum subscription",
        request_body=DeleteTatumSubscriptionSerializer,
        responses={
            200: openapi.Response('Success', content_type='application/json'),
            400: openapi.Response('Bad request', content_type='application/json'),
            500: openapi.Response("Internal Server Error", content_type="application/json"),
        },
    )
    def delete(self, request):
        serializer = DeleteTatumSubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            subscription_id = serializer.validated_data['subscription_id']
            response = remove_tatum_subscription(subscription_id=subscription_id)
            return Response({'data': response}, status=status.HTTP_200_OK, content_type='application/json')

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MnemonicPrivateKey(APIView):
    swagger_schema = GetPrivateKeyByMnemonicXcodeAutoSchema

    @swagger_auto_schema(
        operation_description="Create Tatum subscription",
        request_body=MnemonicPrivateKeySerializer,
        responses={
            201: openapi.Response('Created', content_type='application/json'),
            400: openapi.Response('Bad request', content_type='application/json'),
            500: openapi.Response("Internal Server Error", content_type="application/json"),
        },
    )
    def post(self, request):
        serializer = MnemonicPrivateKeySerializer(data=request.data)
        if serializer.is_valid():
            mnemonic = serializer.validated_data['mnemonic']
            index = serializer.validated_data['index']

            private_key = generate_private_by_mnemonic(mnemonic=mnemonic, index=index)
            return Response({'private_key': private_key}, status=status.HTTP_200_OK,
                            content_type='application/json')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetExchangeRateForCurrency(APIView):
    swagger_schema = GetExchangeRateForCurrencyXcodeAutoSchema

    @swagger_auto_schema(
        operation_description="Get exchange rate for currency",
        request_body=ExchangeRateForCurrencySerializer,
        responses={
            201: openapi.Response('Success', content_type='application/json'),
            400: openapi.Response('Bad request', content_type='application/json'),
            500: openapi.Response("Internal Server Error", content_type="application/json"),
        },
    )
    def post(self, request):
        serializer = ExchangeRateForCurrencySerializer(data=request.data)
        if serializer.is_valid():
            crypto_symbol = serializer.validated_data['crypto_symbol']
            fiat_symbol = serializer.validated_data['crypto_symbol']
            exchange_rate = get_exchange_rate_for_currency(crypto_symbol=crypto_symbol, fiat_symbol=fiat_symbol)
            return Response({'exchange_rate': exchange_rate}, status=status.HTTP_200_OK,
                            content_type='application/json')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlockchainChoicesAPIView(APIView):
    swagger_schema = BlockchainChoicesXcodeAutoSchema

    def get(self, request):
        choices = [choice[0] for choice in Blockchain.choices]
        return JsonResponse({'blockchain_choices': choices})
