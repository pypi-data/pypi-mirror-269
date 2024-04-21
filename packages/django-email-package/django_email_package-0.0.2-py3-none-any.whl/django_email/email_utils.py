from django.core.mail import EmailMessage
from django.template.loader import render_to_string

def send_html_email(template_name, context):
    try:
        html_content = render_to_string('{}.html'.format(template_name), {'context': context})
        email = EmailMessage(
            subject=context['subject'],
            body=html_content,
            from_email=context['from_email'],
            to=context['to'],
            reply_to=context['reply_to']
        )
        email.content_subtype = 'html'
        email.send()
        return True
    except Exception as e:
        print('Error:',e)
        return False
