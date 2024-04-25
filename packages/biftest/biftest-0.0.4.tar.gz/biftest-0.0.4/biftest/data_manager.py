
from request import Request

class Dashboards(Request):

    def __init__(self, url, token):
        super().__init__(url, token)

    def get_list(self, params):
        endpoint = self.url + 'dashboards'
        return self._get_request(endpoint, params)
        
    def create(self, inputId, data):
        endpoint = self.url + 'dashboards'
        return self._post_request(endpoint, data)
    
    def clone(self, inputId, data):
        endpoint = self.url + 'dashboards/' + inputId + '/clone'
        return self._post_request(endpoint, data)
    
    def put(self, inputId, data):
        endpoint = self.url + 'dashboards/' + inputId + '/put'
        return self._post_request(endpoint, data)
        
    def delete(self, inputId, data):
        endpoint = self.url + 'dashboards/' + inputId + '/delete'
        return self._post_request(endpoint, data)
        
    def get_permission(self, inputId, params):
        endpoint = self.url + 'dashboards/' + inputId + '/permission'
        return self._get_request(endpoint, params)
        
    def users_regist(self, inputId, data):
        endpoint = self.url + 'dashboards/' + inputId + '/permission/users'
        return self._post_request(endpoint, data)
        
    def users_put(self, inputId, data):
        endpoint = self.url + 'dashboards/' + inputId + '/permission/users/put'
        return self._post_request(endpoint, data)
        
    def users_delete(self, inputId, data):
        endpoint = self.url + 'dashboards/' + inputId + '/permission/users/delete'
        return self._post_request(endpoint, data)
        
    def groups_regist(self, inputId, data):
        endpoint = self.url + 'dashboards/' + inputId + '/permission/groups'
        return self._post_request(endpoint, data)
        
    def groups_put(self, inputId, data):
        endpoint = self.url + 'dashboards/' + inputId + '/permission/groups/put'
        return self._post_request(endpoint, data)
        
    def groups_delete(self, inputId, data):
        endpoint = self.url + 'dashboards/' + inputId + '/permission/groups/delete'
        return self._post_request(endpoint, data)