# Pulumi Commandx

Mostly helper functions for creating statically typed `Command` resources.

## Development

Note that the generated provider plugin (`pulumi-resource-commandx`) must be on your `PATH` to be used by Pulumi deployments.

## Prerequisites

- Go 1.21
- Pulumi CLI
- Node.js (to build the Node.js SDK)
- Yarn (to build the Node.js SDK)
- Python 3.6+ (to build the Python SDK)
- .NET Core SDK (to build the .NET SDK)
- Gradle (to build the Java SDK)

## Build and Test

```bash
# Build and install the provider (plugin copied to ./bin)
make install_provider

# Regenerate schema, schema-types, and SDKs
make generate

# Test Node.js SDK
$ make install_nodejs_sdk
$ cd examples/simple-ts
$ yarn install
$ yarn link @unmango/pulumi-commandx
$ pulumi stack init test
$ pulumi up
```

## Naming

The `commandx` provider's plugin binary must be named `pulumi-resource-commandx` (in the format `pulumi-resource-<provider>`).
