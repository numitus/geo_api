# pylint: disable=invalid-name

result_serializer = "json"
accept_content = ["json"]
timezone = "UTC"
enable_utc = True
worker_prefetch_multiplier = 1  # disable prefetching
worker_cancel_long_running_tasks_on_connection_loss = True  # kill all long-running
# tasks with late acknowledgment enabled on connection loss (in Celery 6.0, True by
# default)
broker_connection_retry_on_startup = True
task_ignore_result = False
task_acks_late = True

worker_send_task_events = True
task_send_sent_event = True
