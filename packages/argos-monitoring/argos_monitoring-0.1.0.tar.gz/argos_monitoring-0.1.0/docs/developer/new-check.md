# Implementing a new check

## Creating a new check class

If you want to implement a new check, you need to create a new class that inherits from `argos.checks.BaseCheck`.

You need to implement two methods, and specify the type of the data you want to check.

Let's create a new check that ensures that the specified header is present.

```python
class HeaderExists(BaseCheck):
    """Checks that the response contains the specified header."""

    config = "header-exists"
    expected_cls = ExpectedStringValue

    async def run(self):
        response = await self.http_client.head(self.task.url)
        result = (self.expected.value in response.headers)

        return self.response(status=result)
```

## Using configuration values to determine the severity

The agents don't have access to the configuration values, so they can't determine the severity of the check, albeit in some case that could be useful.

If that's your case, you can implement the `finalize` method, and return some extra values in the `run` method, like this:

```python
    async def run(self):
            # ... see earlier example
            return self.response(status=result, extra_arg="extra_value")

    @classmethod
    async def finalize(cls, config, result, extra_arg):
        # You can use the extra_arg here to determine the severity
        return Status.SUCCESS, Severity.OK
```