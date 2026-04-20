"""
HTML Email Templates for Invitation System
"""

INVITATION_EMAIL_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>You're Invited to Join K&T Financial</title>
    <style>
        @media only screen and (max-width: 600px) {{
            .container {{ width: 100% !important; }}
            .content {{ padding: 20px !important; }}
            .button {{ width: 100% !important; }}
        }}
    </style>
</head>
<body style="margin: 0; padding: 0; background-color: #f5f5f5; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
    <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
        <tr>
            <td style="padding: 20px 0;">
                <table class="container" role="presentation" cellspacing="0" cellpadding="0" border="0" width="600" align="center" style="background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                    <!-- Header with Logo -->
                    <tr>
                        <td style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 0; text-align: center;">
                            <img src="https://www.kt-info.com/static/logo.png" alt="K&T Financial" style="max-width: 200px; height: auto;" />
                        </td>
                    </tr>
                    
                    <!-- Hero Illustration -->
                    <tr>
                        <td style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 50%, #4facfe 100%); padding: 60px 40px; text-align: center;">
                            <div style="background: rgba(255, 255, 255, 0.95); border-radius: 16px; padding: 40px; margin: 0 auto; max-width: 480px;">
                                <div style="font-size: 48px; margin-bottom: 20px;">🎉</div>
                                <h1 style="color: #333; font-size: 28px; margin: 0 0 10px 0; font-weight: 700;">
                                    You're Invited!
                                </h1>
                                <p style="color: #666; font-size: 16px; margin: 0;">
                                    Join K&T Financial Team
                                </p>
                            </div>
                        </td>
                    </tr>
                    
                    <!-- Content -->
                    <tr>
                        <td class="content" style="padding: 40px;">
                            <p style="color: #333; font-size: 18px; line-height: 1.6; margin-bottom: 20px;">
                                Hello,
                            </p>
                            
                            <p style="color: #555; font-size: 16px; line-height: 1.6; margin-bottom: 20px;">
                                <strong>{invited_by}</strong> has invited you to join <strong>K&T Financial</strong> as a <span style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 700;">{role}</span>.
                            </p>
                            
                            <p style="color: #555; font-size: 16px; line-height: 1.6; margin-bottom: 30px;">
                                Click the button below to accept this invitation and set up your account. This invitation will expire on <strong style="color: #764ba2;">{expires_at}</strong>.
                            </p>
                            
                            <!-- CTA Button -->
                            <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                                <tr>
                                    <td style="text-align: center; padding: 20px 0;">
                                        <a href="{invitation_url}" class="button" style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #ffffff; text-decoration: none; padding: 16px 40px; border-radius: 30px; font-size: 16px; font-weight: 600; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);">
                                            Accept Invitation →
                                        </a>
                                    </td>
                                </tr>
                            </table>
                            
                            <!-- Alternative Link -->
                            <p style="color: #888; font-size: 14px; line-height: 1.5; margin-top: 30px; text-align: center;">
                                If the button doesn't work, copy and paste this link into your browser:<br>
                                <a href="{invitation_url}" style="color: #667eea; word-break: break-all;">{invitation_url}</a>
                            </p>
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td style="background-color: #f8f9fa; padding: 30px 40px; text-align: center; border-top: 1px solid #eee;">
                            <p style="color: #999; font-size: 13px; margin: 0 0 10px 0;">
                                If you did not expect this invitation, please ignore this email.
                            </p>
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


def render_invitation_email(invitation, invitation_url):
    """Render the invitation email with provided data"""
    return INVITATION_EMAIL_TEMPLATE.format(
        invited_by=invitation.invited_by.username if invitation.invited_by else 'K&T Financial',
        role=invitation.role.name,
        expires_at=invitation.expires_at.strftime('%B %d, %Y at %I:%M %p'),
        invitation_url=invitation_url
    )
