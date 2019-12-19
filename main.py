import argparse
import commands 
import re 

def __help__(): 
   """
   Print list of supported commands 
   """
   print("The following are sample commands that can be execute:"
         +"\n\tGet General Info: get info" 
         +"\n\tGet Info for specific Plug: get info ${plug_number} [Example: get info 1]" 
         +"\n\tSet Plug Name: set plug ${plug_id} to ${new_name} [Example: set plug 1 to New Plug]"  
         +"\n\tTurn On by ID: on ${plug_id} [Example: on 1]"
         +"\n\tTurn On by Name: on ${plug_name} [Example: on Coral Board]" 
         +"\n\tTurn Off by ID: off ${plug_id} [Example: off 1]"
         +"\n\tTurn Off by Name: off ${plug_name} [Example: off Coral Board]" 
   ) 

def main(): 
   """
   The following is intended to be as an interface to easily communicate with the different commands used by Kasa Power Strip
   Currently the Script supports 
      * Getting information regarding the entire strip 
      * Getting information regarding a specific plug 
      * Updating the name of a plug 
      * Turning a specific plug either on/off 
   :positional arguments:
      power_strip_ip       IP addeess of smart power strip
   :optional arguments:
      -h, --help           show this help message and exit
      -cmd CMD, --cmd CMD  command to execute (default: help)
   """
   parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter) 
   parser.add_argument('power_strip_ip', type=str, default='192.168.0.88', help='IP addeess of smart power strip') 
   parser.add_argument('-cmd', '--cmd',  type=str, default='help',         help='command to execute') 
   args = parser.parse_args()
   calls = commands.Commands(args.power_strip_ip)   

   if 'get info' in args.cmd.lower():  
     """"
     Get information regarding the power strip or a specific plug
     :Sample Commands: 
        ubuntu@ori-foglamp:~$ python3 $HOME/Python-KasaSmartPowerStrip/main.py 192.168.0.88 --cmd 'get info' 
        System Info:
           Model: TP-LINK_Power Strip_907C HS300(US)
           Device ID: 8006238CDE704C00681705EF7F7527D41B7E6E5A
           Uptime: 1 day(s) 3 hour(s) 57 minute(s) 26 (seconds)
           Version: 1.0.10
                Build: 190103
                Release: Rel.163517

        ubuntu@ori-foglamp:~$ python3 $HOME/Python-KasaSmartPowerStrip/main.py 192.168.0.88 --cmd 'get info 1' 
        Plug Info:
           ID: 1
           Alias: Coral Board
           State: on
           Up Time: 1 day(s) 3 hour(s) 38 minute(s) 45 (seconds)
     """
     if len(args.cmd.split(' ')) == 3: 
        plug_id = re.split('get info ', args.cmd, flags=re.IGNORECASE)[-1]
        calls.plug_info(plug_id)
     else:
        calls.general_info() 

   elif "set plug name" in args.cmd.lower(): # set plug name 
      """
      Set a plug name 
      :Sample Commands: 
         ubuntu@ori-foglamp:~$ python3 $HOME/Python-KasaSmartPowerStrip/main.py 192.168.0.88 --cmd 'set plug name 3 to Plug 3' 
         Plug 3 was is now named Plug 3
      """
      plug_id = re.split('set plug name ', args.cmd, flags=re.IGNORECASE)[-1].split(' ')[0] 
      plug_name = re.split('to ', args.cmd, flags=re.IGNORECASE)[-1] 
      calls.set_name(int(plug_id), plug_name) 

   elif 'on' in args.cmd.lower(): # Turn on a specific plug 
      """
      Turn on a specific plug either by name or ID 
      :Sample Commands: 
         ubuntu@ori-foglamp:~$ python3 $HOME/Python-KasaSmartPowerStrip/main.py 192.168.0.88 --cmd 'on 2' 
         Plug ID 2 is turned on

         ubuntu@ori-foglamp:~$ python3 $HOME/Python-KasaSmartPowerStrip/main.py 192.168.0.88 --cmd 'on Test' 
         Plug ID Test is turned on
      """
      plug_id = re.split('on ', args.cmd, flags=re.IGNORECASE)[-1]
      try: 
         plug_id = int(plug_id) 
      except Exception as e: 
         pass 
      calls.turn_on(plug_id)  

   elif 'off' in args.cmd.lower(): # Turn off a specific plug 
      """
      Turn ff a specific plgu either by name or ID
      :Sample Commands: 
         ubuntu@ori-foglamp:~$ python3 $HOME/Python-KasaSmartPowerStrip/main.py 192.168.0.88 --cmd 'off 2' 
         Plug ID 2 is turned off

         ubuntu@ori-foglamp:~$ python3 $HOME/Python-KasaSmartPowerStrip/main.py 192.168.0.88 --cmd 'off Test' 
         Plug ID Test is turned off
      """ 
      plug_id = re.split('off ', args.cmd, flags=re.IGNORECASE)[-1]
      try:
         plug_id = int(plug_id)
      except Exception as e:
         pass
      calls.turn_off(plug_id)
   else: 
      __help__()

if __name__ == '__main__':
   main()
