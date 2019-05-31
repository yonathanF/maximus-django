import logging

import jwt
from django.conf import settings
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from jwt.exceptions import DecodeError, ExpiredSignature, InvalidTokenError

logger = logging.getLogger(__name__)


def decode_token(token):
    if len(token) == 0:
        raise KeyError("Token doesn't exist")
    secret = settings.SECRET_KEY
    decoded_payload = jwt.decode(token, secret, algorithms=['HS256'])
    return decoded_payload


def encode_token(user_id, expire_time):
    secret = settings.SECRET_KEY
    payload = {'user_id': user_id, 'exp': expire_time}
    return jwt.encode(payload, secret, algorithm='HS256').decode()


@method_decorator(csrf_exempt, name='dispatch')
class AuthJWT(View):
    def post(self, request):
        logger.info("Starting to authenticate a token.")
        try:
            # TODO ambassador might not use 'token'
            token = request.POST.get('token', '')
            user_id = decode_token(token)['user_id']
            response = JsonResponse({"Status": "Validated"}, status=200)
            response['x-maximus-user'] = user_id
            logger.info("Successfully authenticated token.")
            return response

        except ExpiredSignature:
            logger.warning("Expired token attempted to authenticate.")
            return JsonResponse({"Error": "Expired token. Please renew."},
                                status=403)
        except (DecodeError, InvalidTokenError):
            logger.warning("An invalid token attempted to authenticated.")
            return JsonResponse({"Error": "Could not validate token."},
                                status=403)
        except KeyError:
            logger.warning(
                "Tried to authenticate without a token or incorrect post body."
            )
            return JsonResponse({"Error": "Could not find token."}, status=403)
