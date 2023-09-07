"""update and search the devices in the catalogue
SEARCH:
-search by devicename and print the information about devices with that name
-search by ID and print the information about devices with that ID
-search by service and ....
-search bu measureType and ....
INSERT:
-new device with new parameters
-update old devices changing the parameters (every time the file this is performed the "last_update" field
will be updated to the current date in the format "yyyy-mm-dd hh:mm"
EXIT AND SAVE:
exit and if something was changed save the new version in the same JSON file provided as input

METTERE FUNZIONI RICERCA O NO ? """

import cherrypy
import json
from datetime import date


class Devices():
    exposed = True

    def __init__(self, catalog):
        self.catalog = catalog
        self.catalog_content = json.load(open("catalog.json"))

    def get_devices(self):
        return self.catalog_content['devicesList']

    def get_users(self):
        return self.catalog_content["usersList"]

    def changeDataDevices(self, dict):
        # change name
        if (input("If you want to change deviceName type 'yes'")) == "y":
            newName = input("Insert new name:")
            dict["deviceName"] = newName
        # change measure type
        if (input("If you want to change measureType type 'y'")) == "y":
            newMeasure = input("Insert new measure type:")
            dict["measureType"] = newMeasure
        # change available services
        if (input("If you want to change available services type 'y'")) == "y":
            listavailableServices = []
            listservicesDetails = []
            while True:
                serviceType = input("Insert new service type ('stop' to exit):")
                if serviceType == "stop":
                    dict["availableServices"] = listavailableServices
                    break
                listavailableServices.append(serviceType)
                serviceIP = input("Insert new service IP :")
                dictServices = {
                    "serviceType": serviceType,
                    "serviceIP": serviceIP}
                if "MQTT" in listavailableServices:
                    topics = []
                    topic = input("insert topic ('stop to exit):")
                    while topic != "stop":
                        topics.append(topic)
                if serviceType == "MQTT":
                    dictServices[topic] = topics
                listservicesDetails.append(dictServices)
            dict["availableServices"] = listavailableServices
            dict["servicesDetails"] = listservicesDetails

        # update date
        today = date.today().strftime("%Y/%m/%d")

        oldCatalog = self.catalog_content
        oldCatalog["lastUpdate"] = today
        oldCatalog["devicesList"] = self.get_devices()

        # salvare su catalog.json
        json.dump(oldCatalog, open("catalog.json", "w"))

    def searchByIDDevices(self, id):
        id = int(id)
        devices = self.get_devices()
        found = False
        for dict in devices:
            if dict["deviceID"] == id:
                found = True
                return (dict)
                print(dict)
        if found == False:
            print("There isn't any device with this ID")

    def searchByNameDevices(self, name):
        devices = self.get_devices()
        found = False
        for dict in devices:
            if dict["deviceName"] == name:
                found = True
                return (dict)
                print(dict)
        if found == False:
            print("There isn't any device with this name")

    def searchByMeasureType(self, measure):
        devices = self.get_devices()
        found = False
        result = []
        for dict in devices:
            if measure in dict["measureType"]:
                found = True
                result.append(dict)

        if found == False:
            return ("There isn't any device with the given measure type")
        else:
            return result

    def searchByAvailableServices(self, service):
        devices = self.get_devices()
        found = False
        result = []

        for dict in devices:
            if service in dict["availableServices"]:
                found = True
                result.append(dict)
        if found == False:
            return ("There isn't any device with the given service")
        else:
            return (result)
            print(result)

    def searchByServicesType(self, service):
        devices = self.get_devices()
        found = False
        for dict in devices:
            list_services = dict["servicesDetails"]
            for service in list_services:
                if list_services["serviceType"] == service:
                    found = True
                    return (dict)

        if found == False:
            print("There isn't any device with the given service")

    def InsertNewDevice(self, device):
        devices = self.get_devices()
        found = False
        deviceDict = json.loads(device)
        id = deviceDict["deviceID"]
        for index, dict in enumerate(devices):
            if dict["deviceID"] == int(id):
                devices[index] = deviceDict  # sostituisco il vecchio device col nuovo
                found = True
        if found == False:
            devices.append(deviceDict)

        # change update date
        today = date.today().strftime("%Y/%m/%d")

        oldCatalog = self.file_content
        oldCatalog["lastUpdate"] = today
        oldCatalog["devicesList"] = devices

        # salvare su catalog.json
        json.dump(oldCatalog, open("catalog.json", "w"))

        return oldCatalog

    def printAllDevices(self):
        devices = self.get_devices()
        return (devices)
        print(devices)

    # USERS


class Users():
    def getUsers(self):
        return self.catalog_content["usersList"]

    def changeDataUsers(self, dict):
        # change name
        if (input("If you want to change userName type 'yes'")) == "y":
            newName = input("Insert new name:")
            dict["userName"] = newName
        # change surname
        if (input("If you want to change userSurname type 'y'")) == "y":
            newSurname = input("Insert new user Surname:")
            dict["userSurname"] = newSurname
        # change TELEGRAM INFO ?
        if (input("If you want to change TELEGRAM INFO type 'y'")) == "y":
            pass

        # update date
        today = date.today().strftime("%Y/%m/%d")

        oldCatalog = self.catalog_content
        oldCatalog["lastUpdate"] = today
        oldCatalog["usersList"] = self.get_devices()

        # save on catalog.json
        json.dump(oldCatalog, open("catalog.json", "w"))

    def searchByIDDevices(self, id):
        id = int(id)
        users = self.getUsers()
        found = False
        for dict in users:
            if dict["userID"] == id:
                found = True
                return (dict)
                print(dict)
        if found == False:
            print("There isn't any user with this ID")

    def searchByNameUsers(self, name):
        users = self.getUsers()
        found = False
        for dict in users:
            if dict["userName"] == name:
                found = True
                return (dict)
                print(dict)
        if found == False:
            print("There isn't any user with this name")

    def searchBySurnameUsers(self, surname):
        users = self.getUsers()
        found = False
        for dict in users:
            if dict["userSurname"] == surname:
                found = True
                return (dict)
                print(dict)
        if found == False:
            print("There isn't any user with this surname")

    def searchByTelegramUsers(self, token):
        pass

    def InsertNewUser(self, user):
        users = self.getUsers()
        found = False
        userDict = json.loads(user)
        id = userDict["userID"]
        for index, dict in enumerate(users):
            if dict["userID"] == int(id):
                users[index] = userDict
                found = True
        if found == False:
            users.append(userDict)

        #  update date
        today = date.today().strftime("%Y/%m/%d")

        oldCatalog = self.file_content
        oldCatalog["lastUpdate"] = today
        oldCatalog["usersList"] = users

        # salvare su catalog.json
        json.dump(oldCatalog, open("catalog.json", "w"))

        return oldCatalog

    def printAllUsers(self):
        users = self.getUsers()
        return (users)
        print(users)

    @cherrypy.tools.json_out()
    def GET(self, *uri, **params):
        # as uri command
        # as parameters what we want to search

        command1 = ["devices", "users"]
        command2 = []
        if len(uri)

        commands = ["searchName", "searchID", "searchService", "SearchMeasure", "PrintAll", "insertDevice"]

        if len(uri) != 0:
            if uri[0] in commands and uri[0] != "PrintAll":
                par1 = params['op1']
                if uri[0] == "searchName":
                    res = self.searchByName(par1)
                elif uri[0] == "searchID":
                    res = self.searchByID(par1)
                elif uri[0] == "searchService":
                    res = self.searchByService(par1)
                elif uri[0] == "SearchMeasure":
                    res = self.searchByMeasureType(par1)
                elif uri[0] == "insertDevice":
                    res = self.insertDevice(par1)

                return res

            elif uri[0] == "PrintAll":
                res = self.printAll()

                return res

            elif uri[0] == "insertDevice":
                id = params['op1']
                res = self.insertDevice(id)
                return res

            else:
                raise cherrypy.HTTPError(400, 'Insert a proper command as URI')
        else:
            raise cherrypy.HTTPError(400, 'No URI given, you need to provide a command as a URI')

    # TODO PUT funzione riceve il nuovo diz da aggiungere, se esiste nella lista dei devices lo sostituisce, altrimenti lo aggiunge alla lista
    @cherrypy.tools.json_out()
    def PUT(self, *uri, **params):

        new_device = cherrypy.request.body.read()
        newCatalog = self.NuovaFunzionePerInserireNuovoDevice(json.dumps(json.loads(new_device)))

        return newCatalog


if __name__ == '__main__':
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True
        }
    }
    cherrypy.tree.mount(Devices('catalog.json'), '/', conf)
    # this is needed if you want to have the custom error page
    # cherrypy.config.update({'error_page.400': error_page_400})
    cherrypy.engine.start()
    cherrypy.engine.block()