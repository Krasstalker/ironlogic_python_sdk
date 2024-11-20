import socket

class Z2():
    def __init__(self,HOST:str,PORT:int) -> None:
        self.commands : dict = {
            "<STX>": b"\x02", #Начало команды 
            "<SEP>": b"\xB3", #Разделитель данных
            "<ETX>": b"\x03", #Конец команды. Следом за этим символом идет контрольная сумма 
            "<ENQ>": b"\x05", #Запрос теста связи. В ответ на такой символ SDK ответит символом <ACK> 
            "<ACK>": b"\x06", #Подтверждение получения команды. Высылается после получения любой команды, до момента начала ее обработки. 
            "<LRC>": b"\x0D"  #LRC is a checksum. The Description of the Inhova SDK says that for debugging purposes, they replace it with the OD character 
        }
        self.answers : dict = {
            "EA" : "Чистая карта",
            "E2" : "command format error",
            "E1" : "error validating command data",
            "E8" : "Карта отсутсвует", #The card cannot be read or missing
            "DB" : "Ошибка базы данных Iron Logic SDK", #DataBase Error
            "EF" : "Ошибка записи карты", #Failed to write the card
            "E3" : "Failed to clear the card",
            "E9" : "Попытка записать копию на ту же самую карту", #attempted to repeat copying to the same card
            "ED" : "Карта с этим номером уже зарегистрирована",
            "EK" : "Ключ адаптера не принят",
            "OK" : "command executed successfully"
        }

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((HOST, PORT))

    def __del__(self):
        self.socket.close();

    # Костыльный парсинг для человекочитаемого ответа
    def parse_answer(self,response : bytes, payload : list) -> str:
        answer : list = self.parse_response(response)
        answer_str : str = "".join(answer)
        
        for ans in self.answers:
            if ans in answer_str:
                return self.answers[ans]
        
        if "<SEP>RC<SEP>" in answer_str: #answer readcard
            answer_split : list = answer_str.split("<SEP>")
            card_data: list = answer_split[4].split("||")
            answer_str : dict = {}
            for data in card_data:
                ds : list = data.split("::")
                answer_str[ds[0]] = ds[1]

        if "<SEP>CC<SEP>" in answer_str: #answer clearcard
            answer_str = "Успешно очищено!"

        if any(word in answer_str for word in ["<SEP>CI<SEP>","<SEP>EM<SEP>","<SEP>CX<SEP>","<SEP>CG<SEP>"]): #answer EM CI CX CG
            print("payload",payload)
            print("answer",answer_str)
            answer_str = "Успешно записано!"

        if "<SEP>CO<SEP>" in answer_str: #answer checkout
            answer_str = "Карта успешно выписана!"

        return answer_str
    # Костыльный парсинг для человекочитаемого ответа
        
    # парсинг bytes в utf-8 list
    def parse_response(self, response : bytes) -> list:
        # return list(response)
        resp : list = []
        for byte in list(response):
            byte = bytes([byte])

            if byte in self.commands.values():
                resp.append(list(self.commands.keys())[list(self.commands.values()).index(byte)])
            else:
                resp.append(byte.decode())

        return resp
    # парсинг bytes в utf-8 list

    # принимаем список команд в list, формируем bytes и отправляем в socket 
    def send_payload(self,payload : list) -> dict:
        b_payload : bytes = b""
        for char in payload:
            if char in self.commands:
                b_payload += self.commands[char]
            else:
                # print("char",type(char),char)
                if isinstance(char, int):
                    b_payload += bytes([char])
                else:
                    # print(char)
                    b_payload += str.encode(char)
        
        # print("b_payload",b_payload)
        self.socket.sendall(b_payload)
        print ("Sended:",b_payload.hex())

        status_code = self.socket.recv(1024)
        # print("status_code",status_code)

        if status_code == b"\x06":
            response = self.socket.recv(1024)
            # print("response",type(response),response)

            return self.parse_response(status_code), self.parse_response(response), self.parse_answer(response,payload)
        else:
            return self.parse_response(status_code), None, None
    # принимаем список команд в list, формируем bytes и отправляем в socket 

