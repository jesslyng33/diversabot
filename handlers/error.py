from app import app 
from slack_bolt.error import BoltUnhandledRequestError
from slack_bolt import BoltResponse


@app.error
def handle_errors(error, body, logger):
    """ Handles errors that occur during request servicing. 
    
    NOTE: Comment out this function for verbose error tracebacks.
    This should probably be configurable with a --verbose or --debug flag in the future."""
    if isinstance(error, BoltUnhandledRequestError):
        logger.info(f"Unhandled request for {body}")
        return BoltResponse(status=200, body="")
    else:
        logger.error(f"Error: {error}")
        raise error