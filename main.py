import email, imaplib, logging, os, re, subprocess, sys
import rfc822py3


logging.basicConfig(
    # filename=os.environ['EMLEXP__LOG_PATH'],
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s',
    datefmt='%d/%b/%Y %H:%M:%S',
    )
log = logging.getLogger(__name__)
log.debug( 'starting log' )


MAIL_DOMAIN = os.environ['EMLEXP__MAIL_DOMAIN']
EMAIL = os.environ['EMLEXP__EMAIL']
PASSWORD = os.environ['EMLEXP__PASSWORD']


## connect
try:
    mailer = imaplib.IMAP4_SSL( MAIL_DOMAIN )
    mailer.login( EMAIL, PASSWORD )
    mailer.select( 'inbox' )   # connect's to inbox by default, but good to specify
    log.debug( 'have mailer' )
except Exception as e:
    log.error( 'exception, ```%s```' % e )
    if mailer:
        log.debug( 'closing mailer and logging out' )
        mailer.close()
        mailer.logout()
    raise Exception( 'whoa: ```%s```' % e )

## search
try:
    ( gms, data ) = mailer.search( b'(UNSEEN FROM "brown.edu" HEADER Subject "test sierra_to_annex")' )
except Exception as e:
    log.error( 'exception, ```%s```' % e )
    if mailer:
        log.debug( 'closing mailer and logging out' )
        mailer.close()
        mailer.logout()

print( 'EOF' )
