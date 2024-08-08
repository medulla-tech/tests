from configparser import ConfigParser
from pprint import pprint
import xmlrpc.client
import urllib.parse
import http.client
import argparse
import base64
import json
import ssl
import os

def get_config(conffile):
    configdata = {}
    config = ConfigParser()
    if not os.path.isfile(conffile):
        raise FileNotFoundError(f"The configuration file {conffile} was not found.")
    config.read(conffile)

    configdata['xmlrpc_server'] = config.get("global", "xmlrpc_server")
    configdata['username'] = config.get("global", "login")
    configdata['password'] = config.get("global", "password")
    configdata['user'] = config.get("global", "user")
    configdata['user_passwd'] = config.get("global", "user_passwd")
    return configdata

def execute_request(config, method, params, include_cookie=False, debug=False):
    """
    Execute an XML-RPC request.

    :param config: dict with connection details.
    :param method: XML-RPC method to call.
    :param params: parameters for the method.
    :param include_cookie: whether to include the session cookie in the request.
    :param debug: whether to print debug information.
    :return: tuple (headers, body).
    """
    url = "/"
    agent_info = config
    request_xml = xmlrpc.client.dumps(params, methodname=method, encoding='UTF-8')

    # Prepare HTTP headers
    headers = {
        "User-Agent": "MMC web interface",
        "Host": urllib.parse.urlparse(agent_info['xmlrpc_server']).netloc,
        "Content-Type": "text/xml",
        "Content-Length": str(len(request_xml)),
        "Authorization": "Basic " + base64.b64encode(
            f"{agent_info['username']}:{agent_info['password']}".encode()).decode()
    }

    if include_cookie and 'cookie' in agent_info:
        headers["Cookie"] = agent_info['cookie']

    # Create SSL context if necessary
    context = None
    parsed_url = urllib.parse.urlparse(agent_info['xmlrpc_server'])
    if parsed_url.scheme == 'https':
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

    # Create connection
    connection = http.client.HTTPSConnection(parsed_url.hostname, parsed_url.port, context=context) if parsed_url.scheme == 'https' else http.client.HTTPConnection(parsed_url.hostname, parsed_url.port)

    if debug:
        print(f"Connecting to {parsed_url.scheme}://{parsed_url.hostname}:{parsed_url.port}{url}")
        print("Request headers:")
        pprint(headers)
        print("Request body:")
        print(request_xml)

    try:
        connection.request("POST", url, body=request_xml, headers=headers)
        response = connection.getresponse()
        response_headers = response.getheaders()
        response_body = response.read()

        if debug:
            print("Response status:", response.status)
            print("Response reason:", response.reason)
            print("Response headers:")
            pprint(response_headers)
            print("Response body:")
            print(response_body.decode('utf-8'))

        connection.close()
        return response_headers, response_body.decode('utf-8')
    except Exception as e:
        connection.close()
        raise e

def authenticate_and_get_cookie(config, method, params, debug=False):
    """
    Authenticate user and retrieve session cookie.

    :param config: dict with connection details.
    :param method: XML-RPC method to call.
    :param params: parameters for the method.
    :param debug: whether to print debug information.
    :return: session cookie.
    """
    headers, body = execute_request(config, method, params, debug=debug)

    # Parse headers to extract the cookie
    headers_dict = dict(headers)
    if 'Set-Cookie' in headers_dict:
        cookie = headers_dict['Set-Cookie']
        config['cookie'] = cookie

    else:
        raise Exception('Authentication failed, no cookie received')

    if debug:
        print("Authentication successful, cookie:")
        pprint(cookie)
    else:
        if 'TWISTED_SECURE_SESSION' in cookie:
            print("Authentication successful for TWISTED cookie")
        else:
            print("Authentication successful, cookie received")

    return cookie

def send_xmlrpc_request(config, method, params, debug=False):
    """
    Send an authenticated XML-RPC request.

    :param config: dict with connection details.
    :param method: XML-RPC method to call.
    :param params: parameters for the method.
    :param debug: whether to print debug information.
    :return: parsed XML-RPC response.
    """
    headers, body = execute_request(config, method, params, include_cookie=True, debug=debug)
    response = xmlrpc.client.loads(body)[0][0]

    if isinstance(response, dict) and 'faultCode' in response:
        raise Exception(f"XML-RPC fault: {response['faultString']} ({response['faultCode']})")

    return response

def main():
    parser = argparse.ArgumentParser(description="XML-RPC Client CLI")
    parser.add_argument("--module", required=True, help="The module name")
    parser.add_argument("--function", required=True, help="The function name")
    parser.add_argument("--params", required=True, help="The parameters as a JSON string")
    parser.add_argument("--config", default="xmlrpc_client.ini", help="Path to the configuration file")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")

    args = parser.parse_args()

    # Construct the full path to the config file
    config_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), args.config)

    # Load the configuration
    config = get_config(config_path)

    # Authenticate and get the cookie
    auth_method = "base.ldapAuth"
    auth_params = (config['user'], config['user_passwd'])

    try:
        cookie = authenticate_and_get_cookie(config, auth_method, auth_params, debug=args.debug)
    except Exception as e:
        print(f"Error during authentication: {e}")
        return

    # Prepare the parameters for the function call
    try:
        params = json.loads(args.params)
        if isinstance(params, list):
            params = tuple(params)
        else:
            params = (params,)
    except json.JSONDecodeError as e:
        print(f"Error decoding parameters: {e}.")
        print("Make sure your JSON string is properly formatted. For example:")
        print('Correct format: \'["param1", "param2", 123, true, {"key": "value"}]\'')
        print(f"Params passed: {args.params}")
        return

    # Send an XML-RPC request using the authenticated session
    try:
        method_name = f"{args.module}.{args.function}"
        response = send_xmlrpc_request(config, method_name, params, debug=args.debug)
        pprint(response)  # Use pprint to print the response in a readable format
    except Exception as e:
        print(f"Error during XML-RPC request: {e}")

if __name__ == "__main__":
    main()
