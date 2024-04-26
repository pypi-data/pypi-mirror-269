import os

from typeguard import typechecked

@typechecked
def is_running_in_kubernetes() -> bool:
    """Check if the code is running in a Kubernetes cluster.

    Returns:
        bool: True if running in Kubernetes, False otherwise
    """
    return 'KUBERNETES_SERVICE_HOST' in os.environ
