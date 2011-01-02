import urllib2
import base64

class Basecamp(object):
    """
    Example:
    bc = Basecamp('https://yourcompany.projectpath.com', 'username', 'password')
    print bc.project(123456)
    """
    
    def __init__(self, baseURL, username, password):
        self.baseURL = baseURL
        base64string = base64.encodestring('%s:%s' % (username, password))[:-1]
        self.opener = urllib2.build_opener()
        self.opener.addheaders = [
            ('Content-Type', 'application/xml'),
            ('Accept', 'application/xml'),
            ('Authorization', 'Basic %s' % base64string)]
            
    def _request(self, path, data=None):
        req = urllib2.Request('%s/%s' % (self.baseURL, path))
        return self.opener.open(req).read()
        
    def project(self, project_id):
        return self._request('projects/%u' % project_id)

    def time_entries_report(self, company_id, date_from, date_to):
        """
        Returns a set of time entries of a company in a given time.
        Dates should be in YYYYMMDD format.
        """
        path = 'time_entries/report?from=%u&to=%u&filter_company_id=%u' \
            % (date_from, date_to, company_id)
        return self._request(path)
