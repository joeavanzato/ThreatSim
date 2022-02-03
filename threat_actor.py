

class Actor():

    def __init__(self, args, command_list, command_dict):
        self.mode = args['mode']
        self.actor_file = args['actor']
        self.target = args['target']
        self.remote = args['remote']
