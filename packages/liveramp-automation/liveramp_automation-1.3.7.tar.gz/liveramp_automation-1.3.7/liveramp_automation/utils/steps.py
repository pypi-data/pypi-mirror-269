from pytest_bdd import when, then
from liveramp_automation.utils.parsers import ParseUtils


@then(ParseUtils('The response status code should be {code:d}'))
@when(ParseUtils('The response status code should be {code:d}'))
def verify_endpoint_response_code(code, response_body):
    assert response_body.status_code == code, (
        "Expected code: {}, actual code: {}".format(code, response_body.status_code))


@then(ParseUtils('The response body should contain the {fields}'))
@when(ParseUtils('The response body should contain the {fields}'))
def verify_endpoint_response_exist(fields, response_body):
    response_keys = response_body.json().keys()
    assert all(key in response_keys for key in eval(fields)), \
        "Not all fields: {} in response: {}".format(fields, response_keys)
