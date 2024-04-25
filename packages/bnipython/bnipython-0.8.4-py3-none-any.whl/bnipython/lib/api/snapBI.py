from bnipython.lib.net.httpClient import HttpClient
from bnipython.lib.util.response import responseSnapBI
from bnipython.lib.util.utils import getTimestamp, generateSignatureServiceSnapBI, randomNumber


class SnapBI():
    def __init__(self, client, options={'privateKeyPath', 'channelId', 'ipAddress', 'latitude', 'longitude'}):
        self.client = client
        self.baseUrl = client.getBaseUrl()
        self.config = client.getConfig()
        self.httpClient = HttpClient()
        self.configSnap = options
        self.configSnap['ipAddress'] = options.get('ipAddress', '')
        self.configSnap['latitude'] = options.get('latitude', '')
        self.configSnap['longitude'] = options.get('longitude', '')
        self.configSnap['channelId'] = options.get('channelId', '')

    def getTokenSnapBI(self):
        token = self.httpClient.tokenRequestSnapBI({
            'url': f'{self.baseUrl}/snap/v1/access-token/b2b',
            'clientId': self.config['clientId'],
            'privateKeyPath': self.configSnap['privateKeyPath']
        })
        return token['accessToken']

    def balanceInquiry(self, params={
        'partnerReferenceNo,'
        'accountNo'
    }):
        token = self.getTokenSnapBI()
        body = {
            'partnerReferenceNo': params['partnerReferenceNo'],
            'accountNo': params['accountNo']
        }
        timeStamp = getTimestamp()
        signature = generateSignatureServiceSnapBI({
            'body': body,
            'method': 'POST',
            'url': '/snap-service/v1/balance-inquiry',
            'accessToken': token,
            'timeStamp': timeStamp,
            'apiSecret': self.config['apiSecret']
        })
        res = self.httpClient.requestSnapBI({
            'method': 'POST',
            'apiKey': self.config['apiKey'],
            'accessToken': token,
            'url': f'{self.baseUrl}/snap-service/v1/balance-inquiry',
            'data': body,
            'additionalHeader': {
                'X-SIGNATURE': signature,
                'X-TIMESTAMP': timeStamp,
                'X-PARTNER-ID': self.config['apiKey'],
                'X-IP-Address': self.configSnap['ipAddress'],
                'X-DEVICE-ID': 'bni-python/0.1.0',
                'X-EXTERNAL-ID': randomNumber(),
                'CHANNEL-ID': self.configSnap['channelId'],
                'X-LATITUDE': self.configSnap['latitude'],
                'X-LONGITUDE': self.configSnap['longitude']
            }
        })
        return responseSnapBI(params={'res': res})

    def internalAccountInquiry(self, params={
        'partnerReferenceNo',
        'beneficiaryAccountNo'
    }):
        token = self.getTokenSnapBI()
        body = {
            'partnerReferenceNo': params['partnerReferenceNo'],
            'beneficiaryAccountNo': params['beneficiaryAccountNo'],
        }

        timeStamp = getTimestamp()
        signature = generateSignatureServiceSnapBI({
            'body': body,
            'method': 'POST',
            'url': '/snap-service/v1/account-inquiry-internal',
            'accessToken': token,
            'timeStamp': timeStamp,
            'apiSecret': self.config['apiSecret']
        })
        res = self.httpClient.requestSnapBI({
            'method': 'POST',
            'apiKey': self.config['apiKey'],
            'accessToken': token,
            'url': f'{self.baseUrl}/snap-service/v1/account-inquiry-internal',
            'data': body,
            'additionalHeader': {
                'X-SIGNATURE': signature,
                'X-TIMESTAMP': timeStamp,
                'X-PARTNER-ID': self.config['apiKey'],
                'X-IP-Address': self.configSnap['ipAddress'],
                'X-DEVICE-ID': 'bni-python/0.1.0',
                'X-EXTERNAL-ID': randomNumber(),
                'CHANNEL-ID': self.configSnap['channelId'],
                'X-LATITUDE': self.configSnap['latitude'],
                'X-LONGITUDE': self.configSnap['longitude']
            }
        })
        return responseSnapBI(params={'res': res})

    def transactionStatusInquiry(self, params={
        'originalPartnerReferenceNo',
        'originalReferenceNo',
        'originalExternalId',
        'serviceCode',
        'transactionDate',
        'amount',
        'additionalInfo'
    }):

        token = self.getTokenSnapBI()
        body = {
            'originalPartnerReferenceNo': params['originalPartnerReferenceNo'],
            'originalReferenceNo': params['originalReferenceNo'] if  params['originalReferenceNo'] != '' else '',
            'originalExternalId': params['originalExternalId'] if params['originalExternalId'] != '' else '',
            'serviceCode': params['serviceCode'],
            'transactionDate': params['transactionDate'] if params['transactionDate'] != '' else '',
            'amount': {
                'value': params['amount']['value'],
                'currency': params['amount']['currency']
            },
        }

        additional_info = params.get('additionalInfo')
        if additional_info is not None:
            if isinstance(additional_info, dict):
                body['additionalInfo'] = {
                    'deviceId': additional_info.get('deviceId', ''),
                    'channel': additional_info.get('channel', '')
                }

        timeStamp = getTimestamp()
        signature = generateSignatureServiceSnapBI({
            'body': body,
            'method': 'POST',
            'url': '/snap-service/v1/transfer/status',
            'accessToken': token,
            'timeStamp': timeStamp,
            'apiSecret': self.config['apiSecret']
        })
        res = self.httpClient.requestSnapBI({
            'method': 'POST',
            'apiKey': self.config['apiKey'],
            'accessToken': token,
            'url': f'{self.baseUrl}/snap-service/v1/transfer/status',
            'data': body,
            'additionalHeader': {
                'X-SIGNATURE': signature,
                'X-TIMESTAMP': timeStamp,
                'X-PARTNER-ID': self.config['apiKey'],
                'X-IP-Address': self.configSnap['ipAddress'],
                'X-DEVICE-ID': 'bni-python/0.1.0',
                'X-EXTERNAL-ID': randomNumber(),
                'CHANNEL-ID': self.configSnap['channelId'],
                'X-LATITUDE': self.configSnap['latitude'],
                'X-LONGITUDE': self.configSnap['longitude']
            }
        })
        return responseSnapBI(params={'res': res})

    def transferIntraBank(self, params={
        'partnerReferenceNo',
        'amount',
        'beneficiaryAccountNo',
        'beneficiaryEmail',
        'currency',
        'customerReference',
        'feeType',
        'remark',
        'sourceAccountNo',
        'transactionDate',
        'additionalInfo'
    }
    ):

        token = self.getTokenSnapBI()
        body = {
            'partnerReferenceNo': params['partnerReferenceNo'],
            'amount': {
                'value': params['amount']['value'],
                'currency': params['amount']['currency']
            },
            'beneficiaryAccountNo': params['beneficiaryAccountNo'],
            'beneficiaryEmail': params['beneficiaryEmail'] if params['beneficiaryEmail'] != '' else '',
            'currency': params['currency'] if params['currency'] != '' else '',
            'customerReference': params['customerReference'] if params['customerReference'] != '' else '',
            'feeType': params['feeType'] if params['feeType'] != '' else '',
            'remark': params['remark'] if params['remark'] != '' else '',
            'sourceAccountNo': params['sourceAccountNo'],
            'transactionDate': timeStamp if params['transactionDate'] == '' else params['transactionDate'],
        }
        additional_info = params.get('additionalInfo')
        if additional_info is not None:
            if isinstance(additional_info, dict):
                body['additionalInfo'] = {
                    'deviceId': additional_info.get('deviceId', ''),
                    'channel': additional_info.get('channel', '')
                }

        timeStamp = getTimestamp()
        signature = generateSignatureServiceSnapBI({
            'body': body,
            'method': 'POST',
            'url': '/snap-service/v1/transfer-intrabank',
            'accessToken': token,
            'timeStamp': timeStamp,
            'apiSecret': self.config['apiSecret']
        })
        res = self.httpClient.requestSnapBI({
            'method': 'POST',
            'apiKey': self.config['apiKey'],
            'accessToken': token,
            'url': f'{self.baseUrl}/snap-service/v1/transfer-intrabank',
            'data': body,
            'additionalHeader': {
                'X-SIGNATURE': signature,
                'X-TIMESTAMP': timeStamp,
                'X-PARTNER-ID': self.config['apiKey'],
                'X-IP-Address': self.configSnap['ipAddress'],
                'X-DEVICE-ID': 'bni-python/0.1.0',
                'X-EXTERNAL-ID': randomNumber(),
                'CHANNEL-ID': self.configSnap['channelId'],
                'X-LATITUDE': self.configSnap['latitude'],
                'X-LONGITUDE': self.configSnap['longitude']
            }
        })
        return responseSnapBI(params={'res': res})

    def transferRTGS(self, params={
        'partnerReferenceNo',
        'amount',
        'beneficiaryAccountName',
        'beneficiaryAccountNo',
        'beneficiaryAccountAddress',
        'beneficiaryBankCode',
        'beneficiaryBankName',
        'beneficiaryCustomerResidence',
        'beneficiaryCustomerType',
        'beneficiaryEmail',
        'currency',
        'customerReference',
        'feeType',
        'kodePos',
        'recieverPhone',
        'remark',
        'senderCustomerResidence',
        'senderCustomerType',
        'senderPhone',
        'sourceAccountNo',
        'transactionDate',
        'additionalInfo'
    }):

        token = self.getTokenSnapBI()
        body = {
            'partnerReferenceNo': params['partnerReferenceNo'],
            'amount': {
                'value': params['amount']['value'],
                'currency': params['amount']['currency']
            },
            'beneficiaryAccountName': params['beneficiaryAccountName'],
            'beneficiaryAccountNo': params['beneficiaryAccountNo'],
            'beneficiaryAccountAddress': params['beneficiaryAccountAddress'] if params['beneficiaryAccountAddress'] != '' else '',
            'beneficiaryBankCode': params['beneficiaryBankCode'],
            'beneficiaryBankName': params['beneficiaryBankName'] if params['beneficiaryBankName'] != '' else '',
            'beneficiaryCustomerResidence': params['beneficiaryCustomerResidence'],
            'beneficiaryCustomerType': params['beneficiaryCustomerType'],
            'beneficiaryEmail': params['beneficiaryEmail'] if params['beneficiaryEmail'] != '' else '',
            'currency': params['currency'] if params['currency'] != '' else '',
            'customerReference': params['customerReference'],
            'feeType': params['feeType'] if params['feeType'] != '' else '',
            'kodePos': params['kodePos'] if params['kodePos'] != '' else '',
            'recieverPhone': params['recieverPhone'] if params['recieverPhone'] != '' else '',
            'remark': params['remark'] if params['remark'] != '' else '',
            'senderCustomerResidence': params['senderCustomerResidence'] if params['senderCustomerResidence'] != '' else '',
            'senderCustomerType': params['senderCustomerType'] if params['senderCustomerType'] != '' else '',
            'senderPhone': params['senderPhone'] if params['senderPhone'] != '' else '',
            'sourceAccountNo': params['sourceAccountNo'],
            'transactionDate': timeStamp if params['transactionDate'] == '' else params['transactionDate'],
        }
        additional_info = params.get('additionalInfo')
        if additional_info is not None:
            if isinstance(additional_info, dict):
                body['additionalInfo'] = {
                    'deviceId': additional_info.get('deviceId', ''),
                    'channel': additional_info.get('channel', '')
                }

        timeStamp = getTimestamp()
        signature = generateSignatureServiceSnapBI({
            'body': body,
            'method': 'POST',
            'url': '/snap-service/v1/transfer-rtgs',
            'accessToken': token,
            'timeStamp': timeStamp,
            'apiSecret': self.config['apiSecret']
        })
        res = self.httpClient.requestSnapBI({
            'method': 'POST',
            'apiKey': self.config['apiKey'],
            'accessToken': token,
            'url': f'{self.baseUrl}/snap-service/v1/transfer-rtgs',
            'data': body,
            'additionalHeader': {
                'X-SIGNATURE': signature,
                'X-TIMESTAMP': timeStamp,
                'X-PARTNER-ID': self.config['apiKey'],
                'X-IP-Address': self.configSnap['ipAddress'],
                'X-DEVICE-ID': 'bni-python/0.1.0',
                'X-EXTERNAL-ID': randomNumber(),
                'CHANNEL-ID': self.configSnap['channelId'],
                'X-LATITUDE': self.configSnap['latitude'],
                'X-LONGITUDE': self.configSnap['longitude']
            }
        })
        return responseSnapBI(params={'res': res})

    def transferSKNBI(self, params={
        'partnerReferenceNo',
        'amount',
        'beneficiaryAccountName',
        'beneficiaryAccountNo',
        'beneficiaryAddress',
        'beneficiaryBankCode',
        'beneficiaryBankName',
        'beneficiaryCustomerResidence',
        'beneficiaryCustomerType',
        'beneficiaryEmail',
        'currency',
        'customerReference',
        'feeType',
        'kodePos',
        'recieverPhone',
        'remark',
        'senderCustomerResidence',
        'senderCustomerType',
        'senderPhone',
        'sourceAccountNo',
        'transactionDate',
        'additionalInfo'
    }):

        token = self.getTokenSnapBI()
        body = {
            'partnerReferenceNo': params['partnerReferenceNo'],
            'amount': {
                'value': params['amount']['value'],
                'currency': params['amount']['currency']
            },
            'beneficiaryAccountName': params['beneficiaryAccountName'],
            'beneficiaryAccountNo': params['beneficiaryAccountNo'],
            'beneficiaryAddress': params['beneficiaryAddress'] if params['beneficiaryAddress'] != '' else '',
            'beneficiaryBankCode': params['beneficiaryBankCode'],
            'beneficiaryBankName': params['beneficiaryBankName'] if params['beneficiaryBankName'] != '' else '',
            'beneficiaryCustomerResidence': params['beneficiaryCustomerResidence'],
            'beneficiaryCustomerType': params['beneficiaryCustomerType'],
            'beneficiaryEmail': params['beneficiaryEmail'] if params['beneficiaryEmail'] != '' else '',
            'currency': params['currency'] if params['currency'] != '' else '',
            'customerReference': params['customerReference'],
            'feeType': params['feeType'] if params['feeType'] != '' else '',
            'kodePos': params['kodePos'] if params['kodePos'] != '' else '',
            'recieverPhone': params['recieverPhone'] if params['recieverPhone'] != '' else '',
            'remark': params['remark'] if params['remark'] != '' else '',
            'senderCustomerResidence': params['senderCustomerResidence'] if params['senderCustomerResidence'] != '' else '',
            'senderCustomerType': params['senderCustomerType'] if params['senderCustomerType'] != '' else '',
            'senderPhone': params['senderPhone'] if params['senderPhone'] != '' else '',
            'sourceAccountNo': params['sourceAccountNo'],
            'transactionDate': timeStamp if params['transactionDate'] == '' else params['transactionDate'],
        }
        additional_info = params.get('additionalInfo')
        if additional_info is not None:
            if isinstance(additional_info, dict):
                body['additionalInfo'] = {
                    'deviceId': additional_info.get('deviceId', ''),
                    'channel': additional_info.get('channel', '')
                }

        timeStamp = getTimestamp()
        signature = generateSignatureServiceSnapBI({
            'body': body,
            'method': 'POST',
            'url': '/snap-service/v1/transfer-skn',
            'accessToken': token,
            'timeStamp': timeStamp,
            'apiSecret': self.config['apiSecret']
        })
        res = self.httpClient.requestSnapBI({
            'method': 'POST',
            'apiKey': self.config['apiKey'],
            'accessToken': token,
            'url': f'{self.baseUrl}/snap-service/v1/transfer-skn',
            'data': body,
            'additionalHeader': {
                'X-SIGNATURE': signature,
                'X-TIMESTAMP': timeStamp,
                'X-PARTNER-ID': self.config['apiKey'],
                'X-IP-Address': self.configSnap['ipAddress'],
                'X-DEVICE-ID': 'bni-python/0.1.0',
                'X-EXTERNAL-ID': randomNumber(),
                'CHANNEL-ID': self.configSnap['channelId'],
                'X-LATITUDE': self.configSnap['latitude'],
                'X-LONGITUDE': self.configSnap['longitude']
            }
        })
        return responseSnapBI(params={'res': res})

    def externalAccountInquiry(self, params={
        'beneficiaryBankCode',
        'beneficiaryAccountNo',
        'partnerReferenceNo',
        'additionalInfo'
    }):

        token = self.getTokenSnapBI()
        body = {
            'beneficiaryBankCode': params['beneficiaryBankCode'],
            'beneficiaryAccountNo': params['beneficiaryAccountNo'],
            'partnerReferenceNo': params['partnerReferenceNo'] if params['partnerReferenceNo'] != '' else '',
        }
        additional_info = params.get('additionalInfo')
        if additional_info is not None:
            if isinstance(additional_info, dict):
                body['additionalInfo'] = {
                    'deviceId': additional_info.get('deviceId', ''),
                    'channel': additional_info.get('channel', '')
                }

        timeStamp = getTimestamp()
        signature = generateSignatureServiceSnapBI({
            'body': body,
            'method': 'POST',
            'url': '/snap-service/v1/account-inquiry-external',
            'accessToken': token,
            'timeStamp': timeStamp,
            'apiSecret': self.config['apiSecret']
        })
        res = self.httpClient.requestSnapBI({
            'method': 'POST',
            'apiKey': self.config['apiKey'],
            'accessToken': token,
            'url': f'{self.baseUrl}/snap-service/v1/account-inquiry-external',
            'data': body,
            'additionalHeader': {
                'X-SIGNATURE': signature,
                'X-TIMESTAMP': timeStamp,
                'X-PARTNER-ID': self.config['apiKey'],
                'X-IP-Address': self.configSnap['ipAddress'],
                'X-DEVICE-ID': 'bni-python/0.1.0',
                'X-EXTERNAL-ID': randomNumber(),
                'CHANNEL-ID': self.configSnap['channelId'],
                'X-LATITUDE': self.configSnap['latitude'],
                'X-LONGITUDE': self.configSnap['longitude']
            }
        })
        return responseSnapBI(params={'res': res})

    def transferInterBank(self, params={
        'partnerReferenceNo',
        'amount',
        'beneficiaryAccountName',
        'beneficiaryAccountNo',
        'beneficiaryAddress',
        'beneficiaryBankCode',
        'beneficiaryBankName',
        'beneficiaryEmail',
        'currency',
        'customerReference',
        'sourceAccountNo',
        'transactionDate',
        'feeType',
        'additionalInfo'
    }):

        token = self.getTokenSnapBI()
        body = {
            'partnerReferenceNo': params['partnerReferenceNo'],
            'amount': {
                'value': params['amount']['value'],
                'currency': params['amount']['currency']
            },
            'beneficiaryAccountName': params['beneficiaryAccountName'],
            'beneficiaryAccountNo': params['beneficiaryAccountNo'],
            'beneficiaryAddress': params['beneficiaryAddress'] if params['beneficiaryAddress'] != '' else '',
            'beneficiaryBankCode': params['beneficiaryBankCode'],
            'beneficiaryBankName': params['beneficiaryBankName'] if params['beneficiaryBankName'] != '' else '',
            'beneficiaryEmail': params['beneficiaryEmail'] if params['beneficiaryEmail'] != '' else '',
            'currency': params['currency'] if params['currency'] != '' else '',
            'customerReference': params['customerReference'],
            'feeType': params['feeType'] if params['feeType'] != '' else '',
            'sourceAccountNo': params['sourceAccountNo'],
            'transactionDate': timeStamp if params['transactionDate'] == '' else params['transactionDate'],
        }
        additional_info = params.get('additionalInfo')
        if additional_info is not None:
            if isinstance(additional_info, dict):
                body['additionalInfo'] = {
                    'deviceId': additional_info.get('deviceId', ''),
                    'channel': additional_info.get('channel', '')
                }

        timeStamp = getTimestamp()
        signature = generateSignatureServiceSnapBI({
            'body': body,
            'method': 'POST',
            'url': '/snap-service/v1/transfer-interbank',
            'accessToken': token,
            'timeStamp': timeStamp,
            'apiSecret': self.config['apiSecret']
        })
        res = self.httpClient.requestSnapBI({
            'method': 'POST',
            'apiKey': self.config['apiKey'],
            'accessToken': token,
            'url': f'{self.baseUrl}/snap-service/v1/transfer-interbank',
            'data': body,
            'additionalHeader': {
                'X-SIGNATURE': signature,
                'X-TIMESTAMP': timeStamp,
                'X-PARTNER-ID': self.config['apiKey'],
                'X-IP-Address': self.configSnap['ipAddress'],
                'X-DEVICE-ID': 'bni-python/0.1.0',
                'X-EXTERNAL-ID': randomNumber(),
                'CHANNEL-ID': self.configSnap['channelId'],
                'X-LATITUDE': self.configSnap['latitude'],
                'X-LONGITUDE': self.configSnap['longitude']
            }
        })
        return responseSnapBI(params={'res': res})
