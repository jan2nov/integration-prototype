# -*- coding: utf-8 -*-
"""Docker Client API"""


class DockerClient:
    """Docker Client Interface"""

    def __init__(self):
        """ Constructor of the class"""
        print("Hello World")

    ###########################################################################
    # Create functions
    ###########################################################################

    def create_service(self):
        """

        Args:
        """
        pass

    def create_volume(self):
        """

        Args:
        """
        pass

    ###########################################################################
    # Delete functions
    ###########################################################################

    def delete_service(self):
        """ Removes/stops a service

        Args:
        """
        pass

    ###########################################################################
    # Get functions
    ###########################################################################

    def get_node_list(self):
        """ Get a list of nodes

        Args:
        """
        pass

    def get_node(self):
        """ Get a node

        Args:
        """
        pass

    def get_service_list(self):
        """ Get a list of service

        Args:
        """
        pass

    def get_service(self):
        """ Get a service

        Args:
        """
        pass

    def get_volume(self):
        """ Get a volume

        Args:
        """
        pass

    ###########################################################################
    # Update functions
    ###########################################################################

    def update_service(self):
        """ Update a service's configuration.

        Args:
        """
        pass

    def update_node(self, name, labels):
        """Update node's configuration

          Args:
            name (string): Name of the node.
            labels (dict): Label to add to the node
        """

        #TODO:(NJT) Need to think about wether to create the spec inside this
        #TODO: function. Probably best to do it inside the function
        pass
