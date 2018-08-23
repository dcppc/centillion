# Centillion Tests

## Test Plan

The test plan for Centillion is detailed in
<https://github.com/dcppc/centillion/issues/82>.

The test suite for centillion needs to check
each of the major components of centillion,
as well as check the authentication mechanism
using multiple login credentials.

We implement four checks:

1. Check authentication mechanism(s) (yamasnake and florence python)

2. Check search function/endpoint

3. Check master list function/endpoint

4. Check control panel endpoint

The tests are written such that the back end and front end
are tested separately.


## Continuous Integration Plan

Tests are automatically run using Uncle Archie for continuous
integration and deployment.



