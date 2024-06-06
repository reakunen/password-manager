import objc
import time
import threading
from Foundation import NSObject
from LocalAuthentication import LAContext, LAPolicyDeviceOwnerAuthenticationWithBiometrics
from manager import PasswordManager
import os 

MASTER_PASSWORD_FILE = './passwords/master_password.json'

class BiometricAuth(NSObject):

    def authenticateWithBiometrics(self):
        context = LAContext.alloc().init()
        error = objc.nil

        # Check if the device supports biometric authentication
        success, error = context.canEvaluatePolicy_error_(LAPolicyDeviceOwnerAuthenticationWithBiometrics, error)
        if success:
            reason = "Authenticate to access the application"

            # Create an event to synchronize with the authentication result
            auth_event = threading.Event()

            # Perform the biometric authentication
            def reply(success, error):
                if success:
                    print("Authentication was successful!")
                else:
                    print(f"Authentication failed: {error.localizedDescription()}")
                    exit(-1) 
                # Set the event to indicate that authentication is complete
                auth_event.set()

            context.evaluatePolicy_localizedReason_reply_(LAPolicyDeviceOwnerAuthenticationWithBiometrics, reason, reply)

            # Wait for the authentication process to complete
            auth_event.wait()
        else:
            print(f"Biometric authentication is not available: {error.localizedDescription() if error else 'Unknown error'}")

if __name__ == "__main__":
    auth = BiometricAuth.alloc().init()
    auth.authenticateWithBiometrics()

    # Once authenticated, continue with the application logic
    print("Authenticated! Proceeding with the application logic.")
    # Run your application code here
    if not os.path.exists(MASTER_PASSWORD_FILE):
        manager = PasswordManager()
        manager.welcome_new_user()
    else:
        manager = PasswordManager()
        manager.login_user()
    manager.window.mainloop()
    # Just to demonstrate, let's wait for a few seconds before exiting
    # time.sleep(5)
