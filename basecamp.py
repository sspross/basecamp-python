from xml.etree import ElementTree as ET

import urllib2
import base64

class BasecampError(Exception):
    pass

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
        if isinstance(data, ET._ElementInterface):
            data = ET.tostring(data)
        req = urllib2.Request('%s/%s' % (self.baseURL, path), data=data, \
            # Set header again, because the request overwrites his content-type 
            # header to 'application/x-www-form-urlencoded' if data is set.
            headers={'Content-Type':'application/xml'})
        try:
            return self.opener.open(req)
        except Exception, e:
            raise BasecampError, '%s, %s' % (e.code, e.read())
        
    def project(self, project_id):
        return self._request('projects/%u' % project_id).read()
        
    def time_entries(self, project_id, page=1):
        return self._request('projects/%u/time_entries?page=%u' % (project_id, page)).read()
        
    def person(self, person_id):
        return self._request('people/%u' % person_id).read()
        
    def people(self, company_id):
        return self._request('companies/%u/people.xml' % company_id).read()
        
    def companies(self):
        return self._request('companies.xml').read()
        
    def create_project(self, project_name):
        """
        Creates a project and returns the new project id from the given
        location header.
        """
        request = ET.Element('request')
        project = ET.SubElement(request, 'project')
        ET.SubElement(project, 'name').text = str(project_name)
        result = self._request('projects.xml', request)
        # location looks like /projects/7886826.xml
        return int(result.headers.dict['location'].split('/')[-1].split('.')[0]) 
