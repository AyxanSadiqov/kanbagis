import time

from django.contrib import messages
from django.contrib.auth import logout
from django.utils.translation import ugettext as _

OTURUM_ZAMAN_ASIM_SURESI = 1800


class OturumZamanAsimiKontrol:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.user.is_authenticated:
            gecerli_zaman = int(time.time())

            try:
                request.session['last_activity']
            except:
                request.session['last_activity'] = gecerli_zaman

            if (gecerli_zaman - request.session['last_activity']) >= OTURUM_ZAMAN_ASIM_SURESI:
                logout(request)
                messages.add_message(request, messages.ERROR, _('Oturumunuz zaman aşımına uğradı!'))

            else:
                request.session['last_activity'] = gecerli_zaman

        response = self.get_response(request)
        return response
