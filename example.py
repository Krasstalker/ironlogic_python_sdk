from ilz2 import Z2

il = Z2("127.0.0.1",9999)

# DATE FORMAT DD/MM/YYYY
# TIME FORMAT HH:MM:SS
# card_version = 0
# room_number = 101
station_num : int = 1

# USAGE EXAMPLE
READ_CARD : list = ["<STX>","<SEP>",station_num,"<SEP>","RC","<SEP>","<ETX>","<LRC>"] #READ CARD
# CHECKOUT: list = ["<STX>","<SEP>",station_num,"<SEP>","CO","<SEP>",room_num,"<SEP>",0,"<SEP>",0,"<SEP>","<ETX>","<LRC>"] #CHECKOUT
# CHECKIN : list = [f"<STX>","<SEP>",station_num,"<SEP>","CI","<SEP>",room_num,"<SEP>",date_from,"<SEP>",time_from,"<SEP>",date_to,"<SEP>",time_to,"<SEP>","<SEP>","<SEP>","RP","<SEP>","Reception","<SEP>","<SEP>","<SEP>","""common_doors::0,description::custom door,place::0,typeid::4,guest_card_version::{card_version},service::0,room::{room_number},startdate::{date_from},starttime::{time_from},enddate::{date_to},endtime::{time_to},EmMarine::keep""","<SEP>","<ETX>","<LRC>"] #CHECKIN
# CHECKIN_EX : list = ["<STX>","<SEP>",station_num,"<SEP>","CX","<SEP>",room_number,"<SEP>", date_from ,"<SEP>",time_from, "<SEP>", date_to, "<SEP>",time_to,"<SEP>","<ETX>","<LRC>"] #CHECKIN_EX
# COPYCARD : list = [f"<STX>","<SEP>",station_num,"<SEP>","CG","<SEP>",room_number,"<SEP>",date_from,"<SEP>",time_from,"<SEP>",date_to,"<SEP>",time_to,"<SEP>","<SEP>","<SEP>","RP","<SEP>","Reception","<SEP>","<SEP>","<SEP>","""EmMarine::keep,starttime::{time_from},room::{room_number},startdate::{date_from},service::0,enddate::{date_to},description::custom door,typeid::4,place::0,guest_card_version::{card_version},endtime::{time_to}""","<SEP>","<ETX>"] #COPYCARD
# EMERGENCYCARD : list = ["<STX>","<SEP>",station_num,"<SEP>","EM","<SEP>",room_number,"<SEP>",start_date,"<SEP>",start_time,"<SEP>",end_date,"<SEP>",end_time,"<SEP>","<ETX>","<LRC>"] #EMERGENCYCARD
# USAGE EXAMPLE


status,message,data = il.send_payload(READ_CARD)

print("req",READ_CARD)
print("res",status,message,data)
