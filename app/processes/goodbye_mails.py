import time
from datetime import timedelta

from sqlalchemy.orm import Session

from app.api.applications.models import Application
from app.api.attendees.models import Attendee
from app.api.email_logs.crud import email_log as email_log_crud
from app.api.email_logs.models import EmailLog
from app.api.popup_city.models import PopUpCity
from app.api.products.models import Product
from app.core import models
from app.core.database import SessionLocal
from app.core.logger import logger
from app.core.utils import current_time

POPUP_CITY_SLUG = 'edge-esmeralda'
GOODBYE_TEMPLATE = 'goodbye-ee25'


def process_application_for_goodbye(application: Application):
    logger.info('Processing application %s %s', application.id, application.email)

    event = GOODBYE_TEMPLATE
    params = {'first_name': application.first_name}

    logger.info('Sending email %s to %s', event, application.email)

    email_log_crud.send_mail(
        receiver_mail=application.email,
        event=event,
        params=params,
        entity_type='application',
        entity_id=application.id,
    )

    spouse_attendee = next(
        (a for a in application.attendees if a.category == 'spouse'), None
    )
    if spouse_attendee:
        receiver_mail = spouse_attendee.email
        params['first_name'] = spouse_attendee.name
        logger.info('Sending email %s to spouse %s', event, receiver_mail)
        try:
            email_log_crud.send_mail(
                receiver_mail=receiver_mail,
                event=event,
                params=params,
                entity_type='application',
                entity_id=application.id,
            )
        except Exception as e:
            logger.error('Error sending email to spouse %s', receiver_mail)
            logger.error(e)


def get_sent_goodbye_emails(db: Session):
    logs = (
        db.query(EmailLog.receiver_email.distinct())
        .filter(EmailLog.template == GOODBYE_TEMPLATE)
        .all()
    )
    return [log[0] for log in logs]


def get_applications_for_goodbye(db: Session):
    popup = db.query(PopUpCity).filter(PopUpCity.slug == POPUP_CITY_SLUG).first()
    if not popup:
        raise ValueError('Popup not found')

    popup_id = popup.id
    excluded_application_emails = get_sent_goodbye_emails(db)
    logger.info('Excluded application emails: %s', excluded_application_emails)

    today = current_time()
    one_day_from_now = today + timedelta(days=1)

    applications = (
        db.query(Application)
        .join(Application.attendees)
        .filter(
            Application.popup_city_id == popup_id,
            Application.email.notin_(excluded_application_emails),
            # This ensures ALL products for the application have end_date before one day from now
            ~Application.attendees.any(
                Attendee.products.any(Product.end_date >= one_day_from_now)
            ),
            # This ensures the application has at least one product
            Application.attendees.any(Attendee.products.any()),
        )
        .distinct()
        .all()
    )
    logger.info('Total applications found: %s', len(applications))
    logger.info('Applications ids to process: %s', [a.id for a in applications])

    return applications


def goodbye_emails(db: Session):
    logger.info('Starting goodbye mails')
    applications = get_applications_for_goodbye(db)
    logger.info('Total applications to process: %s', len(applications))
    for application in applications:
        process_application_for_goodbye(application)
    logger.info('Finished goodbye mails')


def get_popup(db: Session):
    popup = db.query(PopUpCity).filter(PopUpCity.slug == POPUP_CITY_SLUG).first()
    if not popup:
        raise ValueError('Popup not found')
    return popup


def main():
    with SessionLocal() as db:
        goodbye_emails(db)
        logger.info('Sleeping for 1 hour...')
        time.sleep(1 * 60 * 60)


if __name__ == '__main__':
    main()
