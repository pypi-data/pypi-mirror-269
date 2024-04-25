from bnipython.lib.net.httpClient import HttpClient
from bnipython.lib.util.utils import generateSignature, getTimestampBNIMove
from bnipython.lib.util.response import responseBNIMove

class BNIMove():
    def __init__(self, client):
        self.client = client.config
        self.baseUrl = client.getBaseUrl()
        self.config = client.getConfig()
        self.token = client.getToken()
        self.httpClient = HttpClient()

    def prescreening(self, params={
        'kodeMitra',
        'npp',
        'namaLengkapKtp',
        'noKtp',
        'noHandphone',
        'alamatUsaha',
        'provinsiUsaha',
        'kotaUsaha',
        'kecamatanUsaha',
        'kelurahanUsaha',
        'kodePosUsaha',
        'sektorEkonomi',
        'totalPenjualan',
        'jangkaWaktu',
        'jenisPinjaman',
        'maximumKredit',
        'jenisKelamin',
        'tanggalLahir',
        'subSektorEkonomi',
        'deskripsi',
        'email'
    }):
        timeStamp = getTimestampBNIMove()
        payload = {**params, **{ 'timestamp': timeStamp }}
        signature = generateSignature(
            {'body': payload, 'apiSecret': self.client['apiSecret']})
        res = self.httpClient.requestV2({
            'method': 'POST',
            'apiKey': self.client['apiKey'],
            'accessToken': self.token,
            'url': f'{self.baseUrl}',
            'path': '/digiloan/prescreening',
            'signature': signature.split('.')[2],
            'timestamp': timeStamp,
            'data': params
        })
        return responseBNIMove(params={'res': res})
    
    def saveImage(self, params={
        'Id',
        'deskripsi',
        'jenisDokumen',
        'namaFile',
        'extensionFile',
        'dataBase64',
    }):
        timeStamp = getTimestampBNIMove()
        payload = {**params, **{ 'timestamp': timeStamp }}
        signature = generateSignature(
            {'body': payload, 'apiSecret': self.client['apiSecret']})
        res = self.httpClient.requestV2({
            'method': 'POST',
            'apiKey': self.client['apiKey'],
            'accessToken': self.token,
            'url': f'{self.baseUrl}',
            'path': '/digiloan/saveimage',
            'signature': signature.split('.')[2],
            'timestamp': timeStamp,
            'data': payload
        })
        return responseBNIMove(params={'res': res})