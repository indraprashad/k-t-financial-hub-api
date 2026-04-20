"""
HTML Email Templates for Notifications
"""

CONSULTATION_BOOKING_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>New Consultation Booking</title>
    <style>
        @media only screen and (max-width: 600px) {{
            .container {{ width: 100% !important; }}
            .content {{ padding: 20px !important; }}
        }}
    </style>
</head>
<body style="margin: 0; padding: 0; background-color: #f5f5f5; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
    <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
        <tr>
            <td style="padding: 20px 0;">
                <table class="container" role="presentation" cellspacing="0" cellpadding="0" border="0" width="600" align="center" style="background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                    <!-- Header -->
                    <tr>
                        <td style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center;">
                            <h1 style="color: #ffffff; margin: 0; font-size: 24px;">📅 New Consultation Booking</h1>
                        </td>
                    </tr>
                    
                    <!-- Content -->
                    <tr>
                        <td class="content" style="padding: 40px;">
                            <p style="color: #333; font-size: 16px; line-height: 1.6; margin-bottom: 20px;">
                                A new consultation booking has been submitted.
                            </p>
                            
                            <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="background-color: #f8f9fa; border-radius: 8px; margin-bottom: 20px;">
                                <tr><td style="padding: 20px;">
                                    <p style="margin: 0 0 10px 0; color: #555;"><strong>Name:</strong> {name}</p>
                                    <p style="margin: 0 0 10px 0; color: #555;"><strong>Email:</strong> {email}</p>
                                    <p style="margin: 0 0 10px 0; color: #555;"><strong>Phone:</strong> {phone}</p>
                                    <p style="margin: 0 0 10px 0; color: #555;"><strong>Service:</strong> {service}</p>
                                    <p style="margin: 0 0 10px 0; color: #555;"><strong>Preferred Date:</strong> {preferred_date}</p>
                                    <p style="margin: 0; color: #555;"><strong>Message:</strong> {message}</p>
                                </td></tr>
                            </table>
                            
                            <p style="color: #888; font-size: 14px; text-align: center;">
                                Submitted at: {created_at}
                            </p>
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td style="background-color: #f8f9fa; padding: 20px; text-align: center; border-top: 1px solid #eee;">
                            <p style="color: #aaa; font-size: 12px; margin: 0;">
                                © 2026 K&T Financial. All rights reserved.
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""

CONTACT_SUBMISSION_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>New Contact Message</title>
    <style>
        @media only screen and (max-width: 600px) {{
            .container {{ width: 100% !important; }}
            .content {{ padding: 20px !important; }}
        }}
    </style>
</head>
<body style="margin: 0; padding: 0; background-color: #f5f5f5; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
    <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
        <tr>
            <td style="padding: 20px 0;">
                <table class="container" role="presentation" cellspacing="0" cellpadding="0" border="0" width="600" align="center" style="background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                    <!-- Header -->
                    <tr>
                        <td style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center;">
                            <h1 style="color: #ffffff; margin: 0; font-size: 24px;">✉️ New Contact Message</h1>
                        </td>
                    </tr>
                    
                    <!-- Content -->
                    <tr>
                        <td class="content" style="padding: 40px;">
                            <p style="color: #333; font-size: 16px; line-height: 1.6; margin-bottom: 20px;">
                                A new contact form submission has been received.
                            </p>
                            
                            <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="background-color: #f8f9fa; border-radius: 8px; margin-bottom: 20px;">
                                <tr><td style="padding: 20px;">
                                    <p style="margin: 0 0 10px 0; color: #555;"><strong>Name:</strong> {name}</p>
                                    <p style="margin: 0 0 10px 0; color: #555;"><strong>Email:</strong> {email}</p>
                                    <p style="margin: 0 0 10px 0; color: #555;"><strong>Phone:</strong> {phone}</p>
                                    <p style="margin: 0 0 10px 0; color: #555;"><strong>Subject:</strong> {subject}</p>
                                    <p style="margin: 0; color: #555;"><strong>Message:</strong></p>
                                    <p style="margin: 10px 0 0 0; color: #333; background: #fff; padding: 15px; border-radius: 5px; border-left: 3px solid #667eea;">{message}</p>
                                </td></tr>
                            </table>
                            
                            <p style="color: #888; font-size: 14px; text-align: center;">
                                Submitted at: {created_at}
                            </p>
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td style="background-color: #f8f9fa; padding: 20px; text-align: center; border-top: 1px solid #eee;">
                            <p style="color: #aaa; font-size: 12px; margin: 0;">
                                © 2026 K&T Financial. All rights reserved.
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""


def render_consultation_email(booking):
    """Render consultation booking email template"""
    return CONSULTATION_BOOKING_TEMPLATE.format(
        name=booking.name,
        email=booking.email,
        phone=booking.phone or 'N/A',
        service=booking.service,
        preferred_date=booking.preferred_date,
        message=booking.message or 'N/A',
        created_at=booking.created_at.strftime('%Y-%m-%d %H:%M')
    )


def render_contact_email(submission):
    """Render contact submission email template"""
    return CONTACT_SUBMISSION_TEMPLATE.format(
        name=submission.name,
        email=submission.email,
        phone=submission.phone or 'N/A',
        subject=submission.subject,
        message=submission.message,
        created_at=submission.created_at.strftime('%Y-%m-%d %H:%M')
    )
