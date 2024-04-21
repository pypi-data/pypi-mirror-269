from . import errors, apiurl_lists, Request_HSSAPI
import datetime



BASEURL = "https://hss-dev.aknet.tech/v1"

class User:
    """
    User Class

     This class is used to obtain information about users.

     attribute:
     token: Enter the HSS User token.
    
    """
    def __init__(self, token) -> None:
        """
        Constructor

        Parameters:
            token: HSS User token
        """
        self.token = token

    def get_data(self, url:str) -> dict:
        """
        Retrieves data from the specified URL using a token.

        Args:
            url (str): The URL to retrieve data from.

        Returns:
            dict: The JSON response from the URL.

        """
        response = Request_HSSAPI.get_with_token(url, self.token)
        if errors.ErrorPrint.handle_http_error(response):
            return None
        return response.json()

    def get_permission(self) -> list:
        """
        Retrieves the permission data for the user.

        Returns:
            A list of schools for which the user has permission.
            If the user has no permission for any school, returns None.
        """
        url = apiurl_lists.make_url(2)
        UserData = self.get_data(url)
        if UserData['body']['schools'] == []:
            return None
        return UserData['body']['schools']

    def get_permission_discordUserID(self, discordUserID:int) -> list:
        """
        Retrieves the permission data for the user.
        Args:
            discordUserID (int): _description_

        Returns:
            list: _description_
        """
        url = apiurl_lists.make_url(2)+f"/{discordUserID}"
        UserData = self.get_data(url)
        return UserData['body']['permissions']['registeredSchools']

    
    def get_id(self, id:int) -> int:
        """
        Retrieves the data associated with the given ID.

        Args:
            id (int): The ID to retrieve data for.

        Returns:
            int: The data associated with the given ID, or None if no data is found.

        """
        url = apiurl_lists.make_url(1, id)
        UserData = self.get_data(url)
        if UserData['body']['data'] == None:
            return None
        return UserData['body']['data']

    def get_me(self) -> dict:
        """
        Retrieves the user data for the authenticated user.

        Returns:
            dict: A dictionary containing the user data.
        """
        url = apiurl_lists.make_url(1,"@me")
        UserData = self.get_data(url)
        return UserData['body']['data']

class NewSchool:
    def __init__(self, token, schoolid: int) -> None:
        self.token = token
        self.schoolid = schoolid
    
    def get_data(self) -> dict:
        """
        Retrieves the school data.
        
        Returns:
            dict: The school data.
        """
        url = apiurl_lists.make_url(0,self.schoolid)
        response = Request_HSSAPI.get_with_token(url, self.token)
        if errors.ErrorPrint.handle_http_error(response):
            return None
        UserData = response.json()
        return UserData['body']['data']
        
        
    def get_classes(self) -> list:
        """
        Retrieves the classes for the school.
        
        Returns:
            list: The classes for the school.        
        """
        url = apiurl_lists.make_url(0,self.schoolid)+"/class"
        response = Request_HSSAPI.get_with_token(url, self.token)
        if errors.ErrorPrint.handle_http_error(response):
            return None
        UserData = response.json()
        classes: list = UserData['body']['classes']
        return classes
        
    def search_class(self, grade, classname) -> int:
        """
        Searches for the specified class.
        
        Args:
            grade (int): The grade of the class to search for.
            classname (int): The class number to search for.
        
        Returns:
            int: The index of the specified class, or None if the class is not found.
        """
        UserData = self.get_data()
        if UserData['userDatas'] == []:
            return None
        for number in range(len(UserData['userDatas'])):
            if UserData['userDatas'][number]['grade'] == grade and UserData['userDatas'][number]['class'] == classname:
                return number
        else:
            return None
            
    def grade(self, number:int) -> int:
        """
        Retrieves the grade for the specified number.

        Args:
            number (int): The number to retrieve the grade for.

        Returns:
            int: The grade for the specified number, or None if no grade is found.
        """
        UserData = self.get_data()
        if UserData['userDatas'] == []:
            return None
        UserData = UserData['userDatas'][number]
        if UserData['grade'] == None:
            return None
        return UserData['grade']
        
    
    def classname(self,number:int) -> str:
        """
        Retrieves the class name for the specified number.

        Args:
            number (int): The number to retrieve the class name for.

        Returns:
            str: The class name for the specified number, or None if no class name is found.
        """
        UserData = self.get_data()
        if UserData['userDatas'] == []:
            return None
        UserData = UserData['userDatas'][number]
        if UserData['class'] == None:
            return None
        return UserData['class']
        
    
    def get_timeline(self,number:int,name:str) -> list[dict]:
        """
        Retrieves the timeline data for the specified number.
        
        Args:
            number (int): The number to retrieve the timeline data for.
            name (str): The name of the timeline data to retrieve.
        """
        UserData = self.get_data()
        if UserData['userDatas'] == []:
            return None
        if UserData['userDatas'][number]['timelineData'] == None:
            return None
        UserData = UserData['userDatas'][number]
        return UserData['timelineData'][name]
        
    def get_default_timeline(self,number:int,name:str) -> list[dict]:
        """
        Retrieves the default timeline data for the specified number.

        Args:
            number (int): The number to retrieve the default timeline data for.
            name (str): The name of the default timeline data to retrieve.
            
        Returns:
            list: The default timeline data for the specified number.
        """
        UserData = self.get_data()
        if UserData['userDatas'] == []:
            return None
        UserData = UserData['userDatas'][number]
        return UserData['defaultTimelineData'][name]
        
    
    def get_homework(self,number) -> list[dict]:
        """"
        Retrieves the homework data for the specified number.
        
        Args:
            number (int): The number to retrieve the homework data for.
        """
        UserData = self.get_data()
        if UserData['userDatas'] == []:
            return None
        UserData = UserData['userDatas'][number]
        return UserData['homework']


    def get_event(self,number:int,name:str) -> list[dict]:
        """
        Retrieves the event data for the specified number.

        Args:
            number (int): The number to retrieve the event data for.
            name (str): The name of the event data to retrieve.

        Returns:
            list: The event data for the specified number.
        """
        UserData = self.get_data()
        if UserData['userDatas'] == []:
            return None
        UserData = UserData['userDatas'][number]
        return UserData['eventData'][name]
        
    def default_timelineindex(self,number:int) -> int:
        UserData = self.get_data()
        if UserData['userDatas'] == []:
            return None
        UserData = UserData['userDatas'][number]
        return UserData['defaultTimelineIndex']
    
    def patch_timeline(self, grade:int, _class:int, date:str, name:str, isEvent:bool,state:str = "add", index:int=None, place:str=None) -> None:
        """ 
        Retrieves the timeline data.
        Args:
            grade (int): The number to retrieve the timeline data for.
            _class (int): The class number of the timeline data to retrieve.
            date (str): The date of the timeline data to retrieve.
            name (str): The name of the timeline data to retrieve.
            isEvent (bool): The event boolean value of the timeline data to retrieve.
            state (str): add, update, delete
            index (int): update, delete only
            place (str): default None
        """
        url = BASEURL+f"/school/{self.schoolid}/userdatas/{grade}/{_class}/{date}"
        _data = {
            "key":"timelineData",
            "value":{
                "name":name,
                "place":place,
                "IsEvent":isEvent
            },
            "state": state
        }
        if index is not None and state != "add":
            _data["index"] = index
            if state == "add":
                raise TypeError('Cannnot index with state "add"')
        res = Request_HSSAPI.patch_with_token(url, self.token, _data)
        errors.ErrorPrint.handle_http_error(res)

    def update_timelineindex(self, grade:int, _class:int, date:str, index:int) -> None:
        """
        Retrieves the homework data for the specified number.

        Args:
            grade (int): The number to retrieve the homework data for.
            _class (int): The class number of the homework data to retrieve.
            date (str): The date of the homework data to retrieve.
            index (int): The index of the homework data to retrieve.
        
        Returns:
            list: The homework data for the specified number.
        """
        url = BASEURL+f"/school/{self.schoolid}/userdatas/{grade}/{_class}/{date}"
        _data = {
            "key":"defaultTimelineIndex",
            "value" : index,
            "state": "update"
        }
        res = Request_HSSAPI.patch_with_token(url, self.token, _data)
        errors.ErrorPrint.handle_http_error(res)

    def patch_defaulttimeline(self, grade:int, _class:int, date:str, name:str, isEvent:bool = False,state:str ="add",index:int=None, place:str="なし") -> None:
        """
        Retrieves the default timeline data for the specified number.

        Args:
            grade (int): The number to retrieve the default timeline data for.
            _class (int): The class number of the default timeline data to retrieve.
            date (str): The date of the default timeline data to retrieve.
            name (str): The name of the default timeline data to retrieve.
            isEvent (bool): The event boolean value of the default timeline data to retrieve.
            state (str): add, update, delete
            index (int): update, delete only
            place (str): default なし
        
        Returns:
            list: The default timeline data for the specified number.
        """
        url = BASEURL+f"/school/{self.schoolid}/userdatas/{grade}/{_class}/{date}"
        _data = {
            "key":"defaultTimelineData",
            "value":{
                "name":name,
                "place":place,
                "IsEvent":isEvent
            },
            "state": state
        }
        if index is not None and state != "add":
            _data["index"] = index
            if state == "add":
                raise TypeError('Cannnot index with state "add"')
        res = Request_HSSAPI.patch_with_token(url, self.token, _data)
        errors.ErrorPrint.handle_http_error(res)
    
    def patch_event(self, grade:int, _class:int, date:str, name:str, isEndofDay:bool, start:datetime, end:datetime, place:str=None , state :str = "add" , index : int = None) -> None:
        """
        Retrieves the event data for the specified number.
        
        Args:
            grade (int): The number to retrieve the event data for.
            _class (int): The class number of the event data to retrieve.
            date (str): The date of the event data to retrieve.
            name (str): The name of the event data to retrieve.
            isEndofDay (bool): The end of day boolean value of the event data to retrieve.
            start (datetime): The start time of the event data to retrieve.
            end (datetime): The end time of the event data to retrieve.
            place (str): The place of the event data to retrieve.
            state (str): The state of the event data to retrieve.
            index (int): The index of the event data to retrieve.

        Returns:
            list: The event data for the specified number.
        """
        
        url = BASEURL+f"/school/{self.schoolid}/userdatas/{grade}/{_class}/{date}"
        _data = {
            "key":"eventData",
            "value":{
                "name":name,
                "timeData":{
                    # 2024-03-31T00:00Z...
                    "start": start,
                    "end": end,
                    "isEndofDay":isEndofDay
                        },
                "place":place
                },
            "state": state
        }
        if index is not None and state != "add":
            _data["index"] = index
            if state == "add":
                raise TypeError('Cannnot index with state "add"')
        res = Request_HSSAPI.patch_with_token(url, self.token, _data)
        errors.ErrorPrint.handle_http_error(res)

    def patch_homework(self, grade:int, _class:int, date:str, name:str, start, end, istooBig:bool = False, comment:str=None, state :str = "add" , index : int = None) -> None:
        """
        Retrieves the homework data for the specified number.

        Args:
            grade (int): The number to retrieve the homework data for.
            _class (int): The class number of the homework data to retrieve.
            date (str): The date of the homework data to retrieve.
            name (str): The name of the homework data to retrieve.
            start (datetime): The start time of the homework data to retrieve.
            end (datetime): The end time of the homework data to retrieve.
            istooBig (bool): The too big boolean value of the homework data to retrieve.
            comment (str): The comment of the homework data to retrieve.
            state (str): The state of the homework data to retrieve.
            index (int): The index of the homework data to retrieve.

        Returns:
            list: The homework data for the specified number.
        """
        url = BASEURL+f"/school/{self.schoolid}/userdatas/{grade}/{_class}/{date}"
        _data = {
            "key":"homework",
            "value":{
                "name":name,    
                "istooBig":istooBig,
                "page":{
                    "start":start,
                    "end":end,
                    "comment":comment}
                },
            "state": state
        }
        if index is not None and state != "add":
            _data["index"] = index
            if state == "add":
                raise TypeError('Cannnot index with state "add"')
        res = Request_HSSAPI.patch_with_token(url, self.token, _data)
        errors.ErrorPrint.handle_http_error(res)