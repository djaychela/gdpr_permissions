from gdpr_permissions.data.capabilities import Capabilities
from gdpr_permissions.data.dbsession import DbSessionFactory


class CapabilitiesService():
    @staticmethod
    def list_all_attributes():
        return ['id', 'capability', 'capability_nice', 'active']

    @staticmethod
    def get_capabilities(mode=''):
        session = DbSessionFactory.create_session()
        capability_output_list = []
        for capability in session.query(Capabilities).order_by('id'):
            if capability.active:
                if mode == 'nice':
                    capability_output_list.append(capability.capability_nice)
                else:
                    capability_output_list.append(capability.capability)
        return capability_output_list

    @staticmethod
    def get_all_capabilities():
        session = DbSessionFactory.create_session()
        cap_list = CapabilitiesService.list_all_attributes()
        all_capability_output_list = []
        for capability in session.query(Capabilities).order_by('id'):
            current_dict = {}
            for cap in cap_list:
                current_dict[cap] = eval('capability.' + cap)
            all_capability_output_list.append(current_dict)
        return all_capability_output_list

    @staticmethod
    def get_single_capability(cap_id):
        session = DbSessionFactory.create_session()
        cap_list = CapabilitiesService.list_all_attributes()
        capability_output = {}
        capability = session.query(Capabilities).get(cap_id)
        for cap in cap_list:
            capability_output[cap] = eval('capability.' + cap)
        return capability_output

    @staticmethod
    def update_capability(cap_to_store):
        session = DbSessionFactory.create_session()
        capability = session.query(Capabilities).get(cap_to_store['id'])
        attributes = CapabilitiesService.list_all_attributes()[1:-1]
        for attribute in attributes:
            exec("capability." + attribute + "='" + cap_to_store[attribute] + "'")
        exec("capability.active=" + str(cap_to_store['active']))
        session.commit()
        return
