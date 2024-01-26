import requests
import json
from datetime import datetime, timedelta
import random
import uuid

levels = [
  'debug',
  'info',
  'warn',
  'error'
  ]

messages = {
  'Action': [
    'Created',
    'Updated',
    'Deleted',
    'Viewed',
    'Logged in',
    'Logged out',
    'Submitted',
    'Approved',
    'Rejected',
    'Cancelled',
    'Assigned',
    'Unassigned',
    'Scheduled',
    'Rescheduled',
    'Completed',
    'Failed',
    'Reviewed',
    'Published',
    'Archived',
    'Restored',
    'Downloaded',
    'Uploaded',
    'Shared'
  ],
  'Resource': [
    'User',
    'Role',
    'Permission',
    'Product',
    'Order',
    'Invoice',
    'Payment',
    'Shipment',
    'Review',
    'Feedback',
    'Comment',
    'Category',
    'Tag',
    'Customer',
    'Vendor',
    'Task',
    'Project',
    'Event',
    'File',
    'Notification',
    'Message',
    'Article',
    'Survey'
  ],
  'Error': [
    'Invalid credentials',
    'Invalid request',
    'Invalid data',
    'Invalid operation',
    'Invalid state',
    'Invalid input',
    'Invalid format',
    'Invalid value',
    'Invalid type',
    'Invalid condition',
    'Invalid format',
    'Invalid value',
    'Invalid type',
    'Invalid condition',
    'Invalid format',
    'Database connection error',
    'File not found',
    'Permission denied',
    'Server timeout',
    'Network error',
    'External service failure',
    'Data corruption',
    'Security breach',
    'Authentication failure'
  ],
  'Constraint': [
    'Unique constraint violation',
    'Referential integrity violation',
    'NotNull constraint violation',
    'Length constraint violation',
    'Pattern constraint violation',
    'Range constraint violation'
  ],
  'Description': [
    'The user successfully completed the action.',
    'The system encountered an unexpected error during the operation.',
    'The requested resource was not found.',
    'The operation failed due to insufficient permissions.',
    'An error occurred while processing the request.',
    'The operation was cancelled by the user.',
    'The requested resource is currently unavailable.',
    'The data provided does not meet the required format.',
    'An unexpected server error occurred.',
    'The operation failed due to a constraint violation.',
    'The system experienced a timeout while processing the request.',
    'Authentication failed. Please check your credentials.',
    'The requested resource has been deleted or no longer exists.',
    'An error occurred while connecting to the database.',
    'The system encountered a security-related issue.',
    'The operation could not be completed due to a network error.',
    'The system encountered an issue with an external service.',
    'The operation failed due to data corruption.',
    'The user session has expired. Please log in again.'
  ]
}

resources = {
  'tier': ['client','server','database','filesystem'],
  'environment': ['development', 'staging', 'production'],
  'exposure': ['public', 'private'],
  'location': ['us-east-1', 'us-west-1', 'eu-west-1', 'ap-southeast-1', 'ap-northeast-1']
}

def generate_log():
  return {
    "level": random.choice(levels),
    "message": (random.choice(messages['Action']) + ' ' +
    random.choice(messages['Resource']) + ': ' +
    random.choice([random.choice(messages['Description']),
      random.choice(messages['Error']) + ': ' +
      str((list(set([random.choice(messages['Constraint'])
        for i in range(random.randint(1,len(messages['Constraint'])-1))]))))])),
    "resourceId": (random.choice(resources['tier']) + '-' +
      random.choice(resources['environment']) + '-' +
      random.choice(resources['exposure']) + '-' +
      random.choice(resources['location'])),
    "timestamp": (datetime.utcnow() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "traceId": str(uuid.uuid4()),
    "spanId": str(uuid.uuid4()),
    "commit": uuid.uuid4().hex,
    "metadata": {
      "parentResourceId": (random.choice(resources['tier']) + '-' +
        random.choice(resources['environment']) + '-' +
        random.choice(resources['exposure']) + '-' +
        random.choice(resources['location']))
    }
  }

def send_log(log_data, url):
  headers = {'Content-Type': 'application/json'}
  response = requests.post(url, data=json.dumps(log_data), headers=headers)
  return response.status_code

if __name__ == "__main__":
  target_url = 'http://localhost:3000'
  num_entries = 10000

  for _ in range(num_entries):
    log_record = generate_log()
    print(json.dumps(log_record))
    status_code = send_log(log_record, target_url)
    print(f"Status code: {status_code}")
