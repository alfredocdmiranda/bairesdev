def get_client_ip_addr(request):
    # Get this solution from https://stackoverflow.com/questions/4581789/how-do-i-get-user-ip-address-in-django

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip_addr = x_forwarded_for.split(',')[0]
    else:
        ip_addr = request.META.get('REMOTE_ADDR')

    return ip_addr