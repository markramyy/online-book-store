from collections import defaultdict

import time


class Notification:
    def send(self, message, recipient):
        raise NotImplementedError("Subclasses must implement the send method.")


class EmailNotification(Notification):
    def send(self, message, recipient):
        print(f"Sending email to {recipient}: {message}")


class SMSNotification(Notification):
    def send(self, message, recipient):
        print(f"Sending SMS to {recipient}: {message}")


class NotificationFactory:
    @staticmethod
    def create_notification(notification_type, use_proxy=False):
        if notification_type == "email":
            notification = EmailNotification()
        elif notification_type == "sms":
            notification = SMSNotification()
        else:
            raise ValueError(f"Unsupported notification type: {notification_type}")

        if use_proxy:
            return NotificationProxy(notification)
        return notification


class NotificationRateLimiterSingleton:
    _instance = None
    _logs = defaultdict(list)

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(NotificationRateLimiterSingleton, cls).__new__(cls)
        return cls._instance

    @classmethod
    def check_and_update(cls, recipient, current_time, rate_limit_seconds):
        # Clean old entries
        cls._logs[recipient] = [
            t for t in cls._logs[recipient]
            if current_time - t < rate_limit_seconds
        ]

        # Check if rate limited
        if cls._logs[recipient]:
            return False

        # Add new timestamp
        cls._logs[recipient].append(current_time)
        return True


# With Singleton Pattern applied
class NotificationProxy(Notification):
    def __init__(self, notification, rate_limit_seconds=5):
        self.notification = notification
        self.rate_limit_seconds = rate_limit_seconds
        self.rate_limiter = NotificationRateLimiterSingleton()

    def send(self, message, recipient):
        current_time = time.time()
        print(f"Current time: {current_time}")

        if not self.rate_limiter.check_and_update(recipient, current_time, self.rate_limit_seconds):
            print(f"Notification rate limit exceeded for {recipient}. Please try again later.")
            return

        self.notification.send(message, recipient)
        print(f"Notification sent to {recipient}")


# Without Singleton Pattern applied
# class NotificationProxy(Notification):
#     # Class-level dictionary to store notification logs across all instances
#     _notification_logs = defaultdict(list)

#     def __init__(self, notification, rate_limit_seconds=5):
#         self.notification = notification
#         self.rate_limit_seconds = rate_limit_seconds

#     def send(self, message, recipient):
#         current_time = time.time()
#         print(f"Current time: {current_time}")

#         # Remove outdated timestamps (older than the rate limit)
#         NotificationProxy._notification_logs[recipient] = [
#             t for t in NotificationProxy._notification_logs[recipient]
#             if current_time - t < self.rate_limit_seconds
#         ]
#         print(f"Notification logs for {recipient}: {NotificationProxy._notification_logs[recipient]}")

#         # If there are recent notifications within the rate limit, block the notification
#         if len(NotificationProxy._notification_logs[recipient]) > 0:
#             print(f"Notification rate limit exceeded for {recipient}. Please try again later.")
#             return

#         # Otherwise, send the notification and log the timestamp
#         self.notification.send(message, recipient)
#         NotificationProxy._notification_logs[recipient].append(current_time)
#         print(f"Updated notification logs for {recipient}: {NotificationProxy._notification_logs[recipient]}")
