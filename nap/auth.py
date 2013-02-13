
# Authentication and Authorisation

class NullAuthorise(object):

    def may(self, request, action, object_id=None, **kwargs):
        return True

class DjangoAuthorise(object):
    '''Permissions based on Django's'''
    def may(self, request, action, object_id=None, **kwargs):
        if not request.user.is_authenticated():
            return request.method == 'GET'

        # Logically these permissions only apply to basic CRUD
        opts = self.model._meta

        if action == 'default':
            if request.method == 'POST' and object_id is None:
                return request.user.has_perm('.'.join([
                    opts.app_label,
                    opts.get_add_permission()
                ]))
            elif request.method == 'PUT' and object_id:
                return request.user.has_perm('.'.join([
                    opts.app_label,
                    opts.get_change_permission()
                ]))
            elif request.method == 'DELETE' and object_id:
                return request.user.has_perm('.'.join([
                    opts.app_label,
                    opts.get_delete_permission()
                ]))
        return False

