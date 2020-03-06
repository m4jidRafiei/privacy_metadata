class privacyExtension():

    def __init__(self, log, prefix, uri):
        self.log = log
        self.prefix = prefix
        self.uri = uri


    def set_privacy_tracking(self, operation, level, target):

        layer = self.get_last_layer()

        if(layer is None):
            layer = 1
            self.log.extensions['Privacy'] = {'prefix': self.prefix[:-1], 'uri': self.uri}
            privacyTracking = {}
        else:
            layer += 1
            privacyTracking = self.log.attributes[self.prefix+'anonymizations']

        tracking = {}
        tracking[self.prefix + 'layer'] = layer
        tracking[self.prefix + 'operation'] = operation    #'substitution'
        tracking[self.prefix + 'level'] = level   #'event'
        tracking[self.prefix + 'target'] = target      #'concept:name'

        if(layer == 1):
            privacyTracking[self.prefix+'tracking'+str(layer)] = {"value": None, "children": tracking}
            self.log.attributes[self.prefix+'anonymizations'] = {"value": None, "children": privacyTracking}
        else:
            privacyTracking['children'][self.prefix+'tracking'+str(layer)]= {"value": None, "children": tracking}


    def set_optional_tracking(self, layer, **keyparam):
        if (keyparam != {}):
            current_layer = self.get_last_layer()
            if(current_layer == None or current_layer < layer):
                return "The layer does not exist!"
            privacyTracking = self.log.attributes[self.prefix + 'anonymizations']
            for key,value in keyparam.items():
                if type(value) is dict:
                    privacyTracking['children'][self.prefix+'tracking' + str(layer)]['children'][key] = {"value": None, "children": value}
                else:
                    privacyTracking['children'][self.prefix + 'tracking' + str(layer)]['children'][key] = value
            return "The parameters have been added."
        else:
            return "No parameter has been passed!"

    def get_last_layer(self):
        try:
            layer = len(self.log.attributes[self.prefix+'anonymizations']['children'])
            return layer
        except Exception as e:
            return None

    def get_layer(self,layer):
        return self.log.attributes[self.prefix + 'anonymizations']['children'][self.prefix+'tracking' + str(layer)]['children']

    def get_anonymizations(self):
        return self.log.attributes[self.prefix + 'anonymizations']['children']

