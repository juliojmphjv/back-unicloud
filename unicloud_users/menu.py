menu_object = {
    "common": [
        {
            "icon": 'carbon:dashboard',
            "text": 'dashboard',
            "link": '/dashboard'
        },
        {
            "icon": "ph:users-three-thin",
            "text": "users",
            "link": "/user-list-default"
        },
    ],
    "root": [
        {
            "icon": 'fluent:database-plug-connected-20-regular',
            "text": 'infra',
            "subMenu": [
                {
                    "icon": 'clarity:resource-pool-outline-badged',
                    "text": 'resources',
                    "link": '/resources'
                },
                {
                    "icon": 'system-uicons:graph-box',
                    "text": 'monitoring',
                    "link": '/monitor'
                },
                {
                    "icon": 'eos-icons:pod-outlined',
                    "text": 'pods',
                    "link": '/unicloud-pods'
                }
            ]
        },
        {
            "icon": 'fluent:money-calculator-20-regular',
            "text": 'financial',
            "subMenu": [
                {
                    "icon": 'clarity:contract-line',
                    "text": 'contracts',
                    "link": '/contracts'
                }
            ]
        },
    ],
    "partner": [
        {
            "icon": "cil:chart-line",
            "text": "sales",
            "subMenu": [
                {
                    "icon": "wpf:business-contact",
                    "text": "partners",
                    "link": "/customers"
                },
                {
                    "icon": "carbon:result-new",
                    "text": "opportunities",
                    "link": "/requests"
                },
                {
                    "icon": "fluent:calculator-20-regular",
                    "text": "calculator",
                    "link": "/calculator"
                }
            ]
        },
    ],
    "customer": [
        {
            "icon": 'carbon:cloud-services',
            "text": 'Cloud',
            "subMenu": [
                {
                    "icon": 'simple-icons:blueprint',
                    "text": 'projects',
                    "link": '/projects'
                },
                {
                    "icon": 'carbon:ibm-cloud-vpc-endpoints',
                    "text": 'vpcs',
                    "link": '/vpcs'
                },
                {
                    "icon": 'eos-icons:edge-computing-outlined',
                    "text": 'edge',
                    "link": '/edge'
                },
                {
                    "icon": 'fa-solid:layer-group',
                    "text": 'policy-groups',
                    "link": '/policy-groups'
                },
                {
                    "icon": 'carbon:data-vis-3',
                    "text": 'elastic',
                    "link": '/elastic-ips'
                }
            ]
        },
        {
            "icon": 'carbon:data-quality-definition',
            "text": 'Compute',
            "subMenu": [
                {
                    "icon": 'carbon:instance-classic',
                    "text": 'instances',
                    "link": '/instances'
                }
            ]
        },
    ]
}
