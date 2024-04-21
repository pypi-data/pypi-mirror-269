## This is needed to allow Airflow to pick up specific metadata fields it needs for certain features.

def get_provider_info():
    return {
        "package-name": "airflow-provider-sapiq",  # Required
        "versions": ["1.0.0",],  # Required        
        "name": "SAP IQ Airflow Provider",  # Required
        "description": "SAP IQ provider for Apache Airflow",  # Required
        "extra-links": ["sample_provider.operators.sample.SampleOperatorExtraLink"],
        'additional-dependencies': ['apache-airflow>=2.3.0'],
        'integrations': [{
            'integration-name': 'SAP IQ',
            'external-doc-url': 'https://www.sap.com/',
            'how-to-guide':  ['/docs/apache-airflow-providers-sapiq/operators.rst'],
            'logo': '/integration-logos/jdbc/JDBC.png',
            'tags': ['protocol'],
        }],
        'operators': [],
        'hooks': [{
            'integration-name': 'SAP IQ',
            'python-modules': ['airflow_provider_sapiq.hooks.sapiq'],
        }],
        'hook-class-names': ['airflow_provider_sapiq.hooks.sapiq.SapIQHook'],
        'connection-types': [{
            'hook-class-name': 'airflow_provider_sapiq.hooks.sapiq.SapIQHook',
            'connection-type': 'sapiq'
        }],
    }