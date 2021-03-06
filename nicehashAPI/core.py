import requests
import warnings
import json

algos = ['Scrypt', 'SHA256', 'ScryptNf', 'X11', 'X13', 'Keccak', 'X15',
         'Nist5', 'NeoScrypt', 'Lyra2RE', 'WhirlpoolX', 'Qubit', 'Quark',
         'Axiom', 'Lyra2REv2', 'ScryptJaneNf16', 'Blake256r8', 'Blake256r14',
         'Blake256r8vnl', 'Hodl', 'DaggerHashimoto', 'Decred', 'CryptoNight',
         'Lbry', 'Equihash', 'Pascal', 'X11Gost', 'Sia', 'Blake2s', 'Skunk']

base_url = 'https://api.nicehash.com/api?method={}'


class Pool:

    def __init__(self, pool_hostname, pool_port, pool_user, pool_password):

        """
        A simple object that contains all the information needed to connect
        to a mining pool.

        Args:
            pool_hostname (str): mining pool hostname
            pool_port (str): mining pool port
            pool_user (str): user name (usually public key to wallet)
            pool_password (str): usually x, or nothing
        """

        self._pool_hostname = str(pool_hostname)
        self._pool_port = str(pool_port)
        self._pool_user = str(pool_user)
        self._pool_password = str(pool_password)

    def save(self, filename):

        """
        Saves pool information in json format.

        Args:
            filename (str): filename to save pool information.
                Use whichever extension you want!

        """
        json.dump(self._to_dict(), open(filename, 'w'))

    @property
    def pool_hostname(self):
        """
        str: mining pool hostname
        """

        return self._pool_hostname

    @property
    def pool_port(self):
        """
        str: mining pool port
        """

        return self._pool_port

    @property
    def pool_user(self):
        """
        str: mining pool username
        """

        return self._pool_user

    @property
    def pool_password(self):
        """
        str: mining pool password
        """

        return self._pool_password

    def _to_dict(self):
        """
        Private method to create a dictionary from attributes

        Returns:
            dict: Dictionary with attribute values in the corresponding keys

        """
        return {'pool_hostname': self._pool_hostname,
                'pool_port': self._pool_port,
                'pool_user': self._pool_user,
                'pool_password': self._pool_password}


def load_pool(filename):

    """
    Function to instantiate a Pool object from a json file.

    Args:
        filename (str): file name where Pool object was saved to

    Returns:
        Pool: Pool object with information parsed from filename file

    """
    dict_pool = json.load(open(filename, 'r'))

    return Pool(dict_pool['pool_hostname'],
                dict_pool['pool_port'],
                dict_pool['pool_user'],
                dict_pool['pool_password'])


def save_pool(pool, filename):

    """
    Helper function to save Pool object. Uses the .save method of Pool object.
    This function only complements the existing load_pool function.

    Args:
        pool (Pool): Pool object to save as .json
        filename (str): name of file where Pool object will be saved

    """

    pool.save(filename)


class API:

    def __init__(self, key_path=None, id_key=None, api_key=None):

        """
        Nicehash API python wrapper.

        Args:
            key_path:
            id_key:
            api_key:
        """

        if key_path is not None:
            with open(key_path, 'r') as f:
                self._id, self._api = f.read().splitlines()
        elif id_key is not None and api_key is not None:
            self._id = str(id_key)
            self._api = str(api_key)
        elif id_key is None and key_path is None and api_key is None:
            warnings.warn("Only public queries are allowed without a key!")
        else:
            raise ValueError("Need a file path or id *AND* API keys")

    def public_query(self):
        pass

    def private_query(self):
        pass

    def API_version(self):
        query = 'https://api.nicehash.com/api'

        r = requests.get(query)

        return r.json()["result"]["api_version"]

    def profitability(self, location='global'):

        location = _check_location(location)

        query = '&'.join([base_url.format('stats.global.current'),
                          'location' + location])

        r = requests.get(query)

        result = r.json()['result']['stats']

        return {self._get_algorithm_name(result_i.pop('algo')): result_i for
                result_i in result}

    def get_orders(self, location, algorithm):

        location = _check_location(location)

        algorithm = _check_algorithm(algorithm)

        query = '&'.join([base_url.format('orders.get&my'),
                          'id=' + self._id,
                          'key=' + self._api,
                          'location=' + location,
                          'algo=' + algorithm])

        r = requests.get(query)

        return r.json()

    def create_order(self, location, algorithm, amount, price, limit, pool):

        location = _check_location(location)

        algorithm = _check_algorithm(algorithm)

        query = '&'.join([base_url.format('orders.create'),
                          'id=' + self._id,
                          'key=' + self._api,
                          'location=' + location,
                          'algo=' + algorithm,
                          'amount=' + str(amount),
                          'price=' + str(price),
                          'limit=' + str(limit),
                          'pool_host=' + pool.pool_hostname,
                          'pool_port=' + pool.pool_port,
                          'pool_user=' + pool.pool_user,
                          'pool_pass=' + pool.pool_password])

        r = requests.get(query)

        return r.json()

    def refill_order(self, location, algorithm, order, amount):

        location = _check_location(location)

        algorithm = _check_algorithm(algorithm)

        query = '&'.join([base_url.format('orders.refill'),
                          'id=' + self._id,
                          'key=' + self._api,
                          'location=' + location,
                          'algo=' + algorithm,
                          'order=' + str(order),
                          'amount=' + str(amount)])

        r = requests.get(query)

        return r.json()

    def remove_order(self, location, algorithm, order):

        location = _check_location(location)

        algorithm = _check_algorithm(algorithm)

        query = '&'.join([base_url.format('orders.remove'),
                          'id=' + self._id,
                          'key=' + self._api,
                          'location=' + location,
                          'algo=' + algorithm,
                          'order=' + str(order)])

        r = requests.get(query)

        return r.json()

    def set_order_price(self, location, algorithm, order, price):

        location = _check_location(location)

        algorithm = _check_algorithm(algorithm)

        query = '&'.join([base_url.format('orders.set.price'),
                          'id=' + self._id,
                          'key=' + self._api,
                          'location=' + location,
                          'algo=' + algorithm,
                          'order=' + str(order),
                          'price=' + str(price)])

        r = requests.get(query)

        return r.json()

    def decrease_order_price(self, location, algorithm, order):

        location = _check_location(location)

        algorithm = _check_algorithm(algorithm)

        query = '&'.join([base_url.format('orders.set.price.decrease'),
                          'id=' + self._id,
                          'key=' + self._api,
                          'location=' + location,
                          'algo=' + algorithm,
                          'order=' + str(order)])

        r = requests.get(query)

        return r.json()

    def set_order_limit(self, location, algorithm, order, limit):

        location = _check_location(location)

        algorithm = _check_algorithm(algorithm)

        query = '&'.join([base_url.format('orders.set.limit'),
                          'id=' + self._id,
                          'key=' + self._api,
                          'location=' + location,
                          'algo=' + algorithm,
                          'order=' + str(order),
                          'limit=' + str(limit)])

        r = requests.get(query)

        return r.json()

    def get_balance(self):

        query = '&'.join([base_url.format('balance'),
                          'id=' + self._id,
                          'key=' + self._api])

        r = requests.get(query)

        return r.json()

    def _get_algorithm_index(self, algorithm):
        return algos.index(algorithm)

    def _get_algorithm_name(self, index):
        return algos[index]


def _check_location(location):
    if location == 'global':
        return ''
    elif location == 'europe' or location == 0:
        return '0'
    elif location == 'us' or location == 1:
        return '1'
    else:
        raise ValueError("Unknown location!")


def _check_algorithm(algorithm):
    if isinstance(algorithm, int):
        if algorithm not in range(len(algos)):
            raise ValueError("Invalid algorithm option!")

        else:
            return str(algorithm)

    elif isinstance(algorithm, str):
        try:
            return str(algos.index(algorithm))
        except ValueError:
            raise ValueError("Unknown algorithm!")

    else:
        raise ValueError("Algorithm parameter must be either an int or str")
