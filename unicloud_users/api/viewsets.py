from rest_framework.viewsets import ModelViewSet
from unicloud_users.api.serializers import UserListSerializer, LoginTokenSerializer, MenuSerializer, UserSerializer, InvitedUserListSerializer, InvitedUserSerializer, InvalidTokenSerializer
from unicloud_users.models import UserProfile
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from ..menu import customer_menu, admin_menu
from rest_framework.renderers import JSONRenderer
from unicloud_customers.models import UserCustomer, InvitedUser, Customer
from django.shortcuts import get_object_or_404
from error_messages import messages
from check_root.unicloud_check_root import CheckRoot
from unicloud_tokengenerator.generator import TokenGenerator
from django.template.loader import get_template
from unicloud_mailersystem.mailer import UniCloudMailer
from logs.setup_log import logger

class UsersViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, )
    def retrieve(self, request):
        checkroot = CheckRoot(request)
        if checkroot.is_root():
            userlist = User.objects.filter(is_staff=True, is_superuser=True)
            serializer = UserListSerializer(userlist, many=True)
            return Response(serializer.data)
        customer_id = UserCustomer.objects.get(user_id=request.user.id).customer_id
        userlist_bycustomer = UserCustomer.objects.filter(customer_id=customer_id)
        ids = []
        for item in userlist_bycustomer:
            ids.append(item.user_id)
        userlist = User.objects.filter(id__in=ids)
        serializer = UserListSerializer(userlist, many=True)
        return Response(serializer.data)

class UserRegisterViewSet(viewsets.ViewSet):
    def user_register(self, request):
        is_invited = InvitedUser.objects.filter(email=request.data['username'])
        serialized_data = None
        isunicloud_user = False
        if is_invited.exists():
            try:
                logger.info("Get Customer of user invited Data")
                customer = Customer.objects.get(id=is_invited[0].customer_id)
                logger.info(f"Customer is {customer}")

                logger.info("Creating User and their profile")
                logger.info(f"Customer is root: {customer.type}")
                if customer.type == "root":
                    isunicloud_user=True
                user = User.objects.create_user(username=request.data['username'], password=request.data['password'], email=request.data['username'], first_name=request.data['first_name'], last_name=request.data['last_name'], is_staff=isunicloud_user, is_superuser=isunicloud_user)
                userprofile = UserProfile(phone=request.data['phone'], address=request.data['address'], city=request.data['city'], state=request.data['state'], country=request.data['country'], user=user)
                userprofile.save()
                logger.info(f"User Created: {user.id}")

                logger.info(customer)
                user_customer = UserCustomer(user=user, customer_id=customer.id)
                user_customer.save()

                serialized_data = UserSerializer(user)
            except Exception as error:
                logger.error(error)
                return Response(messages.permission_denied, 404)
            finally:
                logger.info("Deleting invite")
                is_invited.delete()
                logger.info("Invite Deleted")
            return Response(serialized_data.data)
        return Response(messages.already_exist)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = LoginTokenSerializer
    def get_object(self):
        return self.request.user

class MenuViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    def retrieve(self, request):
        if request.user.is_superuser and request.user.is_staff:
            try:
                menu = {'menu': [*admin_menu, *customer_menu]}
                serializer = MenuSerializer(menu)
                return Response(serializer.data)
            except Exception as error:
                logger.error(error)
                return Response(error)
        serializer = MenuSerializer(customer_menu)
        return Response(serializer.data)

class InviteUsersViewSet(viewsets.ViewSet):
    # permission_classes = (IsAuthenticated)
    def create(self, request):
        customer_id = UserCustomer.objects.get(user_id=request.user.id).customer_id
        customer = Customer.objects.get(id=customer_id)
        try:
            logger.info('Creating an invite')
            token_generator = TokenGenerator(request.data['email'])
            token = token_generator.gettoken()
            invited_user, created = InvitedUser.objects.get_or_create(email=request.data['email'], token=token,
                                                                      customer=customer)
            if created:
                logger.info('Invite created, sending e-mail')
                try:
                    mensagem = {
                        'empresa': customer.razao_social,
                        'link': f'https://broker.uni.cloud/auth-register/?token={token}'
                    }
                    rendered_email = get_template('email/welcome.html').render(mensagem)
                    mailer = UniCloudMailer(request.data['email'], 'Bem vindo ao Uni.Cloud Broker', rendered_email)
                    mailer.send_mail()
                    logger.info('invite sent by e-mail')
                except Exception as error:
                    logger.error(error)
                    return Response(messages.email_notsent, 400)
        except Exception as error:
            logger.error(error)
            return Response(messages.bad_request, 400)

        return Response({'status': 'created'})

    def retrieve(self, request):
        organization = UserCustomer.objects.get(user_id=request.user.id)
        invited_users_list = InvitedUser.objects.filter(customer_id=organization.customer_id)
        serializar = InvitedUserListSerializer(invited_users_list, many=True)

        return Response(serializar.data)

class TokenViewSet(viewsets.ViewSet):

    def check_token(self, request):
        token = InvitedUser.objects.filter(token=request.data['token']).exists()
        if token:
            try:
                token_data = InvitedUser.objects.get(token=request.data['token'])
                serializer = InvitedUserSerializer({'id':token_data.id, 'token':token_data.token, 'email':token_data.email, 'razao_social':token_data.customer.razao_social, 'is_valid':True})
                return Response(serializer.data)
            except Exception as error:
                logger.error(error)

        serializer = InvalidTokenSerializer({'is_valid':False})
        return Response(serializer.data)