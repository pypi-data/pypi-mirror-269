import json

from .HttpUtil import HttpUtil


class CoreATASApi:

    @staticmethod
    def init_result(uri, token, launch, executor, job_execution_id):
        headers = "{\"Content-Type\": \"application/json;charset=UTF-8\",\"auth-key\": \"" + token + "\"}"
        url = uri + "/automation/launch/init"
        body = "{\"launchName\":\"" + launch + "\", \"executor\": \"" + executor + "\", \"jobExecutionId\": \"" + job_execution_id + "\"}"
        method = "post"
        try:
            res = HttpUtil.http_request(url, method, None, None, json.loads(body), headers=eval(headers))
        except Exception:
            raise
        execution_id = json.loads(res)['data']['executionId']
        return execution_id

    @staticmethod
    def save_result(uri, token, data):
        url = uri + "/automation/launch/execute"
        # item = {"executionId": execution_id}
        # data.update(**item)
        screen_path = data['screen_path']
        attachment_path = data['attachment_path']
        if screen_path is None:
            screen = ('snapshot', (
                '', '',
                'image/png'))
        else:
            screen = ('snapshot', (
                screen_path[screen_path.rindex("/") + 1:], open(screen_path, 'rb'),
                'image/png'))
        if attachment_path is None:
            attachment = ('attachment', (
                '', '',
                'image/png'))
        else:
            attachment = ('attachment', (
                attachment_path[attachment_path.rindex("/") + 1:], open(attachment_path, 'rb'),
                'image/png'))
        files = [screen, attachment]
        try:
            res = HttpUtil.http_multipart_request(url, data, files, auth_key=token)
        except Exception:
            raise
        return res

    @staticmethod
    def run_complete(uri, token, execution_id, case_status):
        headers = "{\"Content-Type\": \"application/json;charset=UTF-8\",\"auth-key\": \"" + token + "\"}"
        url = uri + "/automation/launch/execution/complete"
        body = "{\"executionId\":" + str(execution_id) + ", \"caseStatus\": \"" + case_status + "\"}"
        method = "post"
        try:
            res = HttpUtil.http_request(url, method, None, None, json.loads(body), headers=eval(headers))
        except Exception:
            raise
        return res

    @staticmethod
    def get_run_cases(uri, token, id):
        headers = "{\"Content-Type\": \"application/json;charset=UTF-8\",\"auth-key\": \"" + token + "\"}"
        url = uri + "/automation/plan/cases/info"
        body = "{\"executionId\":\"" + id + "\"}"
        method = "post"
        try:
            res = HttpUtil.http_request(url, method, None, None, json.loads(body), headers=eval(headers))
        except Exception:
            raise
        return res
