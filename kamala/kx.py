import requests
import json

#class APIs:
 #   self.API_VISIT = "https://klientiks.ru/clientix/Restapi/list/a/390b96e2763e/u/d969c9cde78c/t/073de5009f21b34afa022cfa7ca2c124/m/AppointmentClientLinks/ik/orders/rvwk/status,statuses/?date=10&offset="
API_VISIT = "https://klientiks.ru/clientix/Restapi/list/a/390b96e2763e/u/d969c9cde78c/t/073de5009f21b34afa022cfa7ca2c124/m/AppointmentClientLinks/ik/orders/rvwk/status,statuses/?date=10&offset="
TABLE_VISIT = 'KAMALA_APPOINTMENTS'
# TABLE_APPOINTMENTS = 'KAMALA_APPOINTMENTS'

API_VISIT2 = "https://klientiks.ru/clientix/Restapi/roistatExportAcl/a/390b96e2763e/u/d969c9cde78c/t/073de5009f21b34afa022cfa7ca2c124/ik/orders/rvwk/status,statuses/?date=1521871200&offset="
# TABLE_APPOINTMENTS2 = 'KAMALA_APPOINTMENTS2'

API_CLIENT = "https://klientiks.ru/clientix/Restapi/list/a/390b96e2763e/u/d969c9cde78c/t/073de5009f21b34afa022cfa7ca2c124/m/clients/date/"
TABLE_CLIENTS = "KAMALA_CLIENT"

API_VISIT_DETAIL = "https://klientiks.ru/clientix/Restapi/getAppointment/a/390b96e2763e/u/d969c9cde78c/t/073de5009f21b34afa022cfa7ca2c124/id/"
# TABLE_APPOINTMENT_DETAILED = "KAMALA_APPOINTMENT_DETAILED"

API_ORDER_DETAIL = "https://klientiks.ru/clientix/Restapi/getAppointment/a/390b96e2763e/u/d969c9cde78c/t/073de5009f21b34afa022cfa7ca2c124/id/"
TABLE_ORDER_DETAIL = "KAMALA_ORDER_DETAIL"


def get_data_chunk(api_endpoint, offset="0"):
    r = requests.get(url=(api_endpoint + str(offset)))
    r.encoding = 'utf-8'
    response = json.loads(r.text)
    return response




# Получить список визитов и продаж
# API_ENDPOINT = "https://klientiks.ru/clientix/Restapi/list/a/390b96e2763e/u/d969c9cde78c/t/073de5009f21b34afa022cfa7ca2c124/m/AppointmentClientLinks/ik/orders/rvwk/status,statuses/?date=100&offset=19700"

# Получить список визитов клиента
# API_ENDPOINT = "https://klientiks.ru/clientix/Restapi/getACL/a/390b96e2763e/u/d969c9cde78c/t/073de5009f21b34afa022cfa7ca2c124/clientId/3239600"

# Получить список визитов 2.0
# API_ENDPOINT = "https://klientiks.ru/clientix/Restapi/roistatExportAcl/a/390b96e2763e/u/d969c9cde78c/t/073de5009f21b34afa022cfa7ca2c124/ik/orders/rvwk/status,statuses/?date=1521871200&offset=19700"

# получить информацию о визите по ID

#API_ENDPOINT = "https://klientiks.ru/clientix/Restapi/getAppointment/a/390b96e2763e/u/d969c9cde78c/t/073de5009f21b34afa022cfa7ca2c124/id/5833264"

# Получить список клиентов (по дате?)
# API_ENDPOINT = "https://klientiks.ru/clientix/Restapi/list/a/390b96e2763e/u/d969c9cde78c/t/073de5009f21b34afa022cfa7ca2c124/m/clients/date/2020-03-08"

# Получить клиента по телефону
# API_ENDPOINT = "https://klientiks.ru/clientix/Restapi/list/a/390b96e2763e/u/d969c9cde78c/t/073de5009f21b34afa022cfa7ca2c124/m/getClientByPhone/phone/79313781533"

# Получить список услуг и товаров
# API_ENDPOINT = "https://klientiks.ru/clientix/Restapi/list/a/390b96e2763e/u/d969c9cde78c/t/073de5009f21b34afa022cfa7ca2c124/m/Services/"

# Получить список сотрудников
# API_ENDPOINT = "https://klientiks.ru/clientix/Restapi/list/a/390b96e2763e/u/d969c9cde78c/t/073de5009f21b34afa022cfa7ca2c124/m/Users/&offset=-10"

# получить список оплат за дату
#API_ENDPOINT = "https://klientiks.ru/clientix/Restapi/list/a/390b96e2763e/u/d969c9cde78c/t/073de5009f21b34afa022cfa7ca2c124/m/getRevenueTransactions/from/2020-01-01"

# получить список абонементов
# API_ENDPOINT = "https://klientiks.ru/clientix/Restapi/list/a/390b96e2763e/u/d969c9cde78c/t/073de5009f21b34afa022cfa7ca2c124/m/ServicePacks/"

#API_APPOINTMENTS = "https://klientiks.ru/clientix/Restapi/list/a/390b96e2763e/u/d969c9cde78c/t/073de5009f21b34afa022cfa7ca2c124/m/AppointmentClientLinks/ik/orders/rvwk/status,statuses/?date=10&offset="
#TABLE_APPOINTMENTS = 'KAMALA_APPOINTMENTS'

#API_APPOINTMENTS2 = "https://klientiks.ru/clientix/Restapi/roistatExportAcl/a/390b96e2763e/u/d969c9cde78c/t/073de5009f21b34afa022cfa7ca2c124/ik/orders/rvwk/status,statuses/?date=1521871200&offset="
#TABLE_APPOINTMENTS2 = 'KAMALA_APPOINTMENTS2'

#API_CLIENTS = "https://klientiks.ru/clientix/Restapi/list/a/390b96e2763e/u/d969c9cde78c/t/073de5009f21b34afa022cfa7ca2c124/m/clients/date/"
#TABLE_CLIENTS = "KAMALA_CLIENTS"

#API_APPOINTMENT_DETAILED = "https://klientiks.ru/clientix/Restapi/getAppointment/a/390b96e2763e/u/d969c9cde78c/t/073de5009f21b34afa022cfa7ca2c124/id/"
#TABLE_APPOINTMENT_DETAILED = "KAMALA_APPOINTMENT_DETAILED"

