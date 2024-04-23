import openai
import os
import json

class AI_Coach_RLL:
    def get_completion(user_messages,system_messages = "", model = "gpt-4-turbo-preview"):
        system_messages=""
        messages = [{"role":"system","content":system_messages},
                    {"role": "user", "content": user_messages}]
        from openai import OpenAI
        
        client = OpenAI(api_key=openai.api_key)
        response = client.chat.completions.create(
            model = model,
            messages = messages,
            temperature=0.2,
        )
        response_message = response.choices[0].message.content
        return response_message
    
    def start_chat(i=1):
        file_name = "The_record_of_Version_1.txt"
        str_i=str(i)
        file = open(file_name, mode='r') # 打开文件进行读取
        record = file.read() # 读取文件的内容
        file.close() # 关闭文件
        text_input=input() # 获取用户输入的问题
        file = open(file_name, mode='a')
        file.write('This is NO.'+str_i+' remark of the user\n')
        file.write(text_input+'\n\n') # 对问题进行记录并写入文件
        file.close() # 关闭文件
        return record,i
        
    def generate_code(user_messages):
        	# 解析用户提问，返回需要的代码知识
        system_messages = """Judge if the text provided by user is a code\
        Your answer must only be 'Yes' or 'No'."""
        # 这段prompt用于检查用户输入是否是代码
        Judge = AI_Coach_RLL.get_completion(user_messages,system_messages)
        if Judge == 'No':
            system_messages = """Below is a question waiting for a solving by programming\ 
            You need to generate a python code to solve the problem perfectly."""
            # 如果输入不是代码，AI将问题转化为代码
            user_messages = AI_Coach_RLL.get_completion(user_messages,system_messages)
        return user_messages
        

    def analyze_code(user_messages,record):
        prompt_code = f"""
        Below is a transcript of our previous chats\ 
        please refer to that record when you have a conversation\ 

        \"\"\"{record}\"\"\"\ 
        
        You will be offered a python code\ 
        And you need to recognize what grammar\ 
        and syntax and algorithm the code has used\ 
        print thses in the following format strictly:
        
        1.The syntax/algorithm:......
        The example:......
        2.The syntax/algorithm:......
        The example:......
        3.The syntax/algorithm:......
        The example:......
        4.The syntax/algorithm:......
        The example:......
        ......
        
        \"\"\"{user_messages}\"\"\"
        """
        response = AI_Coach_RLL.get_completion(prompt_code)
        return response