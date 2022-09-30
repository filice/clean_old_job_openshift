from os import environ
import requests
from datetime import datetime, timedelta


apihost = 'environ['KUBERNETES_PORT_443_TCP_ADDR']:['KUBERNETES_SERVICE_PORT_HTTPS']{endpoint}'

jobsurl = apihost.format(
endpoint = '/apis/batch/v1/namespaces/%s/jobs' % environ['NAMESPACE']
)

with open('/var/run/secrets/kubernetes.io/serviceaccount/token', 'r') as file:
    AUTH_TOKEN = file.read()

headers = {
'Authorization': 'Bearer %s' % AUTH_TOKEN
}

req_jobs = requests.get(jobsurl, headers=headers, verify=False)

jobstodelete = []

for item in req_jobs.json()['items']:
    if 'completionTime' in item['status']:
        elapsed_time = datetime.now() - datetime.strptime(item['status']['completionTime'], '%Y-%m-%dT%H:%M:%SZ')
        if elapsed_time > timedelta(hours=24):
            jobstodelete.append(item['metadata']['selfLink'])
			
for job in jobstodelete:
    delurl = apihost.format(
        endpoint = job
    )

req_del = requests.delete(delurl, headers=headers, verify=False)
