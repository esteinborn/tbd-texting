from django.core.management.base import BaseCommand, CommandError
from twilio_mgr.models import SmsNumber, Message, Location, MessageLog, EmailReminder
from twilio_mgr.management.commands.helper import sender
import datetime
import re
import os


# This is all in compliance of FCC Regulations
# Source: http://blog.textit.in/ensuring-your-sms-messaging-service-complies-with-fcc-regulations-tcpa

class Command(BaseCommand):
    help = 'Sends confirmation to numbers that have not received one yet'

    # def add_arguments(self, parser):
        # parser.add_argument('poll_id', nargs='+', type=int)

    def sms_reminder(self):
        now=datetime.datetime.now()
        targets = SmsNumber.objects.filter(cancelled=False, reminder_sent=False)
        message = Message.objects.get(keyword='DAY_OF_TBD_SMS')
        message_without_loc = Message.objects.get(keyword='DAY_OF_TBD_SMS_NO_LOCATION')

        for sms in targets:
            try:

                if sms.location is None:
                    true_msg = message_without_loc.message
                else:
                    # Prepare Message
                    true_msg = re.sub('\[ADDRESS\]', sms.location.address, message.message)
                    self.stdout.write(self.style.SUCCESS('Sending Message "%s" to "%s"' % (true_msg, sms.sms)))

                # 1. Send Message Twilio
                send_success = sender.twilio_send(sms.sms, true_msg)

                # 2. Mark SMS as intro'd
                sms.reminder_sent = True

                if not send_success:
                    sms.notes = "Error in sending."

                sms.save()

                # 3. Save Message to Message Log
                message_log = MessageLog(sms_number=sms.sms, message=true_msg)
                message_log.save()

                self.stdout.write(self.style.SUCCESS('Successfully sent intro "%s"' % sms.id))

            except Exception as e:
                print('Something Happened while sending message to %s - %s' % (sms.sms, str(e)))


    def email_reminder(self):
        """
        This function sends a confirmation email to folks whose email is in the system.
        """
        now=datetime.datetime.now()
        targets = EmailReminder.objects.filter(cancelled=False, reminder_sent=False)
        message = Message.objects.get(keyword='DAY_OF_TBD_EMAIL')
        message_without_loc = Message.objects.get(keyword='DAY_OF_TBD_EMAIL_NO_LOCATION')
        title = ""
        for email in targets:
            try:

                if email.location is None:
                    true_msg = message_without_loc.message
                    title = message_without_loc.subject
                else:
                    # Prepare Message
                    true_msg = re.sub('\[ADDRESS\]', email.location.address, message.message)
                    title = message.subject

                self.stdout.write(self.style.SUCCESS('Sending Message "%s" to "%s"' % (true_msg, title)))
                # else:
                #     # Prepare Message
                #     true_msg = re.sub('\[ADDRESS\]', email.location.address, message.message)
                #

                # 1. Send Email via sendgrid
                sender.sendgrid_send(email.email, true_msg, title)

                # 2. Mark Email as intro'd
                email.reminder_sent = True
                email.save()

                # 3. Save Message to Message Log
                message_log = MessageLog(email=email.email, message=true_msg)
                message_log.save()

                self.stdout.write(self.style.SUCCESS('Successfully sent intro "%s"' % email.email))

            except Exception as e:
                print('Something Happened while sending message to %s - %s' % (email.email, str(e)))


    def handle(self, *args, **options):
        print("Sending Reminders")
        self.sms_reminder()
        self.email_reminder()
