import smtplib
from email.mime.text import MIMEText # allow us to send text in html emails

def email_send(customer,platform,product,ease_of_use,delivery,quality,refer,comments):
    port=2525
    smtp_server='smtp.mailtrap.io'
    login=''
    password=''
    message=f"<h2> New Feedback Submission</h2><br> Voila! a new feedback has been given <br><ul><li>Customer: {customer}</li><li>Platform: {platform}</li><li>Product: {product}</li><li>Ease of Use: {ease_of_use}</li><li>Quality: {quality}</li><li>Delivery: {delivery}</li><li>Refer: {refer}</li><li>Comments: {comments}</li></ul>"

    sender_email=""
    reciever_email=""
    msg=MIMEText(message,'html')
    msg["Subject"]='Online shopping feedback'
    msg['From']=sender_email
    msg['To']=reciever_email

    #send email
    with smtplib.SMTP(smtp_server,port) as server:
        server.login(login,password)
        server.sendmail(sender_email,reciever_email,msg.as_string())