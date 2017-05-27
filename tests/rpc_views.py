from nap import rpc


class View(rpc.RPCView):
    permit_introspect = True

    @rpc.method
    def echo(self, **kwargs):
        return kwargs
