import os
from rest_framework.viewsets import ModelViewSet
from unicloud_users.api.serializers import UserListSerializer, LoginTokenSerializer, MenuSerializer, UserSerializer, \
    InvitedUserListSerializer, InvitedUserSerializer, InvalidTokenSerializer, LoginV2Serializer, \
    UserPreferenceSerializer
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
from unicloud_customers.customer_permissions import IsCustomer, AllowAny


class UsersViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

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
    permission_classes = (IsCustomer,)

    def create(self, request):
        supported_languages = ["pt", "es", "en", "fr"]
        supported_themes = ["dark", "light"]
        try:
            user_preference = UserPreferencesModel.objects.get(user=request.user)
            if 'language' in request.data.keys() and request.data['language'] in supported_languages:
                user_preference.language = request.data['language']

            if 'theme' in request.data.keys() and request.data['theme'] in supported_themes:
                user_preference.theme = request.data['theme']

            user_preference.save()
            serializer = UserPreferenceSerializer(user_preference)
            return Response(serializer.data)

        except UserPreferencesModel.DoesNotExist:
            language = None
            theme = None
            if not 'language' in request.data.keys() and not 'theme' in request.data.keys():
                return Response(messages.user_preference_without_fields, 400)

            if 'language' in request.data.keys() and request.data['language'] in supported_languages:
                language = request.data['language']

            if 'theme' in request.data.keys() and request.data['theme'] in supported_themes:
                theme = request.data['theme']

            try:
                user_preference = UserPreferencesModel.objects.create(language=language, theme=theme,
                                                                      user=request.user)
                user_preference.save()
                serializer = UserPreferenceSerializer(user_preference)
                return Response(serializer.data)
            except Exception as error:
                logger.error(error)


        except Exception as error:
            logger.error(error)
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
    authentication_classes = []
    permission_classes = (AllowAny,)

    def user_register(self, request):
        isunicloud_user = False
        try:
            is_invited = InvitedUser.objects.get(email=request.data['username'])
            customer = Customer.objects.get(id=is_invited.customer_id)

            if customer.type == "root":
                isunicloud_user = True

            try:
                already_is_user = User.objects.get(username=request.data['username'])
                return Response(messages.user_already_exists, 409)
            except User.DoesNotExist:
                user = User.objects.create_user(username=request.data['username'], password=request.data['password'],
                                                email=request.data['username'], first_name=request.data['first_name'],
                                                last_name=request.data['last_name'], is_staff=isunicloud_user,
                                                is_superuser=isunicloud_user)
                user.save()
                user_profile = UserProfile(phone=request.data['phone'], address=request.data['address'],
                                           city=request.data['city'], state=request.data['state'],
                                           country=request.data['country'], user=user)
                user_profile.save()
                customer_user_from = UserCustomer(user=user, customer=customer)
                customer_user_from.save()
                serialized_data = UserSerializer(user)
                is_invited.delete()
                return Response(serialized_data.data)


        except InvitedUser.DoesNotExist:
            return Response(messages.invitation_doesnt_exists, 404)
        except Customer.DoesNotExist:
            return Response(messages.organization_already_exist, 409)
        except Exception as error:
            logger.error(error)
            return Response({'error': error})


class Indentify(viewsets.ViewSet):

    def identify(self, request):
        try:
            user = User.objects.get(username=request.data['username'])
            requester_organzation_id = UserCustomer.objects.get(user_id=user.id).customer_id
            organization_logo = OrganizationLogo.objects.get(organization_id=requester_organzation_id)
            obj = {
                "logo": organization_logo.logo,
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
    permission_classes = (IsCustomer,)

    def retrieve(self, request):
        try:
            organization = CustomerObject(request)
            if organization.get_customer_object().type == 'root':
                user_menu = {'menu': [*menu_object['common'], *menu_object['root']]}
                serializer = MenuSerializer(user_menu)
                return Response(serializer.data)
            elif organization.get_customer_object().type == 'partner':
                user_menu = {'menu': [*menu_object['common'], *menu_object['partner']]}
                serializer = MenuSerializer(user_menu)
                return Response(serializer.data)
            elif organization.get_customer_object().type == 'customer':
                user_menu = {'menu': [*menu_object['common'], *menu_object['customer']]}
                serializer = MenuSerializer(user_menu)
                return Response(serializer.data)
        except Exception as error:
            logger.error(error)
            return Response(messages.bad_request, 400)


class InviteUsersViewSet(viewsets.ViewSet):
    permission_classes = (IsCustomer,)

    def create(self, request):

        try:
            invited_exists = User.objects.get(username=request.data['email'])
            return Response(messages.user_already_exists, 409)
        except User.DoesNotExist:
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
                    'link': f'{front_url}/register/?token={token}'
                }
                rendered_email = get_template('email/welcome.html').render(mensagem)
                mailer = UniCloudMailer(request.data['email'], 'Bem vindo ao Uni.Cloud Broker', rendered_email)
                mailer.send_mail()
                logger.info('invite sent by e-mail')

                invitation.status = "pending"
                serializar = InvitedUserListSerializer(invitation)
                return Response(serializar.data)

    def retrieve(self, request):
        try:
            organization = UserCustomer.objects.get(user_id=request.user.id)
            invitations = InvitedUser.objects.filter(customer_id=organization.customer_id)
            for invite in invitations:
                date_expires = datetime.datetime.strftime(invite.created_at + datetime.timedelta(hours=24),
                                                          "%Y-%m-%d %H:%M:%S")
                date_expires = datetime.datetime.strptime(date_expires, '%Y-%m-%d %H:%M:%S')
                now = timezone.make_naive(timezone.now())

                if date_expires > now:
                    invite.status = 'pending'
                else:
                    invite.status = 'expired'
            serializar = InvitedUserListSerializer(invitations, many=True)
            return Response(serializar.data)
        except Exception as error:
            logger.error(error)
            return Response({'error': error})


class TokenViewSet(viewsets.ViewSet):
    authentication_classes = []
    permission_classes = (AllowAny,)

    def check_token(self, request):
        try:
            token = InvitedUser.objects.get(token=request.data['token'])
            date_expires = datetime.datetime.strftime(token.created_at + datetime.timedelta(hours=24),
                                                      "%Y-%m-%d %H:%M:%S")
            date_expires = datetime.datetime.strptime(date_expires, '%Y-%m-%d %H:%M:%S')
            now = timezone.make_naive(timezone.now())

            if date_expires > now:
                serializer = InvitedUserSerializer(
                    {'id': token.id, 'token': token.token, 'email': token.email,
                     'razao_social': token.customer.razao_social, 'is_valid': True})
                return Response(serializer.data)
            else:
                return Response(messages.invitation_expires, 410)

        except InvitedUser.DoesNotExist:
            logger.error(messages.invalid_invitation)
            return Response(messages.invalid_invitation, 404)

        except Exception as error:
            logger.error(error)
            return Response({'error': error})

    def update_invitation(self, request):
        logger.info('Re-creating the invite')
        invite = InvitedUser.objects.filter(id=request.data['id'])
        if invite.exists():
            invite = InvitedUser.objects.get(id=request.data['id'])
            token_generator = TokenGenerator(invite.email)
            token = token_generator.gettoken()
            try:
                invite.token = token
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
