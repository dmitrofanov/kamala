import snowflake.connector


def connect():
    # Opens a connection
    ctx = snowflake.connector.connect(
        user='dmitry.mitrofanov',
        password='o22Dm1trof@nova',
        account='ringcentral',
        authenticator='https://ringcentral.okta.com',
        warehouse='RCUSERS_WH',
        database='RCUSERS',
        schema='DMITRYMITROFANOV',
    )
    return ctx
