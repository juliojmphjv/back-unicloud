import os

from rest_framework.viewsets import ModelViewSet
from unicloud_users.api.serializers import UserListSerializer, LoginTokenSerializer, MenuSerializer, UserSerializer, InvitedUserListSerializer, InvitedUserSerializer, InvalidTokenSerializer, LoginV2Serializer, UserPreferenceSerializer
from unicloud_users.models import UserProfile, UserPreferencesModel
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from ..menu import menu_object
from unicloud_customers.customers import CustomerObject
from unicloud_customers.models import UserCustomer, InvitedUser, Customer, OrganizationLogo
from unicloud_customers.api.serializers import LogoSerializer, IdentifySerializer
from error_messages import messages
from check_root.unicloud_check_root import CheckRoot
from unicloud_tokengenerator.generator import TokenGenerator
from django.template.loader import get_template
from unicloud_mailersystem.mailer import UniCloudMailer
from logs.setup_log import logger
import datetime
from django.utils import timezone
import pytz
from unicloud_customers.customer_permissions import IsCustomer

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

class UserPreference(viewsets.ViewSet):
    permission_classes = (IsCustomer, )

    def create(self, request):
        try:
            user_preference = UserPreferencesModel.objects.create(user=request.user, language=request.data['language'], theme=request.data['theme'])
            user_preference.save()
            serializer = UserPreferenceSerializer(user_preference)
            return Response(serializer.data)
        except Exception as error:
            logger.error()
            return Response({'error': error})

    def retrieve(self, request):
        try:
            user_preference = UserPreferencesModel.objects.get(user=request.user)
            serializer = UserPreferenceSerializer(user_preference)
            return Response(serializer.data)
        except UserPreferencesModel.DoesNotExist:
            return Response(messages.user_preference_failed)
        except Exception as error:
            return Response({'error': error})



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
        logger.error(f'invite already exists: {is_invited.exists()}')
        return Response(messages.invite_already_exist, 303)

class Indentify(viewsets.ViewSet):

    def identify(self, request):
        try:
            user = User.objects.get(username=request.data['username'])
            requester_organzation_id = UserCustomer.objects.get(user_id=user.id).customer_id
            organization_logo = OrganizationLogo.objects.get(organization_id=requester_organzation_id)
            obj = {
                "logo":organization_logo.logo,
                "authentication_factors": ["password"],
            }
            serializer = IdentifySerializer(obj)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(messages.login_failed)
            pass

class LoginV2(viewsets.ViewSet):

    def login(self, request):
        try:
            user = User.objects.get(username=request.data['username'])
            if user.check_password(request.data['password']):
                refresh = RefreshToken.for_user(user)
                response = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                serializer = LoginV2Serializer(response)
                return Response(serializer.data)
            else:
                return Response(messages.login_failed)
        except User.DoesNotExist:
            return Response(messages.login_failed)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = LoginTokenSerializer
    def get_object(self):
        return self.request.user

class MenuViewSet(viewsets.ViewSet):
    permission_classes = (IsCustomer, )
    def retrieve(self, request):
        try:
            organization = CustomerObject(request)
            if organization.get_customer_object().type == 'root':
                user_menu = {'menu': [ *menu_object['common'], *menu_object['root']]}
                serializer = MenuSerializer(user_menu)
                return Response(serializer.data)
            elif organization.get_customer_object().type == 'partner':
                user_menu = {'menu': [ *menu_object['common'], *menu_object['partner']]}
                serializer = MenuSerializer(user_menu)
                return Response(serializer.data)
            elif organization.get_customer_object().type == 'customer':
                user_menu = {'menu': [ *menu_object['common'], *menu_object['customer']]}
                serializer = MenuSerializer(user_menu)
                return Response(serializer.data)
        except Exception as error:
            logger.error(error)
            return Response(messages.bad_request, 400)


class InviteUsersViewSet(viewsets.ViewSet):
    permission_classes = (IsCustomer, )
    def create(self, request):
        customer_id = UserCustomer.objects.get(user_id=request.user.id).customer_id
        customer = Customer.objects.get(id=customer_id)
        token = None
        try:
            logger.info('Check if has invite')
            invitation = InvitedUser.objects.get(email=request.data['email'])
            return Response(messages.invite_already_exist, 409)

        except InvitedUser.DoesNotExist:
            logger.info('Invite Does not exists, creating an invite')
            token_generator = TokenGenerator(request.data['email'])
            token = token_generator.gettoken()
            invitation = InvitedUser.objects.create(email=request.data['email'], token=token, customer=customer)
            invitation.save()

            logger.info("Finally sending the invitation email.")
            front_url = os.getenv('URL_FRONT_END')
            mensagem = {
                'empresa': customer.razao_social,
                'link': f'{front_url}/auth-register/?token={token}'
            }
            rendered_email = get_template('email/welcome.html').render(mensagem)
            mailer = UniCloudMailer(request.data['email'], 'Bem vindo ao Uni.Cloud Broker', rendered_email)
            mailer.send_mail()
            logger.info('invite sent by e-mail')

            serializar = InvitedUserListSerializer(invitation)
            return Response(serializar.data)

    def retrieve(self, request):
        try:
            logger.info(request.user.id)
            organization = UserCustomer.objects.get(user_id=request.user.id)
            invitations = InvitedUser.objects.filter(customer_id=organization.customer_id)
            for invite in invitations:
                date_expires = datetime.datetime.strftime(invite.created_at + datetime.timedelta(hours=24),
                                                          "%Y-%m-%d %H:%M:%S")
                date_expires = datetime.datetime.strptime(date_expires, '%Y-%m-%d %H:%M:%S')
                now = timezone.make_naive(timezone.now())

                if date_expires > now:
                    logger.info('pending')
                    setattr(invite, 'status', 'pending')
                else:
                    logger.info('expired')
                    setattr(invite, 'status', 'expired')
            serializar = InvitedUserListSerializer(invitations, many=True)
            return Response(serializar.data)
        except Exception as error:
            logger.error(error)
            return Response({'error': error})


class TokenViewSet(viewsets.ViewSet):

    def check_token(self, request):
        token = InvitedUser.objects.filter(token=request.data['token']).exists()
        if token:
            try:
                token_data = InvitedUser.objects.get(token=request.data['token'])
                date_expires = datetime.datetime.strftime(token_data.created_at + datetime.timedelta(hours=24),
                                                          "%Y-%m-%d %H:%M:%S")
                date_expires = datetime.datetime.strptime(date_expires, '%Y-%m-%d %H:%M:%S')
                now = timezone.make_naive(timezone.now())

                logger.info(f'expire in: {date_expires}')
                logger.info(f'now is: {now}')

                if date_expires > now:
                    serializer = InvitedUserSerializer({'id':token_data.id, 'token':token_data.token, 'email':token_data.email, 'razao_social':token_data.customer.razao_social, 'is_valid':True})
                    return Response(serializer.data)
                else:
                    logger.info(f'Token 24h timedelta expired.'
                                f'Token created at: {token_data.created_at}'
                                f'Time was tried to activate: {now}')
                    return Response(messages.invitation_expires, 410)
            except Exception as error:
                logger.error(error)

        serializer = InvalidTokenSerializer({'is_valid':False})
        return Response(messages.invalid_invitation, 404)

    def update_invitation(self, request):
        logger.info('Re-creating the invite')
        invite = InvitedUser.objects.filter(id=request.data['id'])
        if invite.exists():
            invite = InvitedUser.objects.get(id=request.data['id'])
            token_generator = TokenGenerator(invite.email)
            token = token_generator.gettoken()
            try:
                invite.token=token
                invite.save()
                mensagem = {
                    'empresa': invite.customer.razao_social,
                    'link': f'https://broker.uni.cloud/auth-register/?token={token}'
                }
                rendered_email = get_template('email/welcome.html').render(mensagem)
                mailer = UniCloudMailer(invite.email, 'Bem vindo ao Uni.Cloud Broker', rendered_email)
                mailer.send_mail()
                logger.info('invite sent by e-mail')
                return Response({'status': 'sent'})
            except Exception as error:
                logger.error(error)
                return Response({'error': f'Exception {error}'})
        else:
            return Response(messages.invitation_doesnt_exists, 404)