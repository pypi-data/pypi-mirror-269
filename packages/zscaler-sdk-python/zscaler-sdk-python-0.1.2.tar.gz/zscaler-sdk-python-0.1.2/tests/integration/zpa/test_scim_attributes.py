# -*- coding: utf-8 -*-

# Copyright (c) 2023, Zscaler Inc.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.


import pytest

from tests.integration.zpa.conftest import MockZPAClient


@pytest.fixture
def fs():
    yield


class TestScimAttributes:
    """
    Integration Tests for the SCIM attributes
    """

    def test_scim_attributes_operations(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        try:
            # Test listing SCIM attributes by IDP
            idps = client.idp.list_idps()
            user_idp = next(
                (idp for idp in idps if "USER" in idp.get("sso_type", [])), None
            )
            assert user_idp is not None, "No IdP with sso_type 'USER' found."

            user_idp_id = user_idp["id"]
            resp = client.scim_attributes.list_attributes_by_idp(user_idp_id)
            assert isinstance(
                resp, list
            ), "Response is not in the expected list format."
            assert len(resp) > 0, "No SCIM groups were found for the specified IdP."
        except Exception as exc:
            errors.append(f"Listing SCIM attributes by IDP failed: {exc}")

        try:
            # Test getting a specific SCIM attribute
            attributes = client.scim_attributes.list_attributes_by_idp(user_idp_id)
            assert (
                len(attributes) > 0
            ), "No SCIM attributes found for the specified IdP."

            first_attribute_id = attributes[0][
                "id"
            ]  # Assuming attributes is a list of dicts
            resp = client.scim_attributes.get_attribute(user_idp_id, first_attribute_id)
            assert isinstance(
                resp, dict
            ), "Response is not in the expected dict format."
            assert (
                resp["id"] == first_attribute_id
            ), "Retrieved SCIM attribute ID does not match the requested ID."
        except Exception as exc:
            errors.append(f"Getting a specific SCIM attribute failed: {exc}")

        # Assert that no errors occurred during the test
        assert (
            len(errors) == 0
        ), f"Errors occurred during SCIM attributes operations test: {errors}"
