'''
Below code for communcication from Secondary to Primary

'''
import json
import logging
import os
import re
import socket
import time
from datetime import datetime
import serial
import serial.tools.list_ports as serial_ports


#>>>>>>>>>>>>>>>>   Connection Handlers


def User_Input_Handler():

    global  DUT_Ser, Communication_Service, Bandwidth_Range, Test_type, Secondary_Script_log_filename
    global Received_SSID_PWD, DUT_Type, Distance, __2_4Ghz__,Current_time,Duration

 #------------------------------------------------------------------------------------------------------------------------------------
 #                                          | Serial COM Port Selecton |
 #                                          |__________________________|      
 #  Create a socket object   
    Communication_Service = socket.socket()
    port_no=666   
    __2_4Ghz__=True                 
    # Check  all available ports
    ports = serial_ports.comports()

    # Crating Script logs folder
    if not os.path.exists("Logs"):
        os.makedirs("Logs")
    
    Current_time=datetime

    

   

    try:
        print("\n\tSelect Proper COM Ports ")
        
        if ports == []:
            
            # Return if there is No Com Port available
            print("\n\tNo COM Ports available !!!!\n")
            return
        
             #List All available ports
        for port in sorted(ports):
                #  Available_ports = str(port).split("-")
            print(f'\n{port}')

        Com_Port = str(input("\n>> "))

        # configure port number and Baudrate 
        DUT_Ser = serial.Serial(Com_Port,baudrate=115200,timeout=1) 
    except:
        print("\nError in Opening COM Port..!!!\n \t Please Check for Port Availability and Make Sure you Selected Proper Com Port...!!!\n\n")
        return False



 #------------------------------------------------------------------------------------------------------------------------------------
 #                                          | Select Device Type |
 #                                          |____________________|  

    while True:

        try:            

            DUT_Type =str(input("\nPlease Enter the Device / Module Name \n\t i>    LS10 \n\t ii>   LS11 \n>>  " ))      
            
            DUT_Type = DUT_Type.strip().upper()

            if DUT_Type =="0" or  DUT_Type == "" :
                
                print('\n',6*' ',"Device Name should not be empty or Zero !",'\n')  

            elif len(DUT_Type) >=6 or len(DUT_Type) <3:
                
                 print('\n',6*' ',"please select proper Device !",'\n')   
    
            else :

                print(f"User enterd device name :{DUT_Type}")
                break
               
        except:
             pass
        
 #------------------------------------------------------------------------------------------------------------------------------------
 #                                          | Enter the Test Duration |
 #                                          |_________________________|  

    while True:
            
        try :
                Duration = int(input("\nPlease Enter the Test Duration in Seconds   :-  " ))      
                if Duration < 10.0:
                    print("\n\tDuration time should be more than 10 sec")
                    pass
                elif Duration >= 10.0:
                    break
        except:
                pass      


 #------------------------------------------------------------------------------------------------------------------------------------
 #                                          | Enter the Distance |
 #                                          |____________________|  

    while True:

        try:            

            Distance = float(input("\nPlease Enter the Distance in Mtrs   :-  " ))      
            if Distance >= 1.0:
                  break
   
        except:
             pass    

 #------------------------------------------------------------------------------------------------------------------------------------------
 #                                            | Bandwidth Range Selection |
 #                                            |___________________________| 
    Input_Verification = [1,2,3]

    while True:

        try:
            print("\n\t Select the Bandwidth Range \n\n\t ")
            Bandwidth_Range = int(input(" 1. Basic Test\t\t5M - 25M \n\n 2. Moderate Test\t10M - 50M\n\n 3. Extreme Test\t20M - 100M\n\n>> "))
            if Bandwidth_Range in Input_Verification:
                print("\nUser input is  ",Bandwidth_Range)
                break
        except:
            print("\nInvalid Input, Please Enter 1,2 or 3 as a Input")


 #------------------------------------------------------------------------------------------------------------------------------------------
 #                                            | Test Type  Selection |
 #                                            |______________________| 
    while True:

        try:
            print("\n\t Select the Test Type \n\n\t ")
            Test_type = int(input(" 1. TX Test\n\n 2. RX Test\n\n 3. Full ( TX - RX ) Test\n\n>> "))
            if Test_type in Input_Verification:
                print("\nUser input is  ",Test_type)
                break
        except:
            print("\nInvalid Input, Please Enter 1,2 or 3 as a Input")



 #------------------------------------------------------------------------------------------------------------------------------------------
 #                                            | Network Selection |
 #                                            |___________________| 
 
 #/////////////////////////////////////     2.4Ghz     \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    Received_SSID_PWD = []

    print("\n Please Eneter Network Credentials For 2.4 Ghz")
    while True:
        try:

            SSID=(str(input("\nEnter the SSID\t\t>> ")).strip())
            if SSID != 0 or SSID != None:

                Received_SSID_PWD.append(SSID)
                break
            print("\n Network Name should not be Empty")

        except:
            pass

    while True:
            try:

                PWD=(str(input("\nEnter the Password\t>> ")).strip())
                if PWD == None:
                    print("\n Password should not be Empty")
                    continue
                
                if len(PWD) < 8:

                    print("\n Password Length Not Matched")
                    continue

                else:
                    
                    Received_SSID_PWD.append(PWD)
                    break
            except:
                pass


#/////////////////////////////////////     5Ghz     \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

    print("\n Please Eneter Network Credentials For 5 Ghz")
    while True:
        try:

            SSID=(str(input("\nEnter the SSID\t\t>> ")).strip())
            if SSID != 0 or SSID != None:

                Received_SSID_PWD.append(SSID)
                break
            print("\n Network Name should not be Empty")

        except:
            pass

    while True:
            try:

                PWD=(str(input("\nEnter the Password\t>> ")).strip())
                if PWD == None:
                    print("\n Password should not be Empty")
                    continue
                
                if len(PWD) < 8:

                    print("\n Password Length Not Matched")
                    continue

                else:
                    
                    Received_SSID_PWD.append(PWD)
                    break
            except:
                pass



 #---------------------------------------------------------------------------------------------------------------------------------------
 #                                            | Socket Connection Establishing |
 #                                            |________________________________|                 
    Count=0
    connected = False
    while not connected:
        try:
                # Taking input from the User
                Host_IP=str(input('\n\tEneter the Host Ip address Displaying in Primary System\n\n For Example :- 192.168.41.11 \n\n >>  '))
                
                Communication_Service.connect((Host_IP, port_no))
                connected = True
        except Exception as e:
                Count +=1
                if Count ==3:
                    print("\nPlease check...!!!\n\t Both the Primary and Secondary systems are in same network.\n\t Entered Ip is valid.\n\t Entered Ip is in proper format.")
                elif Count==5:
                    print(f"\nError in Connecting , Please Reboot and try again...!\n {e}" )  
                    return              
                else:
                    print(f"\nError in Connecting to Primary System , Please try again...!\n {e}")                 
                
                time.sleep(1) 


    Test_type = "TX_Test" if Test_type == 1 else "RX_Test" if Test_type == 2 else "Full_Test"
    
    try:
        Secondary_Script_log_filename = f'./Logs/Secondary Script {DUT_Type} {Test_type} {Current_time.now().strftime("%d_%b_%Y__%M-%M-%S")} Logs'

        logging.basicConfig(filename = Secondary_Script_log_filename, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    except:

        print("\nLogs Directory not found to insert Log file\n")


    logging.info(f' {Com_Port} Com Port Selected.')

    logging.info(f' Current test type is {DUT_Type} .')

    logging.info(f' Current test Type is {Test_type} ')

    logging.info(f' Test Duration is {Duration} ')
    
    logging.info(f' Selected  {"Basic Test 5 Mbits - 25 Mbis" if Bandwidth_Range == 1 else "Moderate Test 10 Mbits - 50 Mbis" if Bandwidth_Range == 2 else "Extreme Test 20 Mbits - 100 Mbis"} ')

    logging.info(f' 2.4Ghz SSID is  {Received_SSID_PWD[0]} and Password is {Received_SSID_PWD[1]} ')

    logging.info(f' 5Ghz SSID is  {Received_SSID_PWD[2]} and Password is {Received_SSID_PWD[3]} ')

    logging.info(f' Connected to {Host_IP} Host ')    

    
    return True


def Establishinng_connection():

    global time_format, Device_Logs,  Device_Logs_File_Name,Test_Data

    Test_Data=[]

    

    time_format="%d_%b_%Y__%H-%M-%S"

    if not User_Input_Handler():
        return False
    
    Test_Data.extend([Distance,DUT_Type,Test_type,Duration,Bandwidth_Range])


    Communication_Service.send(json.dumps(Test_Data).encode("utf-8"))

    logging.info(f' Sent {Distance} mtr Distance Successfully ')
    logging.info(f' Sent {DUT_Type} Device type Successfully ')
    logging.info(f' Sent {Test_type} Test  type Successfully ')
    logging.info(f' Sent test {Duration} duration ')
    logging.info(f' Sent {Bandwidth_Range} Bandwidth Range Successfully ')

 
    


    Device_Logs_File_Name = f"./Logs/{DUT_Type} {Test_type} {Current_time.now().strftime(time_format)} Logs"

    Device_Logs = open(Device_Logs_File_Name,"w")

    logging.info(f' Created file to store Device Logs ')
    
    if wifi_configuration(_2_4Ghz=True):
        logging.info(f' Returning true after sucesssfully connecting wifi to 2.4 Ghz  ')
        return True
    else:
        logging.info(f' Returning False after Failing connecting wifi to 2.4 Ghz  ')
        return False
     

def wifi_configuration(_2_4Ghz):
    global re_checking

    
    re_checking=False
    
    for tries in range(6):
        
        print(f"\n{tries+1} Trying to connect wifi... ")
        logging.info(f' {tries+1} Trying to connect wifi...  ')
        

        # If DUT connecte Network then Sucess message will be sent to Primary or else rtries 3 times
        if Network_configuration(re_checking,Received_SSID_PWD,_2_4Ghz):

           
            print("Connected to wifi Sucessfully")
            logging.info(f"Connected to wifi Sucessfully")

            return True


  
        else:
                # send Ctrl + C command to DUT in the Final tries
              
                if tries>=1:
                    DUT_Ser.write(b'\r\nreboot\n\r')
                    logging.info(f'writing reboot command  ')
                    try:
                        Decoded_data=DUT_Ser.readline().decode("utf-8", errors="ignore")
                        Device_Logs.write(f"{Current_time.now().strftime(time_format)} - {Decoded_data.encode("utf-8")}\n")
                    except:
                        pass
                   
                    re_checking=True
                    logging.info(f'Enabling Recheck Process  ')

             
                


    else:
        print("\n Failed to Configure network to Device.!!!\n")
        logging.info(f'Failed to Configure network to Device.!!!')
        # sending Network connection FAIL status
        Communication_Service.send(int(False).to_bytes(1, byteorder="big")) 

        logging.info(f'Sending False command')   

        
        return False        


def Network_configuration(re_checking,SSID_PWD,_2_4Ghz):

    global __2_4Ghz__,SSID
    # Storing a refference of Current Network
    __2_4Ghz__= _2_4Ghz
    # Extracting SSID and PWD
    if _2_4Ghz:
        
        SSID=SSID_PWD[0]
        PWD=SSID_PWD[1]
        logging.info(f"Test is running for 2.4Ghz and the SSID is {SSID} and Password is {PWD}")
        
    else:
      
        SSID=SSID_PWD[2]
        PWD=SSID_PWD[3]
        logging.info(f"Test is running for 5Ghz and the SSID is {SSID} and Password is {PWD}")


    start_time = time.time()
    end_time = start_time + 70
     
    if re_checking:
        logging.info(f"Inside Recheking process")
        while time.time() < end_time:

            # Sending Ctrl+c command 
            DUT_Ser.write(b'\x03\n')  

            time.sleep(2)

            DUT_Ser.write('\n\rwpa_cli status\n\r'.encode("utf-8"))

            if DUT_Ser.in_waiting > 0:

                try:
                    Decoded_data=DUT_Ser.readline().decode("utf-8", errors="ignore")
                    
                    try:
                        Device_Logs.write(f"{Current_time.now().strftime(time_format)} - {Decoded_data.encode("utf-8")}\n")
                    except:
                        pass

                    print("Wifi Config ",Decoded_data)
                    # logging.info(f"Rechecking - Wifi Config Page - {Decoded_data}")

                
                    

                    Decoded_data=DUT_Ser.read_until("uuid").decode("utf-8", errors="ignore")
                    Device_Logs.write(f"{Current_time.now().strftime(time_format)} - {Decoded_data.encode("utf-8")}\n")

                    # logging.info(f"reading all  - {Decoded_data}")

                    #  regular expressions to search for the IP address in the output
                    match = re.search(r'ip_address=\d+\.\d+\.\d+\.\d+', Decoded_data)

                    # Check if a match is found
                    if match:
                        DUT_Ip_address = match.group(0).split("=")
                      
                        DUT_Ip_address=DUT_Ip_address[1]
                     
                        print(f"The IP address {DUT_Ip_address} exists on wlan0.")
                        logging.info(f'The IP address {DUT_Ip_address} exists on wlan0. ')


                        Communication_Service.send(int(True).to_bytes(1, byteorder="big"))
                        logging.info(f' Sent True command after Network connection Sucess ')

                        time.sleep(4)

                        # Sending DUT Wifi IP to Primary for the Iperf Commucnication
                        Communication_Service.send(DUT_Ip_address.encode("utf-8")) 
                        logging.info(f'Sending Device {DUT_Ip_address} IpV4 Address ')   

                        return True


                except UnicodeDecodeError as e:
                    
                    logging.info(f'Exception occured while reading serial data :- {e}  ')   
                    continue



        else:
            print("No IP address exists on wlan0.")  
            logging.info('Ip address Not Found Timeout Error occured!!!') 
        
            return False
            


               



    Wifi_Config=f'''wpa_cli \n
            remove_network all \n
            scan \n
            add_network \n
            set_network 0 ssid "{SSID}"  \n
            set_network 0 psk "{PWD}"     \n
            enable_network 0    \n
            save config \n
    '''
    

    DUT_Ser.write(f'\rLUCI_local 125 "{SSID}","{PWD}"\n'.encode("utf-8") )
    logging.info(f'LUCI_local 125 "{SSID}","{PWD}"          command written to connect wifi')

    Decoded_data=DUT_Ser.readline().decode("utf-8", errors="ignore")

    if "LUCI_local not found" in Decoded_data:
        DUT_Ser.write(Wifi_Config.encode("utf-8") )
        logging.info(f"{Wifi_Config}          command written to connect wifi")

    try:

        Device_Logs.write(f"{Current_time.now().strftime(time_format)} - {Decoded_data}\n")
    except:
        pass

    

  
    time.sleep(3)
    start_time = time.time()
    end_time = start_time + 50



    while time.time() < end_time:

        # Sending Ctrl+c command 
        DUT_Ser.write(b'\x03\n')  

        time.sleep(2)
        DUT_Ser.write('\r\nwpa_cli status\n\r'.encode("utf-8"))

        Decoded_data=DUT_Ser.readline().decode("utf-8", errors="ignore")
                
        Device_Logs.write(f"{Current_time.now().strftime(time_format)} - {Decoded_data}\n")

        if DUT_Ser.in_waiting > 0:

            try:
                

                # logging.info(f"Wifi Config Page - {Decoded_data}")

                

                Decoded_data=DUT_Ser.read_until("uuid").decode("utf-8", errors="ignore")
                Device_Logs.write(f"{Current_time.now().strftime(time_format)} - {Decoded_data}\n")

                # logging.info(f"reading all  - {Decoded_data}")

      

                #  regular expressions to search for the IP address in the output
                match = re.search(r'ip_address=\d+\.\d+\.\d+\.\d+', Decoded_data)

                # Check if a match is found
                if match:
                    DUT_Ip_address = match.group(0).split("=")
                    DUT_Ip_address=DUT_Ip_address[1]
                    print(f"The IP address {DUT_Ip_address} exists on wlan0.")
                    logging.info(f'The IP address {DUT_Ip_address} exists on wlan0. ')

    
                    Communication_Service.send(int(True).to_bytes(1, byteorder="big"))
                    logging.info(f' Sent True command after Network connection Sucess ')

                    time.sleep(4)

                    # Sending DUT Wifi IP to Primary for the Iperf Commucnication
                    Communication_Service.send(DUT_Ip_address.encode("utf-8")) 
                    logging.info(f'Sending Device {DUT_Ip_address} IpV4 Address ')   

                    return True


               



            except UnicodeDecodeError as e:
                 
                 print("Error decoding data:", e)



    else:
        print("No IP address exists on wlan0.")  
        logging.info('Ip address Not Found Timeout Error occured!!!') 
     
        return False



#>>>>>>>>>>>>>>>>   Test Executors 

def Testing():
    
    global  Current_Test_Bandwidth


    # verfiying test TX or RX
    while True:

        print(" inside testing ")
   
        Received_Data = Communication_Service.recv(1024).decode()

        print("Received_Data ",Received_Data)
        logging.info(f"Received_Data in testing function == > {Received_Data}")

        if 'iperf -s' in Received_Data:

             logging.info('Inside Server command')
             print("Test_type ",Test_type)

            # if the test is RX then enter the server command in serial comm
             Server_communication (Received_Data)
            #  print("Test_type ",Test_type)
             if  Test_type != "Full_Test":

                logging.info('returning True from server if the Test is not Full type')
                print(" Calling serial func to get rssi value")
                RSSI_Value = Serial_Data_Reading(RSSI_Value_check=True,client_cmd = False,Received__Data=None)
                logging.info('Calling serail function to get RSSI Value after 2.4Ghz test')
                #sending RSSI value
                Communication_Service.send(str(RSSI_Value).encode())
                logging.info('Sent RSSI Value ')

                print(" returning from testing")
                return 
             
             else:
                 
                 RSSI_Value = Serial_Data_Reading(RSSI_Value_check=True,client_cmd = False,Received__Data=None)
                 logging.info('Calling serail function to get RSSI Value after test')
                 #sending RSSI Values
                 Communication_Service.send(str(RSSI_Value).encode())
                 logging.info('Sent RSSI Value ')
            
                 
                                 

       
                
        elif  "iperf -c" in Received_Data:

         
            logging.info('Inside Client command')

            #  Recieving Current Test Bandwidth
            Current_Test_Bandwidth = float(Communication_Service.recv(1024).decode()) 
            print("Current_Test_Bandwidth ",Current_Test_Bandwidth)        
            logging.info(f'current test bandwidth recieved {Current_Test_Bandwidth}')
                    
            
            

            if Current_Test_Bandwidth == 5.0 and Test_type == "TX_Test":

                RSSI_Value = Serial_Data_Reading(RSSI_Value_check=True,client_cmd = False,Received__Data=None)
                logging.info('Calling serail function to get RSSI Value after test')
                #sending RSSI Values
                Communication_Service.send(str(RSSI_Value).encode())
                logging.info('Sent RSSI Value ')



            # enter client command in serial com
            Current_Iteration_Output = Serial_Data_Reading(RSSI_Value_check=False,client_cmd = True,Received__Data = Received_Data)


            # Calling Below Function to Analyse, take average and to send it to Primary for Each Test.

            if not Result_Analyser(Current_Iteration_Output,False):

                print("\nTX Test Result is Not Good ....!!!")
                logging.info(f'TX Test Result is Not Good ....!!!')

                # Sending False Command to stop test
                Communication_Service.send(int(False).to_bytes(1, byteorder="big"))
                logging.info('Sending False command to stop test')



                # clearing Input Buffer
                DUT_Ser.reset_input_buffer()
                # Reading Serail for RSI Value
                RSSI_Value = Serial_Data_Reading(RSSI_Value_check=True,client_cmd = False,Received__Data=None)
                logging.info('Calling serail function to get RSSI Value after  test')
                #sending RSSI Values
                Communication_Service.send(str(RSSI_Value).encode())
                logging.info('Sent  RSSI Value ')

                return 
            
            # Sending True Command to Continue test
            Communication_Service.send(int(True).to_bytes(1, byteorder="big"))
            logging.info('Sending True command to Continue the test')



        elif "End_test" in Received_Data:
                 
              print("\nTest Ended sucessfully\n")
              logging.info('Ending Test Here')

              return 
            
        

       

def Server_communication(Received__Data):
     
     global Current_Test_Bandwidth


     # Reading Serail for RSI Value
     logging.info(f'Calling Serial_Data_Reading function to check RSSI Values')
     RSSI_Value =  Serial_Data_Reading(RSSI_Value_check=True,client_cmd = False,Received__Data=None)
     Communication_Service.send(str(RSSI_Value).encode())
     logging.info(f'Sending RSSI Values')



     DUT_Ser.flush()
    
     #  writing Server command in serial
     DUT_Ser.write(f"{Received__Data} \n".encode("utf-8") )
     logging.info(f'writing {Received__Data} command to start server')
     print((f'writing {Received__Data} command to start server'))

     #Decoded_data=DUT_Ser.read_until(b'UDP buffer size').decode()
     
         
     Decoded_data=DUT_Ser.readall().decode("utf-8", errors="ignore")

     logging.info(Decoded_data)

    
     if "Server listening on UDP port" not in Decoded_data or "UDP buffer size" not in Decoded_data:
         # Sending confirmation
            Communication_Service.send(int(False).to_bytes(1, byteorder="big"))
            logging.info('Server not started and sending False command ')
            
            return False
     
     else:
         # Sending confirmation
         Communication_Service.send(int(True).to_bytes(1, byteorder="big"))
         logging.info('Server started and sending True command ')


        

     logging.info('waiting for the Current Test bandwidth ')

    #  Recieving Current Test Bandwidth
     Current_Test_Bandwidth = float(Communication_Service.recv(1024).decode()) 


     logging.info(f'Recieved Current_Test_Bandwidth {Current_Test_Bandwidth}')
     Current_Iteration_Output=Serial_Data_Reading(False,False,Received__Data)

     
     logging.info(f'Current Test Iteration Output {Current_Test_Bandwidth}')

     # Calling Below Function to Analyse, take average and to send it to Primary for Each Test.

     if not Result_Analyser(Current_Iteration_Output,True):
         
         print(" RX Test Result is Not Good ....!!!")
         logging.info(f'RX Test Result is Not Good ....!!!')

         # Sending False Command to stop test
         Communication_Service.send(int(False).to_bytes(1, byteorder="big"))
         logging.info('Sending False command to stop test')

         return False
     
     else:
         
        
        # Sending True command to continue test

        Communication_Service.send(int(True).to_bytes(1, byteorder="big"))
        logging.info('Sending True command to Continue the test')


     while True:

        logging.info('waiting to continue test')
        Received_Data = bool(int.from_bytes(Communication_Service.recv(1024),byteorder='big'))
         


        # Checking RX test End
        if  Received_Data:
            logging.info('Recieved confirmation to End RX Test') 
            # Communication_Service.send("RX Test Ended sucessfully".encode())

            DUT_Ser.write(b'\x03')

            return True
        
        else:
            logging.info('Recieved confirmation to Continue RX Test')

            # Recieving Current test Bandwidth
            Current_Test_Bandwidth = float(Communication_Service.recv(1024).decode())            
            
            # Serial_Data_Reading(client_cmd = False,Received_Client_Data=None) 
            Current_Iteration_Output = Serial_Data_Reading(False,False,Received__Data)
            logging.info(f'Current Test Iteration Output {Current_Test_Bandwidth}')

             # Calling Below Function to Analyse, take average and to send it to Primary for Each Test.

            if not Result_Analyser(Current_Iteration_Output,True):
                print(" RX Test Result is Not Good ....!!!")

                # Sending False Command to stop test
                Communication_Service.send(int(False).to_bytes(1, byteorder="big"))
                logging.info(f'RX Test Result is Not Good ....!!!')

                return False
            else:
                

                # Sending True command to continue test
                Communication_Service.send(int(True).to_bytes(1, byteorder="big"))
                logging.info('Sending True command to Continue the test')

            
#>>>>>>>>>>>>>>>>   Data Reading and Analyser 
   

def Serial_Data_Reading(RSSI_Value_check,client_cmd,Received__Data):
        
        Iteration_Output = []
        
        
        # Checking RSSI Value if its True

        if RSSI_Value_check:

            # RSSI_Value variable is to store the RSSI Value
            RSSI_Value=[]
            tries=1
            DUT_Ser.write(b'\x03')

            # Taking RSSI Values 5 time for Better Average value
            while tries <=5:
                

                print(f"RSSI Value check tries {tries}")
                logging.info(f"RSSI Value check tries {tries}")

                while True:
                    
                    RSSI_Value_Found=False

                    # Sending Scan Command and waiting till it gets response from AP
                    DUT_Ser.write(f"wpa_cli scan\n".encode("utf-8") )
                    logging.info(f"Wi-Fi Scan Initiated")
                    time.sleep(10)
                    DUT_Ser.write(f"wpa_cli scan_results\n".encode("utf-8") )

                    start_time = time.time()
                    end_time = start_time + 10
                    while time.time() < end_time:
                          
                            if DUT_Ser.in_waiting > 0:
                              
                                try:
                                    Decoded_data=DUT_Ser.readline().decode("utf-8", errors="ignore")
                                    
                                    try:
                                    
                                        Device_Logs.write(f"{Current_time.now().strftime(time_format)} - {Decoded_data.encode("utf-8")}\n")
                                    except:
                                        print("Decoded_data",Decoded_data)

                                        pass
                                        
                                    logging.info(f"RSSI - {Decoded_data}")
                                    # print(Decoded_data)

                                    if SSID in Decoded_data:
                                        
                                        Decoded_data=Decoded_data.split("\t")

                                        logging.info(f" After split Decoded data {Decoded_data}")
                                        if len(Decoded_data) == 5:
                                            if SSID == Decoded_data[4].strip():
                                                                                            

                                                        logging.info(f"RSSI value found - {Decoded_data[2]}")
                                                        print(f"RSSI value found - {Decoded_data[2]}")
                                                        RSSI_Value.append(Decoded_data[2])
                                                        logging.info(f"Current RSSI value added to RSSI Value list")
                                                        RSSI_Value_Found=True
                                                        break

                                    

                                            

                                except UnicodeDecodeError :
                                    
                                    continue

                    logging.info(f"RSSI_Value_Found {RSSI_Value_Found}")
                    if RSSI_Value_Found:
                        tries+=1
                        logging.info(f"Going back to re tries ")
                        break
                            
                    


            logging.info(f' Availbale RSSI Values   {RSSI_Value}')    

            # Calculating Average Of it and Storing in Same Variable
            RSSI_Value = sum(int(RSSI_Value) for RSSI_Value in RSSI_Value)//5 # calculating the sum of 5 RSSI data and dividing by 5 to take average of 5
            
            logging.info(f' Calculated  Average Value  {RSSI_Value}')
            print(f"\n\nRSSI Value average {RSSI_Value}")


            # Returning Average RSSI Value
            logging.info(f' Returning Average RSSI Value  {RSSI_Value}')
            return RSSI_Value
            

        else:     
            iteration=1
            Send_client_request=True

         # reading serial  for the average Data

            while len(Iteration_Output) <3:
                logging.info(f'{iteration} iteration output {Iteration_Output}')

                if client_cmd and Send_client_request:
                        time.sleep(10)
                        #  writing client  command in serial
                        DUT_Ser.write(f"{Received__Data} \n".encode("utf-8") )
                        logging.info('writing client command ') 

                        # Making Send_client_request False to avoid resending request untill completes
                        Send_client_request = False 


                start_time = time.time()
                end_time = start_time + 100
                logging.info(f'{iteration}   start_time   {start_time}      end_time.    {end_time}')
                while time.time() < end_time:

                    if DUT_Ser.in_waiting > 0:
                        try:
                            
                            Decoded_data = DUT_Ser.readline().decode("utf-8", errors="ignore")
                            Device_Logs.write(f"{Current_time.now().strftime(time_format)} - {Decoded_data.encode("utf-8")}\n")
                            
                            logging.info(f'Reading serial {Decoded_data}') 
                            print(Decoded_data)

                            
                            if Decoded_data== None:
                                continue
                            

                          
                            #if "0.00-60" in Decoded_data or " 0.00-61." in Decoded_data or " 0.00-59" in Decoded_data :
                            
                            if f" 0.00-{Duration}" in Decoded_data or f" 0.0-{Duration}" in Decoded_data or f" 0.00-{Duration+1}" in Decoded_data or f" 0.0-{Duration+1}" in Decoded_data or f" 0.00-{Duration-1}" in Decoded_data or f" 0.0-{Duration-1}" in Decoded_data :

                                if r"Mbits/sec" in Decoded_data or r"Kbits/sec" in Decoded_data:
                                
                                    print(" Inside if Mbits/sec in Decoded_data or Kbits/sec in Decoded_data")
                                    logging.info(f'Inside if r"Mbits/sec" in Decoded_data or r"Kbits/sec" in Decoded_data: ')
                                
                                    # Printing average data Found
                                    print("Average data found ", Decoded_data)
                                    logging.info(f'Average data found {Decoded_data}') 

                                    Iteration_Output.append(Decoded_data)
                                    logging.info(f'Average data appnede to Iteration Output') 

                                    if not client_cmd:
                                        print(f"RX {iteration} iteration Completed")
                                        logging.info(f"RX {iteration} iteration Completed")
                                    else:
                                        print(f"TX {iteration} iteration Completed")
                                        logging.info(f"TX {iteration} iteration Completed")
                                        Send_client_request=True
                                        logging.info(f"Send_client_request made it true'")
                                        

                                    DUT_Ser.reset_input_buffer()
                                    DUT_Ser.reset_output_buffer()
                                    time.sleep(5)
                                    
                                    iteration += 1
                                    logging.info(f" Test iteration increased")
                                    


                                    # Send False command to rerun if iteration is lesser than or equal to 3 and it is RX test  
                                    if not client_cmd and len(Iteration_Output) <3:
                                        
                                        Communication_Service.send(int(False).to_bytes(1, byteorder="big"))
                                        logging.info("Send False command to re run if iteration is lesser than or equal to 3 and it is RX test")
                                        break

                                    elif not client_cmd and len(Iteration_Output) == 3 :

                                        Communication_Service.send(int(True).to_bytes(1, byteorder="big"))
                                        logging.info("Sending  True  After completing 3 iteration RX test")
            
                                        break

                                    elif   client_cmd and len(Iteration_Output) <= 3 :
                                       
                                        DUT_Ser.write(b'\x03')
                                        break

                                else:
                                    logging.info(" Mbits or Kbits not found in the Average data")   
                                    print(" Mbits or Kbits not found in the Average data") 



                            # Send False command to re run if the recieved data is running above 60 seconds
                            #elif  "1.0-62.0 sec" in Decoded_data or "62.0-63.0 sec" in Decoded_data:
                            elif  f"1.0-{Duration+2}.0 sec" in Decoded_data or f"{Duration+2}.0-{Duration+3}.0 sec" in Decoded_data:
                               # print(" Inside  1.0-32.0 sec ")
                                if not client_cmd:

                                    DUT_Ser.write(b'\x03')

                                    time.sleep(10)

                                    #  writing Server command in serial
                                    DUT_Ser.write(f"{Received__Data} \n".encode("utf-8") )
                                    Communication_Service.send(int(False).to_bytes(1, byteorder="big"))
                                    logging.info("Send False command to re run if the recieved data is running above 60 seconds")
                                    
                                    break

                                else:
                                    DUT_Ser.write(b'\x03')
                                    Send_client_request=True
                                    logging.info("stoping current execution and and re sending client request after test running above 60 seconds")
                                    print(" Inside  stoping current execution and and re sending client ")
                                    break



                        except UnicodeDecodeError as e:
                            
                            print("Error decoding data:", e) 
                            logging.info(f" Error in decoding data {e}")         
                
                else:

                    if not client_cmd:

                        DUT_Ser.write(b'\x03')

                        #  writing Server command in serial
                        DUT_Ser.write(f"{Received__Data} \n".encode("utf-8") )
                        Communication_Service.send(int(False).to_bytes(1, byteorder="big"))
                        logging.info("Send False command to re run if the recieved data is not within 100 sec")

                    else:
                        DUT_Ser.write(b'\x03')
                        logging.info("stoping current execution and and re sending client request after waiting 100 sec")
                        print(" stoping current execution and and re sending client request after waiting 100 sec ")
                        Send_client_request=True



        

            logging.info(f"Returning iteration Output :- {Iteration_Output}")

            return Iteration_Output


                
def Result_Analyser(List_Data,Read_datagrams):

    Iteration_Output = []

    Average_Data=[]

    # Search for MBits Data
    Mbits = r"\d+\.\d+\sMbits"


    # Search for Kbits Data
    kbits = r"\d+\sKbits" 

    DataGrams_Pattern_1 =  r'\d+/\s+\d+ \(\d+%\)'
    DataGrams_Pattern_2 =  r'\d+/\s+\d+ \(\d+\.\d+%\)'
    DataGrams_Pattern_3 =  r'\d+/+\d+ \(\d+%\)'
    DataGrams_Pattern_4 =  r'\d+/+\d+ \(\d+\.\d+%\)'
 

    for Output in List_Data:

        Data_Found = re.search(Mbits, Output)


        if Data_Found:
            
            found_string = Data_Found.group()

            logging.info(f" Mbits Data Found : {found_string}")

            Data = found_string.split(" ")

            Average_Data.append(Data[0])

            Iteration_Output.append(Data[0])
            logging.info(' appending to Iteration_Output ')


            if Read_datagrams:

                Datagram_found = re.search(DataGrams_Pattern_1, Output)

        

                if Datagram_found :

                    #DataGrams=Datagram_found.groups()
                    print(Datagram_found[0])

                    Iteration_Output.append(Datagram_found[0])


                elif re.search(DataGrams_Pattern_2, Output) :

                    Datagram_found=re.search(DataGrams_Pattern_2, Output)

                    print(Datagram_found[0])
                    Iteration_Output.append(Datagram_found[0])

                elif re.search(DataGrams_Pattern_3, Output) :

                    Datagram_found=re.search(DataGrams_Pattern_3, Output)

                    print(Datagram_found[0])
                    Iteration_Output.append(Datagram_found[0]) 


                elif re.search(DataGrams_Pattern_4, Output) :

                    Datagram_found=re.search(DataGrams_Pattern_4, Output)

                    print(Datagram_found[0])
                    Iteration_Output.append(Datagram_found[0])

                  
                else:
                        Iteration_Output.append("None")


        else:

            Data_Found = re.search(kbits, Output)

            if Data_Found:
            
                found_string = Data_Found.group()

                logging.info(f" Kbits Data Found : {found_string}")

                Data = found_string.split(" ")

                Average_Data.append(float(Data[0])/1000)

                Iteration_Output.append(f'{float(Data[0])/1000}')
                logging.info(f"Coverting Kbits data to Mbits and appending to Iteration_Output ")

                if Read_datagrams:

                    Datagram_found = re.search(DataGrams_Pattern_1, Output)

            

                    if Datagram_found :

                        #DataGrams=Datagram_found.groups()
                        print(Datagram_found[0])

                        Iteration_Output.append(Datagram_found[0])


                    elif re.search(DataGrams_Pattern_2, Output) :

                        Datagram_found=re.search(DataGrams_Pattern_2, Output)

                        print(Datagram_found[0])
                        Iteration_Output.append(Datagram_found[0])

                    elif re.search(DataGrams_Pattern_3, Output) :

                        Datagram_found=re.search(DataGrams_Pattern_3, Output)

                        print(Datagram_found[0])
                        Iteration_Output.append(Datagram_found[0]) 


                    elif re.search(DataGrams_Pattern_4, Output) :

                        Datagram_found=re.search(DataGrams_Pattern_4, Output)

                        print(Datagram_found[0])
                        Iteration_Output.append(Datagram_found[0])

                    
                    else:
                            Iteration_Output.append("None")
                        
     # Below Expression for calculating Average Data fo 3 iteration and taking only 2 decimal after 

    Average_Data = round(sum(float(Average_Data) for Average_Data in Average_Data )/3,2)
    logging.info(f"Calculating average data of the output iteartion ")

    Iteration_Output.append(Average_Data)

    logging.info(f"Average_Data {Average_Data} Mbits")


    print("Iteration_Output ",Iteration_Output) 
    logging.info(f"Iteration_Output {Iteration_Output}")

    time.sleep(5)

    # sending # iteration Data with Average Data
    Communication_Service.send(json.dumps(Iteration_Output).encode("utf-8"))
    logging.info(f"Sending Iteration output with average data")


   
    logging.info(f"Current_Test_Bandwidth is {Current_Test_Bandwidth}")




    # 0.05 Is the Negotiation Value of AVerage Data
    # if Distance <= 3.0 :
    #     if Average_Data < Current_Test_Bandwidth-0.5:
    #         logging.info(f"Current test is ran within 3 mtr and the result is not good")
    #         return False
    # elif Distance <= 10.0: 
    #     if Average_Data < Current_Test_Bandwidth-5:
    #         logging.info(f"Current test is ran within 10 mtr and the result is not good")
    #         return False
    # else :
    #     if Average_Data < Current_Test_Bandwidth-15:
    #         logging.info(f"Current test is ran above  10 mtr and the result is not good")
    #         return False

    logging.info(f"Sending True after checking everything is Ok.")

    # Sending True if everything is Ok.
    return True




def Logs_Sender(Secondary_Script_log_filename,Device___log_filename):

    BUFFER_SIZE = 4096

   
    print(Secondary_Script_log_filename)
    print(Device___log_filename)
   
    Communication_Service.send(Secondary_Script_log_filename.encode())
     
    time.sleep(2)

    Communication_Service.send(Device___log_filename.encode()) 


    file_paths = [Secondary_Script_log_filename,Device___log_filename]  # Replace with the paths to your files

    time.sleep(3)

    for file_path in file_paths:
        # Get the file size
        file_size = os.path.getsize(file_path)
        # Convert the file size to a string representation
        file_size_str = str(file_size)
        Encoded_File_Size = file_size_str.zfill(16).encode()
        
        logging.info(f" Sent {file_path} file size {file_size_str}")

        logging.info(f" Sent {file_path} file size Encoded {Encoded_File_Size}")

        print(f" Sent {file_path} file size Encoded {Encoded_File_Size}")

        # Send the file size to the client, padded to a fixed length
        Communication_Service.sendall(Encoded_File_Size)

        # Open the file in binary mode
        with open(file_path, 'rb') as file:
            while True:
                # Read a chunk of data from the file
                chunk = file.read(BUFFER_SIZE)
                if not chunk:
                    file.close()
                    # End of file, break the loop
                    time.sleep(3)
                    break

                # Send the chunk to the client
                Communication_Service.sendall(chunk)


 

# Execution Starts Here  

def main():
    
    if Establishinng_connection():
        
        Testing()
        print(" outside testing ")
            
        time.sleep(6)
        # clearing Input Buffer
        DUT_Ser.reset_input_buffer()
        # Reading Serail for RSI Value

        
        

        #   5 Ghz Test  //////////////////////////////////////////////////////////////////////////////////////
        if wifi_configuration(_2_4Ghz=False):

            Testing()
                
            time.sleep(6)
            # clearing Input Buffer
            DUT_Ser.reset_input_buffer()
            # Reading Serail for RSI Value
            RSSI_Value = Serial_Data_Reading(RSSI_Value_check=True,client_cmd = False,Received__Data=None)
            logging.info('Calling serail function to get RSSI Value after 5Ghz test')
            #sending RSSI Values
            Communication_Service.send(str(RSSI_Value).encode())
            logging.info('Sent 5Ghz RSSI Value ')
    
            Logs_Sender(Secondary_Script_log_filename,Device_Logs_File_Name)
            # Communication End's Here By Closing established Socket.
            Communication_Service.close()

            
        else:

            time.sleep(6)
            # clearing Input Buffer
            DUT_Ser.reset_input_buffer()
            # Reading Serail for RSI Value
            RSSI_Value = Serial_Data_Reading(RSSI_Value_check=True,client_cmd = False,Received__Data=None)
            logging.info('Calling serail function to get RSSI Value after 2.4Ghz test')
            
            #sending RSSI Values
            Communication_Service.send(str(RSSI_Value).encode())
            logging.info('Sent 2.4Ghz RSSI Value ')
            #Closing Serial Port
            DUT_Ser.close()

            Logs_Sender(Secondary_Script_log_filename,Device_Logs_File_Name)
            # Communication End's Here By Closing established Socket.
            Communication_Service.close()





if __name__ == "__main__":
    # Call the main function
    main()


