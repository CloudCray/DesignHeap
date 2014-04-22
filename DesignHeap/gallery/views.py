# Create your views here.

from django.shortcuts import render_to_response
from DesignHeap.settings import MEDIA_ROOT
from django.views.decorators.csrf import csrf_exempt, csrf_protect

import re
import base64
dataUrlPattern = re.compile('data:image/(png|jpeg);base64,(.*)$')
