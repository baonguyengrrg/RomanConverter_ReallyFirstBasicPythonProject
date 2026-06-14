from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="Roman Numeral Converter",
    description="A simple API to convert Roman numerals to integers.",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)
roman_map={
        'I': 1,
        'V':5,
        'X':10,
        'L':50,
        'C':100,
        'D':500,
        'M':1000
    }
def roman_to_int(s:str)->int:
    s=s.upper()
    final_ans=0
    n=len(s)
    for i in range(n):
        if s[i] not in roman_map:
            raise ValueError(f"Invalid Roman numeral: {s[i]}")
        if i+1<n and roman_map[s[i]]<roman_map[s[i+1]]:
            final_ans-=roman_map[s[i]]
        else:
            final_ans+=roman_map[s[i]]
    return final_ans

class RomanRequest(BaseModel):
    roman: str
    
@app.post("/convert")
def convert_roman_post(data: RomanRequest):
    if not data.roman.strip():
        raise HTTPException(status_code=400, detail="Roman numeral cannot be empty.")
    try:
        result = roman_to_int(data.roman)
        return {
            "input": data.roman,
            "result": result,
            "status": "success"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))