# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['callite',
 'callite.client',
 'callite.rpctypes',
 'callite.server',
 'callite.shared']

package_data = \
{'': ['*']}

install_requires = \
['redis>=5.0.3,<6.0.0']

setup_kwargs = {
    'name': 'callite',
    'version': '0.1.4',
    'description': 'Slim Redis RPC implementation',
    'long_description': '# RPClite\n\nRPClite is a lightweight Remote Procedure Call (RPC) implementation over Redis, designed to facilitate communication between different components of a distributed system. It minimizes dependencies and offers a simple yet effective solution for decoupling complex systems, thus alleviating potential library conflicts.\n\n## Setting up RPClite\n\nBefore using RPClite, ensure you have a Redis instance running. You can start a Redis server using the default settings or configure it as per your requirements.\n\n## Implementing the Server\n\nTo implement the RPClite server, follow these steps:\n\n1. Import the `RPCService` class from `server.rpc_server`.\n2. Define your main class and initialize the RPC service with the Redis URL and service name.\n3. Register your functions with the RPC service using the `register` decorator.\n4. Run the RPC service indefinitely.\n\nHere\'s an example implementation:\n\n```python\nfrom callite.server import RPCService\n\n\nclass Main:\n    def __init__(self):\n        self.service = "service"\n        self.redis_url = "redis://redis:6379/0"\n        self.rpc_service = RPCService(self.redis_url, self.service)\n\n    def run(self):\n        @self.rpc_service.register\n        def healthcheck():\n            return "OK"\n\n        self.rpc_service.run_forever()\n\n\nif __name__ == "__main__":\n    Main().run()\n```\n\n## Calling the Function from Client\n\nOnce the server is set up, you can call functions remotely from the client side. Follow these steps to call functions:\n\n1. Import the `RPCClient` class from `client.rpc_client`.\n2. Define your client class and initialize the RPC client with the Redis URL and service name.\n3. Call the function using the `execute` method of the RPC client.\n4. Optionally, you can pass arguments and keyword arguments to the function.\n\nHere\'s an example client implementation:\n\n```python\nimport time\nfrom callite.client.rpc_client import RPCClient\n\n\nclass Healthcheck():\n    def __init__(self):\n        self.status = "OK"\n        self.r = RPCClient("redis://redis:6379/0", "service")\n\n    def get_status(self):\n        start = time.perf_counter()\n        self.status = self.r.execute(\'healthcheck\')\n        end = time.perf_counter()\n        print(f"Healthcheck took {end - start:0.4f} seconds")\n        return self.status\n\n    def check(self):\n        return self.get_status()\n\n\nif __name__ == "__main__":\n    Healthcheck().check()\n```\n\nYou can pass arguments and keyword arguments to the `execute` method as follows:\n\n```python\nself.status = self.r.execute(\'healthcheck\', [True], {\'a\': 1, \'b\': 2})\n```\n\nThis setup allows for efficient communication between components of a distributed system, promoting modularity and scalability.\n```',
    'author': 'Emrah Gozcu',
    'author_email': 'gozcu@gri.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
