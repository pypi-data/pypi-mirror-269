from requests.adapters import Retry

default_retry_config: Retry = Retry(
    total=50, backoff_factor=0.25, backoff_jitter=2.5, status_forcelist=[429]
)
