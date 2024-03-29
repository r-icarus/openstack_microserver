# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 Nebula, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from django.core.exceptions import ValidationError  # noqa

from horizon import conf


def validate_port_range(port):
    if port not in range(-1, 65536):
        raise ValidationError("Not a valid port number")


def validate_ip_protocol(ip_proto):
    if ip_proto not in range(-1, 256):
        raise ValidationError("%s is not a valid ip protocol number" %
                              type(ip_proto))


def password_validator():
    return conf.HORIZON_CONFIG["password_validator"]["regex"]


def password_validator_msg():
    return conf.HORIZON_CONFIG["password_validator"]["help_text"]


def validate_port_or_colon_separated_port_range(port_range):
    """accepts a port number or a single-colon separated range"""
    if port_range.count(':') > 1:
        raise ValidationError("One colon allowed in port range")
    ports = port_range.split(':')
    for port in ports:
        try:
            if int(port) not in range(-1, 65536):
                raise ValidationError("Not a valid port number")
        except ValueError:
            raise ValidationError("Port number must be integer")
