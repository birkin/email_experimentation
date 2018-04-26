import email, imaplib, logging, os, re, subprocess, sys
import rfc822py3


logging.basicConfig(
    filename=os.environ['EMLEXP__LOG_PATH'],
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s',
    datefmt='%d/%b/%Y %H:%M:%S',
    )
log = logging.getLogger(__name__)
log.debug( 'starting log' )


MAIL_DOMAIN = os.environ['EMLEXP__MAIL_DOMAIN']


print( 'hello world' )
