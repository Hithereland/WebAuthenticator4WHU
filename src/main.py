import AuthFuncs

user_info = {'userId': '123',
             'passwd': '123'}

def main():
    auth_url = AuthFuncs.get_auth_url()
    if auth_url == "Error":
        print("Connection failed, please check the physical connection.")
        return -1

    post_data = AuthFuncs.make_post_data(auth_url, user_info)
    try:
        statuscode, result = AuthFuncs.login_and_auth(post_data, auth_url)
        print("post_status_code =", statuscode)
        print("result =", result)
    except LookupError:
        print("Authentication failed")

    print("All is done")
    return 0

main()