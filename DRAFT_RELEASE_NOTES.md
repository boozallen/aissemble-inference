# Major Additions

## Model Loading
To give more structure and guidance to the inference process, `model_load` has been added to the dataplane handler. Load will not be called by us so it is up to the user to call it where it makes the most sense.

# Breaking Changes

## Model Handler Implementation
We have moved the required model logic off to a ModelHandler. This seperated the Dataplane and Model handler objectives. The dataplane will be handled by our solutions and will move the request data through validation and transformation to the model layer. This also alleviates some of the required dataplane logic.

To upgrade, update your Dataplane handler to instead extend the Model handler and remove any Dataplane specific functions (e.g. server_ready, server_live, and server_metadata). 

## AissembleOIPFastAPI Initialization
The AissembleOIPFastAPI class is now initialized with the handler and adapter instance and not the class' themselves. This was done to keep consistency across solutions.

To upgrade, pass the initialized handler and adapter to the server. e.g: `AissembleOIPFastAPI(Handler, Adapter) -> AissembleOIPFastAPI(Handler(), Adapter())`

## Update Auth Config
The gRPC authorization config variable `grpc_protected_endpoints` has been removed. Unless there is further demand, it makes the most sense to protect all or no endpoints. 

To upgrade, remove the property from either you environment variables to the Krausening properties file.

# What's Changed
