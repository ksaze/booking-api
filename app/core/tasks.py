import logging

from core.celery_app import celery_app

logger = logging.getLogger("fitness_studio.tasks")


@celery_app.task(name="tasks.send_booking_confirmation_email", bind=True, max_retries=3)
def send_booking_confirmation_email(
    self, client_email: str, client_name: str, class_name: str, date_time_iso: str
) -> bool:
    """
    Sends (or, here, logs) a booking confirmation.

    This is the async counterpart to the "booking_created" event in
    crud/booking.py: once a booking commits, the route handler enqueues
    this task (`send_booking_confirmation_email.delay(...)`) instead of
    blocking the request on an email/SMS provider call.
    """
    logger.info(
        "Booking confirmation -> %s: '%s' is confirmed for %s at %s",
        client_email,
        client_name,
        class_name,
        date_time_iso,
    )
    # TODO: plug in a real email/SMS provider (SES, SendGrid, Twilio, ...).
    return True


@celery_app.task(name="tasks.send_class_reminder")
def send_class_reminder(client_email: str, class_name: str, date_time_iso: str) -> bool:
    """Placeholder for a reminder sent some fixed time before class start."""
    logger.info(
        "Reminder -> %s: '%s' starts at %s", client_email, class_name, date_time_iso
    )
    return True
