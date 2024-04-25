from bnipython.lib.util import constants
from bnipython.lib.bniClient import BNIClient
from bnipython.lib.api.snapBI import SnapBI
import unittest


class TestSnapBI(unittest.TestCase):

    client = BNIClient({
        'env': 'dev',
        'appName': constants.APP_NAME_TEST,
        'clientId': constants.CLIENT_ID_ENCRYPT_SNAP_BI,
        'clientSecret': constants.CLIENT_SECRET_ENCRYPT_SNAP_BI,
        'apiKey': constants.API_KEY_ENCRYPT_SNAP_BI,
        'apiSecret': constants.API_SECRET_ENCRYPT_SNAP_BI,
    })

    def testGetBalance(self):
        print('\n==============================================')
        snap = SnapBI(
            self.client,  {'privateKeyPath': './private.key', 'channelId': '95221'})
        res = snap.balanceInquiry({
            'partnerReferenceNo': '202010290000000000002',
            'accountNo': '0115476117'
        })
        data = res['responseCode']
        self.assertEqual(data, '2001100')
        print('should return responseCode 2001100')

    def testFailedBalanceInquiry(self):
        print('\n==============================================')
        snap = SnapBI(
            self.client,  {'privateKeyPath': './private.key', 'channelId': '95221'})
        res = snap.balanceInquiry({
            'partnerReferenceNo': '202010290000000000002',
            'accountNo': ''
        })
        data = res['responseCode']
        self.assertEqual(data, '4001101')
        print('should return responseCode 4001101')

    def testFailedBalanceInquiryInactiveAccount(self):
        print('\n==============================================')
        snap = SnapBI(
            self.client,  {'privateKeyPath': './private.key', 'channelId': '95221'})
        res = snap.balanceInquiry({
            'partnerReferenceNo': '202010290000000000028',
            'accountNo': '0115476286'
        })
        data = res['responseCode']
        self.assertEqual(data, '4001101')
        print('should return responseCode 4001101')

    def testFailedBalanceInquiryFailedAccount(self):
        print('\n==============================================')
        snap = SnapBI(
            self.client,  {'privateKeyPath': './private.key', 'channelId': '95221'})
        res = snap.balanceInquiry({
            'partnerReferenceNo': '20240226170014912',
            'accountNo': '0317471619'
        })
        data = res['responseCode']
        self.assertEqual(data, '4001101')
        print('should return responseCode 4001101')

    def testGetInternalAccountInquiry(self):
        print('\n==============================================')
        snap = SnapBI(
            self.client,  {'privateKeyPath': './private.key', 'channelId': 'API'})
        res = snap.internalAccountInquiry({
            'partnerReferenceNo': '2023062601000000000509',
            'beneficiaryAccountNo': '317125693'
        })
        data = res['responseCode']
        self.assertEqual(data, '2001500')
        print('should return responseCode 2001500')

    def testFailedInternalAccountInquiry(self):
        print('\n==============================================')
        snap = SnapBI(
            self.client,  {'privateKeyPath': './private.key', 'channelId': 'API'})
        res = snap.internalAccountInquiry({
            'partnerReferenceNo': '2023062601000000000509',
            'beneficiaryAccountNo': ''
        })
        data = res['responseCode']
        self.assertEqual(data, '4001501')
        print('should return responseCode 4001501')

    def testFailedInternalAccountInquiryInactive(self):
        print('\n==============================================')
        snap = SnapBI(
            self.client,  {'privateKeyPath': './private.key', 'channelId': 'API'})
        res = snap.internalAccountInquiry({
            'partnerReferenceNo': '20220510172056712211',
            'beneficiaryAccountNo': '1000287621'
        })
        data = res['responseCode']
        self.assertEqual(data, '4001501')
        print('should return responseCode 4001501')

    def testGetTransactionStatusInquiry(self):
        print('\n==============================================')
        snap = SnapBI(
            self.client,  {'privateKeyPath': './private.key', 'channelId': 'API'})
        res = snap.transactionStatusInquiry({
            'originalPartnerReferenceNo': '202310271020300006',
            'originalReferenceNo': '',
            'originalExternalId': '',
            'serviceCode': '22',
            'transactionDate': '',
            'amount': {
                'value': '110000010',
                'currency': 'IDR'
            },
            'additionalInfo': {
                'deviceId': '09864ADCASA',
                'channel': 'API'
            }
        })
        data = res['responseCode']
        self.assertEqual(data, '2003600')
        print('should return responseCode 2003600')

    def testFailedTransactionStatusInquiry(self):
        print('\n==============================================')
        snap = SnapBI(
            self.client,  {'privateKeyPath': './private.key', 'channelId': 'API'})
        res = snap.transactionStatusInquiry({
            'originalPartnerReferenceNo': '',
            'originalReferenceNo': '',
            'originalExternalId': '',
            'serviceCode': '22',
            'transactionDate': '',
            'amount': {
                'value': '110000010',
                'currency': 'IDR'
            },
            'additionalInfo': {
                'deviceId': '09864ADCASA',
                'channel': 'API'
            }
        })
        data = res['responseCode']
        self.assertEqual(data, '4003601')
        print('should return responseCode 4003601')

    def testGetTransferIntraBank(self):
        print('\n==============================================')
        snap = SnapBI(
            self.client,  {'privateKeyPath': './private.key', 'channelId': 'API'})
        res = snap.transferIntraBank({
            'partnerReferenceNo': '20220426170737356898',
            'amount': {
                'value': '55000.00',
                'currency': 'IDR'
            },
            'beneficiaryAccountNo': '0115476151',
            'beneficiaryEmail': "'",
            'customerReference': '20220426170737356898',
            'currency': 'IDR',
            'remark': '20220426170737356898',
            'feeType': 'OUR',
            'sourceAccountNo': '0115476117',
            'transactionDate': '2022-04-26T17:07:36+07:00',
            'additionalInfo': {
                'deviceId': "",
                'channel': ''
            }
        })
        data = res['responseCode']
        self.assertEqual(data, '2001700')
        print('should return responseCode 2001700')

    def testFailedTransferIntraBank(self):
        print('\n==============================================')
        snap = SnapBI(
            self.client,  {'privateKeyPath': './private.key', 'channelId': 'API'})
        res = snap.transferIntraBank({
            'partnerReferenceNo': '20220527110338724198',
            'amount': {
                'value': '1000000.00',
                'currency': 'IDR'
            },
            'beneficiaryAccountNo': '0115476117',
            'beneficiaryEmail': "'",
            'customerReference': '20220527110338724198',
            'currency': 'IDR',
            'remark': '20220527110338724198',
            'feeType': 'OUR',
            'sourceAccountNo': '0114754574',
            'transactionDate': '2022-05-27T11:03:37+07:00',
        })
        data = res['responseCode']
        self.assertEqual(data, '4031714')
        print('should return responseCode 4031714')

    def testFailedTransferIntraBankDuplicateCustomerReference(self):
        print('\n==============================================')
        snap = SnapBI(
            self.client,  {'privateKeyPath': './private.key', 'channelId': 'API'})
        res = snap.transferIntraBank({
            'partnerReferenceNo': '20220527110338724198',
            'amount': {
                'value': '50000.00',
                'currency': 'IDR'
            },
            'beneficiaryAccountNo': '0115476117',
            'beneficiaryEmail': "'",
            'customerReference': '20220527110338724198',
            'currency': 'IDR',
            'remark': '20220527110338724198',
            'feeType': 'OUR',
            'sourceAccountNo': '0115476151',
            'transactionDate': '2022-05-27T11:03:37+07:00',
        })
        data = res['responseCode']
        self.assertEqual(data, '4031714')
        print('should return responseCode 4031714')

    def testFailedTransferIntraBankBeneficaryAccountNo(self):
        print('\n==============================================')
        snap = SnapBI(
            self.client,  {'privateKeyPath': './private.key', 'channelId': 'API'})
        res = snap.transferIntraBank({
            'partnerReferenceNo': '20220426170737356898',
            'amount': {
                'value': '55000.00',
                'currency': 'IDR'
            },
            'beneficiaryAccountNo': '',
            'beneficiaryEmail': "'",
            'customerReference': '20220426170737356898',
            'currency': 'IDR',
            'remark': '20220426170737356898',
            'feeType': 'OUR',
            'sourceAccountNo': '0115476117',
            'transactionDate': '2022-04-26T17:07:36+07:00',
            'additionalInfo': {
                'deviceId': "",
                'channel': ''
            }
        })
        data = res['responseCode']
        self.assertEqual(data, '2001700')
        print('should return responseCode 2001700')

    def testGetTransferRTGS(self):
        print('\n==============================================')
        snap = SnapBI(
            self.client,  {'privateKeyPath': './private.key', 'channelId': '95221'})
        res = snap.transferRTGS({
            'partnerReferenceNo': '20220513095840015788857',
            'amount': {
                'value': '100000001.00',
                'currency': 'IDR'
            },
            'beneficiaryAccountName': 'PTZomatoMediaIndonesia',
            'beneficiaryAccountNo': '3333333333',
            'beneficiaryAccountAddress': 'JlGatotSubrotoNoKav18RW1KuninganBarKecMampangPrptKotaJakartaSelatanDaerahKhususIbukotaJakarta12710',
            'beneficiaryBankCode': 'CENAIDJA',
            'beneficiaryBankName': 'PTBANKCENTRALASIATbk',
            'beneficiaryCustomerResidence': '1',
            'beneficiaryCustomerType': '2',
            'beneficiaryEmail': '',
            'currency': 'IDR',
            'customerReference': '20220513095840015788857',
            'feeType': 'OUR',
            'kodePos': '-',
            'recieverPhone': '-',
            'remark': 'DANA20220513095840015788857PTZomatoMediaIndonesia',
            'senderCustomerResidence': '-',
            'senderCustomerType': '-',
            'senderPhone': '',
            'sourceAccountNo': '0115476151',
            'transactionDate': '2020-06-17T01:03:04+07:00',
            'additionalInfo': {
                'deviceId': '',
                'channel': ''
            }
        })
        data = res['responseCode']
        self.assertEqual(data, '2002200')
        print('should return responseCode 2002200')

    def testFailedTransferRTGS(self):
        print('\n==============================================')
        snap = SnapBI(
            self.client,  {'privateKeyPath': './private.key', 'channelId': '95221'})
        res = snap.transferRTGS({
            'partnerReferenceNo': '20220513095840015788857',
            'amount': {
                'value': '100000001.00',
                'currency': 'IDR'
            },
            'beneficiaryAccountName': 'PTZomatoMediaIndonesia',
            'beneficiaryAccountNo': '',
            'beneficiaryAccountAddress': 'JlGatotSubrotoNoKav18RW1KuninganBarKecMampangPrptKotaJakartaSelatanDaerahKhususIbukotaJakarta12710',
            'beneficiaryBankCode': 'CENAIDJA',
            'beneficiaryBankName': 'PTBANKCENTRALASIATbk',
            'beneficiaryCustomerResidence': '1',
            'beneficiaryCustomerType': '2',
            'beneficiaryEmail': '',
            'currency': 'IDR',
            'customerReference': '20220513095840015788857',
            'feeType': 'OUR',
            'kodePos': '-',
            'recieverPhone': '-',
            'remark': 'DANA20220513095840015788857PTZomatoMediaIndonesia',
            'senderCustomerResidence': '-',
            'senderCustomerType': '-',
            'senderPhone': '',
            'sourceAccountNo': '0115476151',
            'transactionDate': '2020-06-17T01:03:04+07:00',
            'additionalInfo': {
                'deviceId': '',
                'channel': ''
            }
        })
        data = res['responseCode']
        self.assertEqual(data, '4002201')
        print('should return responseCode 4002201')

    def testFailedTransferRTGSDuplicate(self):
        print('\n==============================================')
        snap = SnapBI(
            self.client,  {'privateKeyPath': './private.key', 'channelId': '95221'})
        res = snap.transferRTGS({
            "partnerReferenceNo": "202310271020300099",
            "amount": {
                "value": "110000010",
                "currency": "IDR" 
            },
            "beneficiaryAccountName": "PTZomatoMediaIndonesia",
            "beneficiaryAccountNo": "33333333",
            "beneficiaryAccountAddress": "JlGatotSubrotoNoKav18RW1KuninganBarKecMampangPrptKotaJakartaSelatanDaerahKhususIbukotaJakarta12710",
            "beneficiaryBankCode": "CENAIDJA",
            "beneficiaryBankName": "PTBANKCENTRALASIATbk",
            "beneficiaryCustomerResidence": "1",
            "beneficiaryCustomerType": "2",
            "beneficiaryEmail": "randra@gmail.com",
            "currency": "IDR",
            "customerReference": "202310271020300005",
            "feeType": "OUR",
            "kodePos": "12550",
            "recieverPhone": "087781726381",
            "remark": "RTGS20220627215840015700021PTXYZIndonesia",
            "senderCustomerResidence": "1",
            "senderCustomerType": "1",
            "senderPhone": "087781726382",
            "sourceAccountNo": "1000164314",
            "transactionDate": "2020-07-01T14:03:04+07:00",
            "additionalInfo": {
                "deviceId": "20013fea6bcc820c",
                "channel": "mobile"
            }
        })
        data = res['responseCode']
        self.assertEqual(data, '4002201')
        print('should return responseCode 4002201')

    def testGetTransferSKNBI(self):
        print('\n==============================================')
        snap = SnapBI(
            self.client,  {'privateKeyPath': './private.key', 'channelId': '95221'})
        res = snap.transferSKNBI({
            'partnerReferenceNo': '20220523150428586179325',
            'amount': {
                'value': '10000001.00',
                'currency': 'IDR'
            },
            'beneficiaryAccountName': 'PTZomatoMediaIndonesia',
            'beneficiaryAccountNo': '0115476117',
            'beneficiaryAddress': 'JlGatotSubrotoNoKav18RW1KuninganBarKecMampangPrptKotaJakartaSelatanDaerahKhususIbukotaJakarta12710',
            'beneficiaryBankCode': 'CENAIDJAXXX',
            'beneficiaryBankName': 'PTBANKCENTRALASIATbk',
            'beneficiaryCustomerResidence': '1',
            'beneficiaryCustomerType': '2',
            'beneficiaryEmail': '',
            'currency': 'IDR',
            'customerReference': '20220523150428586179325',
            'feeType': 'OUR',
            'kodePos': '',
            'recieverPhone': '',
            'remark': 'DANA20220523150428586179325PTZomatoMediaIndonesia',
            'senderCustomerResidence': '',
            'senderCustomerType': '',
            'senderPhone': '',
            'sourceAccountNo': '0115476151',
            'transactionDate': '2020-06-17T01:03:04+07:00',
            'additionalInfo': {
                'deviceId': '',
                'channel': ''
            }
        })
        data = res['responseCode']
        self.assertEqual(data, '2002300')
        print('should return responseCode 2002300')

    def testFailedTransferSKNBI(self):
        print('\n==============================================')
        snap = SnapBI(
            self.client,  {'privateKeyPath': './private.key', 'channelId': '95221'})
        res = snap.transferSKNBI({
            'partnerReferenceNo': '20220523150428586179325',
            'amount': {
                'value': '10000001.00',
                'currency': 'IDR'
            },
            'beneficiaryAccountName': 'PTZomatoMediaIndonesia',
            'beneficiaryAccountNo': '',
            'beneficiaryAddress': 'JlGatotSubrotoNoKav18RW1KuninganBarKecMampangPrptKotaJakartaSelatanDaerahKhususIbukotaJakarta12710',
            'beneficiaryBankCode': 'CENAIDJAXXX',
            'beneficiaryBankName': 'PTBANKCENTRALASIATbk',
            'beneficiaryCustomerResidence': '1',
            'beneficiaryCustomerType': '2',
            'beneficiaryEmail': '',
            'currency': 'IDR',
            'customerReference': '20220523150428586179325',
            'feeType': 'OUR',
            'kodePos': '',
            'recieverPhone': '',
            'remark': 'DANA20220523150428586179325PTZomatoMediaIndonesia',
            'senderCustomerResidence': '',
            'senderCustomerType': '',
            'senderPhone': '',
            'sourceAccountNo': '0115476151',
            'transactionDate': '2020-06-17T01:03:04+07:00',
            'additionalInfo': {
                'deviceId': '',
                'channel': ''
            }
        })
        data = res['responseCode']
        self.assertEqual(data, '4002301')
        print('should return responseCode 4002301')

    def testFailedTransferSKNBIDuplicate(self):
        print('\n==============================================')
        snap = SnapBI(
            self.client,  {'privateKeyPath': './private.key', 'channelId': '95221'})
        res = snap.transferSKNBI({
            "partnerReferenceNo": "202310303845300003",
            "amount": {
                "value": "1000000000",
                "currency": "IDR"
            },
            "beneficiaryAccountName": "SAN",
            "beneficiaryAccountNo": "33333333333",
            "beneficiaryAddress": "JakartaBarat",
            "beneficiaryBankCode": "0140397",
            "beneficiaryBankName": "PT.BANKCENTRALASIATbk.",
            "beneficiaryCustomerResidence": "1",
            "beneficiaryCustomerType": "1",
            "beneficiaryEmail": "try@gmail.co",
            "currency": "IDR",
            "customerReference": "202310303845300013",
            "feeType": "OUR",
            "kodePos": "12550",
            "recieverPhone": "098765",
            "remark": "AlreadyOneYear",
            "senderCustomerResidence": "1",
            "senderCustomerType": "1",
            "senderPhone": "098765",
            "sourceAccountNo": "0115476117",
            "transactionDate": "2023-10-28T16:43:06+07:00",
            "additionalInfo": {
                "deviceId": "123456",
                "channel": "mobilephone"
            }
        })
        data = res['responseCode']
        self.assertEqual(data, '2002300')
        print('should return responseCode 2002300')

    def testGetExternalAccountInquiry(self):
        print('\n==============================================')
        snap = SnapBI(
            self.client,  {'privateKeyPath': './private.key', 'channelId': '95221'})
        res = snap.externalAccountInquiry({
            'beneficiaryBankCode': 'CENAIDJAXXX',
            'partnerReferenceNo': '20240226163135663',
            'beneficiaryAccountNo': '123456789',
            'additionalInfo': {
                'deviceId': '09864ADCASA',
                'channel': 'API'
            }
        })
        data = res['responseCode']
        self.assertEqual(data, '2001600')
        print('should return responseCode 2001600')

    def testFailedExternalAccountInquiry(self):
        print('\n==============================================')
        snap = SnapBI(
            self.client,  {'privateKeyPath': './private.key', 'channelId': '95221'})
        res = snap.externalAccountInquiry({
            'beneficiaryBankCode': 'CENAIDJAXXX',
            'partnerReferenceNo': '20240226163135663',
            'beneficiaryAccountNo': '',
            'additionalInfo': {
                'deviceId': '09864ADCASA',
                'channel': 'API'
            }
        })
        data = res['responseCode']
        self.assertEqual(data, '4001601')
        print('should return responseCode 4001601')

    def testGetTransferInterBank(self):
        print('\n==============================================')
        snap = SnapBI(
            self.client,  {'privateKeyPath': './private.key', 'channelId': '95221'})
        res = snap.transferInterBank({
            'partnerReferenceNo': '20240226163731861',
            'amount': {
                'value': '20000',
                'currency': 'IDR'
            },
            'beneficiaryAccountName': 'SRI ANGGRAINI',
            'beneficiaryAccountNo': '0000000986',
            'beneficiaryAddress': 'Palembang',
            'beneficiaryBankCode': '014',
            'beneficiaryBankName': 'Bank BCA',
            'beneficiaryEmail': 'customertes@outlook.com',
            'currency': 'IDR',
            'customerReference': '20231219085',
            'sourceAccountNo': '1000161562',
            'transactionDate': '2024-01-04T08:37:08+07:00',
            'feeType': 'OUR',
            'additionalInfo': {
                'deviceId': '09864ADCASA',
                'channel': 'API'
            },
        })
        data = res['responseCode']
        self.assertEqual(data, '2001800')
        print('should return responseCode 2001800')

    def testFailedTransferInterBank(self):
        print('\n==============================================')
        snap = SnapBI(
            self.client,  {'privateKeyPath': './private.key', 'channelId': '95221'})
        res = snap.transferInterBank({
            'partnerReferenceNo': '20240226163731861',
            'amount': {
                'value': '20000',
                'currency': 'IDR'
            },
            'beneficiaryAccountName': 'SRI ANGGRAINI',
            'beneficiaryAccountNo': '',
            'beneficiaryAddress': 'Palembang',
            'beneficiaryBankCode': '014',
            'beneficiaryBankName': 'Bank BCA',
            'beneficiaryEmail': 'customertes@outlook.com',
            'currency': 'IDR',
            'customerReference': '20231219085',
            'sourceAccountNo': '1000161562',
            'transactionDate': '2024-01-04T08:37:08+07:00',
            'feeType': 'OUR',
            'additionalInfo': {
                'deviceId': '09864ADCASA',
                'channel': 'API'
            },
        })
        data = res['responseCode']
        self.assertEqual(data, '2001800')
        print('should return responseCode 2001800')

    def testFailedTransferInterBankInsuficientFund(self):
        print('\n==============================================')
        snap = SnapBI(
            self.client,  {'privateKeyPath': './private.key', 'channelId': '95221'})
        res = snap.transferInterBank({
            'partnerReferenceNo': '20240226163731861',
            'amount': {
                'value': '500000',
                'currency': 'IDR'
            },
            'beneficiaryAccountName': 'SRI ANGGRAINI',
            'beneficiaryAccountNo': '0000000986',
            'beneficiaryAddress': 'Palembang',
            'beneficiaryBankCode': '014',
            'beneficiaryBankName': 'Bank BCA',
            'beneficiaryEmail': 'customertes@outlook.com',
            'currency': 'IDR',
            'customerReference': '20231219085',
            'sourceAccountNo': '0317709144',
            'transactionDate': '2024-01-04T08:37:08+07:00',
            'feeType': 'OUR',
            'additionalInfo': {
                'deviceId': '09864ADCASA',
                'channel': 'API'
            },
        })
        data = res['responseCode']
        self.assertEqual(data, '4031814')
        print('should return responseCode 4031814')

    def testFailedTransferInterBankDuplicate(self):
        print('\n==============================================')
        snap = SnapBI(
            self.client,  {'privateKeyPath': './private.key', 'channelId': '95221'})
        res = snap.transferInterBank({
            "partnerReferenceNo": "20231219083708099",
            "amount": {
                "value": "500000",
                "currency": "IDR"
            },
            "beneficiaryAccountName": "SRI ANGGRAINI",
            "beneficiaryAccountNo": "0000000986",
            "beneficiaryAddress": "Palembang",
            "beneficiaryBankCode": "014",
            "beneficiaryBankName": "Bank BCA",
            "beneficiaryEmail": "customertes@outlook.com",
            "currency": "IDR",
            "customerReference":"20231220105908099",
            "feeType": "OUR",
            "remark": "",
            "sourceAccountNo": "1000161562",
            "transactionDate": "2023-12-20T10:59:08+07:00",
            "additionalInfo": {
                "deviceId": "09864ADCASA",
                "channel": "API"
            }
        })
        data = res['responseCode']
        self.assertEqual(data, '4031814')
        print('should return responseCode 4031814')

    # ###################### CASES NEGATIVE #####################

    # def testGetBalanceNegative(self):
    #     print('\n==============================================')
    #     snap = SnapBI(
    #         self.client,  {'privateKeyPath': './private.key', 'channelId': '95221'})
    #     res = snap.balanceInquiry({
    #         'partnerReferenceNo': '2020102900000000000FF',
    #         'accountNo': '0115476117'
    #     })
    #     data = res['responseCode']
    #     self.assertEqual(data, '2001100')
    #     print('should return responseCode 2001100')

    # def testGetInternalAccountInquiryNegative(self):
    #     print('\n==============================================')
    #     snap = SnapBI(
    #         self.client,  {'privateKeyPath': './private.key', 'channelId': '95221'})
    #     res = snap.internalAccountInquiry({
    #         'partnerReferenceNo': '2020102900000000000FF',
    #         'beneficiaryAccountNo': '0115476151'
    #     })
    #     data = res['responseCode']
    #     self.assertEqual(data, '2001500')
    #     print('should return responseCode 2001500')

    # def testGetTransactionStatusInquiryNegative(self):
    #     print('\n==============================================')
    #     snap = SnapBI(
    #         self.client,  {'privateKeyPath': './private.key', 'channelId': '95221'})
    #     res = snap.transactionStatusInquiry({
    #         'originalPartnerReferenceNo': '2022019110200001FF',
    #         'originalReferenceNo': '220531103343739748',
    #         'originalExternalId': '20220531103340',
    #         'serviceCode': '17',
    #         'transactionDate': '2022-05-31',
    #         'amount': {
    #             'value': '15000.00',
    #             'currency': 'IDR'
    #         },
    #         'additionalInfo': {
    #             'deviceId': '123456',
    #             'channel': 'mobilephone'
    #         }
    #     })
    #     data = res['responseCode']
    #     self.assertEqual(data, '2003600')
    #     print('should return responseCode 2003600')

    # def testGetTransferIntraBankNegative(self):
    #     print('\n==============================================')
    #     snap = SnapBI(
    #         self.client,  {'privateKeyPath': './private.key', 'channelId': '95221'})
    #     res = snap.transferIntraBank({
    #         'partnerReferenceNo': '207113OO008426FF',
    #         'amount': {
    #             'value': '500000.00',
    #             'currency': 'IDR'
    #         },
    #         'beneficiaryAccountNo': '1000161562',
    #         'beneficiaryEmail': '',
    #         'currency': 'IDR',
    #         'customerReference': '207113OO00842662',
    #         'feeType': 'OUR',
    #         'remark': 'DANA20220426170737356898YuliantoSariputra',
    #         'sourceAccountNo': '1000164314',
    #         'transactionDate': '2022-09-05T10:29:57+07:00',
    #         'additionalInfo': {
    #             'deviceId': '123456',
    #             'channel': 'mobilephone'
    #         }
    #     })
    #     data = res['responseCode']
    #     self.assertEqual(data, '2001700')
    #     print('should return responseCode 2001700')

    # def testGetTransferRTGSNegative(self):
    #     print('\n==============================================')
    #     snap = SnapBI(
    #         self.client,  {'privateKeyPath': './private.key', 'channelId': '95221'})
    #     res = snap.transferRTGS({
    #         'partnerReferenceNo': '202205130958400157888FF',
    #         'amount': {
    #             'value': '100000001.00',
    #             'currency': 'IDR'
    #         },
    #         'beneficiaryAccountName': 'PTZomatoMediaIndonesia',
    #         'beneficiaryAccountNo': '3333333333',
    #         'beneficiaryAccountAddress': 'JlGatotSubrotoNoKav18RW1KuninganBarKecMampangPrptKotaJakartaSelatanDaerahKhususIbukotaJakarta12710',
    #         'beneficiaryBankCode': 'CENAIDJA',
    #         'beneficiaryBankName': 'PTBANKCENTRALASIATbk',
    #         'beneficiaryCustomerResidence': '1',
    #         'beneficiaryCustomerType': '2',
    #         'beneficiaryEmail': '',
    #         'currency': 'IDR',
    #         'customerReference': '20220513095840015788857',
    #         'feeType': 'OUR',
    #         'kodePos': '-',
    #         'recieverPhone': '-',
    #         'remark': 'DANA20220513095840015788857PTZomatoMediaIndonesia',
    #         'senderCustomerResidence': '-',
    #         'senderCustomerType': '-',
    #         'senderPhone': '',
    #         'sourceAccountNo': '0115476151',
    #         'transactionDate': '2020-06-17T01:03:04+07:00',
    #         'additionalInfo': {
    #             'deviceId': '',
    #             'channel': ''
    #         }
    #     })
    #     data = res['responseCode']
    #     self.assertEqual(data, '2002200')
    #     print('should return responseCode 2002200')

    # def testGetTransferSKNBINegative(self):
    #     print('\n==============================================')
    #     snap = SnapBI(
    #         self.client,  {'privateKeyPath': './private.key', 'channelId': '95221'})
    #     res = snap.transferSKNBI({
    #         'partnerReferenceNo': '202205231504285861793FF',
    #         'amount': {
    #             'value': '10000001.00',
    #             'currency': 'IDR'
    #         },
    #         'beneficiaryAccountName': 'PTZomatoMediaIndonesia',
    #         'beneficiaryAccountNo': '0115476117',
    #         'beneficiaryAddress': 'JlGatotSubrotoNoKav18RW1KuninganBarKecMampangPrptKotaJakartaSelatanDaerahKhususIbukotaJakarta12710',
    #         'beneficiaryBankCode': 'CENAIDJAXXX',
    #         'beneficiaryBankName': 'PTBANKCENTRALASIATbk',
    #         'beneficiaryCustomerResidence': '1',
    #         'beneficiaryCustomerType': '2',
    #         'beneficiaryEmail': '',
    #         'currency': 'IDR',
    #         'customerReference': '20220523150428586179325',
    #         'feeType': 'OUR',
    #         'kodePos': '',
    #         'recieverPhone': '',
    #         'remark': 'DANA20220523150428586179325PTZomatoMediaIndonesia',
    #         'senderCustomerResidence': '',
    #         'senderCustomerType': '',
    #         'senderPhone': '',
    #         'sourceAccountNo': '0115476151',
    #         'transactionDate': '2020-06-17T01:03:04+07:00',
    #         'additionalInfo': {
    #             'deviceId': '',
    #             'channel': ''
    #         }
    #     })
    #     data = res['responseCode']
    #     self.assertEqual(data, '2002300')
    #     print('should return responseCode 2002300')

    # def testGetExternalAccountInquiryNegative(self):
    #     print('\n==============================================')
    #     snap = SnapBI(
    #         self.client,  {'privateKeyPath': './private.key', 'channelId': '95221'})
    #     res = snap.externalAccountInquiry({
    #         'beneficiaryBankCode': '002',
    #         'beneficiaryAccountNo': '888801000157508',
    #         'partnerReferenceNo': '20201029000000000000FF',
    #         'additionalInfo': {
    #             'deviceId': '123456',
    #             'channel': 'mobilephone'
    #         }
    #     })
    #     data = res['responseCode']
    #     self.assertEqual(data, '2001600')
    #     print('should return responseCode 2001600')

    # def testGetTransferInterBankNegative(self):
    #     print('\n==============================================')
    #     snap = SnapBI(
    #         self.client,  {'privateKeyPath': './private.key', 'channelId': '95221'})
    #     res = snap.transferInterBank({
    #         'partnerReferenceNo': '20220902540000000000FF',
    #         'amount': {
    #             'value': '55000',
    #             'currency': 'IDR'
    #         },
    #         'beneficiaryAccountName': 'BONIFASIUSPRIOKO',
    #         'beneficiaryAccountNo': '3333333333',
    #         'beneficiaryAddress': 'Palembang',
    #         'beneficiaryBankCode': '014',
    #         'beneficiaryBankName': 'BCA',
    #         'beneficiaryEmail': 'yories.yolanda@work.bri.co.id',
    #         'currency': 'IDR',
    #         'customerReference': '10052025',
    #         'sourceAccountNo': '0115476151',
    #         'transactionDate': '2022-06-14T12:08:56+07:00',
    #         'feeType': 'OUR',
    #         'additionalInfo': {
    #             'deviceId': '12345679237',
    #             'channel': 'mobilephone'
    #         }
    #     })
    #     data = res['responseCode']
    #     self.assertEqual(data, '2001800')
    #     print('should return responseCode 2001800')


if __name__ == '__main__':
    unittest.main()
