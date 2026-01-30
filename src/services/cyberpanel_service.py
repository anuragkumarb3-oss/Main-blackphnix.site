import os
import requests
import json
import logging

class CyberPanelService:
    def __init__(self):
        self.base_url = os.getenv("CYBERPANEL_URL", "").rstrip("/")
        self.admin_user = os.getenv("CYBERPANEL_ADMIN_USER")
        self.admin_pass = os.getenv("CYBERPANEL_ADMIN_PASS")
        self.verify_ssl = False # Often internal IPs use self-signed certs
        
    def _post(self, endpoint, data):
        url = f"{self.base_url}/api/{endpoint}"
        payload = {
            "adminUser": self.admin_user,
            "adminPass": self.admin_pass,
            **data
        }
        try:
            logging.info(f"CyberPanel Request to {url}: {json.dumps(payload)}")
            response = requests.post(url, data=payload, verify=self.verify_ssl, timeout=30)
            logging.info(f"CyberPanel Response: {response.status_code} - {response.text}")
            try:
                return response.json()
            except:
                if "success" in response.text.lower():
                    return {"status": 1, "message": response.text}
                return {"status": 0, "error": response.text}
        except Exception as e:
            logging.error(f"CyberPanel API Error ({endpoint}): {str(e)}")
            return {"status": 0, "error": str(e)}

    def create_user(self, username, password, email, package="Default"):
        return self._post("createUser", {
            "userName": username,
            "password": password,
            "email": email,
            "packageName": package,
            "acl": "user"
        })

    def create_website(self, domain, owner, package="Default"):
        return self._post("createWebsite", {
            "domainName": domain,
            "owner": owner,
            "packageName": package,
            "phpSelection": "7.4",
            "ssl": 1
        })

    def create_database(self, domain, db_name, db_user, db_pass):
        return self._post("createDatabase", {
            "websiteName": domain,
            "dbName": db_name,
            "dbUser": db_user,
            "dbPass": db_pass
        })

    def create_ftp_account(self, domain, ftp_user, ftp_pass):
        return self._post("createFTPAccount", {
            "domainName": domain,
            "ftpUser": ftp_user,
            "ftpPass": ftp_pass
        })

    def create_email_account(self, domain, email_user, email_pass):
        return self._post("createEmailAccount", {
            "domainName": domain,
            "emailUser": email_user,
            "emailPass": email_pass
        })

    def suspend_website(self, domain):
        return self._post("suspendWebsite", {"domainName": domain})

    def unsuspend_website(self, domain):
        return self._post("unsuspendWebsite", {"domainName": domain})

    def delete_website(self, domain):
        return self._post("deleteWebsite", {"domainName": domain})
