import socket
import os
import time
from datetime import datetime
import serial
import serial.tools.list_ports as serial_ports
import json
import logging
import re




class Configuration:

    def __init__(self) -> None:
        
        
        # Check  all available ports
        self.ports = serial_ports.comports()

        self.Current_time=datetime
        self.time_format="%d_%b_%Y__%H-%M-%S"

        #Create a socket object   
        self.Communication_Service = socket.socket()

        self.port_no = 666   
        self.Input_Verification = [1,2,3]
        self.Received_SSID_PWD = []
        self.UserInput=[]

        # Crating Script logs folder
        if not os.path.exists("Logs"):
            os.makedirs("Logs")


    def Establishinng_connection(self):

        
        if not self.User_Input_Handler():
            return False
        

        else:
            
            self.Secondary_Script_log_filename = f'./Logs/Secondary Script {self.DUT_Type} {self.Test_type} {self.Current_time.now().strftime("%d_%b_%Y__%M-%M-%S")} Logs'
            self.Device_Logs_File_Name = f"./Logs/{self.DUT_Type} {self.Test_type} {self.Current_time.now().strftime(self.time_format)} Logs"

            self.UserInput.extend([self.Distance,self.DUT_Type,self.Test_type,self.Duration,self.Bandwidth_Range])


        #---------------------------------------------------------------------------------------------------------------------------------------
        #                                            | Socket Connection Establishing |
        #                                            |________________________________|                 
            Count=0
           
            while True:
                try:
                        # Taking input from the User
                        Host_IP=str(input('\n\tEneter the Host Ip address Displaying in Primary System\n\n For Example :- 192.168.41.11 \n\n >>  '))
                        
                        self.Communication_Service.connect((Host_IP, self.port_no))
                        break
                except Exception as e:
                        Count +=1
                        if Count ==3:
                            print("\nPlease check...!!!\n\t Both the Primary and Secondary systems are in same network.\n\t Entered Ip is valid.\n\t Entered Ip is in proper format.")
                        elif Count==5:
                            print(f"\nError in Connecting , Please Reboot and try again...!\n {e}" )  
                            return False         
                        else:
                            print(f"\nError in Connecting to Primary System , Please try again...!\n {e}")                 
                        
                        time.sleep(1) 


            
            
            try:
        
                logging.basicConfig(filename = self.Secondary_Script_log_filename, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

            except:

                print("\nLogs Directory not found to insert Log file\n")


            logging.info(f'[Configuration.Establishinng_connection] {self.Com_Port} Com Port Selected.')
            logging.info(f'[Configuration.Establishinng_connection] Current test type is {self.DUT_Type} .')
            logging.info(f'[Configuration.Establishinng_connection] Current test Type is {self.Test_type} ')
            logging.info(f'[Configuration.Establishinng_connection] Test Duration is {self.Duration} ')
            logging.info(f'[Configuration.Establishinng_connection] Selected  {self.Bandwidth_Range} ')
            logging.info(f'[Configuration.Establishinng_connection] 2.4Ghz SSID is  {self.Received_SSID_PWD[0]} and Password is {self.Received_SSID_PWD[1]} ')
            logging.info(f'[Configuration.Establishinng_connection] 5Ghz SSID is  {self.Received_SSID_PWD[2]} and Password is {self.Received_SSID_PWD[3]} ')
            logging.info(f'[Configuration.Establishinng_connection] Connected to {Host_IP} Host ')    



            self.Communication_Service.send(json.dumps(self.UserInput).encode("utf-8"))
            logging.info('[Configuration.Establishinng_connection] Sent Test data Successfully ')


            self.Device_Logs = open(self.Device_Logs_File_Name,"w")
            logging.info(f'[Configuration.Establishinng_connection] Created file to store Device Logs ')


            if self.wifi_configuration(_2_4Ghz=True):
                logging.info(f'[Configuration.Establishinng_connection] Returning true after sucesssfully connecting wifi to 2.4 Ghz  ')
                return True
            else:
                logging.info(f'[Configuration.Establishinng_connection] Returning False after Failing in connecting wifi to 2.4 Ghz  ')
                return False


    def User_Input_Handler(self):
        
        
        #------------------------------------------------------------------------------------------------------------------------------------
        #                                          | Serial COM Port Selecton |
        #                                          |__________________________|      
        #  

            try:
                print("\n\tSelect Proper COM Ports ")
                
                if self.ports != []:

                    #List All available ports
                    for port in sorted(self.ports):
                            
                        print(f'\n{port}')

                else :
                    # Return if there is No Com Port available
                    print("\n\tNo COM Ports available !!!!\n")
                    return False

                self.Com_Port = str(input("\n>> "))

                # configure port number and Baudrate 
                self.DUT_Ser = serial.Serial(self.Com_Port,baudrate=115200,timeout=1) 

            except:
                print("\nError in Opening COM Port..!!!\n \t Please Check for Port Availability and Make Sure you Selected Proper Com Port...!!!\n\n")
                return False


        #------------------------------------------------------------------------------------------------------------------------------------
        #                                          | Select Device Type |
        #                                          |____________________|  

            while True:

                try:            

                    DUT_Type =str(input("\nPlease Enter the Device / Module Name \n\t i>    LS10 \n\t ii>   LS11 \n>>  " ))      
                    
                    self.DUT_Type = DUT_Type.strip().upper()

                    if self.DUT_Type =="0" or  self.DUT_Type == "" :
                        
                        print('\n',6*' ',"Device Name should not be empty or Zero !",'\n')  

                    elif len(self.DUT_Type) >=6 or len(self.DUT_Type) <3:
                        
                        print('\n',6*' ',"please select proper Device !",'\n')   
            
                    else :

                        print(f"User enterd device name :{self.DUT_Type}")
                        break
                    
                except:
                    pass
                


        #------------------------------------------------------------------------------------------------------------------------------------
        #                                          | Enter the Test Duration |
        #                                          |_________________________|  

            while True:
                    
                try :
                        self.Duration = int(input("\nPlease Enter the Test Duration in Seconds   :-  " ))      
                        if self.Duration < 10.0:
                            print("\n\tDuration time should be more than 10 sec")
                            pass
                        elif self.Duration >= 10.0:
                            break
                except:
                        pass      

        
         #------------------------------------------------------------------------------------------------------------------------------------
        #                                          | Enter the Distance |
        #                                          |____________________|  

            while True:

                try:            

                    self.Distance = float(input("\nPlease Enter the Distance in Mtrs   :-  " ))      
                    if self.Distance >= 1.0:
                            break

                except:
                        pass    

        #------------------------------------------------------------------------------------------------------------------------------------------
        #                                            | Bandwidth Range Selection |
        #                                            |___________________________| 
            

            while True:

                try:
                    print("\n\t Select the Bandwidth Range \n\n\t ")
                    Bandwidth_Range = int(input(" 1. Basic Test\t\t5M - 25M \n\n 2. Moderate Test\t10M - 50M\n\n 3. Extreme Test\t20M - 100M\n\n>> "))
                    if Bandwidth_Range in self.Input_Verification:
                        self.Bandwidth_Range = "Basic Test 5 Mbits - 25 Mbis" if Bandwidth_Range == 1 else "Moderate Test 10 Mbits - 50 Mbis" if Bandwidth_Range == 2 else "Extreme Test 20 Mbits - 100 Mbis"
                        print("\nUser input is  ",self.Bandwidth_Range)
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
                    if Test_type in self.Input_Verification:
                        self.Test_type = "TX_Test" if Test_type == 1 else "RX_Test" if Test_type == 2 else "Full_Test"
                        print("\nUser input is  ",self.Test_type)
                        break
                except:
                    print("\nInvalid Input, Please Enter 1,2 or 3 as a Input")




         #------------------------------------------------------------------------------------------------------------------------------------------
        #                                            | Network Selection |
        #                                            |___________________| 
        
        #/////////////////////////////////////     2.4Ghz     \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
            

            print("\n Please Eneter Network Credentials For 2.4 Ghz")
            while True:
                try:

                    SSID=(str(input("\nEnter the SSID\t\t>> ")).strip())
                    if SSID != 0 or SSID != None:

                        self.Received_SSID_PWD.append(SSID)
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
                            
                            self.Received_SSID_PWD.append(PWD)
                            break
                    except:
                        pass



        #/////////////////////////////////////     5Ghz     \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

            print("\n Please Eneter Network Credentials For 5 Ghz")
            while True:
                try:

                    SSID=(str(input("\nEnter the SSID\t\t>> ")).strip())
                    if SSID != 0 or SSID != None:

                        self.Received_SSID_PWD.append(SSID)
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
                            
                            self.Received_SSID_PWD.append(PWD)
                            return True
                    except:
                        pass


    def wifi_configuration(self,_2_4Ghz):
    
    
        re_checking=False
        
        for tries in range(6):
            
            print(f"\n{tries+1} Trying to connect wifi... ")
            logging.info(f'[Configuration.wifi_configuration] {tries+1} Trying to connect wifi...  ')
            

            # If DUT connecte Network then Sucess message will be sent to Primary or else rtries 3 times
            if self.Network_configuration(re_checking,self.Received_SSID_PWD,_2_4Ghz):

            
                print("Connected to wifi Sucessfully")
                logging.info(f"[Configuration.wifi_configuration] Connected to wifi Sucessfully")

                return True


    
            else:
                    # send Ctrl + C command to DUT in the Final tries
                
                    if tries>=1:
                        self.DUT_Ser.write(b'\r\nreboot\n\r')
                        logging.info(f'[Configuration.wifi_configuration] writing reboot command  ')
                        try:
                            Decoded_data = self.DUT_Ser.readline().decode("utf-8", errors="ignore")
                            self.Device_Logs.write(f"{self.Current_time.now().strftime(self.time_format)} - {Decoded_data.encode("utf-8")}\n")
                        except:
                            pass
                    
                        re_checking=True
                        logging.info(f'[Configuration.wifi_configuration] Enabling Recheck Process  ')



        else:
            print("\n Failed to Configure network to Device.!!!\n")
            logging.info(f'[Configuration.wifi_configuration] Failed to Configure network to Device.!!!')
            # sending Network connection FAIL status
            self.Communication_Service.send(int(False).to_bytes(1, byteorder="big")) 

            logging.info(f'[Configuration.wifi_configuration] Sending False command')   
            return False        


    def Network_configuration(self,re_checking,Received_SSID_PWD,_2_4Ghz):

        # Extracting SSID and PWD
        if _2_4Ghz:
            
            self.SSID = self.Received_SSID_PWD[0]
            self.PWD = self.Received_SSID_PWD[1]
            logging.info(f"[Configuration.Network_configuration] Test is running for 2.4Ghz and the SSID is {self.SSID} and Password is {self.PWD}")
            
        else:
        
            self.SSID = Received_SSID_PWD[2]
            self.PWD = Received_SSID_PWD[3]
            logging.info(f"[Configuration.Network_configuration] Test is running for 5Ghz and the SSID is {self.SSID} and Password is {self.PWD}")


        if not re_checking:
             
            Wifi_Config=f'''wpa_cli \n
            remove_network all \n
            scan \n
            add_network \n
            set_network 0 ssid "{self.SSID}"  \n
            set_network 0 psk "{self.PWD}"     \n
            enable_network 0    \n
            save config \n
                        '''


            self.DUT_Ser.write(f'\rLUCI_local 125 "{self.SSID}","{self.PWD}"\n'.encode("utf-8") )
            logging.info(f'[Configuration.Network_configuration] LUCI_local 125 "{self.SSID}","{self.PWD}"  command written to connect wifi')

            Decoded_data = self.DUT_Ser.readline().decode("utf-8", errors="ignore")

            if "LUCI_local not found" in Decoded_data:
                self.DUT_Ser.write(Wifi_Config.encode("utf-8") )
                logging.info(f"[Configuration.Network_configuration] {Wifi_Config}  command written to connect wifi")

            try:

                self.Device_Logs.write(f"{self.Current_time.now().strftime(self.time_format)} - {Decoded_data}\n")
            except:
                pass




        time.sleep(3)
        start_time = time.time()
        end_time = start_time + 50



        while time.time() < end_time:

            # Sending Ctrl+c command 
            self.DUT_Ser.write(b'\x03\n')  

            time.sleep(2)
            self.DUT_Ser.write('\r\nwpa_cli status\n\r'.encode("utf-8"))

            Decoded_data = self.DUT_Ser.readline().decode("utf-8", errors="ignore")
                    
            self.Device_Logs.write(f"{self.Current_time.now().strftime(self.time_format)} - {Decoded_data}\n")

            if self.DUT_Ser.in_waiting > 0:

                try:
                    


                    Decoded_data = self.DUT_Ser.read_until("uuid").decode("utf-8", errors="ignore")
                    self.Device_Logs.write(f"{self.Current_time.now().strftime(self.time_format)} - {Decoded_data}\n")


                    #  regular expressions to search for the IP address in the output
                    match = re.search(r'ip_address=\d+\.\d+\.\d+\.\d+', Decoded_data)

                    # Check if a match is found
                    if match:
                        DUT_Ip_address = match.group(0).split("=")
                        DUT_Ip_address=DUT_Ip_address[1]
                        print(f"The IP address {DUT_Ip_address} exists on wlan0.")
                        logging.info(f'[Configuration.Network_configuration] The IP address {DUT_Ip_address} exists on wlan0. ')


                        self.Communication_Service.send(int(True).to_bytes(1, byteorder="big"))
                        logging.info(f'[Configuration.Network_configuration] Sent True command after Network connection Sucess ')

                        time.sleep(4)

                        # Sending DUT Wifi IP to Primary for the Iperf Commucnication
                        self.Communication_Service.send(DUT_Ip_address.encode("utf-8")) 
                        logging.info(f'[Configuration.Network_configuration] Sending Device {DUT_Ip_address} IpV4 Address ')   

                        return True


                except UnicodeDecodeError as e:
                        
                        print("Error decoding data:", e)



        else:
            print("No IP address exists on wlan0.")  
            logging.info('[Configuration.Network_configuration] Ip address Not Found Timeout Error occured!!!') 
            
            return False




class Test_Driver:
     

    def __init__(self,config) -> None:
        
        self.config = config

        self.Iteration_Output = []


        # Search for self.Mbits Data
        self.Mbits = r"\d+\.\d+\sMbits"


        # Search for Kbits Data
        self.kbits = r"\d+\sKbits" 

        # DataGrams Finding Patterns
        
        self.DataGrams_Pattern_1 =  r'\d+/\s+\d+ \(\d+%\)'
        self.DataGrams_Pattern_2 =  r'\d+/\s+\d+ \(\d+\.\d+%\)'
        self.DataGrams_Pattern_3 =  r'\d+/+\d+ \(\d+%\)'
        self.DataGrams_Pattern_4 =  r'\d+/+\d+ \(\d+\.\d+%\)'

     #>>>>>>>>>>>>>>>>   Test Executors 

    def Testing(self):
        
        global  Current_Test_Bandwidth


        # verfiying test TX or RX
        while True:

            # print(" inside testing ")
    
            Received_Data = self.config.Communication_Service.recv(1024).decode()

            print("Received_Data ",Received_Data)
            logging.info(f"[Test_Driver.Testing] Received_Data in testing function == > {Received_Data}")

            if 'iperf -s' in Received_Data:

                logging.info('[Test_Driver.Testing] Inside Server command')
                print("Test_type ",self.config.Test_type)

                # if the test is RX then enter the server command in serial comm
                self.Server_communication (Received_Data)
                logging.info('[Test_Driver.Testing] exiting')
                print('[Test_Driver.Testing] exiting')
                return

                #  print("Test_type ",Test_type)
                # if  self.config.Test_type != "Full_Test":

                #     logging.info('[Test_Driver.Testing] returning True from server if the Test is not Full type')
                #     print(" Calling serial func to get rssi value")
                #     RSSI_Value = self.Serial_Data_Reading(RSSI_Value_check=True,client_cmd = False,Received__Data=None)
                #     logging.info('[Test_Driver.Testing] Calling serail function to get RSSI Value after 2.4Ghz test')
                #     #sending RSSI value
                #     self.config.Communication_Service.send(str(RSSI_Value).encode())
                #     logging.info('[Test_Driver.Testing] Sent RSSI Value ')

                #     print(" returning from testing")
                #     return 
                
                # else:
                    
                #     RSSI_Value = self.Serial_Data_Reading(RSSI_Value_check=True,client_cmd = False,Received__Data=None)
                #     logging.info('[Test_Driver.Testing] Calling serail function to get RSSI Value after test')
                #     #sending RSSI Values
                #     self.config.Communication_Service.send(str(RSSI_Value).encode())
                #     logging.info('[Test_Driver.Testing] Sent RSSI Value ')
                
                    
             
            elif  "iperf -c" in Received_Data:

            
                logging.info('[Test_Driver.Testing] Inside Client command')

                #  Recieving Current Test Bandwidth
                Current_Test_Bandwidth = float(self.config.Communication_Service.recv(1024).decode()) 
                print("Current_Test_Bandwidth ",Current_Test_Bandwidth)        
                logging.info(f'[Test_Driver.Testing] current test bandwidth recieved {Current_Test_Bandwidth}')
    

                if Current_Test_Bandwidth == 5.0 and self.config.Test_type == "TX_Test":

                    RSSI_Value = self.Serial_Data_Reading(RSSI_Value_check=True,client_cmd = False,Received__Data=None)
                    logging.info('[Test_Driver.Testing] Calling serail function to get RSSI Value after test')
                    #sending RSSI Values
                    self.config.Communication_Service.send(str(RSSI_Value).encode())
                    logging.info('[Test_Driver.Testing] Sent RSSI Value ')



                # enter client command in serial com
                Current_Iteration_Output = self.Serial_Data_Reading(RSSI_Value_check=False,client_cmd = True,Received__Data = Received_Data)


                # Calling Below Function to Analyse, take average and to send it to Primary for Each Test.

                if not self.Result_Analyser(Current_Iteration_Output,False):

                    print("\nTX Test Result is Not Good ....!!!")
                    logging.info(f'[Test_Driver.Testing] TX Test Result is Not Good ....!!!')

                    # Sending False Command to stop test
                    self.config.Communication_Service.send(int(False).to_bytes(1, byteorder="big"))
                    logging.info('[Test_Driver.Testing] Sending False command to stop test')



                    # clearing Input Buffer
                    self.config.DUT_Ser.reset_input_buffer()
                    # Reading Serail for RSI Value
                    RSSI_Value = self.Serial_Data_Reading(RSSI_Value_check=True,client_cmd = False,Received__Data=None)
                    logging.info('[Test_Driver.Testing] Calling serail function to get RSSI Value after  test')
                    #sending RSSI Values
                    self.config.Communication_Service.send(str(RSSI_Value).encode())
                    logging.info('[Test_Driver.Testing] Sent  RSSI Value ')

                    return 
                
                # Sending True Command to Continue test
                self.config.Communication_Service.send(int(True).to_bytes(1, byteorder="big"))
                logging.info('[Test_Driver.Testing] Sending True command to Continue the test')



            elif "End_test" in Received_Data:
                    
                print("\nTest Ended sucessfully\n")
                logging.info('[Test_Driver.Testing] Ending Test Here')

                return 
                
   
    def Result_Analyser(self,List_Data,Read_datagrams):

        
        Average_Data = []

        for Output in List_Data:

            Data_Found = re.search(self.Mbits, Output)


            if Data_Found:
                
                found_string = Data_Found.group()

                logging.info(f"[Test_Driver.Result_Analyser]  Mbits Data Found : {found_string}")

                Data = found_string.split(" ")

                Average_Data.append(Data[0])

                self.Iteration_Output.append(Data[0])
                logging.info('[Test_Driver.Result_Analyser]  appending to Iteration_Output ')


                if Read_datagrams:

                    Datagram_found = re.search(self.DataGrams_Pattern_1, Output)

            

                    if Datagram_found :

                        #DataGrams=Datagram_found.groups()
                        logging.info(f'[Test_Driver.Result_Analyser] {Datagram_found[0]}')

                        self.Iteration_Output.append(Datagram_found[0])


                    elif re.search(self.DataGrams_Pattern_2, Output) :

                        Datagram_found=re.search(self.DataGrams_Pattern_2, Output)

                        logging.info(f'[Test_Driver.Result_Analyser] {Datagram_found[0]}')
                        self.Iteration_Output.append(Datagram_found[0])

                    elif re.search(self.DataGrams_Pattern_3, Output) :

                        Datagram_found=re.search(self.DataGrams_Pattern_3, Output)

                        logging.info(f'[Test_Driver.Result_Analyser] {Datagram_found[0]}')
                        self.Iteration_Output.append(Datagram_found[0]) 


                    elif re.search(self.DataGrams_Pattern_4, Output) :

                        Datagram_found=re.search(self.DataGrams_Pattern_4, Output)

                        logging.info(f'[Test_Driver.Result_Analyser] {Datagram_found[0]}')
                        self.Iteration_Output.append(Datagram_found[0])

                    
                    else:
                            self.Iteration_Output.append("None")


            else:

                Data_Found = re.search(self.kbits, Output)

                if Data_Found:
                
                    found_string = Data_Found.group()

                    logging.info(f"[Test_Driver.Result_Analyser]  Kbits Data Found : {found_string}")

                    Data = found_string.split(" ")

                    Average_Data.append(float(Data[0])/1000)

                    self.Iteration_Output.append(f'{float(Data[0])/1000}')
                    logging.info(f"[Test_Driver.Result_Analyser] Coverting Kbits data to self.Mbits and appending to Iteration_Output ")

                    if Read_datagrams:

                        Datagram_found = re.search(self.DataGrams_Pattern_1, Output)

                

                        if Datagram_found :

                            #DataGrams=Datagram_found.groups()
                            logging.info(f'[Test_Driver.Result_Analyser] {Datagram_found[0]}')

                            self.Iteration_Output.append(Datagram_found[0])


                        elif re.search(self.DataGrams_Pattern_2, Output) :

                            Datagram_found=re.search(self.DataGrams_Pattern_2, Output)

                            logging.info(f'[Test_Driver.Result_Analyser] {Datagram_found[0]}')
                            self.Iteration_Output.append(Datagram_found[0])

                        elif re.search(self.DataGrams_Pattern_3, Output) :

                            Datagram_found=re.search(self.DataGrams_Pattern_3, Output)

                            logging.info(f'[Test_Driver.Result_Analyser] {Datagram_found[0]}')
                            self.Iteration_Output.append(Datagram_found[0]) 


                        elif re.search(self.DataGrams_Pattern_4, Output) :

                            Datagram_found=re.search(self.DataGrams_Pattern_4, Output)

                            logging.info(f'[Test_Driver.Result_Analyser] {Datagram_found[0]}')
                            self.Iteration_Output.append(Datagram_found[0])

                        
                        else:
                                self.Iteration_Output.append("None")
                            
        # Below Expression for calculating Average Data fo 3 iteration and taking only 2 decimal after 

        Average_Data = round(sum(float(Average_Data) for Average_Data in Average_Data )/3,2)
        logging.info(f"[Test_Driver.Result_Analyser] Calculating average data of the output iteartion ")

        self.Iteration_Output.append(Average_Data)

        logging.info(f"[Test_Driver.Result_Analyser] Average_Data {Average_Data} self.Mbits")


        #print("Iteration_Output ",self.Iteration_Output) 
        logging.info(f"[Test_Driver.Result_Analyser] Iteration_Output {self.Iteration_Output}")

        time.sleep(5)

        # sending # iteration Data with Average Data
        self.config.Communication_Service.send(json.dumps(self.Iteration_Output).encode("utf-8"))
        logging.info(f"[Test_Driver.Result_Analyser] Sending Iteration output with average data")


    
        logging.info(f"[Test_Driver.Result_Analyser] Current_Test_Bandwidth is {Current_Test_Bandwidth}")




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

        logging.info(f"[Test_Driver.Result_Analyser] Sending True after checking everything is Ok.")


        self.Iteration_Output.clear()
        

        # Sending True if everything is Ok.
        return True


    def Serial_Data_Reading(self,RSSI_Value_check,client_cmd,Received__Data):
        
        Iteration_Output = []
        pattern =r'\b0.0\b\-\d{2}'
        
        
        # Checking RSSI Value if its True

        if RSSI_Value_check:

            # RSSI_Value variable is to store the RSSI Value
            RSSI_Value=[]
            tries=1
            self.config.DUT_Ser.write(b'\x03')

            # Taking RSSI Values 5 time for Better Average value
            while tries <=5:
                

                print(f"RSSI Value check tries {tries}")
                logging.info(f"[Test_Driver.Serial_Data_Reading] RSSI Value check tries {tries}")

                while True:
                    
                    RSSI_Value_Found=False

                    # Sending Scan Command and waiting till it gets response from AP
                    self.config.DUT_Ser.write(f"wpa_cli scan\n".encode("utf-8") )
                    logging.info(f"[Test_Driver.Serial_Data_Reading] Wi-Fi Scan Initiated")
                    time.sleep(10)
                    self.config.DUT_Ser.write(f"wpa_cli scan_results\n".encode("utf-8") )

                    start_time = time.time()
                    end_time = start_time + 10
                    while time.time() < end_time:
                          
                            if self.config.DUT_Ser.in_waiting > 0:
                              
                                try:
                                    Decoded_data = self.config.DUT_Ser.readline().decode("utf-8", errors="ignore")
                                    
                                    try:
                                    
                                        self.config.Device_Logs.write(f"{self.config.Current_time.now().strftime(self.config.time_format)} - {Decoded_data.encode("utf-8")}\n")
                                    except:
                                        print("Decoded_data",Decoded_data)

                                        pass
                                        
                                    logging.info(f"[Test_Driver.Serial_Data_Reading] RSSI - {Decoded_data}")
                                    # print(Decoded_data)

                                    if self.config.SSID in Decoded_data:
                                        
                                        Decoded_data=Decoded_data.split("\t")

                                        logging.info(f"[Test_Driver.Serial_Data_Reading]  After split Decoded data {Decoded_data}")
                                        if len(Decoded_data) == 5:
                                            if self.config.SSID == Decoded_data[4].strip():
                                                                                            

                                                        logging.info(f"[Test_Driver.Serial_Data_Reading] RSSI value found - {Decoded_data[2]}")
                                                        print(f"RSSI value found - {Decoded_data[2]}")
                                                        RSSI_Value.append(Decoded_data[2])
                                                        logging.info(f"[Test_Driver.Serial_Data_Reading] Current RSSI value added to RSSI Value list")
                                                        RSSI_Value_Found=True
                                                        break

                                    

                                            

                                except UnicodeDecodeError :
                                    
                                    continue

                    logging.info(f"[Test_Driver.Serial_Data_Reading] RSSI_Value_Found {RSSI_Value_Found}")
                    if RSSI_Value_Found:
                        tries+=1
                        logging.info(f"[Test_Driver.Serial_Data_Reading] Going back to re tries ")
                        break
                            
                    


            logging.info(f'[Test_Driver.Serial_Data_Reading] Availbale RSSI Values   {RSSI_Value}')    

            # Calculating Average Of it and Storing in Same Variable
            RSSI_Value = sum(int(RSSI_Value) for RSSI_Value in RSSI_Value)//5 # calculating the sum of 5 RSSI data and dividing by 5 to take average of 5
            
            logging.info(f'[Test_Driver.Serial_Data_Reading] Calculated  Average Value  {RSSI_Value}')
            print(f"\n\nRSSI Value average {RSSI_Value}")


            # Returning Average RSSI Value
            logging.info(f'[Test_Driver.Serial_Data_Reading] Returning Average RSSI Value  {RSSI_Value}')
            return RSSI_Value
            

        else:     
            iteration=1
            Send_client_request=True

         # reading serial  for the average Data

            while len(Iteration_Output) <3:
                logging.info(f'[Test_Driver.Serial_Data_Reading] {iteration} iteration output {Iteration_Output}')

                if client_cmd and Send_client_request:
                        time.sleep(10)
                        #  writing client  command in serial
                        self.config.DUT_Ser.write(f"{Received__Data} \n".encode("utf-8") )
                        logging.info('[Test_Driver.Serial_Data_Reading] writing client command ') 

                        # Making Send_client_request False to avoid resending request untill completes
                        Send_client_request = False 


                start_time = time.time()
                end_time = start_time + 100
                logging.info(f'[Test_Driver.Serial_Data_Reading] {iteration}   start_time   {start_time}      end_time.    {end_time}')
                while time.time() < end_time:

                    if self.config.DUT_Ser.in_waiting > 0:
                        try:
                            
                            Decoded_data = self.config.DUT_Ser.readline().decode("utf-8", errors="ignore")
                            self.config.Device_Logs.write(f"{self.config.Current_time.now().strftime(self.config.time_format)} - {Decoded_data.encode("utf-8")}\n")
                            
                            logging.info(f'[Test_Driver.Serial_Data_Reading] Reading serial {Decoded_data}') 
                            print(Decoded_data)

                            
                            if Decoded_data== None:
                                continue
                            

                          
                            #if "0.00-60" in Decoded_data or " 0.00-61." in Decoded_data or " 0.00-59" in Decoded_data :

                            if re.search(pattern,Decoded_data) :
                            
                            # if f" 0.00-{self.config.Duration}" in Decoded_data or f" 0.0-{self.config.Duration}" in Decoded_data or f" 0.00-{self.config.Duration+1}" in Decoded_data or f" 0.0-{self.config.Duration+1}" in Decoded_data or f" 0.00-{self.config.Duration-1}" in Decoded_data or f" 0.0-{self.config.Duration-1}" in Decoded_data :

                                if r"Mbits/sec" in Decoded_data or r"Kbits/sec" in Decoded_data:
                                
                                    #print(" Inside if Mbits/sec in Decoded_data or Kbits/sec in Decoded_data")
                                    logging.info(f'[Test_Driver.Serial_Data_Reading] Inside if r"Mbits/sec" in Decoded_data or r"Kbits/sec" in Decoded_data: ')
                                
                                    # Printing average data Found
                                    #print("Average data found ", Decoded_data)
                                    logging.info(f'[Test_Driver.Serial_Data_Reading] Average data found {Decoded_data}') 

                                    Iteration_Output.append(Decoded_data)
                                    logging.info(f'[Test_Driver.Serial_Data_Reading] Average data appnede to Iteration Output') 

                                    if not client_cmd:
                                        print(f"RX {iteration} iteration Completed")
                                        logging.info(f"[Test_Driver.Serial_Data_Reading] RX {iteration} iteration Completed")
                                    else:
                                        print(f"TX {iteration} iteration Completed")
                                        logging.info(f"[Test_Driver.Serial_Data_Reading] TX {iteration} iteration Completed")
                                        Send_client_request=True
                                        logging.info(f"[Test_Driver.Serial_Data_Reading] Send_client_request made it true'")
                                        

                                    self.config.DUT_Ser.reset_input_buffer()
                                    self.config.DUT_Ser.reset_output_buffer()
                                    time.sleep(5)
                                    
                                    iteration += 1
                                    logging.info(f"[Test_Driver.Serial_Data_Reading]  Test iteration increased")
                                    


                                    # Send False command to rerun if iteration is lesser than or equal to 3 and it is RX test  
                                    if not client_cmd and len(Iteration_Output) <3:
                                        
                                        self.config.Communication_Service.send(int(False).to_bytes(1, byteorder="big"))
                                        logging.info("[Test_Driver.Serial_Data_Reading] Send False command to re run if iteration is lesser than or equal to 3 and it is RX test")
                                        break

                                    elif not client_cmd and len(Iteration_Output) == 3 :

                                        self.config.Communication_Service.send(int(True).to_bytes(1, byteorder="big"))
                                        logging.info("[Test_Driver.Serial_Data_Reading] Sending  True  After completing 3 iteration RX test")
            
                                        break

                                    elif   client_cmd and len(Iteration_Output) <= 3 :
                                       
                                        self.config.DUT_Ser.write(b'\x03')
                                        break

                                else:
                                    logging.info("[Test_Driver.Serial_Data_Reading]  Mbits or Kbits not found in the Average data")   
                                    #print(" Mbits or Kbits not found in the Average data") 



                            # Send False command to re run if the recieved data is running above 60 seconds
                            #elif  "1.0-62.0 sec" in Decoded_data or "62.0-63.0 sec" in Decoded_data:
                            elif  f"1.0-{self.config.Duration+5}.0 sec" in Decoded_data or f"{self.config.Duration+2}.0-{self.config.Duration+5}.0 sec" in Decoded_data:
                               # print(" Inside  1.0-32.0 sec ")
                                if not client_cmd:

                                    self.config.DUT_Ser.write(b'\x03')

                                    time.sleep(10)

                                    #  writing Server command in serial
                                    self.config.DUT_Ser.write(f"{Received__Data} \n".encode("utf-8") )
                                    self.config.Communication_Service.send(int(False).to_bytes(1, byteorder="big"))
                                    logging.info("[Test_Driver.Serial_Data_Reading] Send False command to re run if the recieved data is running above 60 seconds")
                                    
                                    break

                                else:
                                    self.config.DUT_Ser.write(b'\x03')
                                    Send_client_request=True
                                    logging.info("[Test_Driver.Serial_Data_Reading] stoping current execution and and re sending client request after test running above 60 seconds")
                                    print(" Inside  stoping current execution and and re sending client ")
                                    break



                        except UnicodeDecodeError as e:
                            
                            #print("Error decoding data:", e) 
                            logging.info(f"[Test_Driver.Serial_Data_Reading]  Error in decoding data {e}")         
                
                else:

                    if not client_cmd:

                        self.config.DUT_Ser.write(b'\x03')

                        #  writing Server command in serial
                        self.config.DUT_Ser.write(f"{Received__Data} \n".encode("utf-8") )
                        self.config.Communication_Service.send(int(False).to_bytes(1, byteorder="big"))
                        logging.info("[Test_Driver.Serial_Data_Reading] Send False command to re run if the recieved data is not within 100 sec")

                    else:
                        self.config.DUT_Ser.write(b'\x03')
                        logging.info("[Test_Driver.Serial_Data_Reading] stoping current execution and and re sending client request after waiting 100 sec")
                        print(" stoping current execution and and re sending client request after waiting 100 sec ")
                        Send_client_request=True



        

            logging.info(f"[Test_Driver.Serial_Data_Reading] Returning iteration Output :- {Iteration_Output}")

            return Iteration_Output


    def Logs_Sender(self,Secondary_Script_log_filename,Device___log_filename):

        BUFFER_SIZE = 4096

    
        print(Secondary_Script_log_filename)
        print(Device___log_filename)
    
        self.config.Communication_Service.send(Secondary_Script_log_filename.encode())
        
        time.sleep(2)

        self.config.Communication_Service.send(Device___log_filename.encode()) 


        file_paths = [Secondary_Script_log_filename,Device___log_filename]  # Replace with the paths to your files

        time.sleep(3)

        for file_path in file_paths:
            # Get the file size
            file_size = os.path.getsize(file_path)
            # Convert the file size to a string representation
            file_size_str = str(file_size)
            Encoded_File_Size = file_size_str.zfill(16).encode()
            
            logging.info(f"[Test_Driver.Logs_Sender]  Sent {file_path} file size {file_size_str}")

            logging.info(f"[Test_Driver.Logs_Sender] Sent {file_path} file size Encoded {Encoded_File_Size}")

            #print(f" Sent {file_path} file size Encoded {Encoded_File_Size}")

            # Send the file size to the client, padded to a fixed length
            self.config.Communication_Service.sendall(Encoded_File_Size)

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
                    self.config.Communication_Service.sendall(chunk)

    def Server_communication(self,Received__Data):
        
        global Current_Test_Bandwidth


        # Reading Serail for RSI Value
        logging.info(f'[Test_Driver.Server_communication] Calling Serial_Data_Reading function to check RSSI Values')
        RSSI_Value =  self.Serial_Data_Reading(RSSI_Value_check=True,client_cmd = False,Received__Data=None)
        self.config.Communication_Service.send(str(RSSI_Value).encode())
        logging.info(f'[Test_Driver.Server_communication] Sending RSSI Values')



        self.config.DUT_Ser.flush()
        
        #  writing Server command in serial
        self.config.DUT_Ser.write(f"{Received__Data} \n".encode("utf-8") )
        logging.info(f'[Test_Driver.Server_communication] writing {Received__Data} command to start server')
        print((f'writing {Received__Data} command to start server'))

        #Decoded_data=DUT_Ser.read_until(b'UDP buffer size').decode()
        
            
        Decoded_data = self.config.DUT_Ser.readall().decode("utf-8", errors="ignore")

        logging.info(f'[Test_Driver.Server_communication] {Decoded_data}')

        
        if "Server listening on UDP port" not in Decoded_data or "UDP buffer size" not in Decoded_data:
            # Sending confirmation
                self.config.Communication_Service.send(int(False).to_bytes(1, byteorder="big"))
                logging.info('[Test_Driver.Server_communication] Server not started and sending False command ')
                
                return False
        
        else:
            # Sending confirmation
            self.config.Communication_Service.send(int(True).to_bytes(1, byteorder="big"))
            logging.info('[Test_Driver.Server_communication] Server started and sending True command ')


            

        logging.info('[Test_Driver.Server_communication] waiting for the Current Test bandwidth ')

        #  Recieving Current Test Bandwidth
        Current_Test_Bandwidth = float(self.config.Communication_Service.recv(1024).decode()) 


        logging.info(f'[Test_Driver.Server_communication] Recieved Current_Test_Bandwidth {Current_Test_Bandwidth}')
        Current_Iteration_Output = self.Serial_Data_Reading(False,False,Received__Data)

        
        logging.info(f'[Test_Driver.Server_communication] Current Test Iteration Output {Current_Test_Bandwidth}')

        # Calling Below Function to Analyse, take average and to send it to Primary for Each Test.

        if not self.Result_Analyser(Current_Iteration_Output,True):
            
            print(" RX Test Result is Not Good ....!!!")
            logging.info(f'[Test_Driver.Server_communication] RX Test Result is Not Good ....!!!')

            # Sending False Command to stop test
            self.config.Communication_Service.send(int(False).to_bytes(1, byteorder="big"))
            logging.info('[Test_Driver.Server_communication] Sending False command to stop test')

            return False
        
        else:
            
            
            # Sending True command to continue test

            self.config.Communication_Service.send(int(True).to_bytes(1, byteorder="big"))
            logging.info('[Test_Driver.Server_communication] Sending True command to Continue the test')


        while True:

            logging.info('[Test_Driver.Server_communication] waiting to continue test')
            Received_Data = bool(int.from_bytes(self.config.Communication_Service.recv(1024),byteorder='big'))
            


            # Checking RX test End
            if  Received_Data:
                logging.info('[Test_Driver.Server_communication] Recieved confirmation to End RX Test') 
                # Communication_Service.send("RX Test Ended sucessfully".encode())

                self.config.DUT_Ser.write(b'\x03')

                return True
            
            else:
                logging.info('[Test_Driver.Server_communication] Recieved confirmation to Continue RX Test')

                # Recieving Current test Bandwidth
                Current_Test_Bandwidth = float(self.config.Communication_Service.recv(1024).decode())            
                
                # Serial_Data_Reading(client_cmd = False,Received_Client_Data=None) 
                Current_Iteration_Output = self.Serial_Data_Reading(False,False,Received__Data)
                logging.info(f'[Test_Driver.Server_communication] Current Test Iteration Output {Current_Test_Bandwidth}')

                # Calling Below Function to Analyse, take average and to send it to Primary for Each Test.

                if not self.Result_Analyser(Current_Iteration_Output,True):
                    print(" RX Test Result is Not Good ....!!!")

                    # Sending False Command to stop test
                    self.config.Communication_Service.send(int(False).to_bytes(1, byteorder="big"))
                    logging.info(f'[Test_Driver.Server_communication] RX Test Result is Not Good ....!!!')

                    return False
                else:
                    

                    # Sending True command to continue test
                    self.config.Communication_Service.send(int(True).to_bytes(1, byteorder="big"))
                    logging.info('[Test_Driver.Server_communication] Sending True command to Continue the test')




# Execution Starts Here  

def main():



    config = Configuration()
    
    Driver = Test_Driver(config)

    if config.Establishinng_connection():
        
        Driver.Testing()
        # print(" outside testing ")
            
        time.sleep(6)
        # clearing Input Buffer
        config.DUT_Ser.reset_input_buffer()
        # Reading Serail for RSI Value

        logging.info('[main] Calling serail function to get RSSI Value after 2.4Ghz test')
        RSSI_Value = Driver.Serial_Data_Reading(RSSI_Value_check=True,client_cmd = False,Received__Data=None)
        
        
        #sending RSSI Values
        config.Communication_Service.send(str(RSSI_Value).encode())
        logging.info('[main] Sent 2.4Ghz RSSI Value ')
    
    

        #   5 Ghz Test  //////////////////////////////////////////////////////////////////////////////////////
        if config.wifi_configuration(_2_4Ghz=False):

            Driver.Testing()
                
            time.sleep(6)
            # clearing Input Buffer
            config.DUT_Ser.reset_input_buffer()
            # Reading Serail for RSI Value
            RSSI_Value = Driver.Serial_Data_Reading(RSSI_Value_check=True,client_cmd = False,Received__Data=None)
            logging.info('[main] Calling serail function to get RSSI Value after 5Ghz test')
            #sending RSSI Values
            config.Communication_Service.send(str(RSSI_Value).encode())
            logging.info('[main] Sent 5Ghz RSSI Value ')
    
            Driver.Logs_Sender(config.Secondary_Script_log_filename,config.Device_Logs_File_Name)
            # Communication End's Here By Closing established Socket.
            config.Communication_Service.close()

            
        else:

            time.sleep(6)
            # clearing Input Buffer
            config.DUT_Ser.reset_input_buffer()
            # Reading Serail for RSI Value
            RSSI_Value = Driver.Serial_Data_Reading(RSSI_Value_check=True,client_cmd = False,Received__Data=None)
            logging.info('[main] Calling serail function to get RSSI Value after 2.4Ghz test')
            
            #sending RSSI Values
            config.Communication_Service.send(str(RSSI_Value).encode())
            logging.info('[main] Sent 2.4Ghz RSSI Value ')
            #Closing Serial Port
            config.DUT_Ser.close()

            Driver.Logs_Sender(config.Secondary_Script_log_filename,config.Device_Logs_File_Name)
            # Communication End's Here By Closing established Socket.
            config.Communication_Service.close()





if __name__ == "__main__":
    # Call the main function
    main    ()


