# Python library to interact with cPanel API

## Install 

```
pip install cpanel-client
```

## Create a new cPanel account 

```
server = ServerAPI('WHM_USERNAME', 'WHM_PASSWORD', 'https://your-whm-url.com', 2087)  
          
# create account 
result = server.create_account('USER_EMAIL_ADDRESS', 'USER_DOMAIN', 'package_name')
print(result)
success = result['success']
self.assertEqual(success, 1)
if success == 1:
    print('New cPanel Account created')

# Suspend account
suspend_result = server.suspend_account(c_username)

# Terminate account
destroy_result = server.terminate_account(result['username'])

```
