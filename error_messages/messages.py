
permission_denied = {
    'data': {
        'detail': 'User not allowed to perform this operation.',
        'code': 'not_allowed',
        'messages': [
            {
                'token_class': 'AccessToken',
                'token_type': 'access',
                'message': 'User not allowed to perform this operation.',
            }
         ]
    }
}

email_notsent = {
    'data': {
        'detail': 'Error in mailer system',
        'code': 'email_notsent',
        'messages': [
            {
                'token_class': 'AccessToken',
                'token_type': 'access',
                'message': 'We can`t sent the e-mail',
            }
        ]
    }
}

bad_request = {
    'data': {
        'detail': 'bad request',
        'code': 'exception_occured',
        'messages': [
            {
                'token_class': 'AccessToken',
                'token_type': 'access',
                'message': 'An exception occured',
            }
        ]
    }
}

invite_already_exist = {
    'data': {
        'detail': 'Invite Already Exists',
        'code': 'try_to_create_a_register_who_exists',
        'messages': [
            {
                'token_class': 'AccessToken',
                'token_type': 'access',
                'message': 'You Try to create a register who already exists',
            }
        ]
    }
}

organization_already_exist = {
    'data': {
        'detail': 'Organization Already Exists',
        'code': 'try_to_create_a_register_who_exists',
        'messages': [
            {
                'token_class': 'AccessToken',
                'token_type': 'access',
                'message': 'You Try to create a organization register who already exists',
            }
        ]
    }
}

invitation_expires = {
    'data': {
        'detail': 'Invite expires',
        'code': 'The invitation already expires',
        'messages': [
            {
                'token_class': 'AccessToken',
                'token_type': 'access',
                'message': 'This invitation already expires, please, contact your Sys Admin and request to re-send',
            }
        ]
    }
}

invalid_invitation = {
    'data': {
        'detail': 'Invalid Invite',
        'code': 'The invitation is invalid',
        'messages': [
            {
                'token_class': 'AccessToken',
                'token_type': 'access',
                'message': 'This invitation dont exists',
            }
        ]
    }
}

invitation_doesnt_exists = {
    'data': {
        'detail': 'Invitation doesnt exists',
        'code': 'The invitation doesnt exists',
        'messages': [
            {
                'token_class': 'AccessToken',
                'token_type': 'access',
                'message': 'This invitation doesnt exists',
            }
        ]
    }
}

login_failed = {
    'data': {
        "detail": "No active account found or incorrect password with the given credentials",
        'code': 'login_failed',
        'messages': [
            {
                'token_class': 'AccessToken',
                'token_type': 'access',
                'message': 'No active account found or incorrect password with the given credentials',
            }
        ]
    }
}

user_preference_failed = {
    'data': {
        "detail": "User Havent Preferences",
        'code': 'get_preferences_failed',
        'messages': [
            {
                'token_class': 'AccessToken',
                'token_type': 'access',
                'message': 'User Havent Preferences',
            }
        ]
    }
}

user_already_exists = {
    'data': {
        "detail": "User Already Exists",
        'code': 'user_already_exists',
        'messages': [
            {
                'token_class': 'AccessToken',
                'token_type': 'access',
                'message': 'An user with this username already exists.',
            }
        ]
    }
}

language_unsupported = {
    'data': {
        "detail": "Language unsupported",
        'code': 'language_unsupported',
        'messages': [
            {
                'token_class': 'AccessToken',
                'token_type': 'access',
                'message': 'This language is not supported by broker',
            }
        ]
    }
}

theme_unsupported = {
    'data': {
        "detail": "Theme unsupported",
        'code': 'theme_unsupported',
        'messages': [
            {
                'token_class': 'AccessToken',
                'token_type': 'access',
                'message': 'This theme is not supported by broker',
            }
        ]
    }
}

user_preference_without_fields = {
    'data': {
        "detail": "Post without required fields",
        'code': 'post_without_required_fields',
        'messages': [
            {
                'token_class': 'AccessToken',
                'token_type': 'access',
                'message': 'You need to send theme or language field',
            }
        ]
    }
}

opportunity_doesnt_exist = {
    'data': {
        "detail": "Opportunity does'nt exist",
        'code': 'opp_does_not_exists',
        'messages': [
            {
                'token_class': 'AccessToken',
                'token_type': 'access',
                'message': 'This Opportunity does not exists',
            }
        ]
    }
}

cnpj_error = {
    'data': {
        "detail": "Invalid CNPJ",
        'code': 'invalid_cnpj',
        'messages': [
            {
                'token_class': 'AccessToken',
                'token_type': 'access',
                'message': 'CNPJ wrong or invalid',
            }
        ]
    }
}

subscription_already_exists = {
    'data': {
        "detail": "Already exists subscription with this name.",
        'code': 'subscription_exists',
        'messages': [
            {
                'token_class': 'AccessToken',
                'token_type': 'access',
                'message': 'Already exists subscription with this name.',
            }
        ]
    }
}

subscription_doesnt_existis = {
    'data': {
        "detail": "Subscription does not exists.",
        'code': 'subscription_doesnt_exists',
        'messages': [
            {
                'token_class': 'AccessToken',
                'token_type': 'access',
                'message': 'Subscription does not exists.',
            }
        ]
    }
}

already_existis_subscription_whith_this_name = {
    'data': {
        "detail": "Already existis subscription whith this name.",
        'code': 'already_exists_this_name',
        'messages': [
            {
                'token_class': 'AccessToken',
                'token_type': 'access',
                'message': 'Already existis subscription whith this name.',
            }
        ]
    }
}

deleted = {
    'data': 'deleted'
}