from .all_service import get_auth_refresh_id_via_username, set_taiga_user_data


def login(domain, username, password, tg_id):
    status_code, auth_token, refresh, taiga_id = get_auth_refresh_id_via_username(domain, username, password)
    if status_code == 200:
        print(auth_token)
        print("LEN", len(auth_token))
        set_taiga_user_data(tg_id=tg_id, domain=domain,auth_type="Bearer", refresh=refresh, auth_token=auth_token, taiga_id=taiga_id)
        return 200
    else: return 401