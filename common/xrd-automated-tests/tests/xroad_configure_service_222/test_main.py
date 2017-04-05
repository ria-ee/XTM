# coding=utf-8
import unittest

import configure_service_2_2_2
from tests.xroad_add_to_acl_218 import add_to_acl_2_1_8
from main.maincontroller import MainController
from helpers import xroad


class XroadConfigureService(unittest.TestCase):
    def test_xroad_configure_service(self):
        MainController.driver_autostart = False
        main = MainController(self)
        main.log_in = True
        main.close_webdriver = True

        ss_host = main.config.get('ss2.host')
        ss_user = main.config.get('ss2.user')
        ss_pass = main.config.get('ss2.pass')

        client = xroad.split_xroad_id(main.config.get('ss2.client_id'))
        requester = xroad.split_xroad_id(main.config.get('ss1.client_id'))

        wsdl_url = main.config.get('wsdl.remote_path').format(main.config.get('wsdl.service_wsdl'))

        service_name = main.config.get('services.test_service')  # xroadGetRandom
        service_2_name = main.config.get('services.test_service_2')  # bodyMassIndex

        subject_list = [xroad.get_xroad_subsystem(requester)]

        # Configure the service
        test_configure_service = configure_service_2_2_2.test_configure_service(case=main, client=client,
                                                                                check_add_errors=False,
                                                                                check_edit_errors=False,
                                                                                check_parameter_errors=False,
                                                                                service_name=service_name)

        # Add the subject to ACL
        test_configure_service_acl = add_to_acl_2_1_8.test_add_subjects(case=main, client=client,
                                                                        wsdl_url=wsdl_url,
                                                                        service_name=service_name,
                                                                        service_subjects=subject_list,
                                                                        remove_data=False,
                                                                        allow_remove_all=False)
        test_configure_service_acl_2 = add_to_acl_2_1_8.test_add_subjects(case=main, client=client,
                                                                          wsdl_url=wsdl_url,
                                                                          service_name=service_2_name,
                                                                          service_subjects=subject_list,
                                                                          remove_data=False,
                                                                          allow_remove_all=False)
        # Enable the service
        test_enable_service = configure_service_2_2_2.test_enable_service(case=main, client=client, wsdl_url=wsdl_url)

        # Delete the added service
        test_delete_service = configure_service_2_2_2.test_delete_service(case=main, client=client, wsdl_url=wsdl_url)

        try:
            # Open webdriver
            main.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)

            # Configure the service
            test_configure_service()
            # Configure service ACL

            main.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)
            test_configure_service_acl()

            # Configure second service ACL
            main.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)
            test_configure_service_acl_2()

            # Enable service
            main.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)
            test_enable_service()
        except:
            main.log('XroadConfigureService: Failed to configure service')
            try:
                # Delete service
                main.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)
                test_delete_service()
            except:
                main.log('XroadConfigureService: Failed to delete added data.')

            raise
        finally:
            # Test teardown
            main.tearDown()


class XroadDeleteService(unittest.TestCase):
    def test_xroad_configure_service(self):
        MainController.driver_autostart = False
        main = MainController(self)
        main.log_in = True
        main.close_webdriver = True

        ss_host = main.config.get('ss2.host')
        ss_user = main.config.get('ss2.user')
        ss_pass = main.config.get('ss2.pass')

        client = xroad.split_xroad_id(main.config.get('ss2.client_id'))

        wsdl_url = main.config.get('wsdl.remote_path').format(main.config.get('wsdl.service_wsdl'))

        # Delete the added service
        test_delete_service = configure_service_2_2_2.test_delete_service(case=main, client=client, wsdl_url=wsdl_url)

        try:
            # Delete service
            main.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)
            test_delete_service()
        except:
            main.log('XroadDeleteService: Failed to delete service')
            raise
        finally:
            # Test teardown
            main.tearDown()