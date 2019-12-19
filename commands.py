from KasaSmartPowerStrip import SmartPowerStrip

class Commands:
   def __init__(self, access_ip:str): 
      """
      Commands to be used for smart power strip (HS300) 
      :args: 
         access_ip:str - IP of smart 
      :param: 
         self.power_strip:KasaSmartPowerStrip.SmartPowerStrip - SmartPowerStrip class decleration call 
      """ 
      self.power_strip = SmartPowerStrip('%s' % access_ip)

   def __convert_seconds(self, seconds:int)->str:
      """
      Convert seconds to datetime format (X days X hours X minutes X seconds) 
      :args: 
         seconds:int - length of time (in seconds plug has been up) 
      :return: 
         datetime from seconds
      """
      minute, second = divmod(seconds, 60) 
      hour, minute = divmod(minute, 60) 
      day, hour = divmod(hour, 24) 
      
      return "%d day(s) %d hour(s) %02d minute(s) %02d (seconds)" % (day, hour, minute, second)

   def general_info(self): 
      """
      Get general information regarding smart powerstrip 
      :info: 
         info:dict - data regarding power strip
         output:str - string to print to string with relevent iformatioon
      :sample output: 
         System Info:
            Model: TP-LINK_Power Strip_907C HS300(US)
            Device ID: 8006238CDE704C00681705EF7F7527D41B7E6E5A
            Uptime: 1 day(s) 1 hour(s) 47 minute(s) 10 (seconds)
            Version: 1.0.10
                Build: 190103
                Release: Rel.163517       
      """
      info = self.power_strip.get_system_info()['system']['get_sysinfo']
      output = 'System Info:\n\tModel: %s %s\n\tDevice ID: %s\n\tUptime: %s\n\tVersion: %s\n\t\t%s: %s\n\t\tRelease: %s'
      uptime = 0 
      for plug in range(1,7): 
         uptime += self.power_strip.get_plug_info(plug)[0]['on_time']

      print(output % (info['alias'], info['model'], info['deviceId'], self.__convert_seconds(uptime), info['sw_ver'].split(" ")[0], 
                      info['sw_ver'].split(" ")[1], info['sw_ver'].split(" ")[2], info['sw_ver'].split(" ")[3]))

   def plug_info(self, plug_id:int): 
      """
      Get info regarding a specific plug (1-6)
      :args: 
         plug_id:int - plug to get information of 
      """
      plug_info = self.power_strip.get_plug_info(plug_id)[0] 
      if plug_info['state'] == 0: 
         plug_info['state'] = 'off'
      else: 
         plug_info['state'] = 'on'

      output = 'Plug Info:\n\tID: %s\n\tAlias: %s\n\tState: %s\n\tUp Time: %s'
      print(output % (plug_id, plug_info['alias'], plug_info['state'], self.__convert_seconds(plug_info['on_time'])))
  
   def turn_on(self, plug_id): 
      """
      Turn on plug based on either ID number of name
      :args: 
         plug_id - either name or ID of plug to turn on
      """
      if isinstance(plug_id, int) and plug_id in range(1,7):
         try: 
            self.power_strip.toggle_plug('on', plug_num=plug_id)
         except ValueError or TypeError: 
            print('Invalid Plug Number.')
            return 
      else: 
         try: 
            self.power_strip.toggle_plug('on', plug_name=plug_id)
         except ValueError or TypeError: 
            print('Unable to find plug with name %s' % plug_id) 
            return 
      print("Plug ID %s is turned on" % plug_id) 

   def turn_off(self, plug_id):
      """
      Turn off plug based on either ID number of name
      :args: 
         plug_id - either name or ID of plug to turn on
      """
      if isinstance(plug_id, int) and plug_id in range(1,7):
         try:
            self.power_strip.toggle_plug('off', plug_num=plug_id)
         except ValueError or TypeError:
            print('Invalid Plug Number.')
            return
      else:
         try:
            self.power_strip.toggle_plug('off', plug_name=plug_id)
         except ValueError or TypeError:
            print('Unable to find plug with name %s' % plug_id)
            return
      print("Plug ID %s is turned off" % plug_id)


