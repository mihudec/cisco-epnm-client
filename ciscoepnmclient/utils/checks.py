from requests import Response


def check_terminate_uni(response: Response):
    result, message = (None, None)
    if response.status_code == 200:
        data = response.json()
        completion_status = None
        try:
            completion_status = data["com.response-message"]["com.data"]["saext.terminate-service-request"]["completion-status"]
            if completion_status.upper() == "FAILED":
                result = False
                message = "ERROR: {}".format(data["com.response-message"]["com.data"]["saext.terminate-service-request"]["error"])
            if completion_status.upper() == "SUCCESS":
                result = True
                message = "SUCCESS"
        except Exception as e:
            message = repr(e)
    else:
        result = None
    return (result, message)

def check_provision_uni(response: Response):
    result, message = (None, None)
    if response.status_code == 200:
        data = response.json()
        completion_status = None
        try:
            completion_status = data["com.response-message"]["com.data"]["saext.provision-service-request"]["completion-status"]
            if completion_status.upper() == "FAILED":
                result = False
                message = "ERROR: {}".format(data["com.response-message"]["com.data"]["saext.provision-service-request"]["error"])
            if completion_status.upper() == "SUCCESS":
                result = True
                message = "SUCCESS"
        except Exception as e:
            message = repr(e)
    else:
        result = None
    return (result, message)


def check_terminate_service(response: Response):
    result, message = (None, None)
    if response.status_code == 200:
        data = response.json()
        completion_status = None
        try:
            completion_status = data["com.response-message"]["com.data"]["saext.terminate-service-request"]["completion-status"]
            if completion_status.upper() == "FAILED":
                result = False
                message = "ERROR: {}".format(data["com.response-message"]["com.data"]["saext.terminate-service-request"]["error"])
            if completion_status.upper() == "SUCCESS":
                result = True
                message = "SUCCESS"
        except Exception as e:
            message = repr(e)
    else:
        result = None
    return (result, message)

def check_provision_service(response: Response):
    result, message = (None, None)
    if response.status_code == 200:
        data = response.json()
        completion_status = None
        try:
            completion_status = data["com.response-message"]["com.data"]["saext.provision-service-request"]["completion-status"]
            if completion_status.upper() == "FAILED":
                result = False
                message = "ERROR: {}".format(data["com.response-message"]["com.data"]["saext.provision-service-request"]["error"])
            if completion_status.upper() == "SUCCESS":
                result = True
                message = "SUCCESS"
        except Exception as e:
            message = repr(e)
    else:
        result = None
    return (result, message)