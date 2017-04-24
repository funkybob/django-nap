from nap import rpc


class View(rpc.RPCView):

    @rpc.method
    def echo(self, **kwargs):
        return kwargs
