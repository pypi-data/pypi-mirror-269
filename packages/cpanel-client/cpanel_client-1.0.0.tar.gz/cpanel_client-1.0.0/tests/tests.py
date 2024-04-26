import unittest

from cpanel.cpanel import ServerAPI


class CPanelTest(unittest.TestCase):
    
    def test_create_suspend_terminate_cpanel_account(self):
        
        server = ServerAPI('USERNAME', 'PASSWORD', 'https://your-whm-url.com', 2087)
            
        # create account 
        result = server.create_account('sminrana@gmail.com', 'inafiz.com', 'package_name')
        print(result)
        success = result['success']
        self.assertEqual(success, 1)
        if success == 1:
            c_username = result['username']
            self.assertIsNotNone(c_username)
            
            # Suspend account
            suspend_result = server.suspend_account(c_username)
            self.assertEqual(suspend_result['success'], 1)
            
            # Terminate account
            destroy_result = server.terminate_account(result['username'])
            self.assertEqual(destroy_result['success'], 1)
            

if __name__ == '__main__':
    unittest.main()