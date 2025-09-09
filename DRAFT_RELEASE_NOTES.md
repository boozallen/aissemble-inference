# Major Additions

## Model Loading
To give more structure and guidance to the inference process, `model_load` has been added to the dataplane handler. Load will not be called by us so it is up to the user to call it where it makes the most sense.

# Breaking Changes

## Update Auth Config
The gRPC authorization config variable `grpc_protected_endpoints` has been removed. Unless there is further demand, it makes the most sense to protect all or no endpoints. 

# What's Changed
