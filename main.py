import email, imaplib, logging, os, pprint, re, subprocess, sys, urllib


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
    ( ok_response, id_list ) = mailer.search( 'utf-8', b'Subject', b'"test sierra_to_annex"' )  # response, eg, ```('OK', [b'2 3'])```
except Exception as e:
    log.error( 'exception, ```%s```' % e )
    if mailer:
        log.debug( 'closing mailer and logging out' )
        mailer.close()
        mailer.logout()

## process
try:
    recent_id = id_list[0].split()[-1]  # str; & id_list is really a list of a single space-delimited string
    ( ok_response, rfc822_obj_list ) = mailer.fetch( recent_id, '(RFC822)' )
    email_rfc822_tuple = rfc822_obj_list[0]
    email_rfc822_bytestring = email_rfc822_tuple[1]  # tuple[0] example, ```b'3 (RFC822 {5049}'```
    email_obj = email.message_from_string( email_rfc822_bytestring.decode('utf-8') )  # email is a standard python import
    log.debug( 'is_multipart(), `%s`' % email_obj.is_multipart() )
    items_list_of_tuples = email_obj.items()  # eg, [ ('Subject', 'the subject text'), () ] -- BUT does NOT provide body-content
    log.debug( 'items_list_of_tuples, ```%s```' % pprint.pformat(items_list_of_tuples) )
    body_message = email_obj.get_payload( decode=True )  # body-content in bytes
    log.debug( 'type(body_message), `%s`' % type(body_message) )
    log.debug( 'body_message, ```%s```' % body_message )
    final = body_message.decode( 'utf-8' )
    # final = urllib.parse.unquote( tmp )
    log.debug( 'final, ```%s```' % final )
except Exception as e:
    log.error( 'exception, ```%s```' % e )
finally:
    if mailer:
        log.debug( 'closing mailer and logging out' )
        mailer.close()
        mailer.logout()

# try:
#     recent_id = id_list[0].split()[-1]  # str; & id_list is really a list of a single space-delimited string
#     ( ok_response, rfc822_obj_list ) = mailer.fetch( recent_id, '(RFC822)' )
#     email_rfc822_tuple = rfc822_obj_list[0]
#     email_rfc822_bytestring = email_rfc822_tuple[1]  # tuple[0] example, ```b'3 (RFC822 {5049}'```
#     email_obj = email.message_from_string( email_rfc822_bytestring.decode('utf-8') )  # email is a standard python import
#     log.debug( 'is_multipart(), `%s`' % email_obj.is_multipart() )
#     items_list_of_tuples = email_obj.items()  # eg, [ ('Subject', 'the subject text'), () ] -- BUT does NOT provide body-content
#     log.debug( 'items_list_of_tuples, ```%s```' % pprint.pformat(items_list_of_tuples) )
#     body_message = email_obj.get_payload()  # body-content in unicode
#     log.debug( 'type(body_message), `%s`' % type(body_message) )
#     log.debug( 'body_message, ```%s```' % body_message )
#     tmp = body_message.replace( '\r', '' )
#     tmp = tmp.replace( '=\n', '' )
#     tmp = tmp.replace( '=', '%' )
#     final = urllib.parse.unquote( tmp )
#     log.debug( 'final, ```%s```' % final )
# except Exception as e:
#     log.error( 'exception, ```%s```' % e )
# finally:
#     if mailer:
#         log.debug( 'closing mailer and logging out' )
#         mailer.close()
#         mailer.logout()

print( 'EOF' )
