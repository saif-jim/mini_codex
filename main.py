# a coding agent like codex or claude code
# can read,write and edit files

#Imports
import os
from pathlib import Path

from dotenv import load_dotenv,find_dotenv
import json
from groq import Groq
from tools import read_file,write_file,run_command

load_dotenv()

api_key=os.environ.get("API_KEY")
client = Groq(api_key=api_key)

# ====================================================================================


system_prompt = """You are a coding agent that can make programme in any language.
You are provided with tools that can make directory,remove directory,create and remove file.
Use this tools like an expert softwere engineer and satisfy the user. You are developed by Saif Al Jim using openai's API."""

memory = [{"role":"system","content":system_prompt}]

def call_tool(name,args):
# a separate function for calling tools
# using key word args cuz previously i messed up xD
    match name:
        case "read_file":
            result = read_file(**args)
        
        case "write_file":
            result = write_file(**args)
        case "run_command":
            result = run_command(**args)
        
        case _:
            result = None

    return result

#====================================TOOLS==================================
# Reading tools from tool_schema json file
with open("tool_schemas.json","r",encoding="utf-8") as file:
    tools = json.load(file)["tools"]

#=====================================================================

def agent(query):
    
    memory.append(
        
        {"role":"user","content":query+f"Current dir : {Path.cwd()}"}
        
        )
    
    while True:

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=memory,
            tools=[tools[0],tools[1],tools[2]]
        )

        llm_call = response.choices[0].message
        memory.append(llm_call)

        if not llm_call.tool_calls:
            print("\n",llm_call.content,"\n")
            return
        
        for tool in llm_call.tool_calls:
            
            args = json.loads(tool.function.arguments)
            tool_name = tool.function.name

            print(f"Tool Call: {tool_name}")
            
            result = call_tool(tool_name,args)

            memory.append(
            {
            "role": "tool",
            # must match the `id` from the assistant's `tool_calls`
            "tool_call_id": tool.id,
            "name": tool_name,
            "content": str(result) if result is not None else ""
        }
        )

            

def main():
    
    while True:
        query = input(">> ")
    
        if query.lower() in ["exit","bye","goodbye","quit"]:
            break
        
        agent(query=query)


if __name__ == "__main__":
    main()
        

        

