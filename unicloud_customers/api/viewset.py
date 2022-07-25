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


class CustomerViewSet(viewsets.ViewSet):
    permission_classes = (IsPartner,)

    def create(self, request):
        response = None
        status = None
        consulta_receitafederal = ConsultaReceita(request.data['cnpj'])
        customer_data = consulta_receitafederal.get_data()
        check_requester = CheckRoot(request)
        requester_organzation_id = UserCustomer.objects.get(user_id=request.user.id).customer_id
        requester_organization_instance = Customer.objects.get(id=requester_organzation_id)
        if check_requester.is_root():
            type=request.data['type']
        else: type='customer'
        customer, created = Customer.objects.get_or_create(razao_social=customer_data['nome'], telefone=customer_data['telefone'], email=customer_data['email'], bairro=customer_data['bairro'], logradouro=customer_data['logradouro'], numero=customer_data['numero'], cep=customer_data['cep'], municipio=customer_data['municipio'], nome_fantasia=customer_data['fantasia'], natureza_juridica=customer_data['natureza_juridica'], estado=customer_data['uf'], cnpj=customer_data['cnpj'], type=type)
        if created:
            relationship = CustomerRelationship(customer=customer, partner=requester_organization_instance)
            relationship.save()
            token_generator = TokenGenerator(request.data['email'])
            token = token_generator.gettoken()
            invited_user, created = InvitedUser.objects.get_or_create(email=request.data['email'],customer=customer, token=token)
            if created:
                mensagem = {
                    'empresa': customer.razao_social,
                    'link': f'http://127.0.0.1:3000/auth-register/?token={token}'
                }
                rendered_email = get_template('email/welcome.html').render(mensagem)
                mailer = UniCloudMailer(request.data['email'], 'Bem vindo ao Uni.Cloud Broker', rendered_email)
                mailer.send_mail()
                response = CustomerSerializer(customer)
                status = 200
                return Response(response.data, status)
            return Response(response, status)
        if not created:
            response = messages.already_exist
            status = 400
            return Response(response, status)
        response = CustomerSerializer(customer)
        status = 200
        return Response(response.data, status)


    def list(self, request):
        organization = Customer.objects.get(id=UserCustomer.objects.get(user_id=request.user.id).customer_id)
        customers = []
        customer_list = CustomerRelationship.objects.filter(partner_id=organization.id)
        for customer in customer_list:
            customers.append(customer.customer_id)
        customerlist = Customer.objects.filter(id__in=customers)

        serializer = CustomerSerializer(customerlist, many=True)
        return Response(serializer.data)

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
                        update_logo = OrganizationLogo.objects.get(organization=customer)
                        update_logo.objects.update(logo=file_uploaded)
                        update_logo.save()
                        serializer = LogoSerializer(update_logo)
                        return Response(serializer.data)
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