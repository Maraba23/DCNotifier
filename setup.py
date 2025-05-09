from setuptools import setup, find_packages

setup(
    name='dcnotifier',  # Nome do pacote no PyPI
    version='0.1.0',          # Versão do seu pacote
    packages=find_packages(), # Encontra automaticamente os pacotes (pasta com __init__.py)
    
    # DEPENDÊNCIAS
    install_requires=[
        'requests',    # Exemplo de dependência
    ],

    # METADADOS
    author='Marcelo Rabello Barranco',
    author_email='rabello.barranco@gmail.com',
    description='Biblioteca para enviar notificações para o Discord de forma simples e rápida. Uso principal em aplicações de monitoramento.',
    keywords='discord, notifications, webhook',  # Palavras-chave para ajudar na busca
    
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # Formato do README
    
    license='Apache-2.0',  # Tipo de licença
    url='https://github.com/Maraba23/DCNotifier',  # Repositório do projeto

    # CLASSIFIERS ajudam o PyPI a categorizar seu pacote
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],

    python_requires='>=3.11',  # Versão mínima do Python
)
