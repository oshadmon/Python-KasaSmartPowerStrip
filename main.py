"""
The following are sample commands how to call different Smart Plug Functions using the main

# Get General information
ubuntu@ori-foglamp:~/$ python3 $HOME/Python-KasaSmartPowerStrip/main.py 192.168.0.88 --cmd 'get info' 
System Info:
        Model: TP-LINK_Power Strip_907C HS300(US)
        Device ID: 8006238CDE704C00681705EF7F7527D41B7E6E5A
        Uptime: 1 day(s) 2 hour(s) 32 minute(s) 35 (seconds)
        Version: 1.0.10
                Build: 190103
                Release: Rel.163517

# General Information for a specific plug 
ubuntu@ori-foglamp:~/$ python3 $HOME/Python-KasaSmartPowerStrip/main.py 192.168.0.88 --cmd 'get info 3' 
Plug Info:
        ID: 3
        Alias: Plug 3
        State: off
        Up Time: 0 day(s) 0 hour(s) 00 minute(s) 00 (seconds)
"""
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
   parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter) 
   parser.add_argument('power_strip_ip', type=str, default='192.168.0.88', help='IP addeess of smart power strip') 
   parser.add_argument('-cmd', '--cmd',  type=str, default='help',         help='command to execute') 
   args = parser.parse_args()
   calls = commands.Commands(args.power_strip_ip)   
   if 'get info' in args.cmd.lower(): 
     if len(args.cmd.split(' ')) == 3: 
        plug_id = re.split('get info ', args.cmd, flags=re.IGNORECASE)[-1]
        calls.plug_info(plug_id)
     else:
        calls.general_info() 
   elif "set plug name" in args.cmd.lower():
      plug_id = re.split('set plug name ', args.cmd, flags=re.IGNORECASE)[-1].split(' ')[0] 
      plug_name = re.split('to ', args.cmd, flags=re.IGNORECASE)[-1] 
      calls.set_name(int(plug_id), plug_name) 

   elif 'on' in args.cmd.lower(): 
      plug_id = re.split('on ', args.cmd, flags=re.IGNORECASE)[-1]
      try: 
         plug_id = int(plug_id) 
      except Exception as e: 
         pass 
      calls.turn_on(plug_id)  
   elif 'off' in args.cmd.lower():
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
