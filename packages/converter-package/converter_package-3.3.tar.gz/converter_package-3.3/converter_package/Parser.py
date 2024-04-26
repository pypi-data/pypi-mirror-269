import os
from converter_package import Action
import yaml
from converter_package import Repository
from converter_package import ComputeNode

from converter_package import CloudFramework
from converter_package import Container
from converter_package import Workflows

home = str(os.getcwd())


def ReadFile(file_path):
    nodelist = []

    imagelist = []
    application = ""
    with open(file_path, 'r') as yaml_file:
        file = yaml.safe_load(yaml_file)
    topology = file.get('topology_template')
    node_template = topology.get('node_templates')
    node_names = node_template.keys()
    print(node_names)
    for x in node_names:
        node = node_template.get(x)
        type = node.get('type')
        properties = node.get('properties')
        if 'Cloud_Framework' in type:
            cloud = CloudFramework.CloudFramework()
            cloud.set_type(type)
            application = properties.get('application')
            cloud.set_application(application)
            if 'deployment_phase' in properties:
                actions = properties.get('deployment_phase')
                actionlist = []
                for actionset in actions:
                    component_names = []
                    action = Action.Action()
                    action.set_name(actionset.get('name'))
                    action.set_order(actionset.get('order'))
                    images = actionset.get('components')
                    for image in images:
                        print(image)
                        object = Image.Image()
                        object.set_image_type(image.get('type'))
                        component_names.append(image.get('component').lower())
                        object.set_path(image.get('component').lower())
                        object.set_component(image.get('component'))
                        if not imagelist:
                            imagelist.append(object)
                        if imagelist[-1].get_path() != image.get('component').lower():
                            imagelist.append(object)

                    actionlist.append(
                        {'action': action.get_name(), 'order': action.get_order(),
                         'components': images})
                cloud.set_actions(actionlist)
            nodelist.append(cloud)
            if 'workflows' in properties:
                workflows = properties.get('workflows')
                workflowlist = []
                actionlist = []
                for workflowset in workflows:
                    workflow = Workflows.Workflows()
                    workflow.set_scenario(workflowset.get('scenario'))
                    workflow.set_condition(workflowset.get('condition'))
                    actions = workflowset.get('actions')
                    actionlist = []
                    for actionset in actions:
                        component_names = []
                        action = Action.Action()
                        action.set_name(actionset.get('name'))
                        action.set_order(actionset.get('order'))
                        if action.get_name() != 'send':
                            images = actionset.get('components')
                            for image in images:
                                print(image)
                                object = Image.Image()
                                object.set_image_type(image.get('type'))
                                component_names.append(image.get('component').lower())
                                object.set_path(image.get('component').lower())
                                object.set_component(image.get('component'))

                            actionlist.append(
                                {'action': action.get_name(), 'order': action.get_order(),
                                 'components': images})
                        if action.get_name() == 'send':
                            if actionset.get('input'):
                                target_list = actionset.get('input')
                            for target in target_list:
                                target.update(component=target.get('component').lower(), to=target.get('to').lower())

                            actionlist.append(
                                {'action': action.get_name(), 'order': action.get_order(),
                                 'send': target_list})
                    workflowlist.append({'scenario': workflow.get_scenario(), 'condition': workflow.get_condition(),
                                         'actions': actionlist})
                cloud.set_workflows(workflowlist)
        if 'Component' in type:
            container = Container.Container()
            container.set_type(type)
            registry = properties.get('registry')
            registry_properties = registry.get('properties')
            image = registry_properties.get('image')
            container.set_image(image)
            type = registry_properties.get('type')
            container.set_registry_type(type)
            name = properties.get('name')
            container.set_name(name)
            container.set_application(application)
            if properties.get('instance'):
                instance_num = properties.get('instance')
                container.set_instance(instance_num)
            else:
                container.set_instance(1)
            service = properties.get('external_ip')
            container.set_service(service)
            unit = properties.get('deployment_unit')
            if unit == "vm":
                flavor = properties.get("flavor")
                container.set_flavor(flavor)
            container.set_unit(unit)
            ports = properties.get('ports')
            if ports:
                container.set_port(ports)
            else:
                container.set_port(None)
            storage_type = properties.get('storage_type')
            container.set_storage_type(storage_type)
            if storage_type == "persistent":
                container.set_volumeMounts_name(name + '-persistent-storage')
                container.set_volumeMounts_path('/var/lib/' + name)
                container.set_volumes_name(name + '-persistent-storage')
                container.set_volumes_claimname(name + '-pv-claim')
            if properties.get('dependency'):
                dependency = properties.get('dependency')
                container.set_dependency(dependency)
            else:
                container.set_dependency(None)
            requirements = node.get('requirements')[0]
            host = requirements.get('host')
            container.set_host(host)
            nodelist.append(container)
        if 'EdgeNode' in type:
            edgenode = ComputeNode.ComputeNode()
            edgenode.set_name(x)
            edgenode.set_type(type)
            if properties:
                if properties.get('gpu_model'):
                    gpu_model = properties.get('gpu_model')
                    gpu_properties = gpu_model.get('properties')
                    if gpu_properties.get('model'):
                        model = gpu_properties.get('model')
                        edgenode.set_gpu_model(model)
                    if gpu_properties.get('brand'):
                        brand = gpu_properties.get('brand')
                        edgenode.set_gpu_brand(brand)
                    if not gpu_properties.get('brand'):
                        edgenode.set_gpu_brand("None")
                    dedicated = gpu_properties.get('dedicated')
                    edgenode.set_gpu_dedicated(dedicated)
                wifi_antenna = properties.get('wifi_antenna')
                if wifi_antenna:
                    edgenode.set_wifi_antenna(wifi_antenna)
                if not wifi_antenna:
                    edgenode.set_wifi_antenna("None")
                if not properties.get('gpu_model'):
                    edgenode.set_gpu_model("None")
                    edgenode.set_gpu_dedicated("None")
                    edgenode.set_gpu_brand("None")
            if not properties:
                edgenode.set_gpu_model("None")
                edgenode.set_gpu_dedicated("None")
                edgenode.set_wifi_antenna("None")
                edgenode.set_gpu_brand("None")
            capabilities = node.get('capabilities')
            if capabilities.get('host'):
                host = capabilities.get('host')
                host_properties = host.get('properties')
                if host_properties.get('num_cpus'):
                    num_cpus = host_properties.get('num_cpus')
                    edgenode.set_num_cpu(num_cpus)
                else:
                    edgenode.set_num_cpu(None)
                mem_size = host_properties.get('mem_size')
                edgenode.set_mem_size(mem_size)
                if host_properties.get('disk_size') is not None:
                    disk_size = host_properties.get('disk_size')
                    edgenode.set_disk_size(disk_size)
                else:
                    edgenode.set_disk_size("200 MB")
            else:
                edgenode.set_num_cpu(None)
                edgenode.set_mem_size(None)
                edgenode.set_disk_size("200 MB")
            os = capabilities.get('os')
            os_properties = os.get('properties')
            os_type = os_properties.get('type')
            architecture = os_properties.get('architecture')
            edgenode.set_architecture(architecture)
            edgenode.set_os(os_type)
            nodelist.append(edgenode)
        if 'PublicCloud' in type:
            vm = ComputeNode.ComputeNode()
            vm.set_name(x)
            vm.set_type(type)
            capabilities = node.get('capabilities')
            if capabilities.get('host'):
                host = capabilities.get('host')
                host_properties = host.get('properties')
                num_cpus = host_properties.get('num_cpus')
                vm.set_num_cpu(num_cpus)
                mem_size = host_properties.get('mem_size')
                vm.set_mem_size(mem_size)
                disk_size = host_properties.get('disk_size')
                vm.set_disk_size(disk_size)
            else:
                vm.set_num_cpu(None)
                vm.set_mem_size(None)
                vm.set_disk_size("200 MB")
            os = capabilities.get('os')
            os_properties = os.get('properties')
            os_type = os_properties.get('type')
            vm.set_os(os_type)
            architecture = os_properties.get('architecture')
            vm.set_architecture(architecture)
            nodelist.append(vm)

    return (nodelist)
