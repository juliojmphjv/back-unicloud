from rest_framework.permissions import IsAuthenticated, IsAdminUser
from unicloud_customers.customer_permissions import IsCustomer, IsPartner, IsRoot
from unicloud_customers.customers import CustomerObject
from ..models import InvitedUser, Customer, UserCustomer, CustomerRelationship, OrganizationLogo
from .serializers import CustomerSerializer, CustomerTypeSerializer, LogoSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from ..receita_federal import ConsultaReceita
from rest_framework.decorators import permission_classes
from error_messages import messages
from django.template.loader import get_template
from unicloud_tokengenerator.generator import TokenGenerator
from unicloud_mailersystem.mailer import UniCloudMailer
from check_root.unicloud_check_root import CheckRoot
from logs.setup_log import logger
from rest_framework.parsers import FileUploadParser
import filetype
from unicloud_customers.customers import CustomerObject, PartnerObject
import os


class PartnerViewSet(viewsets.ViewSet):
    permission_classes = (IsRoot,)

    def create(self, request):
        customer_data = None
        cnpj = None
        try:
            consulta_receitafederal = ConsultaReceita(request.data['cnpj'])
            customer_data = consulta_receitafederal.get_data()
            cnpj = consulta_receitafederal.get_parsed()
        except Exception as error:
            logger.error(error)

        requester = CustomerObject(request).get_customer_object()
        if requester.type == 'root':
            try:
                customer = Customer.objects.get(cnpj=cnpj)
                response = messages.organization_already_exist
                status = 409
                return Response(response, status)
            except Customer.DoesNotExist:
                customer = Customer.objects.create(razao_social=customer_data['nome'],
                                                   telefone=customer_data['telefone'],
                                                   email=customer_data['email'],
                                                   bairro=customer_data['bairro'],
                                                   logradouro=customer_data['logradouro'],
                                                   numero=customer_data['numero'],
                                                   cep=customer_data['cep'],
                                                   municipio=customer_data['municipio'],
                                                   nome_fantasia=customer_data['fantasia'],
                                                   natureza_juridica=customer_data['natureza_juridica'],
                                                   estado=customer_data['uf'], cnpj=cnpj, type='partner')
                customer.save()
                token_generator = TokenGenerator(request.data['email'])
                token = token_generator.gettoken()
                try:
                    InvitedUser.objects.get(email=request.data['email'])
                    response = messages.invite_already_exist
                    status = 409
                    return Response(response, status)
                except InvitedUser.DoesNotExist:
                    invite = InvitedUser.objects.create(email=request.data['email'],customer=customer, token=token)
                    invite.save()
                    try:
                        front_url = os.getenv('URL_FRONT_END')
                        mensagem = {
                            'empresa': customer.razao_social,
                            'link': f'{front_url}/register/?token={token}'
                        }
                        rendered_email = get_template('email/welcome.html').render(mensagem)
                        mailer = UniCloudMailer(request.data['email'], 'Bem vindo ao Uni.Cloud Broker', rendered_email)
                        mailer.send_mail()
                    except Exception as error:
                        logger.error(error)

                    response = CustomerSerializer(customer)
                    status = 200
                    return Response(response.data, status)

    def list(self, request):
        logger.info('Listing')
        try:
            partner_list = Customer.objects.filter(type='partner')
            serilizer = CustomerSerializer(partner_list, many=True)
            return Response(serilizer.data)
        except Customer.DoesNotExist:
            logger.error('Customer query doesnt exists')
            return Response({'error': 'query doesnt work'})
        except Exception as error:
            logger.error(error)


class CustomerViewSet(viewsets.ViewSet):
    permission_classes = (IsPartner,)

    def list(self, request):
        try:
            customers = PartnerObject(request).get_customer_of_partner_list()
            serializer = CustomerSerializer(customers, many=True)
            return Response(serializer.data)
        except Exception as error:
            logger.error(error)

class OneCustomerViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    def partial_update(self, request, pk):
        if request.user.is_superuser and request.user.is_staff and request.user.is_authenticated:
            customer = Customer.objects.filter(pk=pk)
            customer.update(**request.data)
            serializer = CustomerSerializer(customer, many=True)
            return Response(serializer.data)

class CustomerType(viewsets.ViewSet):
    permission_classes(IsAuthenticated,)
    def get_type(self, request):
        customer_id = UserCustomer.objects.get(user_id=request.user.id).customer_id
        customer = Customer.objects.get(id=customer_id)
        serializer = CustomerTypeSerializer(customer)
        return Response(serializer.data)

class Organization(viewsets.ViewSet):
    permission_classes(IsAuthenticated, )
    parser_classes = [FileUploadParser]
    def get_organization(self, request):
        customer_id = UserCustomer.objects.get(user_id=request.user.id).customer_id
        customer = Customer.objects.get(id=customer_id)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

class OrganizationLogoViewSet(viewsets.ViewSet):
    permission_classes = (IsCustomer, )
    serializer_class = LogoSerializer
    def create(self, request):
        try:
            customer_id = UserCustomer.objects.get(user_id=request.user.id).customer_id
            customer = Customer.objects.get(id=customer_id)
            file_uploaded = request.FILES.get('file_uploaded')
            if filetype.is_image(file_uploaded):
                if customer.type == 'root' or customer.type == 'partner':
                    if OrganizationLogo.objects.filter(organization=customer).exists():
                        try:
                            update_logo = OrganizationLogo.objects.get(organization=customer)
                            update_logo.logo = file_uploaded
                            update_logo.save()
                            serializer = LogoSerializer(update_logo)
                            return Response(serializer.data)
                        except Exception as error:
                            logger.error(error)

                    else:
                        createlogo = OrganizationLogo.objects.create(logo=file_uploaded, organization=customer)
                        createlogo.save()
                    serializer = LogoSerializer(createlogo)
                    return Response(serializer.data)
                return Response({'error': 'Not Allowed'})
            return Response({'error': 'Its not an image'})
        except Exception as error:
            logger.info(error)

    def get_logo(self, request):
        try:
            customer_obj = CustomerObject(request)
            customer = customer_obj.get_customer_object()
            if customer.type == 'customer':
                logger.info('Requester is a customer')
                relationship = CustomerRelationship.objects.get(customer_id=customer.id)
                organization_father = Customer.objects.get(id=relationship.partner_id)
                father_logo = OrganizationLogo.objects.filter(organization=organization_father.id).exists()
                if father_logo:
                    logger.info('Has a partner father')
                    customer_logo = OrganizationLogo.objects.get(organization=organization_father.id)
                    serializer = LogoSerializer(customer_logo)
                    return Response(serializer.data)
                else:
                    logger.info('hasnt a partner father')
                    if Customer.objects.filter(type='root').exists():
                        organization_root = Customer.objects.get(type='root')
                        if OrganizationLogo.objects.filter(organization_id=organization_root.id).exists():
                            logger.info('Root has a logo')
                            customer_logo = OrganizationLogo.objects.get(organization_id=organization_root.id)
                            logger.info(customer_logo)
                            serializer = LogoSerializer(customer_logo)
                            return Response(serializer.data)
                        else:
                            logger.info('Root hasnt a logo')
                            return Response({'logo': None})
                    else:
                        logger.info('root doenst exists')
                        return Response({'logo': None})
            else:
                logger.info(f'Customer type: {customer.type}')
                logger.info('Resquester is not a Customer')
                organization_root = Customer.objects.get(type='root')
                logger.info(organization_root)
                if OrganizationLogo.objects.filter(organization_id=organization_root.id).exists():
                    logger.info(f'Root has a logo: {OrganizationLogo.objects.filter(organization_id=organization_root.id).exists()}')
                    customer_logo = OrganizationLogo.objects.get(organization_id=organization_root.id)
                    logger.info(customer_logo)
                    serializer = LogoSerializer(customer_logo)
                    return Response(serializer.data)
                else: return Response({'logo': None})

        except Exception as error:
            logger.error(f'Erro Except: {error}')
            return Response({'logo': error})